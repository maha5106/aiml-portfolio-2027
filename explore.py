import psutil
import time

print("=== PULSEML SYSTEM RECONNAISSANCE ="
"==")
print(f"TIMESTAMP:'{time.strftime('%Y-%m-%d %H:%M:%S')}'")

#CPU percent(instant reading)

cpu_percent =psutil.cpu_percent(interval=1)
print(f"CPU Usage:{cpu_percent}%")

#2.RAM Usage(instant reading)

ram = psutil.virtual_memory()
print(f"RAM Usage:{ram.percent}%")

#3.Disk I/O(cumulative since boot)

disk_io = psutil.disk_io_counters()
print(f"Disk Read:{disk_io.read_bytes}bytes")
print(f"Disk Write:{disk_io.write_bytes}bytes")

#4.Network I/O(cumulative since boot)

net_io = psutil.net_io_counters()
print(f"Network Read:{net_io.bytes_recv}bytes")
print(f"Network Write:{net_io.bytes_sent}bytes")

#5.Battery (instant reading)
battery = psutil.sensors_battery()
if battery.percent:
    print(f"Battery.percent:{battery.percent}%")
else:
    print("Battery: N/A(desktop)")

#6.process count

process_count = len(psutil.pids())
print(f"Process Count:{process_count}")
