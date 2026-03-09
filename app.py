from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from generator import XiaohongshuRequest, generate_post


app = Flask(__name__)


def _parse_keywords(raw_keywords: str) -> list[str]:
    normalized = (raw_keywords or "").replace("，", ",")
    return [keyword.strip() for keyword in normalized.split(",") if keyword.strip()]


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    payload = request.get_json(silent=True) or request.form

    req = XiaohongshuRequest(
        topic=str(payload.get("topic", "")),
        audience=str(payload.get("audience", "")),
        objective=str(payload.get("objective", "")),
        keywords=_parse_keywords(str(payload.get("keywords", ""))),
    )

    try:
        post = generate_post(req)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(
        {
            "title": post.title,
            "opening": post.opening,
            "body": post.body,
            "cta": post.cta,
            "hashtags": post.hashtags,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
