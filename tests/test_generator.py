import unittest

from generator import (
    STYLE_GANHUO,
    STYLE_SEEDING,
    STYLE_SHARE,
    XiaohongshuRequest,
    generate_post,
)
from main import _parse_keywords


class TestGenerator(unittest.TestCase):
    def test_generate_post_contains_all_sections(self):
        request = XiaohongshuRequest(
            topic="时间管理",
            audience="大学生",
            objective="提升学习效率",
            tone="干货",
            keywords=["番茄钟", "复盘"],
            seed=7,
        )

        post = generate_post(request)

        self.assertTrue(post.title)
        self.assertTrue(post.opening)
        self.assertTrue(post.body)
        self.assertTrue(post.cta)
        self.assertGreaterEqual(len(post.hashtags), 3)

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
            topic=" 时间 管理 ",
            audience="大学生",
            objective="提升 学习效率",
            keywords=["复盘", "复盘", "  ", "时间 管理"],
            seed=1,
        )

        post = generate_post(request)
        self.assertIn("#时间管理", post.hashtags)
        self.assertEqual(post.hashtags.count("#复盘"), 1)
        self.assertLessEqual(len(post.hashtags), 6)

    def test_parse_keywords_support_chinese_comma(self):
        self.assertEqual(
            _parse_keywords("效率，学习方法, 复盘 ,"),
            ["效率", "学习方法", "复盘"],
        )

    def test_parse_keywords_handles_none(self):
        self.assertEqual(_parse_keywords(None), [])

    def test_style_ganhuo_contains_practical_tone(self):
        post = generate_post(
            XiaohongshuRequest(
                topic="学习规划",
                audience="大学生",
                objective="提分",
                tone=STYLE_GANHUO,
                seed=10,
            )
        )
        self.assertIn("①", post.body)

    def test_style_share_contains_warm_tone(self):
        post = generate_post(
            XiaohongshuRequest(
                topic="运动习惯",
                audience="上班族",
                objective="保持状态",
                tone=STYLE_SHARE,
                seed=10,
            )
        )
        self.assertIn("按自己的节奏", post.body)

    def test_style_seeding_contains_recommendation_tone(self):
        post = generate_post(
            XiaohongshuRequest(
                topic="早睡",
                audience="熬夜党",
                objective="精神更好",
                tone=STYLE_SEEDING,
                seed=10,
            )
        )
        self.assertIn("真心推荐", post.body)

    def test_post_contains_emojis(self):
        post = generate_post(
            XiaohongshuRequest(
                topic="时间管理",
                audience="大学生",
                objective="提升效率",
                tone=STYLE_SHARE,
                seed=3,
            )
        )
        content = post.title + post.opening + post.body + post.cta
        self.assertRegex(content, r"[\U0001F300-\U0001FAFF]")

    def test_titles_have_viral_hook_keywords(self):
        post = generate_post(
            XiaohongshuRequest(
                topic="时间管理",
                audience="大学生",
                objective="提升效率",
                tone=STYLE_GANHUO,
                seed=1,
            )
        )
        hooks = ["收藏", "不走弯路", "看这一篇", "被问"]
        self.assertTrue(any(hook in post.title for hook in hooks))

    def test_style_hashtags_more_natural(self):
        post = generate_post(
            XiaohongshuRequest(
                topic="时间管理",
                audience="大学生",
                objective="提升效率",
                tone=STYLE_SHARE,
                seed=1,
            )
        )
        self.assertTrue(any(tag in post.hashtags for tag in ["#经验分享", "#一起成长"]))


if __name__ == "__main__":
    unittest.main()
