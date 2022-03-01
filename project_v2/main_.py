

from datetime import datetime

time_from = datetime.time(datetime.strptime("09:00:00","%H:%M:%S"))
time_to = datetime.time(datetime.strptime("20:30:00","%H:%M:%S"))


time = datetime.time(datetime.now())

print(time)

print(time_from)