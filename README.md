# SCA DevOps Bootcamp — Monitoring Lab Stack

## What's Inside

| Service            | What It Does                          | Port  |
|--------------------|---------------------------------------|-------|
| pay-api            | The Flask application we're monitoring | 5000  |
| node-exporter      | Exposes system metrics (CPU, memory…) | 9100  |
| prometheus         | Scrapes and stores metrics            | 9090  |
| grafana            | Dashboards and visualization          | 3000  |
| loki               | Log aggregation backend               | 3100  |
| alloy              | Collects Docker logs → ships to Loki  | 12345 |
| traffic-generator  | Simulates user traffic against pay-api| —     |

## Prerequisites

- An EC2 instance (Ubuntu 22.04+ recommended, t2.medium or larger)
- Docker and Docker Compose installed
- Security group open for ports: 22, 3000, 5000, 9090, 9100

## Quick Start

```bash
# 1. Clone or copy this folder to your EC2 instance
# 2. Navigate into the folder
cd monitoring-stack

# 3. Start everything
docker compose up -d --build

# 4. Check all containers are running
docker compose ps

# 5. Wait 2-3 minutes for traffic to generate, then open:
#    Prometheus  →  http://<YOUR-EC2-IP>:9090
#    Grafana     →  http://<YOUR-EC2-IP>:3000   (admin / admin)
#    pay-api     →  http://<YOUR-EC2-IP>:5000
```

## Verify It Works

1. **pay-api** — Visit `http://<IP>:5000` and `http://<IP>:5000/payment`
2. **Node Exporter** — Visit `http://<IP>:9100/metrics` (system metrics)
3. **pay-api metrics** — Visit `http://<IP>:5000/metrics` (application metrics)
4. **Prometheus** — Visit `http://<IP>:9090`, go to Status → Targets. All three targets should show **UP**.
5. **Grafana** — Visit `http://<IP>:3000`, log in with admin/admin

## Stop Everything

```bash
docker compose down          # stops containers
docker compose down -v       # stops AND deletes stored data
```

## Folder Structure

```
monitoring-stack/
├── docker-compose.yml              # Defines all services
├── README.md                       # This file
├── pay-api/
│   ├── app.py                      # Flask application code
│   ├── requirements.txt            # Python dependencies
│   └── Dockerfile                  # Container build instructions
├── config/
│   ├── prometheus.yml              # Prometheus scrape configuration
│   ├── loki-config.yml             # Loki storage configuration
│   └── alloy-config.alloy          # Alloy log collection config
└── traffic-generator/
    └── generate-traffic.sh         # Script that simulates user traffic
```
