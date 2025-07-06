import requests
from google.cloud import bigquery
import os


def download_data() -> json[list[dict]]:
    base_url = "https://api.mobilize.us/v1/"
    endpoint = "attendances"
    headers = {"Authorization": "Bearer {}".format(os.environ.get("MOBILIZE_API_KEY"))}

    response = requests.get(base_url + endpoint, headers=headers)
    result = response.json
    return result


def save_data(data: list[dict]) -> str:
    fp = "data/attendances.json"
    f = open(filepath, "w")
    import json

    json.dump(data, f, indent=4)


def load_events(filepath: str):
    file = open("data/attendances.json", "r")
    data = file.read()

    for row in data:
        try:
            client = bigquery.Client()
            table = client.get_table("wfp-data-project.mobilize.events")
            event = {
                key: value
                for key, value in row["event"].items()
                if key
                in (
                    "created_date",
                    "modified_date",
                    "id",
                    "title",
                    "event_type",
                    "summary",
                    "description",
                )
            }
            client.insert_rows(table, [event])
        except:
            print("error loading row")


# Only execute if in the main thread
# This avoids executing if a function is imported into another module
if __name__ =="__main__":
    data = download_data()
    filepath = save_data(data)
    loadevents(filepath)
