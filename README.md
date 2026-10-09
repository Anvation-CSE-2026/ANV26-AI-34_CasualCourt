# ⚖️ CasualCourt — Autonomous Business Process Investigator

<p align="center">
  <img src="logo.png" alt="CasualCourt Logo" width="140" />
</p>

<h3 align="center">Turning Operational Data into Actionable Root-Cause Insights</h3>

<p align="center">
  An intelligent investigation platform that identifies operational anomalies, evaluates competing hypotheses, and uncovers the underlying causes using evidence-driven analysis.
</p>

<p align="center">
  <a href="https://casualcourt-app-kssem.web.app/"><strong>🌐 Live Demo</strong></a> •
  <a href="https://github.com/Anvation-CSE-2026/ANV26-AI-34_CasualCourt"><strong>💻 GitHub Repository</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-UI-38B2AC?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
</p>

---

## 🚀 Overview

**CasualCourt** is an autonomous business process investigation platform built to help businesses understand not just *what went wrong*, but *why it happened*.

It analyzes operational telemetry across orders, suppliers, inventory, payments, customer support, and competitor pricing to identify anomalies and investigate their potential root causes.

Instead of relying on isolated metrics or surface-level correlations, CasualCourt evaluates competing hypotheses, analyzes supporting and contradicting evidence, and ranks the most plausible explanations.

### 🎯 The Problem We Solve

A sudden increase in order cancellations doesn't automatically mean the payment system is broken. The real cause might be delayed suppliers, inventory shortages, or another upstream operational issue.

CasualCourt connects these signals to help distinguish **root causes from misleading correlations**.

---

## 🌟 Key Features

| Feature | Description |
|---|---|
| 🧠 **Automated Root-Cause Analysis** | Generates and evaluates competing hypotheses to identify likely operational bottlenecks. |
| 🔍 **Causal & Evidence Analysis** | Examines event timing, lead-lag relationships, supplier delays, stockouts, and operational anomalies. |
| 🛡️ **Adversarial Defense Engine** | Challenges misleading signals and evaluates evidence against alternative explanations. |
| 📂 **Custom Dataset Upload** | Supports CSV and JSON operational data with schema validation. |
| 📊 **Interactive Investigation Dashboard** | Presents investigation progress, hypothesis rankings, evidence breakdowns, and defense analysis. |
| 🏭 **Multi-Source Operational Analysis** | Connects order, inventory, supplier, payment, support, and competitor data into one investigation workflow. |

---

## 🏆 What Makes CasualCourt Different?

Traditional dashboards show metrics. CasualCourt investigates relationships between them.

- **Beyond anomaly detection:** Investigates possible explanations for abnormal business behavior.
- **Evidence-driven ranking:** Compares competing hypotheses rather than relying on a single signal.
- **False-positive resistance:** Uses counter-evidence and alternative explanations to challenge misleading conclusions.
- **Cross-system investigation:** Connects events across multiple operational data sources.
- **Flexible analysis:** Supports investigation of custom datasets in addition to the supplied demo scenario.

> **Our goal:** Help businesses move from *“What happened?”* to *“What most likely caused it, and what evidence supports that conclusion?”*

---

## 🏗️ System Architecture

CasualCourt follows a modular architecture that separates data ingestion, investigation orchestration, hypothesis evaluation, evidence scoring, and defense analysis.

```text
┌──────────────────────────────────────────────┐
│             Frontend Dashboard               │
│      Interactive Investigation Interface     │
└──────────────────────┬───────────────────────┘
                       │ HTTP / REST API
┌──────────────────────▼───────────────────────┐
│                FastAPI Backend                │
├──────────────────────────────────────────────┤
│              Data Loader                     │
│      Upload • Parsing • Validation            │
├──────────────────────────────────────────────┤
│             Orchestrator                     │
│        Investigation Workflow                │
├───────────────────┬──────────────────────────┤
│ Hypothesis Engine │ Evidence Engine           │
│ Candidate Causes │ Evidence & Scoring         │
├───────────────────┴──────────────────────────┤
│               Defense Engine                  │
│       Counter-Evidence & Noise Filtering      │
├──────────────────────────────────────────────┤
│       Ranked Hypotheses & Investigation       │
│                  Results                     │
└──────────────────────────────────────────────┘
```

### 📁 Repository Structure

```text
ANV26-AI-34_CasualCourt/
│
├── backend/
│   ├── main.py
│   ├── orchestrator.py
│   ├── hypothesis_engine.py
│   ├── evidence_engine.py
│   ├── defense_engine.py
│   ├── data_loader.py
│   ├── models.py
│   ├── investigation_engine.py
│   └── test_engine.py
│
├── CasualCourt_demo_dataset/
│   ├── orders.csv
│   ├── supplier_events.csv
│   ├── inventory.csv
│   ├── payments.csv
│   ├── tickets.csv
│   ├── competitor_prices.csv
│   └── investigation_config.json
│
├── code.html
├── logo.png
├── logo.jpg
├── .gitignore
└── README.md
```

