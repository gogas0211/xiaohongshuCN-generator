from __future__ import annotations

from flask import Flask, jsonify, render_template, request, abort

from generator import (
    XiaohongshuRequest,
    generate_post,
    generate_ten_posts,
    generate_three_posts,
    select_best_post,
)

app = Flask(__name__)

# ✅ 防护：拦截 UptimeRobot（关键）
@app.before_request
def block_uptime_robot():
    ua = request.headers.get("User-Agent", "")
    if "UptimeRobot" in ua:
        abort(403)


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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    payload = request.json or {}
    req = _build_request(payload)
    post = generate_post(req)
    return jsonify({"post": post})


@app.route("/api/generate_three", methods=["POST"])
def api_generate_three():
    payload = request.json or {}
    req = _build_request(payload)
    posts = generate_three_posts(req)
    return jsonify({"posts": posts})


@app.route("/api/generate_ten", methods=["POST"])
def api_generate_ten():
    payload = request.json or {}
    req = _build_request(payload)
    posts = generate_ten_posts(req)
    return jsonify({"posts": posts})


@app.route("/api/select_best", methods=["POST"])
def api_select_best():
    payload = request.json or {}
    posts = payload.get("posts", [])
    best = select_best_post(posts)
    return jsonify({"best": best})


if __name__ == "__main__":
    app.run(debug=True)
