from __future__ import annotations

import ast
import sys
from pathlib import Path
from typing import List

from .db import get_db, DB
import kagglehub
from kagglehub import KaggleDatasetAdapter
import pandas as pd

DATASET_FILE_NAME = "tracks_features.csv"


def _read_file(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")



#Execute .sql files to initialize table contents
def init_db() -> None:
    db: DB = get_db()

    schema_sql = _read_file("schema.sql")
    example_sql = _read_file("example.sql")
    db.execute_script(schema_sql)
    db.execute_script(example_sql)

    print("Database initialized and exampleed.")

def import_data() -> None: 
    df = kagglehub.dataset_load(
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
    print(df["release_date"].head())

    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d', errors="coerce")
    songs_df = df[["id", "name", "release_date"]]
    songs_df.rename(columns={"id": "sid"}, inplace=True)

    
    df['artists'] = df['artists'].apply(lambda x: ast.literal_eval(x))
    df['artist_ids'] = df['artist_ids'].apply(lambda x: ast.literal_eval(x))
    artists_df = df.explode(["artists", "artist_ids"])[["artists", "artist_ids"]].drop_duplicates(subset=["artist_ids"])
    artists_df.rename(columns={"artist_ids": "artid", "artists": "name"}, inplace=True)
    artists_df = artists_df[["artid", "name"]]
    albums_df = df[["album_id", "album", "release_date"]].drop_duplicates(subset=["album_id"])
    albums_df = albums_df.rename(columns={"album_id": "alid", "album": "title"}).drop_duplicates(subset=["alid"])
    
    

    print("Importing songs...")
    db.import_df(songs_df, "songs")
    print("Importing artists...")
    db.import_df(artists_df, "artists")
    print("Importing albums...")
    db.import_df(albums_df, "albums")
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
        import_data()
        return 0
    if cmd == "ping":
        return ping()
    if cmd == "list":
        return list_students()
    if cmd == "download":
        download_data()
        return 0

    print(f"Unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
