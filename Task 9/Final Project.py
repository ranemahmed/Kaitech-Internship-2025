import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

# Prepare Data
sensor_data = [
    ("S1", "2025-04-28 10:00", 35.2, 12.1, 0.002),
    ("S2", "2025-04-28 10:00", 36.5, 14.0, 0.003),
    ("S1", "2025-04-28 11:00", 36.1, 12.5, 0.0021),
    ("S3", "2025-04-28 10:00", 34.0, 11.8, 0.0025),
    ("S2", "2025-04-28 11:00", 37.2, 14.3, 0.0031),
    ("S1", "2025-04-28 12:00", 37.0, 13.0, 0.0022),
]
df = pd.DataFrame(sensor_data, columns=["sensor_id", "timestamp", "temperature", "stress", "displacement"])
df['timestamp'] = pd.to_datetime(df['timestamp'])

# App Setup
root = tk.Tk()
root.title("Sensor Data Analyzer")
root.geometry("1100x700")
root.configure(bg="#e8f0f8")

sidebar = tk.Frame(root, bg="#d9e6f2", width=220)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

main_area = tk.Frame(root, bg="#e8f0f8")
main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tk.Label(main_area, text="Sensor Data Analyzer", font=("Helvetica", 20, "bold"),
         fg="#0b3d91", bg="#e8f0f8").pack(pady=10)


output_frame = tk.Frame(main_area, bg="white", width=800, height=200)
output_frame.pack(pady=10)
output_frame.pack_propagate(False)

output_text = scrolledtext.ScrolledText(output_frame, font=("Consolas", 10), wrap=tk.WORD)
output_text.pack(fill=tk.BOTH, expand=True)


plot_title = tk.Label(main_area, text="Visualization Output", font=("Helvetica", 14, "bold"),
                      fg="#0b3d91", bg="#e8f0f8")
plot_title.pack(pady=(5, 0))

plot_frame = tk.Frame(main_area, bg="#e8f0f8", height=400)
plot_frame.pack(fill=tk.BOTH, expand=True)


def clear_plot():
    for widget in plot_frame.winfo_children():
        widget.destroy()

#Plots
def show_temperature_plot():
    clear_plot()
    fig, ax = plt.subplots(figsize=(8, 4))
    for sensor in df['sensor_id'].unique():
        sensor_df = df[df['sensor_id'] == sensor]
        ax.plot(sensor_df['timestamp'], sensor_df['temperature'], marker='o', label=sensor)
    ax.set_title("Temperature Over Time")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def show_stress_displacement_plot():
    clear_plot()
    fig, ax = plt.subplots(figsize=(8, 4))
    for sensor in df['sensor_id'].unique():
        sensor_df = df[df['sensor_id'] == sensor]
        ax.scatter(sensor_df['displacement'], sensor_df['stress'], label=sensor, s=80)
    ax.set_title("Stress vs Displacement")
    ax.set_xlabel("Displacement (mm)")
    ax.set_ylabel("Stress")
    ax.legend()
    ax.grid(True)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

def show_correlation_heatmap():
    clear_plot()
    fig, ax = plt.subplots(figsize=(6, 4))
    corr = df[['temperature', 'stress', 'displacement']].corr()
    sns.heatmap(corr, annot=True, cmap='Blues', fmt=".2f", ax=ax)
    ax.set_title("Correlation Heatmap")
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

#Feature Extraction and Analysis
def show_average_per_sensor():
    output_text.delete('1.0', tk.END)
    avg = df.groupby('sensor_id')[['temperature', 'stress', 'displacement']].mean()
    output_text.insert(tk.END, "Average Readings per Sensor:\n")
    output_text.insert(tk.END, avg.round(3).to_string())

def show_highest_avg_stress_sensor():
    output_text.delete('1.0', tk.END)
    avg = df.groupby('sensor_id')['stress'].mean()
    max_sensor = avg.idxmax()
    max_value = avg.max()
    output_text.insert(tk.END, f"Sensor with Highest Average Stress:\nSensor: {max_sensor} - Stress: {max_value:.2f}")

def show_high_temp_readings():
    output_text.delete('1.0', tk.END)
    high_temp = df[df['temperature'] > 36.0]
    output_text.insert(tk.END, "Readings with Temperature > 36.0°C:\n")
    output_text.insert(tk.END, high_temp.to_string(index=False))

def sidebar_label(title):
    return tk.Label(sidebar, text=title, font=("Helvetica", 12, "bold"),
                    bg="#d9e6f2", fg="#0b3d91", anchor="w", padx=10)

def sidebar_button(text, command):
    return tk.Button(sidebar, text=text, width=22, height=2, bg="#0077cc", fg="white",
                     activebackground="#005fa3", font=("Arial", 10, "bold"), bd=0, command=command)

sidebar_label("📋 Data Insights").pack(pady=(15, 5))
sidebar_button("Avg per Sensor", show_average_per_sensor).pack(pady=4)
sidebar_button("Highest Stress Sensor", show_highest_avg_stress_sensor).pack(pady=4)
sidebar_button("Temp > 36.0°C", show_high_temp_readings).pack(pady=4)

tk.Label(sidebar, text="––––––––––––––", bg="#d9e6f2", fg="#0b3d91").pack(pady=8)

sidebar_label("📊 Visualizations").pack(pady=(5, 5))
sidebar_button("Temp Over Time", show_temperature_plot).pack(pady=4)
sidebar_button("Stress vs Displacement", show_stress_displacement_plot).pack(pady=4)
sidebar_button("Correlation Heatmap", show_correlation_heatmap).pack(pady=4)

root.mainloop()

#------------------------------------------------------
#ML insight: 

#Predictive Maintenance:
# This sensor data can help predict when something might go wrong before it actually does.
# For example, if stress or temperature slowly increases over time, it might mean a part is wearing out.
# We can use these patterns to schedule maintenance early and avoid sudden failures.

#Anomaly Detection: 
# If a sensor suddenly shows strange readings — like a sudden jump in displacement or stress — that could be a warning sign.
# Even without knowing exactly what’s wrong, we can train a model to spot anything that looks unusual compared to normal behavior.
# This helps detect problems early, even if they’ve never happened before.

#Structural Health Prediction: 
# Over time, we can look at the sensor data and learn what "healthy" and "risky" conditions look like.
# Then we can build a simple system that checks if a sensor is showing signs of danger.
# This would help monitor the overall health of a structure and decide when to take action.
