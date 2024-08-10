import re
from datetime import datetime
import pandas as pd
from bokeh.plotting import figure, output_file, save

# Path file
file_path = r'C:\Users\barli\OneDrive\Desktop\test python\soal4\soal_chart_bokeh.txt'
output_folder = r'C:\Users\barli\OneDrive\Desktop\test python\soal4'

def extract_data(file_path):
    timestamps = []
    sender_speeds = []

    # Regular expressions for extracting relevant data
    timestamp_regex = re.compile(r'Timestamp:\s*(.+)')
    speed_regex = re.compile(r'\[\s*\d+\]\s+\d+\.\d+-\d+\.\d+\s+sec\s+(\d+\.\d+)\s+MBytes\s+([\d.]+)\s+Mbits/sec')

    with open(file_path, 'r') as file:
        current_timestamp = None

        for line in file:
            timestamp_match = timestamp_regex.match(line)
            if timestamp_match:
                try:
                    current_timestamp = datetime.strptime(timestamp_match.group(1), '%Y-%m-%d %H:%M:%S')
                    print(f"Extracted timestamp: {current_timestamp}")  # Debug statement
                except ValueError:
                    print(f"Timestamp format error: {timestamp_match.group(1)}")
                continue

            print(f"Checking line for speed data: {line.strip()}")  # Debug statement

            speed_match = speed_regex.search(line)
            if speed_match and current_timestamp:
                try:
                    sender_speed = float(speed_match.group(2))
                    timestamps.append(current_timestamp)
                    sender_speeds.append(sender_speed)
                    print(f"Extracted speed: {sender_speed} at {current_timestamp}")  # Debug statement
                except ValueError:
                    print(f"Speed format error: {speed_match.group(2)}")

    return pd.DataFrame({
        'Timestamp': timestamps,
        'Sender Speed (Mbits/sec)': sender_speeds
    })

try:
    # Extract data from the file
    data = extract_data(file_path)

    # Check if data was extracted
    if data.empty:
        print("Data tidak ditemukan atau tidak valid.")
    else:
        # Set up output file path
        output_file(f"{output_folder}\\speed_sender_chart.html")

        # Create plot
        p = figure(x_axis_type='datetime', title="Speed Sender Over Time", width=800, height=400)
        p.line(data['Timestamp'], data['Sender Speed (Mbits/sec)'], line_width=2, color='blue', legend_label="Sender Speed")

        # Add labels and legend
        p.xaxis.axis_label = 'Timestamp'
        p.yaxis.axis_label = 'Speed (Mbits/sec)'
        p.legend.location = "top_left"

        # Save plot as HTML file
        save(p)

        print(f"Plot saved as 'speed_sender_chart.html' in folder '{output_folder}'.")

except FileNotFoundError:
    print("File tidak ditemukan.")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")
