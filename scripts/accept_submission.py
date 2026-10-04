#!/usr/bin/env python3
import argparse
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import recipe_contract as rc
from normalise_recipe import NormaliseError, normalise


def main():
    parser = argparse.ArgumentParser(description="Place an approved submission at recipes/<owner>/<id>/recipe.md, normalised and checked.")
    parser.add_argument("submission", help="the submitted recipe.md")
    parser.add_argument("--repo", default=".", help="the recipe repository root")
    parser.add_argument("--replace", action="store_true", help="overwrite a recipe already accepted at that path")
    parser.add_argument("--external", action="store_true", help="the author is not on the Intempt team")
    args = parser.parse_args()

    try:
        text = normalise(pathlib.Path(args.submission).read_text(encoding="utf-8"))
    except (NormaliseError, OSError) as exc:
        print(f"cannot read the submission: {exc}", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as scratch:
        staged = pathlib.Path(scratch) / "recipe.md"
        staged.write_text(text, encoding="utf-8")
        try:
            front, _ = rc.read(staged)
        except rc.RecipeError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    owner, rid = str(front.get("owner") or ""), str(front.get("id") or "")
    if not owner or not rid:
        print("the submission needs both owner and id", file=sys.stderr)
        return 1
    if args.external and owner == "intempt":
        print("an outside author cannot publish under recipes/intempt/; set owner to the creator's handle", file=sys.stderr)
        return 1

    target = pathlib.Path(args.repo) / "recipes" / owner / rid / "recipe.md"
    if target.exists() and not args.replace:
        print(f"{target} already exists; pass --replace to overwrite it", file=sys.stderr)
        return 1

    previous = target.read_text(encoding="utf-8") if target.exists() else None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    problems = rc.validate(target, front)
    if problems:
        if previous is None:
            target.unlink()
            for d in (target.parent, target.parent.parent):
                if not any(d.iterdir()):
                    d.rmdir()
        else:
            target.write_text(previous, encoding="utf-8")
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1

    status, waiting = rc.availability(front)
    print(f"accepted {target} ({'Install now' if status == 'install_now' else 'Coming soon: ' + ', '.join(waiting)})")
    print("next: commit it on a feature/ branch and open a pull request to staging")
    return 0


if __name__ == "__main__":
    sys.exit(main())
