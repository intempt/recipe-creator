import pathlib
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
EXAMPLE = ROOT / "examples" / "intempt" / "trial-expiring-nudge" / "recipe.md"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def example_text():
    return EXAMPLE.read_text(encoding="utf-8")


def write_recipe(text, owner="intempt", rid="trial-expiring-nudge"):
    base = pathlib.Path(tempfile.mkdtemp())
    path = base / owner / rid / "recipe.md"
    path.parent.mkdir(parents=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def cleanup(path):
    shutil.rmtree(pathlib.Path(path).parents[2], ignore_errors=True)
