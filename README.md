# 🚀 DevOps CI/CD Pipeline — Production Telemetry Dashboard

A **production-grade** CI/CD pipeline that builds, tests, scans, and deploys a live system-metrics dashboard — fully containerised with Docker, orchestrated by Jenkins, and reverse-proxied through Nginx.

---

## 🏗️ Architecture

```
┌──────────────┐      ┌───────────────────────────────────────────────┐
│   Developer  │──git push──▶│              Jenkins CI/CD               │
└──────────────┘      │  ┌─────────┬────────┬────────┬──────────┐    │
                      │  │Checkout │  Lint  │  Test  │  Build   │    │
                      │  ├─────────┼────────┼────────┼──────────┤    │
                      │  │  Scan   │ Deploy │ Health │  Notify  │    │
                      │  └─────────┴────────┴────────┴──────────┘    │
                      └──────────────────┬──────────────────────────┘
                                         │ docker compose up
                                         ▼
                      ┌──────────────────────────────────────────┐
                      │          Docker Compose Stack           │
                      │                                          │
                      │  ┌────────────┐     ┌────────────────┐  │
                      │  │   Nginx    │◄───▶│   Flask App    │  │
                      │  │  :80 (pub) │     │  :5000 (priv)  │  │
                      │  └────────────┘     └────────────────┘  │
                      │         ▲                                │
                      │         │ devops-net (bridge)            │
                      └─────────┼────────────────────────────────┘
                                │
                      ┌─────────┴─────────┐
                      │   Browser / User  │
                      └───────────────────┘
```

---

## ✨ Features

| Layer | What's Included |
|---|---|
| **Dashboard** | Animated SVG gauges, live sparkline graphs, particle background, glassmorphism UI |
| **Metrics** | CPU, RAM, disk, network I/O, uptime, active threads, request count, API latency |
| **Backend** | Flask with health checks, metric history ring-buffer, request counter middleware |
| **Docker** | Multi-stage builds, non-root user, HEALTHCHECK, resource limits |
| **Orchestration** | Docker Compose with dependency ordering, restart policies, named networks |
| **CI/CD** | 8-stage Jenkins pipeline — lint, test, build, security scan, deploy, health verify |
| **Nginx** | Rate limiting, gzip compression, security headers (CSP, XSS, etc.) |
| **Testing** | pytest with 7+ tests, JUnit XML reporting for Jenkins |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-lightgrey?logo=flask)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?logo=jenkins)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?logo=nginx)

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose v2
- Python 3.9+ (for local dev)

### Run with Docker Compose (recommended)

```bash
# Clone and deploy
git clone <repo-url> && cd Devops-project
docker compose up -d --build

# View the dashboard
open http://localhost
```

### Run Locally (development)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
# Dashboard at http://localhost:5000
```

### Run Tests

```bash
pip install -r requirements.txt
pytest test_app.py -v
```

### Lint

```bash
flake8 app.py test_app.py
```

---

## 🔄 Jenkins Pipeline Stages

| # | Stage | Description |
|---|---|---|
| 1 | **Checkout** | Pull latest code from SCM |
| 2 | **Install** | Create venv, install pinned dependencies |
| 3 | **Lint** | Run flake8 code quality checks |
| 4 | **Test** | Run pytest, publish JUnit XML results |
| 5 | **Build** | Build versioned Docker images (app + nginx) |
| 6 | **Scan** | Trivy vulnerability scan on built images |
| 7 | **Deploy** | `docker compose up -d --build` |
| 8 | **Health** | Curl `/health` endpoint to verify deployment |

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Dashboard UI |
| `/metrics` | GET | Current system metrics (JSON) |
| `/metrics/history` | GET | Last 60 metric snapshots (JSON) |
| `/health` | GET | Structured health check |

---

## 📁 Project Structure

```
Devops-project/
├── app.py                  # Flask application with metrics endpoints
├── test_app.py             # pytest test suite (7+ tests)
├── requirements.txt        # Pinned Python dependencies
├── templates/
│   └── index.html          # Dashboard UI (gauges, sparklines, particles)
├── Dockerfile              # Multi-stage app image (non-root, healthcheck)
├── Dockerfile.nginx        # Nginx image with healthcheck
├── Dockerfile.jenkins      # Jenkins with Docker + Python tooling
├── nginx.conf              # Rate limiting, gzip, security headers
├── docker-compose.yml      # Multi-container orchestration
├── Jenkinsfile             # 8-stage CI/CD pipeline
├── .dockerignore           # Optimised Docker build context
└── .flake8                 # Linting configuration
```

---

## 📄 License

MIT
