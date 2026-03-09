from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from generator import XiaohongshuRequest, generate_post, generate_ten_posts, generate_three_posts, select_best_post


app = Flask(__name__)


def _parse_keywords(raw_keywords: str) -> list[str]:
    normalized = (raw_keywords or "").replace("，", ",")
    return [keyword.strip() for keyword in normalized.split(",") if keyword.strip()]


def _build_request(payload) -> XiaohongshuRequest:
    return XiaohongshuRequest(
        topic=str(payload.get("topic", "")),
        audience=str(payload.get("audience", "")),
        objective=str(payload.get("objective", "")),
        keywords=_parse_keywords(str(payload.get("keywords", ""))),
    )


def _post_to_dict(post):
    return {
        "title": post.title,
        "cover_text": post.cover_text,
        "opening": post.opening,
        "body": post.body,
        "cta": post.cta,
        "hashtags": post.hashtags,
    }


@app.get("/")
def index():
    return render_template("index.html", result=None, error=None, multi_results=None, best_result=None)


@app.post("/generate")
def generate():
    is_json = request.is_json
    payload = request.get_json(silent=True) or request.form

    req = _build_request(payload)

    try:
        post = generate_post(req)
    except ValueError as exc:
        if is_json:
            return jsonify({"error": str(exc)}), 400
        return render_template("index.html", result=None, error=str(exc), multi_results=None, best_result=None), 400

    result = _post_to_dict(post)

    if is_json:
        return jsonify(result)
    return render_template("index.html", result=result, error=None, multi_results=None, best_result=None)


@app.post("/generate-multi")
def generate_multi():
    payload = request.get_json(silent=True) or request.form
    req = _build_request(payload)

    try:
        posts = generate_three_posts(req)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"versions": [_post_to_dict(post) for post in posts]})


@app.post("/generate-best")
def generate_best():
    payload = request.get_json(silent=True) or request.form
    req = _build_request(payload)

    try:
        posts = generate_ten_posts(req)
        best = select_best_post(posts)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "best": _post_to_dict(best),
            "candidates": [_post_to_dict(post) for post in posts],
        }
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
