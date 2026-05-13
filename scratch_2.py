# Plotting dst values only
from datetime import datetime as dt
import matplotlib.pyplot as plt


# Defining lists to store timestamps and corresponding values
dst_date = []
dst_value = []

with open('Oct 2025.request', 'r') as d:
    dst_lines = d.readlines()

year = int(dst_lines[0][3:5]) + 2000
month = int(dst_lines[0][5:7])

for line in dst_lines:
    day = int(line[8:10])
    for i in range(0, 24):
        Date = dt(year, month, day, hour = i)
        dst_date.append(Date)
        dst = int(line[(20 + 4*i):(24 + 4*i)])
        dst_value.append(dst)

plt.plot(dst_date, dst_value)
plt.title("dst index for January 2026")
plt.xlabel("Date and Time in UTC")
plt.ylabel("dst index (nT)")
plt.axhline(y=-200, linestyle=':', color='red', linewidth=2)
plt.axhline(y=-100, linestyle=':', color='orange', linewidth=2)
plt.axhline(y=-50, linestyle=':', color='yellow', linewidth=2)

plt.grid()

plt.show()