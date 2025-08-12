import pandas as pd
import json
import os
from datetime import datetime
from sqlalchemy import create_engine

class Solution():

    def execute(self):

        """Write your solution here."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

            # File path
            source_file = os.path.join("source", "scrap.csv")
            target_dir = "target"
            os.makedirs(target_dir, exist_ok=True)

            df = pd.read_csv(source_file)

            # Split duplicate and clean data
            duplicate_mask = df.duplicated(subset=['ids'], keep=False)
            df_reject = df[duplicate_mask]
            df_clean = df[~duplicate_mask]

            # Save reject CSV
            reject_csv_path = os.path.join(target_dir, f"data_reject_{timestamp}.csv")
            df_reject.to_csv(reject_csv_path, index=False)

            # Prepare clean JSON
            def format_json(df):
                data_list = []
                for _, row in df.iterrows():
                    data_list.append({
                        "dates": pd.to_datetime(row["dates"], dayfirst=True).strftime('%Y-%m-%d'),
                        "ids": str(row["ids"]),
                        "names": str(row["names"]).upper(),
                        "monthly_listeners": int(row["monthly_listeners"]),
                        "popularity": int(row["popularity"]),
                        "followers": int(row["followers"]),
                        "genres": self.safe_json_parse(row["genres"]),
                        "first_release": str(row["first_release"]),
                        "last_release": str(row["last_release"]),
                        "num_releases": int(row["num_releases"]),
                        "num_tracks": int(row["num_tracks"]),
                        "playlists_found": str(row["playlists_found"]),
                        "feat_track_ids": self.safe_json_parse(row["feat_track_ids"])
                    })
                return {"row_count": len(data_list), "data": data_list}

            clean_json = format_json(df_clean)
            clean_json_path = os.path.join(target_dir, f"data_{timestamp}.json")
            with open(clean_json_path, "w") as f:
                json.dump(clean_json, f, indent=4)

            # DB Connection
            user = "postgres"
            password = "UnlockDatabase"
            host = "host.docker.internal" if os.environ.get("IN_DOCKER") else "localhost"
            port = 5432
            database = "edts_test"

            #engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
            engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}")


            # Insert to DB
            df_clean.to_sql("data", engine, if_exists="replace", index=False)
            df_reject.to_sql("data_reject", engine, if_exists="replace", index=False)

            print("Finish process successfully")

        except Exception as e:
            print(f"Error occured: {e}")
        return
    
    def safe_json_parse(self, value):
        if pd.isna(value) or str(value).strip() == "":
            return []
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return []


if __name__ == "__main__":
    _ = Solution().execute()