---

## 📊 Demo Investigation: Order Cancellation Spike

The included demo dataset represents an e-commerce business experiencing a sharp increase in order cancellations.

### Scenario

<pre>
Normal Cancellation Rate     ~8%
           │
           ▼
Supplier Lead Times Increase
           │
           ▼
Inventory Stockouts Occur
           │
           ▼
Order Fulfilment Is Disrupted
           │
           ▼
Cancellation Rate Rises to ~31%
</pre>

### 🔬 Investigation Findings

| Hypothesis | Expected Assessment |
|---|---|
| 🥇 Supplier / Delivery Disruption | Primary suspected root cause |
| 🥈 Inventory Shortage | Intermediate contributing factor |
| 🥉 Payment Failure | Contradicted by stable payment success |
| 4️⃣ Competitor Pricing | Lower-priority explanation |

The scenario also contains a misleading signal: customer support tickets increase after cancellations, even though payment gateway success remains approximately 99%.

This allows the investigation engine to demonstrate why temporal order, supporting evidence, and contradictory evidence matter.

*Note: These are the expected findings encoded in the demo scenario, not a claim of independently verified live investigation results.*

---

## ⚡ Getting Started

### Prerequisites

- Python 3.9 or later
- pip
- Git
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/Anvation-CSE-2026/ANV26-AI-34_CasualCourt.git

cd ANV26-AI-34_CasualCourt
```

### 2. Install Backend Dependencies

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
.venv\Scripts\activate.bat
```

Install the dependencies:

```bash
python -m pip install fastapi uvicorn pandas numpy pydantic python-multipart
```

### 3. Start the Backend

From the repository root, run:

```bash
uvicorn backend.main:app --reload --port 8001
```

If your environment requires running the application directly, use:

```bash
cd backend
python main.py
```

Backend URLs:

- **API Base URL:** http://127.0.0.1:8001
- **Interactive API Documentation:** http://127.0.0.1:8001/docs

### 4. Launch the Frontend

Open `code.html` directly in your browser, or serve the repository root using Python:

```bash
python -m http.server 8000
```

Then open:

http://localhost:8000/code.html

**Important:** The frontend must be configured to communicate with your locally running backend. Opening the HTML file alone does not start the API server.

---

## 🔌 API Reference

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Checks backend health and data-directory readiness. |
| `/api/sample-investigation` | GET / POST | Runs an investigation using the demo dataset. |
| `/api/upload-and-validate` | POST | Uploads and validates custom dataset files. |
| `/api/run-uploaded-investigation` | POST | Investigates uploaded operational data. |

Use the Swagger interface at `/docs` to inspect the actual request schemas, parameters, and responses supported by your running backend.

---

## 🧪 Testing

Run the available backend test module from the repository root:

```bash
python -m unittest backend.test_engine
```

Review the test output to confirm which checks pass in your environment.

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| Python | Investigation logic and data processing |
| FastAPI | REST API and backend service |
| Pandas & NumPy | Data manipulation and numerical analysis |
| Pydantic | Request validation and structured data models |
| Tailwind CSS | Frontend styling |
| HTML & JavaScript | Interactive dashboard |
| Firebase Hosting | Live frontend hosting |

---

## 🌐 Live Application

Experience CasualCourt through the deployed web application.

**👉 [Launch CasualCourt Live](https://casualcourt-app-kssem.web.app/)**

For source code, backend implementation, and project assets, visit the [GitHub repository](https://github.com/Anvation-CSE-2026/ANV26-AI-34_CasualCourt).

*The live frontend and locally documented API are separate deployment components. Backend-dependent features require a reachable, correctly configured API.*

---

## 👥 Project Information

- **Project Name:** CasualCourt
- **Project ID:** ANV26-AI-34
- **Repository:** [Anvation-CSE-2026/ANV26-AI-34_CasualCourt](https://github.com/Anvation-CSE-2026/ANV26-AI-34_CasualCourt)
- **Live Demo:** [casualcourt-app-kssem.web.app](https://casualcourt-app-kssem.web.app/)

---

## 🔮 Our Vision

We envision a future where businesses don't need to manually investigate disconnected dashboards to understand operational failures.

CasualCourt aims to make business investigations more structured, evidence-driven, and explainable—helping teams discover likely root causes faster and make better-informed operational decisions.

---

<p align="center">
  <strong>⚖️ CasualCourt — Investigate the Evidence. Discover the Cause.</strong>
</p>
