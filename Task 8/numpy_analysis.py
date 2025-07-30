import numpy as np

sensor_data = [
    ("S1", "2025-04-28 10:00", 35.2, 12.1, 0.002),
    ("S2", "2025-04-28 10:00", 36.5, 14.0, 0.003),
    ("S1", "2025-04-28 11:00", 36.1, 12.5, 0.0021),
    ("S3", "2025-04-28 10:00", 34.0, 11.8, 0.0025),
    ("S2", "2025-04-28 11:00", 37.2, 14.3, 0.0031),
    ("S1", "2025-04-28 12:00", 37.0, 13.0, 0.0022),
]

dtype = [('sensor_id', 'U10'), ('timestamp', 'U20'), ('temperature', 'f4'), ('stress', 'f4'), ('displacement', 'f4')]
structured_array = np.array(sensor_data, dtype=dtype)

unique_sensors = np.unique(structured_array['sensor_id'])

print("Average readings per sensor:")
sensor_averages = {}
for sensor in unique_sensors:
    sensor_rows = structured_array[structured_array['sensor_id'] == sensor]
    avg_temp = np.mean(sensor_rows['temperature'])
    avg_stress = np.mean(sensor_rows['stress'])
    avg_disp = np.mean(sensor_rows['displacement'])
    sensor_averages[sensor] = {'temp': avg_temp, 'stress': avg_stress, 'disp': avg_disp}
    print(f"{sensor} => Temp: {avg_temp:.2f}°C, Stress: {avg_stress:.2f}, Displacement: {avg_disp:.5f}")

max_stress_sensor = max(sensor_averages.items(), key=lambda x: x[1]['stress'])
print(f"\nSensor with highest average stress: {max_stress_sensor[0]} ({max_stress_sensor[1]['stress']:.2f})")

high_temp_readings = structured_array[structured_array['temperature'] > 36.0]
print("\nReadings with temperature > 36.0°C:")
for row in high_temp_readings:
    print(row)






    
