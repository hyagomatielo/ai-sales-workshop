"""Build the public site and its resource catalog using only the standard library."""

import json
import shutil
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    ".pdf": "Guides & documents",
    ".docx": "Guides & documents",
    ".doc": "Guides & documents",
    ".pptx": "Presentations",
    ".ppt": "Presentations",
    ".xlsx": "Data & spreadsheets",
    ".xls": "Data & spreadsheets",
    ".csv": "Data & spreadsheets",
    ".zip": "Activity kits",
    ".txt": "Prompts & notes",
    ".md": "Prompts & notes",
}


def build(root: Path = ROOT) -> list[dict]:
    assets = root / "assets"
    output = root / "_site"
    catalog = []
    files = []
    for source in sorted(assets.rglob("*"), key=lambda path: path.as_posix().casefold()):
        relative = source.relative_to(assets)
        if any(part.startswith(".") for part in relative.parts):
            continue
        if source.is_symlink():
            raise ValueError(f"Symbolic links are not supported: {relative}")
        if not source.is_file():
            continue
        files.append((source, relative))
        catalog.append({
            "name": source.stem.replace("_", " ").replace("-", " "),
            "filename": source.name,
            "category": relative.parts[0].replace("_", " ").replace("-", " ")
            if len(relative.parts) > 1 else CATEGORIES.get(source.suffix.lower(), "Other resources"),
            "type": source.suffix.lstrip(".").upper() or "FILE",
            "size": source.stat().st_size,
            "url": "assets/" + quote(relative.as_posix(), safe="/"),
        })
    if output.exists():
        shutil.rmtree(output)
    output.mkdir()
    shutil.copyfile(root / "index.html", output / "index.html")
    for source, relative in files:
        destination = output / "assets" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
    (output / "resources.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (output / ".nojekyll").touch()
    return catalog


if __name__ == "__main__":
    print(f"Built workshop site with {len(build())} resources.")
