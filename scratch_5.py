# Gives trajectory and velocities before decay, compares with dst index

import ephem
import math
import matplotlib.pyplot as plt
from datetime import datetime as dt
import numpy as np

# Constants
G = 6.67e-11    # SI
M = 5.97e+24    # SI
R = 6378000     # SI, m

print("="*30, "STARLINK Decays in January 2025", "="*30, sep="\n")

# Corresponding to the number of satellites, we have sets of altitudes, dates and velocities
sat_list = ['2020', '5784', '1486', '2152', '3666', '3684', '5404', '1528', '2244', '4009', '1720', '2347', '1602',
            '2181', '2392', '2441', '3886', '2546', '2541', '2477', '2573', '2688', '4003', '4601', '1891', '5144',
            '5466', '30406']
alt_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
            [], [], [], []]
date_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
            [], [], [], []]
vel_list = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
            [], [], [], []] # Not used in LBP results


# Number of brackets = number of satellites

# Defining observer to calculate altitude w.r.t.
obs = ephem.Observer()
obs.lon = '0'
obs.lat = '0'
obs.elevation = 0


# Bulk analysis begins
for i in range(0, 28):  # Stopping number = number of satellites
    satname = sat_list[i]
    satfile = satname + '.txt'  # To be used for accessing each file
    with open(satfile, 'r') as f:
        tle_lines = f.readlines()
    satname = 'Starlink-' + satname # To be used for naming the satellite object

    # Parse all TLEs (every 2 lines = 1 TLE set)
    for j in range(0, len(tle_lines), 2):
        line1 = tle_lines[j].strip()
        line2 = tle_lines[j + 1].strip()
        sat = ephem.readtle(satname, line1, line2)
        obs.date = sat.epoch    # Observation time set as = TLE epoch
        sat.compute(obs)
        v = (G * M * 2 * math.pi * sat.n / 86400) ** (1 / 3)    # in m
        alt_list[i].append(sat.elevation/1000) # Altitude in km
        date_list[i].append(ephem.Date(sat.epoch).datetime())
        vel_list[i].append(v/1000)
    altitude = (sat.elevation) / 1000
    while altitude > 100:
        obs.date = ephem.Date(obs.date + 0.1).datetime()
        sat.compute(obs)
        altitude = sat.elevation / 1000
        alt_list[i].append(altitude)
        date_list[i].append(ephem.Date(obs.date).datetime())
        vel_list[i].append(velocity(sat.n) / 1000)

# print("At", date_list[-1], ", the altitude is", alt_list[-1], "km and the velocity is", vel_list[-1], "km/s")

First_Date = date_list[0][0]
Last_Date = date_list[0][-1]

for i in range(1, 28):  # Stopping number = number of satellite
    Last_Date = max(Last_Date, date_list[i][-1])

# Defining lists to store timestamps and corresponding values
dst_date = []
dst_value = []

def dst_func(File_Name):    # The variable takes name of the dst file
    with open(File_Name, 'r') as d:
        dst_lines = d.readlines()

    year = int(dst_lines[0][3:5]) + 2000
    month = int(dst_lines[0][5:7])

    for line in dst_lines:
        day = int(line[8:10])
        for i in range(0, 24):
            Date = dt(year, month, day, hour = i)
            if Date >= First_Date:
                dst_date.append(Date)
                dst = int(line[(20 + 4*i):(24 + 4*i)])
                dst_value.append(dst)
        if Date >= Last_Date:
            break

dst_func('Dec 2024.request')
dst_func('Jan 2025.request')

# HSV colormap provides evenly spaced hues, unique colours required to plot 28 lines!
colors = plt.cm.hsv(np.linspace(0, 0.96, 28))

# The plot begins!
for i in range(0, 28):  # Stopping number = number of satellites
    satname = 'STARLINK-' + sat_list[i][0:5]
    color = colors[i]
    plt.plot(date_list[i], alt_list[i], lw=1, label = satname, color = color)
plt.title("Decays of STARLINK Satellites after the January 2025 Storm")
# plt.xlabel("Date and Time in UTC")
plt.ylabel("Altitude (km)")
plt.axhline(y=100, linestyle=':', color='blue', linewidth=2)
plt.text(0.01, 102, 'Karman Line', color='blue', fontsize=10,
         transform=plt.gca().get_yaxis_transform())
plt.axhspan(ymin = 320, ymax = 260, color='gray', linewidth=4, alpha = 0.1)
plt.axhline(y=280, linestyle=':', color='red', linewidth=2)
plt.legend(ncol=2, fontsize="small")

ax2 = plt.twinx()
ax2.plot(dst_date, dst_value, lw=0.5, alpha=0.5)
ax2.set_ylabel("Dst (nT)")
plt.axhline(y=-50, linestyle='dashed', color='olive', linewidth=1, alpha = 0.5)
plt.text(0.95, -48, 'Mild', color='olive', fontsize=8,
         transform=plt.gca().get_yaxis_transform())
plt.axhline(y=-100, linestyle='dashed', color='orange', linewidth=1, alpha = 0.5)
plt.text(0.95, -98, 'Moderate', color='orange', fontsize=8,
         transform=plt.gca().get_yaxis_transform())
plt.axhline(y=-200, linestyle='dashed', color='red', linewidth=1, alpha = 0.5)
plt.text(0.95, -198, 'Severe', color='red', fontsize=8,
         transform=plt.gca().get_yaxis_transform())
# plt.axhline(y=ref_alt, linestyle=':', color='blue', linewidth=2)
plt.xlim(First_Date, Last_Date)

# plt.axvline(x=ref_epoch.datetime(), linestyle=':', color='blue', linewidth=2)
plt.grid()


plt.grid()

plt.show()
