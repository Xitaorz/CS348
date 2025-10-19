from __future__ import annotations

import sys
from pathlib import Path
from typing import List

from .db import get_db, DB
import kagglehub
import os

DATASET_FILE_NAME = "tracks_features.csv"


def _read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")



#Execute .sql files to initialize table contents
def init_db() -> None:
    db: DB = get_db()

    schema_sql = _read_file("schema.sql")
    db.execute_script(schema_sql)

    example_sql = _read_file("example.sql")
    db.execute_script(example_sql)

    print("Database initialized and exampleed.")

def import_data() -> None: 
    path = kagglehub.dataset_download("rodolfofigueroa/spotify-12m-songs")
    print(f"Data downloaded to {path}")
    file = os.path.join(path, DATASET_FILE_NAME)
    db: DB = get_db()
    db.import_csv(file, "Songs", sample=True)

def download_data() -> None:
    path = kagglehub.dataset_download("rodolfofigueroa/spotify-12m-songs")
    print(f"Data downloaded to {path}")

#Tests connection
def ping() -> int:
    db: DB = get_db()
    if db.ping():
        print("DB OK")
        return 0
    print("DB DOWN")
    return 1

#list all rows in Students table
def list_students() -> int:
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
    if cmd == "download":
        download_data()
        return 0
    if cmd == "import":
        import_data()
        return 0

    print(f"Unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
