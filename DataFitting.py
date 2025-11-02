import csv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import statsmodels.api as sm

COL_COUNT = 548

def read_first_row_except_first(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        first_row = next(reader, [])
        return [str(cell) for cell in first_row[330:COL_COUNT + 1]]

csv_path = r"C:\Users\euaggelia\Desktop\PythonProject\datatable.csv"
values = read_first_row_except_first(csv_path)

time_objects = [datetime.strptime(t, "%Y-%m-%dT%H:%M:%S") for t in values]

start_time = time_objects[0]

time_seconds = [(t - start_time).total_seconds() for t in time_objects]

import csv
START_COL = 330
END_COL = 549
START_ROW = 463
END_ROW = 512

def compute_mean_intensities(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as f:
        reader = list(csv.reader(f))

        MEANINTS3 = []
        for col_idx in range(START_COL, END_COL):
            values = []
            for row_idx in range(START_ROW, END_ROW):
                try:
                    val = float(reader[row_idx][col_idx])
                    if val != 0.0:
                        values.append(val)
                except (IndexError, ValueError):
                    continue
            if values:
                mean_val = sum(values) / len(values)
            else:
                mean_val = 0.0
            MEANINTS3.append(mean_val)
    return MEANINTS3


MEANINTS3 = compute_mean_intensities(csv_path)

def oscillatory_linear(t, A, B, w, b, c):
    return A * np.cos(w * t) + B * np.sin(w * t) + b * t + c


t_data = np.array(time_seconds)
y_data = np.array(MEANINTS3)

initial_guess = [15, 15, 0.000628, 0.0002, 2.5]

params, _ = curve_fit(oscillatory_linear, t_data, y_data, p0=initial_guess)

t_fit = np.linspace(min(t_data), max(t_data), num=1000)
y_fit = oscillatory_linear(t_fit, *params)

plt.figure(figsize=(10, 5))
plt.plot(t_data, y_data, 'o', label='Original Data', markersize=3)
plt.plot(t_fit, y_fit, '-', label='Fit: A*cos(wt)+B*sin(wt)+linear(t)', linewidth=2)
plt.xlabel('Time (s)')
plt.ylabel('Signal Intensity')
plt.title('Fit to Oscillatory + Linear Trend')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

param_names = ['A', 'B', 'w', 'b', 'c']
for name, val in zip(param_names, params):
    print(f"{name} = {val:.6f}")
