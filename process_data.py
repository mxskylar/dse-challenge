import json
from mobilize.attendance import Attendance

if __name__ =="__main__":
  attendances: list[Attendance] = []
  # Open attendances JSON file
  with open('data/attendances.json') as f:
    attendances = [Attendance(**attendance) for attendance in json.loads(f.read())]
    print(attendances[0])
