from __future__ import annotations

import sys
from pathlib import Path
from typing import List

from .db import get_db, DB


def _read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")




def init_db() -> None:
    """
    Initialize schema and example data in the configured MySQL database.
    """
    db: DB = get_db()

    schema_sql = _read_file("schema.sql")
    db.execute_script(schema_sql)

    example_sql = _read_file("example.sql")
    db.execute_script(example_sql)

    print("Database initialized and exampleed.")


def ping() -> int:
    """
    CLI connectivity check; exit code 0 = success.
    """
    db: DB = get_db()
    if db.ping():
        print("DB OK")
        return 0
    print("DB DOWN")
    return 1


def list_students() -> int:
    """
    CLI command: fetch all students and print them.
    Exit code 0 = success, 1 = failure.
    """
    try:
        db: DB = get_db()
        result = db.list_students()
        if result:
            for row in result:
                print(row)
            return 0
        else:
            print("No rows found.")
            return 1
    except Exception as e:
        print("Error:", e)
        return 1

def main(argv: List[str]) -> int:

    cmd = argv[1].lower()
    if cmd == "init":
        init_db()
        return 0
    if cmd == "ping":
        return ping()
    if cmd == "list":
        return list_students()

    print(f"Unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
