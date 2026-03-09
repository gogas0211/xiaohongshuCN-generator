from __future__ import annotations

import argparse
from typing import Optional

from generator import XiaohongshuRequest, generate_post


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="小红书文案自动生成器")
    parser.add_argument("--topic", required=True, help="文案主题")
    parser.add_argument("--audience", required=True, help="目标人群")
    parser.add_argument("--objective", required=True, help="内容目标")
    parser.add_argument("--tone", default="亲切分享型", help="语气/风格，可用：干货型、亲切分享型、爆款种草型")
    parser.add_argument(
        "--keywords",
        default="",
        help="关键词，使用逗号分隔，例如：效率,学习方法,复盘",
    )
    parser.add_argument("--no-cta", action="store_true", help="不生成行动号召")
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    return parser.parse_args()


def _parse_keywords(raw_keywords: Optional[str]) -> list[str]:
    """支持中英文逗号的关键词解析。"""

    if not raw_keywords:
        return []
    normalized = raw_keywords.replace("，", ",")
    return [keyword.strip() for keyword in normalized.split(",") if keyword.strip()]


def main() -> None:
    args = parse_args()
    request = XiaohongshuRequest(
        topic=args.topic,
        audience=args.audience,
        objective=args.objective,
        tone=args.tone,
        keywords=_parse_keywords(args.keywords),
        no_cta=args.no_cta,
        seed=args.seed,
    )

    post = generate_post(request)

    print("=" * 20 + " 小红书文案 " + "=" * 20)
    print(f"\n【标题】\n{post.title}")
    print(f"\n【封面文案】\n{post.cover_text}")
    print(f"\n【开头】\n{post.opening}")
    print(f"\n【正文】\n{post.body}")
    if post.cta:
        print(f"\n【行动号召】\n{post.cta}")
    print(f"\n【话题标签】\n{' '.join(post.hashtags)}")


if __name__ == "__main__":
    main()
