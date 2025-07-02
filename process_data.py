import json
from mobilize.attendance import Attendance

ATTENDANCES_DATA_FILE = "data/attendances.json"

if __name__ =="__main__":
  attendances: list[Attendance] = []
  # Open attendances JSON file
  with open(ATTENDANCES_DATA_FILE) as f:
    attendances = [Attendance(**attendance) for attendance in json.loads(f.read())]
    print(attendances[0])
