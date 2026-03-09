from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass
class _Request:
    json_data: Any = None
    form: dict[str, Any] | None = None

    def get_json(self, silent: bool = False):
        if self.json_data is None and not silent:
            raise ValueError("No JSON payload")
        return self.json_data


_current_request: _Request | None = None


class _RequestProxy:
    def get_json(self, silent: bool = False):
        if _current_request is None:
            return None
        return _current_request.get_json(silent=silent)

    @property
    def form(self) -> dict[str, Any]:
        if _current_request is None or _current_request.form is None:
            return {}
        return _current_request.form


request = _RequestProxy()


class Response:
    def __init__(self, body: str, status_code: int = 200, mimetype: str = "text/plain"):
        self._body = body
        self.status_code = status_code
        self.mimetype = mimetype

    def get_data(self, as_text: bool = False):
        if as_text:
            return self._body
        return self._body.encode("utf-8")

    def get_json(self):
        return json.loads(self._body)


def jsonify(obj: Any) -> Response:
    return Response(json.dumps(obj, ensure_ascii=False), mimetype="application/json")


def render_template(template_name: str) -> str:
    template_path = Path("templates") / template_name
    return template_path.read_text(encoding="utf-8")


class Flask:
    def __init__(self, name: str):
        self.name = name
        self._routes: dict[tuple[str, str], Callable[..., Any]] = {}
        self.config: dict[str, Any] = {}

    def route(self, path: str, methods: list[str]):
        def decorator(func: Callable[..., Any]):
            for method in methods:
                self._routes[(method.upper(), path)] = func
            return func

        return decorator

    def get(self, path: str):
        return self.route(path, ["GET"])

    def post(self, path: str):
        return self.route(path, ["POST"])

    def test_client(self):
        app = self

        class _Client:
            def open(self, path: str, method: str, json_payload: Any = None):
                global _current_request
                handler = app._routes.get((method.upper(), path))
                if handler is None:
                    return Response("Not Found", status_code=404)

                _current_request = _Request(json_data=json_payload, form={})
                result = handler()
                _current_request = None

                if isinstance(result, tuple):
                    resp, status = result
                    resp.status_code = status
                    return resp
                if isinstance(result, Response):
                    return result
                if isinstance(result, str):
                    return Response(result, mimetype="text/html")
                return Response(str(result))

            def get(self, path: str):
                return self.open(path, "GET")

            def post(self, path: str, json: Any = None):
                return self.open(path, "POST", json_payload=json)

        return _Client()

    def run(self, debug: bool = False):
        print("Development server stub: this local flask shim does not start a real HTTP server.")
