from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import List

from .db import get_db, DB
import kagglehub
from kagglehub import KaggleDatasetAdapter

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
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "rodolfofigueroa/spotify-12m-songs",
        "tracks_features.csv",
        # Provide any additional arguments like 
        # sql_query or pandas_kwargs. See the 
        # documenation for more information:
        # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
    )
    db: DB = get_db()

    df = df.sample(n=200, random_state=1)
    
    songs_df = df["id", "name", "release_date"]
    db.import_df(songs_df, "songs")
    
    df['artists'] = df['artists'].apply(lambda x: ast.literal_eval(x))
    df['artist_ids'] = df['artist_ids'].apply(lambda x: ast.literal_eval(x))
    artists_df = df.explode(["artists", "artist_ids"])[["artists", "artist_ids"]].drop_duplicates(subset=["artist_ids", "artists"])

    print("Importing songs...")
    db.import_df(df, "songs")
    print("Importing artists...")
    db.import_df(artists_df, "artists")
    print("Data imported to DB.")


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
