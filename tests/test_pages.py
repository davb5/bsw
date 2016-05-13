import os
import unittest

from bsw.pages import Page
import bsw.includes


class TestPages(unittest.TestCase):
    def setUp(self):
        self.test_page_filename = os.path.join(os.path.dirname(__file__),
                                               "data",
                                               "pages",
                                               "test_page.html")
        self.test_include_path = os.path.join(os.path.dirname(__file__),
                                              "data",
                                              "templates",
                                              "includes",
                                              "test_include.html")

    def test_page_init(self):
        page = Page(self.test_page_filename)
        self.assertIsNone(page.body)
        self.assertIsNone(page.body_raw)
        self.assertIsNone(page.rendered_page)
        self.assertFalse(page.page_vars)
        self.assertEqual(page.filename, self.test_page_filename)

    def test_page_load(self):
        test_page = Page(self.test_page_filename)
        test_page.load()
        self.assertIn("My sample page", test_page.body_raw.strip())

    def test_page_extract_vars(self):
        test_page = Page(self.test_page_filename)
        test_page.load()
        test_page.extract_vars()
        self.assertIn("template", test_page.page_vars)
        self.assertEqual(test_page.page_vars["template"],
                         "test_template.html")
        self.assertIn("author", test_page.page_vars)
        self.assertEqual(test_page.page_vars["author"],
                         "Dave Barker")

    def test_page_strip_vars(self):
        test_page = Page(self.test_page_filename)
        test_page.load()
        test_page.extract_vars()
        test_page.strip_vars()
        self.assertNotIn("<!-- template = \"test_template.htm\" -->",
                         test_page.body)

    def test_replace_includes(self):
        # Preload the includes cache
        with open(self.test_include_path, "r") as test_include_file:
            test_include_data = test_include_file.read()

        bsw.includes.include_cache["test_include.html"] = test_include_data

        test_page = Page(self.test_page_filename)
        test_page.load()
        test_page.extract_vars()
        test_page.strip_vars()
        test_page.replace_includes()
        self.assertNotIn("<!-- include(\"test_include.html\") -->",
                         test_page.rendered_page)
        self.assertIn("<h1>This is a test include</h1>",
                      test_page.rendered_page)
