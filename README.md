# ⚖️ CasualCourt — Autonomous Business Process Investigator

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.0+-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com/)

**CasualCourt** is an autonomous business process investigation platform designed to analyze operational telemetry, supply chain metrics, customer support tickets, payment gateways, and competitor pricing to discover root causes behind operational anomalies (such as sudden order cancellation spikes).

---

## 🌟 Key Features

- **Automated Root Cause Diagnosis**: Formulates and evaluates multiple competing hypotheses to isolate exact operational bottlenecks.
- **Causal & Evidence Analysis**: Measures temporal lead-lag patterns, supplier lead-time inflation, inventory stockouts, and anomaly timing.
- **Adversarial & Defense Engine**: Filters out false positive signals and noisy metrics (e.g., post-cancellation support tickets vs. true payment gateway outages).
- **Custom Dataset Upload & Validation**: Flexible ingestion engine supporting custom CSV/JSON operational telemetry uploads with schema verification.
- **Interactive UI Dashboard**: Modern, responsive web frontend featuring live investigation progress, hypothesis rankings, evidence breakdown, defense analysis, and interactive data visualization.

---

## 🏗️ Project Architecture

```
ANV26-AI-34_CasualCourt/
├── backend/                        # FastAPI Backend Service
│   ├── main.py                     # API routes & server configuration
│   ├── orchestrator.py             # Pipeline orchestration engine
│   ├── hypothesis_engine.py       # Hypothesis generation logic
│   ├── evidence_engine.py         # Evidence scoring & statistical metrics
│   ├── defense_engine.py          # Noise filtration & counter-argument evaluation
│   ├── data_loader.py             # Data loader & dynamic schema validation
│   ├── models.py                  # Pydantic data models & response schemas
│   ├── investigation_engine.py    # Core investigation process wrapper
│   └── test_engine.py             # Unit verification tests
├── CasualCourt_demo_dataset/       # Demo CSV Operational Telemetry
│   ├── orders.csv                 # Order transactions & status logs
│   ├── supplier_events.csv        # Supplier lead time & dispatch logs
│   ├── inventory.csv              # SKU stock level telemetry
│   ├── payments.csv               # Payment gateway transaction metrics
│   ├── tickets.csv                # Customer support ticket logs
│   ├── competitor_prices.csv      # Competitor price tracking
│   └── investigation_config.json  # Investigation rules & parameters
├── code.html                       # Frontend Dashboard Application
├── logo.png / logo.jpg             # Project Branding Assets
├── .gitignore                      # Git exclusion rules
└── README.md                       # Project Documentation
```

---

## 📊 Demo Scenario Overview

The included demo dataset (`CasualCourt_demo_dataset`) models an e-commerce platform experiencing a sudden jump in order cancellation rate from **~8% to ~31%** around Day 42:

1. **Root Cause**: Supplier B lead times inflated drastically around Day 38.
2. **Intermediate Impact**: Inventory stockouts occurred around Day 41.
3. **Outcome**: Unfulfilled orders led to massive customer cancellation spikes.
4. **Noise Signal**: Payment support tickets spiked after cancellations occurred, but payment gateway success remained stable (~99%).

### Expected Engine Ranking:
1. **Supplier / Delivery Disruption** (Primary Root Cause)
2. **Inventory Shortage** (Mediating Factor)
3. **Payment Failure** (Refuted / Filtered Noise Signal)
4. **Competitor Pricing** (Low Correlation Signal)

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have Python 3.9+ installed. Install the required backend dependencies:

```bash
pip install fastapi uvicorn pandas numpy pydantic python-multipart
```

### 2. Launch Backend API
Start the FastAPI server on port 8001:

```bash
cd backend
python main.py
```
Or with Uvicorn directly:
```bash
uvicorn backend.main:app --reload --port 8001
```

The API will be available at:
- **Base URL**: `http://127.0.0.1:8001`
- **Interactive API Docs (Swagger)**: `http://127.0.0.1:8001/docs`

### 3. Launch Frontend Application
Open `code.html` directly in any web browser, or serve it using Python's built-in HTTP server:

```bash
# From repository root
python -m http.server 8000
```
Then visit `http://localhost:8000/code.html` in your web browser.

---

## 🔌 API Endpoints Summary

| Endpoint | Method | Description |
|---|---|---|
| `/api/health` | `GET` | Health check & data directory readiness |
| `/api/sample-investigation` | `GET / POST` | Executes investigation on the included demo dataset |
| `/api/upload-and-validate` | `POST` | Uploads and validates custom dataset files |
| `/api/run-uploaded-investigation` | `POST` | Runs root-cause investigation on uploaded session data |

---

## 🤝 Team / Repository Info

- **Repository**: [Anvation-CSE-2026/ANV26-AI-34_CasualCourt](https://github.com/Anvation-CSE-2026/ANV26-AI-34_CasualCourt.git)
- **Project ID**: ANV26-AI-34
