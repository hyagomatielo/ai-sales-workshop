import json
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

from scripts.build import build


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "assets").mkdir()
        (self.root / "index.html").write_text("<h1>Workshop</h1>", encoding="utf-8")

    def test_empty_library_and_static_files(self):
        (self.root / "assets" / ".gitkeep").touch()
        self.assertEqual(build(self.root), [])
        output = self.root / "_site"
        self.assertEqual(json.loads((output / "resources.json").read_text()), [])
        self.assertEqual((output / "index.html").read_text(), "<h1>Workshop</h1>")
        self.assertTrue((output / ".nojekyll").exists())
        self.assertFalse((output / "scripts").exists())

    def test_catalog_download_paths_categories_and_sizes(self):
        names = ["sales_plan.txt", "sample.csv", "Activity kits/Example #1 + 20%.txt",
                 "Activity kits/日本語.txt", "unknown.bin"]
        for name in names:
            path = self.root / "assets" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"workshop")
        catalog = build(self.root)
        self.assertEqual(len(catalog), len(names))
        for item in catalog:
            self.assertEqual((self.root / "_site" / unquote(item["url"])).read_bytes(), b"workshop")
            self.assertEqual(item["size"], 8)
        by_filename = {item["filename"]: item for item in catalog}
        self.assertEqual(by_filename["sales_plan.txt"]["name"], "sales plan")
        self.assertEqual(by_filename["sample.csv"]["category"], "Data & spreadsheets")
        self.assertEqual(by_filename["unknown.bin"]["category"], "Other resources")
        self.assertEqual(by_filename["Example #1 + 20%.txt"]["category"], "Activity kits")
        self.assertIn("%23", by_filename["Example #1 + 20%.txt"]["url"])

    def test_hidden_files_excluded_and_deleted_assets_removed(self):
        secret = self.root / "assets" / ".private"
        secret.mkdir()
        (secret / "hidden.txt").write_text("hidden")
        asset = self.root / "assets" / "example.txt"
        asset.write_text("example")
        self.assertEqual(len(build(self.root)), 1)
        asset.unlink()
        self.assertEqual(build(self.root), [])
        self.assertFalse((self.root / "_site" / "assets" / "example.txt").exists())


if __name__ == "__main__":
    unittest.main()
