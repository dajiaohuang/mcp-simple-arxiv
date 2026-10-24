import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


class HtmlUrlTests(unittest.TestCase):
    def test_only_terminal_version_suffix_is_removed(self):
        # Import the client without optional PDF/network dependencies or package server startup.
        converter = types.ModuleType("docling.document_converter")
        converter.DocumentConverter = object
        modules = {name: types.ModuleType(name) for name in ("feedparser", "httpx", "docling")}
        modules["docling.document_converter"] = converter
        path = Path(__file__).resolve().parents[1] / "mcp_simple_arxiv" / "arxiv_client.py"
        spec = importlib.util.spec_from_file_location("arxiv_url_test_client", path)
        module = importlib.util.module_from_spec(spec)
        modules[spec.name] = module
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(module)
        client = module.ArxivClient()
        cases = {
            "solv-int/9901000": "solv-int/9901000",
            "solv-int/9901000v2": "solv-int/9901000",
            "9901.00000v12": "9901.00000",
            "9901.00000": "9901.00000",
        }
        for paper_id, base_id in cases.items():
            with self.subTest(paper_id=paper_id):
                self.assertEqual(client._get_html_url(paper_id), f"https://arxiv.org/html/{base_id}")


if __name__ == "__main__":
    unittest.main()
