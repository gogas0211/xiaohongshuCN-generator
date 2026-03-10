from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional


DEFAULT_TONE = "真实分享"


@dataclass
class XiaohongshuRequest:
    topic: str
    audience: str
    objective: str
    keywords: List[str] = field(default_factory=list)
    tone: str = DEFAULT_TONE
    no_cta: bool = False
    seed: Optional[int] = None


@dataclass
class XiaohongshuPost:
    title: str
    opening: str
    body: str
    cta: str
    hashtags: List[str]

    def to_text(self) -> str:
        parts = [
            "【标题】",
            self.title,
            "",
            "【开头】",
            self.opening,
            "",
            "【正文】",
            self.body,
        ]
        if self.cta:
            parts.extend(["", "【行动号召】", self.cta])
        parts.extend(["", "【话题标签】", " ".join(self.hashtags)])
        return "\n".join(parts)


def _normalize_keywords(keywords: List[str]) -> List[str]:
    seen = set()
    result = []
    for kw in keywords:
        clean = kw.strip()
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result


def _pick(rng: random.Random, choices: List[str]) -> str:
    return choices[rng.randrange(len(choices))]


def _title_templates(topic: str) -> List[str]:
    return [
        f"买{topic}一年，我终于明白为什么很多人后悔",
        f"第一批做{topic}的人，现在都怎么样了？",
        f"{topic}到底值不值？真实体验一次说清楚",
        f"很多人劝我别碰{topic}，但我还是试了",
        f"如果重新开始，我一定先搞懂{topic}",
        f"关于{topic}，我踩过的坑比你想得多",
        f"做了{topic}之后，我才发现很多人都误会了",
        f"{topic}不是不能做，而是很多人一开始就做错了",
        f"我花了很久才明白：{topic}真的别急着下结论",
        f"想做{topic}的人，建议先看完这篇再决定",
    ]


def _opening_templates(topic: str) -> List[str]:
    return [
        f"最近很多朋友都在问我一件事：{topic}到底靠不靠谱？",
        f"说实话，我一开始做{topic}的时候，也纠结了很久。",
        f"如果再让我选一次，我会更早认真研究{topic}这件事。",
        f"买之前我以为{topic}会很简单，实际体验后才发现完全不是一回事。",
        f"很多人对{topic}其实有误解，真正用过之后感受会完全不一样。",
        f"关于{topic}，网上说法很多，但真正有用的经验并不多。",
    ]


def _experience_templates(topic: str, audience: str) -> List[str]:
    return [
        f"我自己接触{topic}已经有一段时间了，最明显的感受是：很多事情只有亲自试过才知道值不值。",
        f"如果你和我一样，属于{audience}，那你大概率也会在刚开始时被各种说法弄得更犹豫。",
        f"我原本以为只要开始做{topic}就会马上见效，后来才发现真正重要的是长期体验和细节成本。",
        f"我身边也有几位朋友在做{topic}，大家共同的感受是：优点确实明显，但坑也真的存在。",
    ]


def _pros_templates(topic: str, keywords: List[str]) -> List[str]:
    kw_text = "、".join(keywords[:3]) if keywords else "成本、体验、效率"
    return [
        f"先说让我最满意的地方。围绕{kw_text}这几个点，{topic}确实有它很香的一面。",
        f"真正体验下来，{topic}的优势不是嘴上说说，而是日常使用里会明显感觉到轻松很多。",
        f"如果只看实际感受，{topic}在不少场景里确实比我预期更友好。",
    ]


def _cons_templates(topic: str) -> List[str]:
    return [
        f"但我也想说实话，{topic}并不是完全没有问题，有些地方很多人开始之前根本不会注意。",
        f"不过客观说，{topic}也有让人纠结的地方，尤其是刚开始接触时会更明显。",
        f"如果你只看优点，很容易冲动决定，但{topic}的几个现实问题一定要提前想清楚。",
    ]


def _summary_templates(topic: str, audience: str) -> List[str]:
    return [
        f"所以如果你是{audience}，我会觉得：{topic}不是不能做，而是一定要先想清楚自己的真实需求。",
        f"总结下来，{topic}到底值不值，不是看别人怎么说，而是看它是不是真的适合你的生活方式。",
        f"说到底，{topic}没有绝对答案，关键是你更在意省钱、体验，还是长期稳定性。",
    ]


def _cta_templates(topic: str) -> List[str]:
    return [
        f"如果你也在纠结{topic}，可以先收藏这篇，后面慢慢对照看。",
        f"你现在更倾向继续了解{topic}，还是已经准备做决定了？评论区聊聊。",
        f"如果你也有关于{topic}的真实经历，欢迎留言，我想看看大家的感受是不是一样。",
        f"这类内容如果你还想继续看，我可以再整理一版更具体的避坑清单。",
    ]


