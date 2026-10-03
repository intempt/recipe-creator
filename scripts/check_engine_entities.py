#!/usr/bin/env python3
import ast
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from recipe_contract import BUILDABLE_ENTITIES as BUILDABLE

BUILDABLE_ENTITIES = set(BUILDABLE)


def engine_entities(source):
    for node in ast.walk(ast.parse(source)):
        target = getattr(node, "target", None) or (node.targets[0] if isinstance(node, ast.Assign) else None)
        if isinstance(target, ast.Name) and target.id == "ALLOWED_ENTITIES" and getattr(node, "value", None) is not None:
            return {row.elts[0].value for row in node.value.elts}
    return None


def main():
    if len(sys.argv) != 2:
        print("usage: check_engine_entities.py <path to llm-wrapper md_import.py>", file=sys.stderr)
        return 2
    engine = engine_entities(pathlib.Path(sys.argv[1]).read_text())
    if engine is None:
        print("no ALLOWED_ENTITIES in that file", file=sys.stderr)
        return 2
    added = sorted(engine - BUILDABLE_ENTITIES)
    dropped = sorted(BUILDABLE_ENTITIES - engine)
    if added or dropped:
        if added:
            print(f"the engine can build these but recipe_contract.py does not list them: {', '.join(added)}", file=sys.stderr)
        if dropped:
            print(f"recipe_contract.py lists these but the engine no longer builds them: {', '.join(dropped)}", file=sys.stderr)
        print("update BUILDABLE_ENTITIES and COMING_SOON_ENTITIES, then run render_entities_doc.py and rebuild_bodies.py", file=sys.stderr)
        return 1
    print(f"{len(engine)} entities match the engine")
    return 0


if __name__ == "__main__":
    sys.exit(main())
