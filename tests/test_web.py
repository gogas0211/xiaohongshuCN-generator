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
        self.assertIn("生成3个版本", text)
        self.assertIn("生成10篇→选最好的", text)

    def test_generate_success_json(self):
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

    def test_generate_success_form(self):
        resp = self.client.post(
            "/generate",
            data={
                "topic": "时间管理",
                "audience": "大学生",
                "objective": "提升学习效率",
                "keywords": "番茄钟,复盘",
            },
        )
        self.assertEqual(resp.status_code, 200)
        text = resp.get_data(as_text=True)
        self.assertIn("【标题】", text)
        self.assertIn("【开头】", text)
        self.assertIn("【正文】", text)

    def test_generate_validation_error_json(self):
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

    def test_generate_multi_versions(self):
        resp = self.client.post(
            "/generate-multi",
            json={
                "topic": "时间管理",
                "audience": "大学生",
                "objective": "提升学习效率",
                "keywords": "番茄钟,复盘",
            },
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("versions", data)
        self.assertEqual(len(data["versions"]), 3)
        self.assertIn("opening", data["versions"][0])

    def test_generate_best_versions(self):
        resp = self.client.post(
            "/generate-best",
            json={
                "topic": "时间管理",
                "audience": "大学生",
                "objective": "提升学习效率",
                "keywords": "番茄钟,复盘",
            },
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("best", data)
        self.assertIn("candidates", data)
        self.assertEqual(len(data["candidates"]), 10)
        self.assertIn("body", data["best"])


if __name__ == "__main__":
    unittest.main()