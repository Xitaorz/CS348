from __future__ import annotations

from dotenv import load_dotenv
load_dotenv() 

import os
from typing import Any, Iterable, List, Dict, Optional

import pymysql
from pymysql.cursors import DictCursor


print(
    "DB env ->",
    os.getenv("MYSQL_HOST"),
    os.getenv("MYSQL_PORT"),
    os.getenv("MYSQL_USER"),
    "(password set:" , "yes" if os.getenv("MYSQL_PASS") else "no", ")",
    os.getenv("MYSQL_DB"),
)

class DB:

    def __init__(self) -> None:
        self._conn: Optional[pymysql.connections.Connection] = None

    def connect(self) -> None:
        host = os.getenv("MYSQL_HOST", "127.0.0.1")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASS", "")
        database = os.getenv("MYSQL_DB", "")

        # Establish connection
        self._conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=DictCursor,
            autocommit=True,
        )

    def _ensure_conn(self) -> pymysql.connections.Connection:
        if self._conn is None:
            raise RuntimeError("DB connection has not been established. Call connect() first.")
        return self._conn
    
    def execute_script(self, sql_text: str) -> None:
        conn = self._ensure_conn()
        statements = [s.strip() for s in sql_text.split(";") if s.strip()]
        with conn.cursor() as cur:
            for stmt in statements:
                cur.execute(stmt)
    
    #list all students
    def list_students(self) -> List[Dict[str, Any]]:
        """
        Execute a SELECT query and return rows as list of dicts.
        """
        conn = self._ensure_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM Students")
            rows = cur.fetchall()
        return list(rows)

    # Ping the db and test the connection
    def ping(self) -> bool:
        try:
            conn = self._ensure_conn()
            conn.ping(reconnect=True)
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                _ = cur.fetchone()
            return True
        except Exception as e:
            print("PING ERROR:", repr(e))
            return False

def get_db() -> DB:
    db = DB()
    db.connect()
    return db
