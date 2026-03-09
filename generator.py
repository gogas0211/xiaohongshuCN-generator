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
    topic: str
    audience: str
    objective: str
    tone: str = DEFAULT_TONE
    keywords: List[str] = field(default_factory=list)
    no_cta: bool = False
    seed: Optional[int] = None


@dataclass
class XiaohongshuPost:
    title: str
    cover_text: str
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


def _viral_title_templates(topic: str, audience: str, objective: str, style: str) -> List[str]:
    style_prefix = {
        STYLE_GANHUO: "实操版",
        STYLE_SHARE: "亲测版",
        STYLE_SEEDING: "种草版",
    }[style]

    return [
        f"被问爆了🔥 {topic}这样做，{objective}真的快",
        f"别再瞎试了！{topic}{style_prefix}，一篇讲透",
        f"看这一篇就够✅ {audience}做{topic}的完整路线",
        f"收藏率超高：{topic}从混乱到稳定的3步法",
        f"我后悔没早点知道！{topic}原来可以这么轻松",
        f"真的有用！{topic}让我明显更接近{objective}",
        f"不走弯路版：{topic}高效执行清单（可直接照做）",
        f"普通人也能上手：{topic}低门槛但高回报的方法",
        f"这套方法太顶了✨ 我靠{topic}慢慢做到{objective}",
        f"效率翻倍的关键：{topic}别靠意志力，靠流程",
        f"近期最惊喜改变！{topic}让我状态稳定了",
        f"从拖延到自律：{topic}真实复盘（含避坑）",
    ]


def _build_hashtags(style: str, topic: str, objective: str, audience: str, keywords: List[str]) -> List[str]:
    """自动生成 5~8 个标签。"""

    style_tags = {
        STYLE_GANHUO: ["方法论", "效率提升", "自我管理"],
        STYLE_SHARE: ["经验分享", "真实经历", "一起成长"],
        STYLE_SEEDING: ["亲测有效", "自用分享", "好用不踩雷"],
    }
    fallback_tags = ["小红书文案", "内容创作", "个人成长", "执行力", "复盘"]

    candidates = [topic, objective, audience] + keywords[:3] + style_tags[style] + fallback_tags

    hashtags: List[str] = []
    seen = set()
    for part in candidates:
        tag = part.replace(" ", "")
        if not tag or tag in seen:
            continue
        hashtags.append(f"#{tag}")
        seen.add(tag)
        if len(hashtags) >= 8:
            break

    while len(hashtags) < 5:
        extra = fallback_tags[len(hashtags) % len(fallback_tags)]
        tag = f"#{extra}"
        if tag not in hashtags:
            hashtags.append(tag)

    return hashtags


