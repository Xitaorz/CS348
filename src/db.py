from __future__ import annotations
import pandas as pd

import os
from typing import Any, List, Dict, Optional

import pymysql
from pymysql.cursors import DictCursor
from sqlalchemy import create_engine

from dotenv import load_dotenv
load_dotenv() 

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

    def import_csv(self, file_path: str, table_name: str, sample=False) -> int | None:
        df = pd.read_csv(file_path)
        if sample:
            df = df.sample(n=200, random_state=1)
        
        print(create_engine(self.connection_string))
        print(df.to_sql(table_name, create_engine(self.connection_string), if_exists='replace', index=False))
    
    def import_df(self, df: pd.DataFrame, table_name: str) -> int | None:
        return df.to_sql(table_name, create_engine(self.connection_string), if_exists='replace', index=False)

    def connect(self) -> None:
        host = os.getenv("MYSQL_HOST", "127.0.0.1")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASS", "")
        database = os.getenv("MYSQL_DB", "")
        self.connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

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
    
    #execute sql scripts
    def execute_script(self, sql_text: str) -> None:
        conn = self._ensure_conn()
        statements = [s.strip() for s in sql_text.split(";") if s.strip()]
        with conn.cursor() as cur:
            for stmt in statements:
                cur.execute(stmt)
    
    #list all students
    def list_students(self) -> List[Dict[str, Any]]:
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

#initialize and return a db
def get_db() -> DB:
    db = DB()
    db.connect()
    return db
