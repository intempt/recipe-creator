#!/usr/bin/env python3
import argparse
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import injection
import portability
import recipe_contract as rc

FORMAT = "intempt-recipe-bundle/1"
MAX_BYTES = 250 * 1024


def problems_for(path, raw):
    if len(raw) > MAX_BYTES:
        return [f"the file is {len(raw)} bytes; the submission form takes at most {MAX_BYTES} (250 KB)"]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return ["the file is not UTF-8"]
    try:
        front, _ = rc.read(path)
    except rc.RecipeError as exc:
        return [str(exc)]
    problems = [f"contract: {p}" for p in rc.validate(path, front)]
    _, patterns = injection.load_patterns()
    problems += [f"injection {f['pattern_id']} at {f['where']}: {f['evidence']}. {f['message']}"
                 for f in injection.scan_text(text, patterns) if f["severity"] == "block"]
    problems += [f"portability {f['kind']} at {f['where']}: {f['evidence']}. {f['fix']}"
                 for f in portability.scan_text(text)]
    return problems


def manifest_for(path, raw):
    front, _ = rc.read(path)
    status, waiting = rc.availability(front)
    manifest = {"format": FORMAT, "id": front["id"], "owner": front["owner"]}
    if front.get("curator"):
        manifest["curator"] = front["curator"]
    manifest.update({
        "version": str(front.get("version") or ""),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "availability": status,
        "waitingOn": waiting,
        "checks": {
            "injection": f"{injection.load_patterns()[0]} sha256:{injection.pattern_digest()}",
            "portability": portability.VERSION,
        },
    })
    return manifest


def main():
    parser = argparse.ArgumentParser(description="Validate a recipe.md and write the bundle intempt recipe submit and the web form accept.")
    parser.add_argument("recipe", type=pathlib.Path, help="<owner>/<id>/recipe.md")
    parser.add_argument("--out", type=pathlib.Path, required=True, help="Directory to write recipe.md and manifest.json into.")
    args = parser.parse_args()
    if not args.recipe.is_file():
        print(f"package: {args.recipe} is not a file", file=sys.stderr)
        return 2
    raw = args.recipe.read_bytes()
    try:
        problems = problems_for(args.recipe, raw)
    except injection.PatternsTampered as exc:
        print(f"package: {exc}", file=sys.stderr)
        return 2
    if problems:
        for line in problems:
            print(f"  {line}")
        print(f"package: {len(problems)} problem(s); nothing written")
        return 1
    manifest = manifest_for(args.recipe, raw)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "recipe.md").write_bytes(raw)
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"package: wrote {args.out}/recipe.md and manifest.json ({manifest['availability']}, sha256 {manifest['sha256'][:12]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
