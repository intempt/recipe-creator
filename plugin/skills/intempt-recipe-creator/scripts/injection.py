#!/usr/bin/env python3
import argparse
import hashlib
import json
import pathlib
import re
import sys
import urllib.parse

import yaml

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recipe_contract as rc

PATTERNS = HERE / "fixtures" / "injection_patterns.json"
PIN = HERE / "fixtures" / "SUITE_SHA256"
COMMENT = re.compile(r"<!--(.*?)-->", re.S)
URL = re.compile(r"https?://[^\s<>\"'`)\]]+", re.I)


class PatternsTampered(Exception):
    pass


def pattern_digest():
    return hashlib.sha256(PATTERNS.read_bytes()).hexdigest()


def load_patterns():
    pinned = PIN.read_text(encoding="utf-8").strip() if PIN.exists() else ""
    actual = pattern_digest()
    if pinned != actual:
        raise PatternsTampered(
            f"{PATTERNS.name} has sha256 {actual}, but fixtures/SUITE_SHA256 pins {pinned or 'nothing'}. "
            "Refusing to scan with rules nobody reviewed. If the change is intended, update SUITE_SHA256 in the same commit.")
    spec = json.loads(PATTERNS.read_text(encoding="utf-8"))
    flags = 0
    for name in spec.get("flags") or []:
        flags |= getattr(re, name)
    compiled = []
    for p in spec["patterns"]:
        entry = dict(p)
        if p.get("regex"):
            entry["compiled"] = re.compile(p["regex"], flags)
        if p.get("directive"):
            entry["compiled_directive"] = re.compile(p["directive"], flags)
        if not (p.get("regex") or p.get("comment") or p.get("url")):
            raise PatternsTampered(f"pattern {p['id']} declares no matcher")
        compiled.append(entry)
    return spec["version"], compiled


def entries(text):
    head, body = rc.split(text.replace("\r\n", "\n"))
    out = []
    if head is None:
        return [("file", "all", text)]
    try:
        front = yaml.safe_load(head) or {}
    except yaml.YAMLError:
        return [("frontmatter", "frontmatter", head), ("body", "body", body)]
    for where, value in rc.text_fields(front):
        out.append((where, "frontmatter", value))
    out.append(("body", "body", body))
    return out


def in_scope(scope, kind, where):
    if scope == "all":
        return True
    if scope == "descriptions":
        return kind == "frontmatter" and (where == "description" or (where.startswith("steps.") and where.endswith(".description")))
    return scope == kind or kind == "all"


def host_allowed(url, allowed):
    host = (urllib.parse.urlsplit(url).hostname or "").lower().rstrip(".")
    return any(host == h or host.endswith("." + h) for h in allowed)


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def scan_text(text, patterns):
    findings = []

    def add(p, where, value, index, evidence):
        findings.append({
            "pattern_id": p["id"],
            "severity": p["severity"],
            "label": p["label"],
            "where": where,
            "line": line_of(value, index),
            "evidence": evidence.replace("\n", " ").strip()[:120],
            "message": p["message"],
        })

    for where, kind, value in entries(text):
        for p in patterns:
            if not in_scope(p["scope"], kind, where):
                continue
            if "compiled" in p:
                for m in p["compiled"].finditer(value):
                    add(p, where, value, m.start(), m.group(0).encode("unicode_escape").decode("ascii"))
            elif p.get("comment"):
                for m in COMMENT.finditer(value):
                    if m.group(0) in (p.get("allow") or []):
                        continue
                    directive = p.get("compiled_directive")
                    if directive is None or directive.search(m.group(1)):
                        add(p, where, value, m.start(), m.group(0))
            elif p.get("url"):
                for m in URL.finditer(value):
                    if not host_allowed(m.group(0), p.get("allowed_hosts") or []):
                        add(p, where, value, m.start(), m.group(0))
    return findings


def scan_file(path, patterns=None):
    if patterns is None:
        _, patterns = load_patterns()
    return scan_text(pathlib.Path(path).read_text(encoding="utf-8"), patterns)


def main():
    parser = argparse.ArgumentParser(description="Scan recipe.md files for prompt injection aimed at the agent, the engine or the reviewer.")
    parser.add_argument("paths", nargs="+", type=pathlib.Path, help="recipe.md files, or folders to search for them")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        version, patterns = load_patterns()
    except PatternsTampered as exc:
        print(f"injection: {exc}", file=sys.stderr)
        return 2
    files = rc.recipe_files(args.paths)
    if not files:
        print("injection: no recipe.md found", file=sys.stderr)
        return 2
    report = {str(path): scan_file(path, patterns) for path in files}
    blocking = sum(1 for found in report.values() for f in found if f["severity"] == "block")
    if args.json:
        print(json.dumps({"patterns": version, "sha256": pattern_digest(), "files": len(files), "findings": report}, indent=1))
    else:
        for path, found in report.items():
            for f in found:
                print(f"{path} {f['where']}:{f['line']}: {f['pattern_id']} ({f['label']}): {f['evidence']}")
                print(f"  {f['message']}")
        print(f"injection: {len(files)} file(s) scanned with {version}, {blocking} blocking finding(s)")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
