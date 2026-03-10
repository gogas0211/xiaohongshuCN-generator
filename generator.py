from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Sequence


DEFAULT_TONE = "真诚"
STYLE_GANHUO = "干货型"
STYLE_SHARE = "亲切分享型"
STYLE_SEEDING = "爆款种草型"

STYLE_ALIASES = {
    "干货": STYLE_GANHUO,
    "干货型": STYLE_GANHUO,
    "亲切": STYLE_SHARE,
    "亲切分享": STYLE_SHARE,
    "亲切分享型": STYLE_SHARE,
    "分享": STYLE_SHARE,
    "爆款": STYLE_SEEDING,
    "种草": STYLE_SEEDING,
    "爆款种草": STYLE_SEEDING,
    "爆款种草型": STYLE_SEEDING,
}


@dataclass
class XiaohongshuRequest:
    """小红书文案生成请求参数。"""

    topic: str
    audience: str
    objective: str
    tone: str = DEFAULT_TONE
    keywords: List[str] = field(default_factory=list)
    no_cta: bool = False
    seed: Optional[int] = None


@dataclass
class XiaohongshuPost:
    """结构化小红书文案输出。"""

    title: str
    opening: str
    body: str
    cta: str
    hashtags: List[str]


def _normalize_keywords(keywords: Optional[Iterable[str]]) -> List[str]:
    if not keywords:
        return []
    return [str(keyword).strip() for keyword in keywords if str(keyword).strip()]


def _pick(rng: random.Random, choices: Sequence[str]) -> str:
    return choices[rng.randrange(len(choices))]


def _require_non_empty(field_name: str, value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} 不能为空")
    return normalized


def _normalize_style(tone: str) -> str:
    normalized = (tone or "").strip()
    return STYLE_ALIASES.get(normalized, STYLE_SHARE)


def _build_hashtags(style: str, topic: str, objective: str, audience: str, keywords: List[str]) -> List[str]:
    """生成更自然的 hashtags，控制数量并补充平台常见语义标签。"""

    base_tags = [topic, objective]
    if keywords:
        base_tags.extend(keywords[:2])
    # 人群标签放在后面，避免过度“生硬人群词”抢占前排。
    base_tags.append(audience)

    style_tags = {
        STYLE_GANHUO: ["学习方法", "效率提升"],
        STYLE_SHARE: ["经验分享", "一起成长"],
        STYLE_SEEDING: ["自用分享", "好用不踩雷"],
    }
    candidates = base_tags + style_tags[style]

    hashtags: List[str] = []
    seen = set()
    for part in candidates:
        tag = part.replace(" ", "")
        if not tag or tag in seen:
            continue
        hashtags.append(f"#{tag}")
        seen.add(tag)
        if len(hashtags) >= 6:
            break
    return hashtags


def _build_style_blocks(style: str, topic: str, audience: str, objective: str, keywords: List[str]) -> dict[str, Sequence[str]]:
    keyword_line = f"我自己会重点盯这几个关键词：{'、'.join(keywords)}。" if keywords else "这次不堆概念，直接给你能马上照做的步骤。"

    if style == STYLE_GANHUO:
        return {
            "titles": [
                f"🔥{topic}真的别硬撑！3步直接做到{objective}",
                f"看这一篇就够了✅ {audience}做{topic}的高效模板",
                f"收藏率超高！{topic}实操清单，照做就能{objective}",
            ],
            "openings": [
                f"今天不讲大道理，直接把我做{topic}最有效的流程给你📌。",
                f"如果你也总在{topic}上卡住，这篇可以直接当执行清单。",
            ],
            "bodies": [
                f"① 先把目标钉死：你现在要的就是“{objective}”，别一开始就分心。",
                f"② 把{topic}拆小：每次只做一个动作，完成感会上来，执行就稳了。",
                "③ 睡前复盘3分钟：保留有效动作，没效果的当场删掉。",
                keyword_line,
                "我自己就是靠这套从“想很多做很少”变成“每天都在推进”💪。",
            ],
            "ctas": [
                "要不要我把这份模板做成可打印版？评论区留“模板”我就发📮",
                "如果你想看进阶版（含避坑清单），点个收藏，我下篇继续拆✨",
            ],
        }

    if style == STYLE_SEEDING:
        return {
            "titles": [
                f"被问麻了😍 这个{topic}方法我真想安利给所有{audience}",
                f"挖到宝了✨ 做{topic}这样安排，真的更容易{objective}",
                f"近期最惊喜的改变！靠它做{topic}，轻松又上头",
            ],
            "openings": [
                f"认真说，这个{topic}方法我已经连用一段时间，体验感太好了🚀。",
                f"本来我也怕{topic}坚持不下来，结果这个做法真的让我改观了。",
            ],
            "bodies": [
                f"先给结论：它让我更稳定地做到“{objective}”，而且不会有压迫感。",
                f"核心思路是把{topic}做成“随手能开始”的动作，门槛越低越容易坚持。",
                "最香的是反馈很快，你会明显感觉到：自己真的在变好。",
                keyword_line,
                "如果你也想找一个轻松但有效的方法，这个我真心推荐你试一周💖。",
            ],
            "ctas": [
                "想看我完整流程（含翻车点）吗？留言“想抄作业”我就整理👇",
                "被种草的话先收藏，按这个节奏做7天，你会看到区别🧾",
            ],
        }

    return {
        "titles": [
            f"普通人也能做到✨ 我是这样把{topic}慢慢做起来的",
            f"最近变化最大的一件事：{topic}让我更容易{objective}",
            f"写给{audience}的真心话：{topic}其实可以很轻松",
        ],
        "openings": [
            f"这篇就当朋友聊天，我把自己做{topic}时最真实的感受分享给你🤍。",
            f"最近不少人问我{topic}怎么坚持，我把自己在用的小方法写清楚了。",
        ],
        "bodies": [
            f"以前我总想一步到位，后来才发现围绕“{objective}”慢慢推进更不累。",
            f"我现在会给{topic}留一个固定小时间，不求做很多，但求每天不断线。",
            "状态不好的那天，我就把目标缩小一点，先完成再优化，心态会轻松很多。",
            keyword_line,
            "如果你也在这个阶段，别急，按自己的节奏来，真的会一点点变好🌱。",
        ],
        "ctas": [
            "如果你也在实践类似方法，欢迎留言聊聊，我们可以互相打气💬",
            "觉得这篇有用就先收藏，执行卡住时回来对照，会更有方向📒",
        ],
    }


def generate_post(request: XiaohongshuRequest) -> XiaohongshuPost:
    """根据输入参数生成一篇结构化小红书文案。"""

    topic = _require_non_empty("topic", request.topic)
    audience = _require_non_empty("audience", request.audience)
    objective = _require_non_empty("objective", request.objective)
    tone = (request.tone or "").strip() or DEFAULT_TONE

    rng = random.Random(request.seed)
    keywords = _normalize_keywords(request.keywords)
    style = _normalize_style(tone)
    blocks = _build_style_blocks(style, topic, audience, objective, keywords)

    cta = "" if request.no_cta else _pick(rng, blocks["ctas"])
    hashtags = _build_hashtags(style, topic, objective, audience, keywords)

    return XiaohongshuPost(
        title=_pick(rng, blocks["titles"]),
        opening=_pick(rng, blocks["openings"]),
        body="\n".join(blocks["bodies"]),
        cta=cta,
        hashtags=hashtags,
    )
