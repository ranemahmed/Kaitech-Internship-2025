import tkinter as tk
from tkinter import messagebox
from collections import defaultdict
import statistics


sensor_data = [
    ("S1", "2025-04-28 10:00", 35.2, 12.1, 0.002),
    ("S2", "2025-04-28 10:00", 36.5, 14.0, 0.003),
    ("S1", "2025-04-28 11:00", 36.1, 12.5, 0.0021),
    ("S3", "2025-04-28 10:00", 34.0, 11.8, 0.0025),
    ("S2", "2025-04-28 11:00", 37.2, 14.3, 0.0031),
    ("S1", "2025-04-28 12:00", 37.0, 13.0, 0.0022),
]


root = tk.Tk()
root.title("Sensor Data Analyzer")
root.geometry("700x650")
root.configure(bg="#f0f4f7") 


title_label = tk.Label(
    root,
    text="Sensor Data Analyzer",
    font=("Helvetica", 18, "bold"),
    fg="#004080",
    bg="#f0f4f7"
)
title_label.pack(pady=(10, 5))

result_text = tk.Text(
    root,
    height=25,
    width=85,
    font=("Consolas", 10),
    bg="white",
    fg="black",
    wrap=tk.WORD
)
result_text.pack(pady=10)

def group_by_sensor():
    data = defaultdict(list)
    for reading in sensor_data:
        sid = reading[0]
        data[sid].append(reading)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Grouped by Sensor (Dictionary):\n\n")
    for sid, readings in data.items():
        result_text.insert(tk.END, f"{sid}:\n")
        for r in readings:
            result_text.insert(tk.END, f"  {r}\n")
    return data

def show_extremes():
    result_text.delete(1.0, tk.END)
    sensors = set()
    for sid, _, temp, stress, _ in sensor_data:
        if temp > 36.5 or stress > 13.5:
            sensors.add(sid)
    result_text.insert(tk.END, "Sensors with extreme temperature >36.5 or stress >13.5:\n")
    result_text.insert(tk.END, f"{list(sensors)}\n")

def compare_intervals():
    result_text.delete(1.0, tk.END)
    r10 = [r for r in sensor_data if "10:00" in r[1]]
    r11 = [r for r in sensor_data if "11:00" in r[1]]
    result_text.insert(tk.END, "10:00 Readings:\n")
    for r in r10:
        result_text.insert(tk.END, f"{r}\n")
    result_text.insert(tk.END, "\n11:00 Readings:\n")
    for r in r11:
        result_text.insert(tk.END, f"{r}\n")

def summarize_data():
    data = group_by_sensor()
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Sensor Summary (Max, Min, Avg Temp + Max Displacement):\n\n")
    for sid, readings in data.items():
        temps = [r[2] for r in readings]
        disps = [r[4] for r in readings]
        result_text.insert(tk.END, f"{sid}:\n")
        result_text.insert(tk.END, f"  Max Temp: {max(temps)}\n")
        result_text.insert(tk.END, f"  Min Temp: {min(temps)}\n")
        result_text.insert(tk.END, f"  Avg Temp: {round(statistics.mean(temps), 2)}\n")
        result_text.insert(tk.END, f"  Max Displacement: {max(disps)}\n\n")

def stress_set():
    s_ids = {r[0] for r in sensor_data if r[3] > 13.0}
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Sensors with stress > 13.0 (Set):\n")
    result_text.insert(tk.END, f"{s_ids}\n")

def sorted_timestamps():
    timestamps = sorted({r[1] for r in sensor_data})
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Sorted Timestamps (List):\n")
    for ts in timestamps:
        result_text.insert(tk.END, f"{ts}\n")

def latest_readings():
    latest = {}
    for reading in sensor_data:
        sid, ts = reading[0], reading[1]
        if sid not in latest or ts > latest[sid][1]:
            latest[sid] = reading
    recent_tuple = tuple(latest.values())
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, "Most Recent Readings per Sensor (Tuple):\n")
    for item in recent_tuple:
        result_text.insert(tk.END, f"{item}\n")

btn_style = {
    "width": 30,
    "bg": "#0066cc",
    "fg": "white",
    "font": ("Arial", 10, "bold"),
}

tk.Button(root, text="Group by Sensor", command=group_by_sensor, **btn_style).pack(pady=2)
tk.Button(root, text="Show Extreme Sensors", command=show_extremes, **btn_style).pack(pady=2)
tk.Button(root, text="Compare 10:00 vs 11:00", command=compare_intervals, **btn_style).pack(pady=2)
tk.Button(root, text="Summarize Sensor Data", command=summarize_data, **btn_style).pack(pady=2)
tk.Button(root, text="Sensors with Stress > 13 (Set)", command=stress_set, **btn_style).pack(pady=2)
tk.Button(root, text="Sorted Timestamps (List)", command=sorted_timestamps, **btn_style).pack(pady=2)
tk.Button(root, text="Latest Readings (Tuple)", command=latest_readings, **btn_style).pack(pady=2)

root.mainloop()
