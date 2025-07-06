import json
import pandas as pd

from google.cloud import bigquery, RetriableGbqTimeoutException
from ingest_mobilize_pipeline import ATTENDANCE_DATA_FILE


EVENT_COLUMNS = (
    "created_date",
    "modified_date",
    "id",
    "title",
    "event_type",
    "summary",
    "description",
)

def insert_events(file_path: str, tries: int = 3):
    attendances = []
    with open(file_path, "r") as f:
        attendances = json.loads(f.read())
    
    # Construct rows for each event associated with an attendance
    events = []
    for attendance in attendances:
        events.append({
            key: value
            for key, value in attendance["event"].items()
            if key
            in EVENT_COLUMNS
        })
    
    # The same event may be associated with more than one attendance,
    # so duplicates need to be dropped.
    df = pd.DataFrame(events).drop_duplicates()
    rows = df.to_list()
    
    # Retries if insert times out
    while tries > 0:
        try:
            client = bigquery.Client()
            table = client.get_table("wfp-data-project.mobilize.events")
            client.insert_rows(table, rows)
            break
        # Retries up to n times if the insert to GBQ times out
        except RetriableGbqTimeoutException as e:
            tries = tries - 1
            if tries == 0:
                raise e
            else:
                print("Retrying GBQ insert after timing out...")


if __name__ == "__main__":
    insert_events(ATTENDANCE_DATA_FILE)
    print("Data successfully inserted into GBQ!")