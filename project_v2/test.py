

from datetime import datetime

time_from = datetime.time(datetime.strptime("09:00:00","%H:%M:%S"))
time_to = datetime.time(datetime.strptime("20:30:00","%H:%M:%S"))

now_min = datetime.now().minute.__str__()


time = datetime.time(datetime.now()).__str__()

now_min = time[4]
print(now_min)

# print(time)

# print(time_from)