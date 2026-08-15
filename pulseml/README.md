# PulseML — Real-Time System Anomaly Detection

**Status:** Day 2 Complete — Data Collection Phase Active  
**Goal:** Build an unsupervised anomaly detector that learns "normal" laptop behavior and alerts on anomalies in real time.

---

## What is PulseML?

PulseML is a personal system health monitor that:

1. **Collects** 6 system metrics every 5 seconds (CPU, RAM, Disk I/O, Network I/O, Battery, Process Count)
2. **Calculates** deltas for cumulative counters (Disk/Network bytes per interval)
3. **Stores** everything in a local SQLite time-series database
4. **Trains** an Isolation Forest model to learn "normal" behavior
5. **Serves** a live dashboard via FastAPI with real-time anomaly alerts

---

## Architecture
<img width="1251" height="739" alt="image" src="https://github.com/user-attachments/assets/aa3e120c-a2dd-485c-866f-64476b61104f" />

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Collection** | `psutil` | Cross-platform system metrics (CPU, RAM, Disk, Network, Battery, Processes) |
| **Database** | `SQLite3` | Lightweight, serverless time-series storage for 4,000+ daily readings |
| **ML / Anomaly Detection** | `scikit-learn` (Isolation Forest) | Unsupervised learning — no labels required |
| **ML Ops** | `joblib` | Model serialization and inference pipeline |
| **Backend** | `FastAPI` + `Pydantic v2` | High-performance async API with strict type validation |
| **Real-Time Streaming** | `Server-Sent Events (SSE)` | One-way event stream from backend to dashboard |
| **Visualization** | `Chart.js` | Zero-dependency, lightweight real-time charts |
| **Containerization** | `Docker` | Reproducible deployment across environments |
| **Deployment** | `Render` / `Railway` / `Fly.io` | Modern PaaS — free tier, auto-deploy from GitHub |
| **Dependency Management** | `uv` | Modern Python package installer (replaces `pip` + `requirements.txt`) |

## Data Schema

Table: `metrics`

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `id` | `INTEGER` | Auto-increment primary key | `1` |
| `timestamp` | `TEXT` | ISO-8601 local datetime | `2026-08-15 14:32:05` |
| `cpu_percent` | `REAL` | CPU utilization (0.0 – 100.0) | `23.5` |
| `ram_percent` | `REAL` | RAM utilization (0.0 – 100.0) | `86.2` |
| `disk_read_delta` | `INTEGER` | Bytes read since last sample | `1,048,576` |
| `disk_write_delta` | `INTEGER` | Bytes written since last sample | `524,288` |
| `net_read_delta` | `INTEGER` | Net bytes received since last sample | `2,048` |
| `net_write_delta` | `INTEGER` | Net bytes sent since last sample | `1,024` |
| `battery_percent` | `REAL` | Battery charge level (0.0 – 100.0) | `78.0` |
| `process_count` | `INTEGER` | Number of active OS processes | `338` |

**Key Design Decision:**  
`disk_*_delta` and `net_*_delta` store **per-interval deltas**, not cumulative counters. This prevents the "ever-increasing" problem that breaks time-series models.

