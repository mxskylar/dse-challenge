import json
import requests
import os


ATTENDANCE_DATA_FILE = "data/attendances.json"


def get_mobilize_data(endpoint) -> json[list[dict]]:
    url = f"https://api.mobilize.us/v1/{endpoint}"
    headers = {"Authorization": f"Bearer {os.environ.get("MOBILIZE_API_KEY")}"}
    return requests.get(url, headers=headers).json()


def save_data(data: list[dict], file_path):
    with open(file_path) as f:
        json_data = json.dumps(data, f, indent=4)
        f.write(json_data)
    print(f"Data saved to: {file_path}")


if __name__ == "__main__":
    data = get_mobilize_data("attendances")
    # Cache attendance data so that it may be inserted offline by another pipeline
    save_data(data, ATTENDANCE_DATA_FILE)
