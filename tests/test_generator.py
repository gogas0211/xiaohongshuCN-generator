import unittest

from generator import (
    DEFAULT_TONE,
    XiaohongshuRequest,
    generate_post,
    generate_ten_posts,
    generate_three_posts,
    select_best_post,
)
from main import _parse_keywords


class TestGenerator(unittest.TestCase):
    def test_generate_post_contains_all_sections(self):
        request = XiaohongshuRequest(
            topic="新能源车",
            audience="上班族",
            objective="降低通勤成本",
            keywords=["用车成本", "真实体验"],
            seed=7,
        )

        post = generate_post(request)

        self.assertTrue(post.title)
        self.assertTrue(post.opening)
        self.assertTrue(post.body)
        self.assertTrue(post.cta)
        self.assertGreaterEqual(len(post.hashtags), 5)
        self.assertLessEqual(len(post.hashtags), 8)

    def test_default_tone(self):
        req = XiaohongshuRequest(topic="学习", audience="学生", objective="提分")
        self.assertEqual(req.tone, DEFAULT_TONE)

    def test_no_cta_flag(self):
        request = XiaohongshuRequest(
            topic="早起习惯",
            audience="职场新人",
            objective="建立稳定作息",
            no_cta=True,
            seed=42,
        )

        post = generate_post(request)
        self.assertEqual(post.cta, "")

    def test_same_seed_is_deterministic(self):
        request1 = XiaohongshuRequest(
            topic="自律打卡",
            audience="备考人群",
            objective="保持执行力",
            keywords=["计划", "复习"],
            seed=123,
        )
        request2 = XiaohongshuRequest(
            topic="自律打卡",
            audience="备考人群",
            objective="保持执行力",
            keywords=["计划", "复习"],
            seed=123,
        )

        post1 = generate_post(request1)
        post2 = generate_post(request2)

        self.assertEqual(post1.title, post2.title)
        self.assertEqual(post1.opening, post2.opening)
        self.assertEqual(post1.body, post2.body)
        self.assertEqual(post1.cta, post2.cta)
        self.assertEqual(post1.hashtags, post2.hashtags)

    def test_empty_required_fields_raise_error(self):
        with self.assertRaises(ValueError):
            generate_post(
                XiaohongshuRequest(
                    topic="   ",
                    audience="大学生",
                    objective="提升学习效率",
                )
            )

    def test_hashtags_deduplicate_and_trim_spaces(self):
        request = XiaohongshuRequest(
            topic=" 新能源 车 ",
            audience="上班族",
            objective="降低通勤成本",
            keywords=["用车成本", "用车成本", "  ", " 真实体验 "],
            seed=1,
        )

        post = generate_post(request)
        self.assertIn("#新能源车", post.hashtags)
        self.assertEqual(post.hashtags.count("#用车成本"), 1)
        self.assertLessEqual(len(post.hashtags), 8)
        self.assertGreaterEqual(len(post.hashtags), 5)

    def test_parse_keywords_support_chinese_comma(self):
        self.assertEqual(_parse_keywords("效率，学习方法, 复盘 ,"), ["效率", "学习方法", "复盘"])

    def test_parse_keywords_handles_none(self):
        self.assertEqual(_parse_keywords(None), [])

    def test_post_contains_viral_structure(self):
        post = generate_post(
            XiaohongshuRequest(
                topic="新能源车",
                audience="上班族",
                objective="降低通勤成本",
                seed=2,
            )
        )
        self.assertTrue(any(flag in post.opening for flag in ["很多朋友", "纠结", "误解", "网上说法很多"]))
        self.assertIn("1.", post.body)
        self.assertIn("2.", post.body)

    def test_titles_have_at_least_ten_templates_effect(self):
        req = XiaohongshuRequest(topic="时间管理", audience="大学生", objective="提升效率", seed=1)
        titles = {
            generate_post(XiaohongshuRequest(**{**req.__dict__, "seed": i})).title
            for i in range(30)
        }
        self.assertGreaterEqual(len(titles), 10)

    def test_generate_three_posts(self):
        posts = generate_three_posts(
            XiaohongshuRequest(topic="时间管理", audience="大学生", objective="提升效率", seed=10)
        )
        self.assertEqual(len(posts), 3)
        self.assertTrue(all(post.title for post in posts))

    def test_generate_ten_posts_and_select_best(self):
        posts = generate_ten_posts(
            XiaohongshuRequest(topic="时间管理", audience="大学生", objective="提升效率", seed=21)
        )
        self.assertEqual(len(posts), 10)
        best = select_best_post(posts)
        self.assertIn(best, posts)

    def test_select_best_post_rejects_empty(self):
        with self.assertRaises(ValueError):
            select_best_post([])


if __name__ == "__main__":
    unittest.main()