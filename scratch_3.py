# Scatter plot

import matplotlib.pyplot as plt
import numpy as np

x_n = [233.791, 267.698, 262.815, 297.011, 336.603, 269.561, 280.064, 294.211, 290.77]
y_n = [-4.549, 5.232, -8.655, -5.098, -2.131, -3.742, -4.241, -7.09, -3.372]

x_j6 = [247.919, 240.985, 262.626, 275.401, 322.916, 285.013, 274.359, 277.199, 286.342, 351.189]
y_j6 = [-5.355, -3.755, -7.992, -4.082, -0.174, -1.665, 0.143, -2.371, -3.602, 3.442]

x_j5 = [242.318, 195.204, 233.334, 255.255, 253.065, 237.138, 222.7, 247.264, 257.313, 238.132, 270.261, 266.132,
        259.47, 267.132, 264.719, 266.763, 247.572, 270.284, 267.412, 279.115, 272.733, 267.041, 246.914, 254.151,
        280.269, 266.674, 252.897, 352.734]
y_j5 = [-4.378, 2.951, -4.104, -5.207, 3.587, 2.426, 0.751, -2.747, -4.699, 0.692, -4.911, -2.849, -2.742, -1.915,
        -2.532, -2.441, 1.796, -2.307, -0.372, -1.356, -1.615, -0.476, 1.604, -4.835, -3.586, -5.333, -5.221, -0.292]

x = x_n + x_j6
y = y_n + y_j6

r = np.corrcoef(x, y)[0, 1]
print("The coefficient of correlation is", r)

plt.scatter(x_n, y_n, label = 'November 2025')
plt.scatter(x_j6, y_j6, label='January 2026')
plt.scatter(x_j5, y_j5, label='January 2025')


plt.xlabel('Height during quiet period (km)')
plt.ylabel('Prediction error (days)')
plt.title('Trend of Variation in Prediction Error with Height during quiet period')
plt.legend()
plt.grid()
plt.show()