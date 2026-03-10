import unittest

from app import app


class TestWebApp(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_page(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        text = resp.get_data(as_text=True)
        self.assertIn("小红书文案自动生成器", text)
        self.assertIn("topic", text)
        self.assertIn("audience", text)
        self.assertIn("objective", text)
        self.assertIn("keywords", text)

    def test_generate_success(self):
        resp = self.client.post(
            "/generate",
            json={
                "topic": "时间管理",
                "audience": "大学生",
                "objective": "提升学习效率",
                "keywords": "番茄钟,复盘",
            },
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("title", data)
        self.assertIn("opening", data)
        self.assertIn("body", data)
        self.assertIn("cta", data)
        self.assertIn("hashtags", data)

    def test_generate_validation_error(self):
        resp = self.client.post(
            "/generate",
            json={
                "topic": "",
                "audience": "大学生",
                "objective": "提升学习效率",
                "keywords": "",
            },
        )
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
