"""Fix compressinja 0.0.2's regex for Python 3.11 and newer."""

from importlib.metadata import distribution
from pathlib import Path


ORIGINAL = r"_tag_re = re.compile(r'(?:<(/?)([a-zA-Z0-9_-]+)\s*|(>\s*))(?s)')"
FIXED = r"_tag_re = re.compile(r'(?:<(/?)([a-zA-Z0-9_-]+)\s*|(>\s*))', re.DOTALL)"


def patch(path):
    source = path.read_text(encoding="utf-8")
    if ORIGINAL in source:
        path.write_text(source.replace(ORIGINAL, FIXED), encoding="utf-8")
    elif FIXED not in source:
        raise RuntimeError("Unexpected compressinja source; review compatibility patch")


if __name__ == "__main__":
    package = distribution("compressinja")
    if package.version != "0.0.2":
        raise RuntimeError("Compatibility patch requires compressinja 0.0.2")
    patch(Path(package.locate_file("compressinja/html.py")))
