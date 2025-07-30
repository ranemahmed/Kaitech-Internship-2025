from collections import defaultdict
from datetime import datetime
from openpyxl import Workbook
import json

sensor_data = [
    ("S1", "2025-04-28 10:00", 35.2, 12.1, 0.002),
    ("S2", "2025-04-28 10:00", 36.5, 14.0, 0.003),
    ("S1", "2025-04-28 11:00", 36.1, 12.5, 0.0021),
    ("S3", "2025-04-28 10:00", 34.0, 11.8, 0.0025),
    ("S2", "2025-04-28 11:00", 37.2, 14.3, 0.0031),
    ("S1", "2025-04-28 12:00", 37.0, 13.0, 0.0022),
]

sensor_readings = defaultdict(list)
for record in sensor_data:
    sensor_id = record[0]
    sensor_readings[sensor_id].append(record)

high_stress_sensors = set()
for sensor_id, ts, temp, stress, disp in sensor_data:
    if stress > 13.0:
        high_stress_sensors.add(sensor_id)

summary = {}
for sensor_id, readings in sensor_readings.items():
    temps = [r[2] for r in readings]
    stresses = [r[3] for r in readings]
    disps = [r[4] for r in readings]

    summary[sensor_id] = {
        'max_temp': max(temps),
        'min_temp': min(temps),
        'avg_temp': round(sum(temps) / len(temps), 3),
        'max_stress': max(stresses),
        'min_stress': min(stresses),
        'avg_stress': round(sum(stresses) / len(stresses), 3),
        'max_disp': max(disps),
    }

timestamps = sorted(set([r[1] for r in sensor_data]))

latest_per_sensor = {}
for record in sensor_data:
    sensor_id, ts = record[0], record[1]
    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")

    if sensor_id not in latest_per_sensor or dt > latest_per_sensor[sensor_id][1]:
        latest_per_sensor[sensor_id] = (record, dt)

latest_readings = tuple([info[0] for info in latest_per_sensor.values()])

compare_readings = defaultdict(dict)
for sensor_id, records in sensor_readings.items():
    for r in records:
        compare_readings[r[1]][sensor_id] = {
            'Temperature': r[2],
            'Stress': r[3],
            'Displacement': r[4]
        }

compare_readings_list = []
for ts in sorted(compare_readings.keys()):
    entry = {'Timestamp': ts}
    for sensor in sensor_readings.keys():
        if sensor in compare_readings[ts]:
            vals = compare_readings[ts][sensor]
            entry[f'{sensor}_Temperature'] = vals['Temperature']
            entry[f'{sensor}_Stress'] = vals['Stress']
            entry[f'{sensor}_Displacement'] = vals['Displacement']
        else:
            entry[f'{sensor}_Temperature'] = None
            entry[f'{sensor}_Stress'] = None
            entry[f'{sensor}_Displacement'] = None
    compare_readings_list.append(entry)

def write_sheet(wb, sheet_name, headers, rows):
    ws = wb.create_sheet(title=sheet_name)
    ws.append(headers)
    for row in rows:
        ws.append(row)

wb = Workbook()
wb.remove(wb.active)

organized_rows = []
for sensor_id in sorted(sensor_readings.keys()):
    sorted_readings = sorted(sensor_readings[sensor_id], key=lambda x: datetime.strptime(x[1], "%Y-%m-%d %H:%M"))
    for r in sorted_readings:
        organized_rows.append(r)

write_sheet(
    wb,
    "Organized_Readings",
    ['Sensor', 'Timestamp', 'Temperature', 'Stress', 'Displacement'],
    organized_rows
)

extreme_rows = []
for sensor_id, stats in summary.items():
    extreme_rows.append([
        sensor_id,
        stats['max_temp'],
        stats['min_temp'],
        stats['max_stress'],
        stats['min_stress'],
        stats['max_disp']
    ])
write_sheet(
    wb,
    "Extreme_Values",
    ['Sensor', 'Max_Temperature', 'Min_Temperature', 'Max_Stress', 'Min_Stress', 'Max_Displacement'],
    extreme_rows
)

compare_headers = ['Timestamp']
for sensor_id in sorted(sensor_readings.keys()):
    compare_headers += [f'{sensor_id}_Temperature', f'{sensor_id}_Stress', f'{sensor_id}_Displacement']

compare_rows = []
for entry in compare_readings_list:
    row = [entry['Timestamp']]
    for sensor_id in sorted(sensor_readings.keys()):
        row.append(entry[f'{sensor_id}_Temperature'])
        row.append(entry[f'{sensor_id}_Stress'])
        row.append(entry[f'{sensor_id}_Displacement'])
    compare_rows.append(row)

write_sheet(wb, "Compared_Readings", compare_headers, compare_rows)

summary_rows = []
for sensor_id, stats in summary.items():
    summary_rows.append([
        sensor_id,
        stats['max_temp'],
        stats['min_temp'],
        stats['avg_temp'],
        stats['max_stress'],
        stats['min_stress'],
        stats['avg_stress'],
        stats['max_disp'],
    ])
write_sheet(
    wb,
    "Summary",
    ['Sensor', 'Max_Temperature', 'Min_Temperature', 'Avg_Temperature',
     'Max_Stress', 'Min_Stress', 'Avg_Stress', 'Max_Displacement'],
    summary_rows
)

temp_stats_rows = []
for sensor_id, stats in summary.items():
    temp_stats_rows.append([
        sensor_id,
        stats['max_temp'],
        stats['min_temp'],
        stats['avg_temp'],
    ])

write_sheet(
    wb,
    "Temperature_Stats",
    ['Sensor', 'Max_Temperature', 'Min_Temperature', 'Avg_Temperature'],
    temp_stats_rows
)

max_disp_rows = []
for sensor_id, stats in summary.items():
    max_disp_rows.append([
        sensor_id,
        stats['max_disp'],
    ])

write_sheet(
    wb,
    "Max_Displacement",
    ['Sensor', 'Max_Displacement'],
    max_disp_rows
)

grouped_rows = []
for sensor_id, readings in sensor_readings.items():
    for r in readings:
        grouped_rows.append(r)
write_sheet(
    wb,
    "Grouped_Data",
    ['Sensor', 'Timestamp', 'Temperature', 'Stress', 'Displacement'],
    grouped_rows
)

high_stress_rows = [(s,) for s in sorted(high_stress_sensors)]
write_sheet(wb, "High_Stress_Sensors", ['Sensor'], high_stress_rows)

timestamps_rows = [(ts,) for ts in sorted(timestamps)]
write_sheet(wb, "All_Timestamps", ['Timestamp'], timestamps_rows)

most_recent_rows = []
for record, dt in latest_per_sensor.values():
    most_recent_rows.append(record)
write_sheet(
    wb,
    "Most_Recent_Readings",
    ['Sensor', 'Timestamp', 'Temperature', 'Stress', 'Displacement'],
    most_recent_rows
)

excel_filename = "sensor_analysis_Task5.xlsx"
wb.save(excel_filename)
print(f"Excel file saved as '{excel_filename}'")

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, default=str)

save_json("organized_readings.json", organized_rows)
save_json("extreme_values.json", extreme_rows)
save_json("compared_readings.json", compare_readings_list)
save_json("summary.json", summary_rows)
save_json("temperature_stats.json", temp_stats_rows)
save_json("max_displacement.json", max_disp_rows)
save_json("grouped_data.json", grouped_rows)
save_json("high_stress_sensors.json", high_stress_rows)
save_json("all_timestamps.json", timestamps_rows)
save_json("most_recent_readings.json", most_recent_rows)

print("JSON files saved.")