def _build_body(rng: random.Random, req: XiaohongshuRequest) -> str:
    topic = req.topic.strip()
    audience = req.audience.strip()
    keywords = _normalize_keywords(req.keywords)

    experience = _pick(rng, _experience_templates(topic, audience))
    pros_intro = _pick(rng, _pros_templates(topic, keywords))
    cons_intro = _pick(rng, _cons_templates(topic))
    summary = _pick(rng, _summary_templates(topic, audience))

    pros_points = [
        "1. 真实使用门槛没有想象中那么高，适应之后会轻松很多。",
        "2. 只要场景匹配，长期体验往往比一开始担心的更稳定。",
        "3. 如果你比较在意日常成本和使用感受，这一点会非常明显。",
    ]

    cons_points = [
        "1. 前期信息很多，容易被各种说法带偏，反而更难判断。",
        "2. 不同人的使用场景差别很大，别人的“真香”不一定完全适合你。",
        "3. 如果忽略了一些现实条件，后面可能会有落差感。",
    ]

    body_parts = [
        experience,
        "",
        pros_intro,
        *pros_points,
        "",
        cons_intro,
        *cons_points,
        "",
        summary,
    ]
    return "\n".join(body_parts)


def _build_hashtags(req: XiaohongshuRequest) -> List[str]:
    topic = req.topic.strip()
    audience = req.audience.strip()
    keywords = _normalize_keywords(req.keywords)

    tags = []

    def add_tag(text: str) -> None:
        clean = text.strip().replace(" ", "")
        if not clean:
            return
        tag = f"#{clean}"
        if tag not in tags:
            tags.append(tag)

    add_tag(topic)

    generic = [
        "经验分享",
        "真实体验",
        "避坑指南",
        "收藏备用",
    ]
    for tag in generic:
        add_tag(tag)

    if audience:
        add_tag(audience)

    for kw in keywords[:4]:
        add_tag(kw)

    return tags[:8]


def generate_post(request: XiaohongshuRequest) -> XiaohongshuPost:
    if not request.topic or not request.topic.strip():
        raise ValueError("topic 不能为空")
    if not request.audience or not request.audience.strip():
        raise ValueError("audience 不能为空")
    if not request.objective or not request.objective.strip():
        raise ValueError("objective 不能为空")

    rng = random.Random(request.seed)
    topic = request.topic.strip()

    title = _pick(rng, _title_templates(topic))
    opening = _pick(rng, _opening_templates(topic))
    body = _build_body(rng, request)
    cta = "" if request.no_cta else _pick(rng, _cta_templates(topic))
    hashtags = _build_hashtags(request)

    return XiaohongshuPost(
        title=title,
        opening=opening,
        body=body,
        cta=cta,
        hashtags=hashtags,
    )


def generate_three_posts(request: XiaohongshuRequest) -> List[XiaohongshuPost]:
    base_seed = request.seed or 1
    posts = []
    for i in range(3):
        req = XiaohongshuRequest(
            topic=request.topic,
            audience=request.audience,
            objective=request.objective,
            keywords=list(request.keywords),
            tone=request.tone,
            no_cta=request.no_cta,
            seed=base_seed + i,
        )
        posts.append(generate_post(req))
    return posts


def generate_ten_posts(request: XiaohongshuRequest) -> List[XiaohongshuPost]:
    base_seed = request.seed or 1
    posts = []
    for i in range(10):
        req = XiaohongshuRequest(
            topic=request.topic,
            audience=request.audience,
            objective=request.objective,
            keywords=list(request.keywords),
            tone=request.tone,
            no_cta=request.no_cta,
            seed=base_seed + i,
        )
        posts.append(generate_post(req))
    return posts


def _score_post(post: XiaohongshuPost) -> int:
    score = 0

    title_rules = ["后悔", "值不值", "误会", "先看完", "踩过的坑", "到底"]
    for rule in title_rules:
        if rule in post.title:
            score += 3

    score += min(len(post.hashtags), 8)
    score += 2 if "真实" in post.body else 0
    score += 2 if "很多人" in post.opening else 0
    score += 2 if "评论区" in post.cta or "留言" in post.cta else 0

    return score


def select_best_post(posts: List[XiaohongshuPost]) -> XiaohongshuPost:
    if not posts:
        raise ValueError("posts 不能为空")
    return max(posts, key=_score_post)
