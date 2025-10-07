from __future__ import annotations

import os
from flask import Flask, jsonify
from .db import get_db, DB


def create_app() -> Flask:
    app = Flask(__name__)

    db: DB = get_db()

    @app.get("/health/db")
    def health_db():
        if db.ping():
            return jsonify({"db": "ok"})
        return jsonify({"db": "down"}), 500

    @app.get("/students")
    def list_students():
        try:
            rows = db.list_students()
            return jsonify(rows)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