def _build_prompt_blocks(style: str, topic: str, audience: str, objective: str, keywords: List[str]) -> dict[str, Sequence[str]]:
    """爆款小红书 Prompt 算法：钩子标题→痛点共鸣→真实经历→方法总结→结尾总结→CTA。"""

    keyword_line = f"我这段时间重点盯的是：{'、'.join(keywords)}。" if keywords else "先不聊抽象概念，直接讲可执行动作。"

    pain_openings = [
        f"你是不是也遇到过：明明想把{topic}做好，但总是三天热度、结果不稳定？",
        f"最扎心的是，很多{audience}在{topic}上花了很多时间，却还是看不到明显变化。",
        f"如果你也有“想做但总被打断”的困扰，这篇就是写给你的。",
    ]

    real_experience = [
        "【真实经历】我之前也反复重开计划，工具越换越多，执行却总断档。",
        "后来我把目标拆小到“今天就能完成”的粒度，连续两周后节奏才真正稳下来。",
    ]

    method_summary = [
        "【方法总结】核心就三件事：先把目标写清、再把动作拆小、最后按天复盘。",
        f"围绕“{objective}”做{topic}时，千万别追求一次做满，先把连续性做出来。",
    ]

    final_summary = [
        "【总结】先稳定，再优化；先完成，再完美。这个顺序对普通人最友好。",
        "当你开始每天都能推进一点点，结果就会在某个时间点突然变得很明显。",
    ]

    if style == STYLE_GANHUO:
        body_lines = [
            f"① 先定结果：把“{objective}”写成一句话，贴在每天都能看到的位置。",
            f"② 再拆动作：把{topic}拆成10~20分钟的小任务，降低启动成本。",
            "③ 做复盘：每天只记两件事——哪个动作有效、哪个动作该删。",
            keyword_line,
            *real_experience,
            *method_summary,
            *final_summary,
            "这套方式不是玄学，是可复用的执行流程💪。",
        ]
    elif style == STYLE_SEEDING:
        body_lines = [
            f"先给你结果：我靠这套做{topic}后，明显更容易做到“{objective}”。",
            "它最香的点是：门槛低、反馈快，忙的时候也能推进。",
            "不会有强压迫感，反而越做越有掌控感。",
            keyword_line,
            *real_experience,
            *method_summary,
            *final_summary,
            "如果你也在找“轻松但有效”的方法，这个真的可以试一周💖。",
        ]
    else:
        body_lines = [
            f"我以前总想一步到位，后来发现围绕“{objective}”慢慢推进更不累。",
            f"现在我会给{topic}固定一个小时间，不求多，但求每天不断线。",
            "状态不好的日子，就把目标缩小，先完成再优化，压力会小很多。",
            keyword_line,
            *real_experience,
            *method_summary,
            *final_summary,
            "慢慢来，你会看到自己的变化是可累计的🌱。",
        ]

    return {
        "titles": _viral_title_templates(topic, audience, objective, style),
        "cover_texts": [
            f"{topic}\n3步上手\n{objective}",
            f"{topic}避坑指南\n{audience}必看",
            f"亲测有效\n{topic}\n执行模板",
            f"别再硬撑\n{topic}\n这样做更稳",
        ],
        "openings": pain_openings,
        "bodies": body_lines,
        "ctas": [
            "看完有启发的话，点个赞+收藏；你想看哪类场景模板，评论区告诉我👇",
            "如果你想要我把这套流程做成可直接套用的清单，留言“模板”我就发📮",
            "这篇先帮你走通从0到1，下篇我继续拆“如何稳定坚持30天”✨",
        ],
    }


def generate_post(request: XiaohongshuRequest) -> XiaohongshuPost:
    topic = _require_non_empty("topic", request.topic)
    audience = _require_non_empty("audience", request.audience)
    objective = _require_non_empty("objective", request.objective)
    tone = (request.tone or "").strip() or DEFAULT_TONE

    rng = random.Random(request.seed)
    keywords = _normalize_keywords(request.keywords)
    style = _normalize_style(tone)
    blocks = _build_prompt_blocks(style, topic, audience, objective, keywords)

    cta = "" if request.no_cta else _pick(rng, blocks["ctas"])
    hashtags = _build_hashtags(style, topic, objective, audience, keywords)

    return XiaohongshuPost(
        title=_pick(rng, blocks["titles"]),
        cover_text=_pick(rng, blocks["cover_texts"]),
        opening=_pick(rng, blocks["openings"]),
        body="\n".join(blocks["bodies"]),
        cta=cta,
        hashtags=hashtags,
    )


def _score_post(post: XiaohongshuPost) -> int:
    score = 0
    hook_words = ["收藏", "被问", "不走弯路", "效率", "惊喜", "讲透"]
    score += sum(1 for word in hook_words if word in post.title) * 2
    score += min(len(post.hashtags), 8)
    score += 2 if "【总结】" in post.body else 0
    score += 2 if "【真实经历】" in post.body else 0
    score += 2 if post.cta else 0
    score += 1 if post.cover_text else 0
    return score


def _generate_n_posts(request: XiaohongshuRequest, n: int) -> List[XiaohongshuPost]:
    posts: List[XiaohongshuPost] = []
    base_seed = request.seed
    for idx in range(n):
        seed = None if base_seed is None else base_seed + idx
        variant = XiaohongshuRequest(
            topic=request.topic,
            audience=request.audience,
            objective=request.objective,
            tone=request.tone,
            keywords=list(request.keywords),
            no_cta=request.no_cta,
            seed=seed,
        )
        posts.append(generate_post(variant))
    return posts


def generate_three_posts(request: XiaohongshuRequest) -> List[XiaohongshuPost]:
    return _generate_n_posts(request, 3)


def generate_ten_posts(request: XiaohongshuRequest) -> List[XiaohongshuPost]:
    return _generate_n_posts(request, 10)


def select_best_post(posts: List[XiaohongshuPost]) -> XiaohongshuPost:
    if not posts:
        raise ValueError("posts 不能为空")
    return max(posts, key=_score_post)
