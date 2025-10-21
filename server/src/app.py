from __future__ import annotations

import os
import time
from flask import Flask, jsonify, request
from .db import get_db, DB
from .manage import init_db
from flask_cors import CORS  



def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    max_retries = 30
    retry_delay = 1
    db = None
    
    for attempt in range(max_retries):
        try:
            db = get_db()
            print(f"Database connected successfully!")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Database connection attempt {attempt + 1}/{max_retries} failed. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print(f"Failed to connect to database after {max_retries} attempts: {e}")
                raise
    
    if db is None:
        raise RuntimeError("Database connection failed")
    
    try:
        with db._ensure_conn().cursor() as cur:
            cur.execute("SHOW TABLES LIKE 'users'")
            if not cur.fetchone():
                init_db()
                print("Database initialization complete.")
                import_data()
                print("Data imported.")
    except Exception as e:
        print(f"Error: {e}")

    @app.get("/health/db")
    def health_db():
        if db.ping():
            return jsonify({"db": "ok"})
        return jsonify({"db": "down"}), 500

    @app.get("/users")
    def list_users():
        try:
            rows = db.list_users()
            return jsonify(rows)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.get("/search")
    def search():
        """
        Search for songs, artists, and albums.
        Query parameter: q (search query)
        Example: /search?q=debug
        """
        try:
            query = request.args.get('q', '')
            if not query:
                return jsonify({"error": "Missing 'q' query parameter"}), 400
            
            results = db.search(query)
            return jsonify({
                "query": query,
                "count": len(results),
                "results": results
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.get("/tables")
    def show_tables():
        """Show all tables in the database."""
        try:
            tables = db.show_tables()
            return jsonify({
                "count": len(tables),
                "tables": tables
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.get("/ratings/average")
    def rating_averages():
        """
        Get average ratings for all songs.
        Shows song name, artist, average rating, and number of ratings.
        Implements query from test-sample-rating-avg.sql
        """
        try:
            ratings = db.get_rating_averages()
            return jsonify({
                "count": len(ratings),
                "ratings": ratings
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
