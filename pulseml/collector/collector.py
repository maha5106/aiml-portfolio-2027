import psutil
import time
import sqlite3

# how many seconds to wait between readings
INTERVAL = 5 

conn = sqlite3.connect('data/metrics.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp REAL,
        cpu_percent REAL,
        ram_percent REAL,
        disk_read_delta INTEGER,
        disk_write_delta INTEGER,
        net_read_delta INTEGER,
        net_write_delta INTEGER,
        battery_percent REAL,
        process_count INTEGER
    )
''')
conn.commit()
print("The collector started and will log every 5 seconds")

previous_disk_read = 0
previous_disk_write = 0
previous_net_read = 0
previous_net_write = 0

while True:
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    cpu_percent = psutil.cpu_percent(interval=1)
    ram_percent = psutil.virtual_memory().percent
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    battery_percent = psutil.sensors_battery().percent if psutil.sensors_battery() else None
    process_count = len(psutil.pids())

    # Calculate deltas for disk and network I/O
    disk_read_delta = disk_io.read_bytes - previous_disk_read
    disk_write_delta = disk_io.write_bytes - previous_disk_write
    net_read_delta = net_io.bytes_recv - previous_net_read
    net_write_delta = net_io.bytes_sent - previous_net_write

    cursor.execute('''
        INSERT INTO metrics (timestamp, cpu_percent, ram_percent, disk_read_delta, disk_write_delta, net_read_delta, net_write_delta, battery_percent, process_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (timestamp, cpu_percent, ram_percent, disk_read_delta, disk_write_delta, net_read_delta, net_write_delta, battery_percent, process_count))

    conn.commit()
    print(f"Logged metrics at {timestamp}: CPU {cpu_percent}%, RAM {ram_percent}%, Disk Read Delta {disk_read_delta} bytes, Disk Write Delta {disk_write_delta} bytes, Network Read Delta {net_read_delta} bytes, Network Write Delta {net_write_delta} bytes, Battery {battery_percent}%, Process Count {process_count}")

    # Update previous values
    previous_disk_read = disk_io.read_bytes
    previous_disk_write = disk_io.write_bytes
    previous_net_read = net_io.bytes_recv
    previous_net_write = net_io.bytes_sent

    time.sleep(INTERVAL)
