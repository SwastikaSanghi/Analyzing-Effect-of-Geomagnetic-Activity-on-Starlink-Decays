# Single satellite analysis without dst

import ephem
import math
import matplotlib.pyplot as plt
from datetime import datetime

G = 6.67e-11    # SI
M = 5.97e+24    # SI
R = 6378000     # SI, m

obs = ephem.Observer()
obs.lon = '0'
obs.lat = '0'
obs.elevation = 0

alt_list = []
date_list = []
vel_list = []

def velocity(n):    # Returns in metres/second
    mean_motion = n
    v = (G * M * 2 * math.pi * mean_motion / 86400) ** (1 / 3)
    return v

with open('30406.txt', 'r') as f:
    tle_lines = f.readlines()

# Parse all TLEs (every 2 lines = 1 TLE set)
for j in range(0, len(tle_lines), 2):
    line1 = tle_lines[j].strip()
    line2 = tle_lines[j + 1].strip()
    sat = ephem.readtle('Starlink-30406', line1, line2)
    obs.date = sat.epoch
    sat.compute(obs)
    # print("Altitude is", sat.elevation/1000)
    if line1[21:23] == '01':
        print("During quiet times, the altitude is", round(sat.elevation/1000, 3), "km")
    v = (G * M * 2 * math.pi * sat.n / 86400) ** (1 / 3)    # in m
    alt_list.append(sat.elevation/1000) # Altitude in km
    date_list.append(ephem.Date(sat.epoch).datetime())
    vel_list.append(v / 1000)
    if 280 >= int(sat.elevation/1000) >= 279:
        print("=" * 30)
        print(sat.name)
        ref_epoch = ephem.Date(sat.epoch)
        print("ref_epoch is", ref_epoch)
        print("Reference altitude is", round(sat.elevation/1000, 3), "km")
        pred_epoch = ref_epoch
        while (sat.elevation)/1000 > 100:
            pred_epoch = ephem.Date(pred_epoch) + 1
            obs.date = pred_epoch
            sat.compute(obs)

        # Following piece of code used to find reference epoch in special cases
"""    if int(sat.elevation / 1000) == 265:
        print("=" * 30)
        print(sat.name)
        ref_epoch = ephem.Date(sat.epoch)
        print("ref_epoch is", ref_epoch)
        print("Reference altitude is", round(sat.elevation / 1000, 3), "km")
        pred_epoch = ref_epoch
        while (sat.elevation) / 1000 > 100:
            pred_epoch = ephem.Date(pred_epoch) + 1
            obs.date = pred_epoch
            sat.compute(obs)"""

altitude = (sat.elevation)/1000

print("Last TLE epoch is", ephem.Date(sat.epoch).datetime())
print("Last TLE altitude is", round(altitude, 3), "km")

print("For this satellite, reference epoch (280 km) is", ref_epoch)
print("Predicted re-entry epoch is", ephem.Date(pred_epoch))

while altitude > 100:
    obs.date = ephem.Date(obs.date + 0.1).datetime()
    sat.compute(obs)
    altitude = sat.elevation/1000
    alt_list.append(altitude)
    date_list.append(ephem.Date(obs.date).datetime())
    vel_list.append(velocity(sat.n)/1000)

Karman_epoch = ephem.Date(obs.date)

print("Actual re-entry epoch is", Karman_epoch, "at", round(altitude, 3), "km")
print("Prediction error is", round(pred_epoch - Karman_epoch, 3), "days")
print("Day difference, which is the number of days spent between reference altitude (280 km) and Karman line, is")
print(round(Karman_epoch - ref_epoch, 3))
print("Satellite decay rate is", round(180/(Karman_epoch - ref_epoch), 3), "km/day")


plt.plot(date_list, alt_list)
plt.title("Altitude Descent for STARLINK-30406")
plt.xlabel("Date and Time in UTC")
plt.ylabel("Altitude (km)")
# plt.axhline(y=ref_alt, linestyle=':', color='blue', linewidth=2)
plt.axhline(y=280, linestyle=':', color='red', linewidth=2)
plt.axhline(y=100, linestyle=':', color='red', linewidth=2)
# plt.axvline(x=ref_epoch.datetime(), linestyle=':', color='blue', linewidth=2)
plt.grid()

plt.show()
