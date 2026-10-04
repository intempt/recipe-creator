#!/usr/bin/env python3
import argparse
import json
import pathlib
import re
import sys
import urllib.parse

import yaml

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recipe_contract as rc

VERSION = "intempt-recipe-portability/1.0.0"

FIX = ("Move it into an `inputs` row: say what the installer supplies and what happens if it is missing, "
       "and have the step say \"the <thing> chosen for this run\" instead of the value.")

EXAMPLE_DOMAINS = ("example.com", "example.org", "example.net")
EXAMPLE_TLDS = ("example", "test", "invalid", "localhost")
WORKSPACE_HOSTS = ("app.intempt.com",)

URL = re.compile(r"https?://[^\s<>\"'`)\]]+", re.I)
EMAIL = re.compile(r"(?<![\w.%+-])[A-Za-z0-9._%+-]+@((?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})\b")
WORKSPACE_PATH = re.compile(r"/(?:orgs?|organi[sz]ations?|projects?|workspaces?|accounts?)/[^/?#\s]+", re.I)
WORKSPACE_QUERY = re.compile(r"(?:^|&)(?:org|orgName|organization|project|projectName|workspace)=", re.I)

RULES = (
    ("uuid", "a UUID", re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)),
    ("numeric_id", "a long numeric id", re.compile(r"(?<![\d.,])\d{9,}(?![\d.,])")),
    ("opaque_id", "an opaque id", re.compile(
        r"\bc[a-z0-9]{24}\b"
        r"|\b[0-9a-f]{24}\b"
        r"|\b(?:seg|jrn|wf|exp|org|prj|proj|usr|acc|evt|cmp)_(?=[A-Za-z0-9]*\d)[A-Za-z0-9]{3,}\b"
        r"|\b(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[a-z])(?=[A-Za-z0-9]*[A-Z])[A-Za-z0-9]{20,}\b")),
    ("entity_id", "a hardcoded id for something in your project", re.compile(
        r"\b(?:segment|journey|workflow|experiment|dashboard|report|form|list|campaign|personalization|audience|project|org|organization)"
        r"[ _-]?id\b\s*(?:=|:|is|equals|of|#)?\s*[\"'`]?(?=[\w-]*\d)[\w-]+"
        r"|\b(?:segment|journey|workflow|experiment|dashboard|list|form|campaign)\s+#?\d{3,}\b", re.I)),
)


def email_is_example(domain):
    domain = domain.lower()
    return domain in EXAMPLE_DOMAINS or any(domain.endswith("." + d) for d in EXAMPLE_DOMAINS) \
        or domain.rsplit(".", 1)[-1] in EXAMPLE_TLDS


def workspace_link(url):
    parts = urllib.parse.urlsplit(url)
    host = (parts.hostname or "").lower()
    if any(host == h or host.endswith("." + h) for h in WORKSPACE_HOSTS):
        return True
    return bool(WORKSPACE_PATH.search(parts.path) or WORKSPACE_QUERY.search(parts.query))


def entries(text):
    head, body = rc.split(text.replace("\r\n", "\n"))
    if head is None:
        return [("file", text)]
    try:
        front = yaml.safe_load(head) or {}
    except yaml.YAMLError:
        return [("frontmatter", head), ("body", body)]
    return list(rc.text_fields(front)) + [("body", body)]


def scan_text(text):
    findings = []
    seen = set()

    def add(kind, label, where, value, index, evidence):
        key = (kind, evidence)
        if key in seen:
            return
        seen.add(key)
        findings.append({
            "kind": kind,
            "severity": "block",
            "label": label,
            "where": where,
            "line": value.count("\n", 0, index) + 1,
            "evidence": evidence[:120],
            "fix": FIX,
        })

    for where, value in entries(text):
        urls = [(m.start(), m.end(), m.group(0)) for m in URL.finditer(value)]
        for start, _, url in urls:
            if workspace_link(url):
                add("workspace_link", "a link into one workspace, project or org", where, value, start, url)
        for m in EMAIL.finditer(value):
            if not email_is_example(m.group(1)):
                add("email", "an email address", where, value, m.start(), m.group(0))
        for kind, label, rule in RULES:
            for m in rule.finditer(value):
                if kind != "entity_id" and any(s <= m.start() < e for s, e, url in urls if workspace_link(url)):
                    continue
                add(kind, label, where, value, m.start(), m.group(0))
    return findings


def scan_file(path):
    return scan_text(pathlib.Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Flag values in a recipe.md that only exist in the author's workspace.")
    parser.add_argument("paths", nargs="+", type=pathlib.Path, help="recipe.md files, or folders to search for them")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    files = rc.recipe_files(args.paths)
    if not files:
        print("portability: no recipe.md found", file=sys.stderr)
        return 2
    report = {str(path): scan_file(path) for path in files}
    total = sum(len(found) for found in report.values())
    if args.json:
        print(json.dumps({"version": VERSION, "files": len(files), "findings": report}, indent=1))
    else:
        for path, found in report.items():
            for f in found:
                print(f"{path} {f['where']}:{f['line']}: {f['kind']} ({f['label']}): {f['evidence']}")
                print(f"  {f['fix']}")
        print(f"portability: {len(files)} file(s) scanned with {VERSION}, {total} finding(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
