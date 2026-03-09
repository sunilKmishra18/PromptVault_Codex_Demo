import os
import tempfile
import unittest

import app as app_module


class PromptVaultRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()

        app_module.DB_PATH = self.temp_db.name
        app_module.app.config.update(TESTING=True)
        app_module.init_db()

        self.client = app_module.app.test_client()

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def test_home_page_renders(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"PromptVault", response.data)

    def test_add_prompt_get_renders_form(self):
        response = self.client.get("/add")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add Prompt", response.data)

    def test_add_prompt_rejects_missing_fields(self):
        response = self.client.post(
            "/add",
            data={"title": "", "category": "Writing", "description": "Test"},
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"All fields are required.", response.data)

    def test_add_prompt_persists_and_redirects_home(self):
        response = self.client.post(
            "/add",
            data={
                "title": "Email Draft",
                "category": "Work",
                "description": "Write a professional follow-up email.",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Prompt saved successfully!", response.data)
        self.assertIn(b"Email Draft", response.data)

    def test_search_returns_matching_prompt(self):
        self.client.post(
            "/add",
            data={
                "title": "Brainstorm Ideas",
                "category": "Creative",
                "description": "Generate five startup ideas.",
            },
        )

        response = self.client.get("/search?q=startup")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Brainstorm Ideas", response.data)

    def test_search_with_blank_query_shows_no_results(self):
        response = self.client.get("/search")

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"No prompts found", response.data)


if __name__ == "__main__":
    unittest.main()
