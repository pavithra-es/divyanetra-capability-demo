# ⚡ DivyaNetra – Agentic AI Capability Demo

## AMI Network Health | Smart Meter Rollout Risk | Executive Intelligence

DivyaNetra is a **local Agentic AI Capability Demo** that demonstrates how multiple intelligent agents can monitor, analyze, predict, recommend, and execute controlled operational workflows for a Smart Meter / AMI ecosystem.

The demo follows the DivyaNetra operating model:

```text
SENSE
  ↓
GROUND
  ↓
REASON & DECIDE
  ↓
ACT
```

---

# 🎯 Use Cases

This implementation covers three primary capability demonstrations.

## 🥇 1. AMI Network Health Agent

Continuously monitors smart meter telemetry and identifies communication or network issues.

### Workflow

```text
AMI / Meter Telemetry
        ↓
Monitoring Agent
        ↓
Diagnosis Agent
        ↓
Prediction Agent
        ↓
Recommendation Agent
        ↓
Human Approval
        ↓
Work Order / Crew Dispatch / Alert
```

### Demonstrated Capabilities

- Monitor smart meter signals
- Detect communication degradation
- Identify at-risk meters
- Identify affected region
- Identify problematic concentrator
- Diagnose probable root cause
- Calculate network risk score
- Predict outage probability
- Estimate operational impact
- Recommend remediation action
- Require human approval
- Create a simulated work order
- Dispatch a simulated crew
- Generate a simulated Teams alert

---

## 🥈 2. Smart Meter Rollout Risk Agent

Analyzes smart meter rollout projects and predicts operational and delivery risks.

### Workflow

```text
Rollout Progress
       +
Vendor Performance
       +
Workforce Availability
       +
Material Availability
          ↓
Rollout Risk Agent
          ↓
Risk Prediction
          ↓
Recommendation
```

### Demonstrated Capabilities

- Analyze rollout progress
- Compare expected vs actual progress
- Detect schedule variance
- Analyze vendor SLA
- Detect poor vendor performance
- Analyze installation rejection rates
- Detect workforce shortages
- Analyze material availability
- Calculate rollout risk score
- Predict potential project delay
- Generate recovery recommendations

---

## 🥉 3. Executive Query Agent

Allows executives and business users to ask questions across operational domains.

### Example Questions

```text
What requires immediate attention today?

Which region has the highest network risk?

Which rollout project is delayed?

Which vendor is performing poorly?
```

### Workflow

```text
Executive Question
        ↓
DivyaNetra Supervisor Agent
        ↓
Intent / Domain Routing
        ↓
Network Health Agent
        OR
Rollout Risk Agent
        OR
Cross-Domain Analysis
        ↓
Executive Insight
```

---

# 🏗️ Architecture

## High-Level Architecture

```text
┌─────────────────────────────────────────────────────┐
│                       01 SENSE                      │
│                                                     │
│  AMI / MDM │ Network Events │ Vendor │ Workforce   │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                      02 GROUND                      │
│                                                     │
│              BRONZE → SILVER → GOLD                │
│                                                     │
│              DuckDB Local Lakehouse                 │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                 03 REASON & DECIDE                  │
│                                                     │
│           DivyaNetra Supervisor Agent               │
│                        │                            │
│       ┌────────────────┼───────────────┐            │
│       ▼                ▼               ▼            │
│  Network Health   Rollout Risk    Executive Query   │
│       Agents          Agents          Agent          │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│                       04 ACT                        │
│                                                     │
│              Human Approval / HITL                  │
│                        │                            │
│       ┌────────────────┼──────────────┐             │
│       ▼                ▼              ▼             │
│   Work Order       Crew Dispatch   Teams Alert      │
└─────────────────────────────────────────────────────┘
```

---

# 📁 Project Structure

```text
divyanetra-demo/
│
├── app.py
├── database.py
├── setup_data.py
├── agents.py
├── actions.py
├── requirements.txt
├── README.md
│
└── divyanetra.duckdb
```

> **Note:** Do not manually create `divyanetra.duckdb`. DuckDB creates it automatically when the setup script runs.

---

# 🛠️ Technology Stack

| Component | Technology |
|---|---|
| User Interface | Streamlit |
| Database | DuckDB |
| Data Processing | Pandas |
| Data Generation | NumPy |
| Visualization | Plotly |
| Programming Language | Python |
| Agent Pattern | Python Multi-Agent Architecture |
| Governance | Audit Logs |
| Human Approval | Streamlit HITL |
| Ticketing | Mock ServiceNow |
| Notifications | Mock Microsoft Teams |

---

# 🆓 Free Resources

This demo runs locally using free and open-source technologies.

```text
Python      → Free
DuckDB      → Free
Streamlit   → Free
Pandas      → Free
NumPy       → Free
Plotly      → Free
```

No cloud account is required.

---

# ⚙️ Prerequisites

Install **Python 3.10 or above**.

Check your Python version:

```bash
python --version
```

---

# 🚀 Installation

## Step 1 – Open the Project Folder

```cmd
cd E:\divyanetra-demo
```

## Step 2 – Create a Virtual Environment (Recommended)

```cmd
python -m venv venv
```

Activate it:

### Windows

```cmd
venv\Scripts\activate
```

## Step 3 – Install Dependencies

```cmd
pip install -r requirements.txt
```

Your `requirements.txt` should contain:

```text
streamlit
duckdb
pandas
numpy
plotly
pyarrow
```

---

# 🗄️ Create Demo Data

Run:

```cmd
python setup_data.py
```

This script will:

1. Create the DuckDB database
2. Generate simulated AMI meter telemetry
3. Generate rollout project data
4. Generate vendor performance data
5. Create Bronze tables
6. Create Silver tables
7. Create Gold KPI tables

Expected output:

```text
==============================================
DivyaNetra Demo Data Created Successfully
==============================================

Bronze Layer:
 - bronze_meter_telemetry
 - bronze_rollout_progress
 - bronze_vendor_performance

Silver Layer:
 - silver_meter_telemetry
 - silver_rollout_progress
 - silver_vendor_performance

Gold Layer:
 - gold_network_kpi
 - gold_rollout_kpi
```

---

# 🥉 Bronze Layer – Raw Data

The Bronze layer represents raw source data.

### Tables

```text
bronze_meter_telemetry
bronze_rollout_progress
bronze_vendor_performance
```

### Simulated Sources

```text
AMI / MDM
Network Telemetry
Smart Meter Events
Rollout Progress
Vendor Performance
```

---

# 🥈 Silver Layer – Cleaned and Validated Data

The Silver layer performs cleaning, validation, and business transformations.

### Tables

```text
silver_meter_telemetry
silver_rollout_progress
silver_vendor_performance
```

### Network Health Logic

A meter is marked as `AT_RISK` when:

```text
Signal Strength < 50
OR
Packet Loss > 10
OR
Latency > 200
```

Otherwise:

```text
HEALTHY
```

---

# 🥇 Gold Layer – Business Intelligence

The Gold layer contains business-ready KPIs.

### Tables

```text
gold_network_kpi
gold_rollout_kpi
```

## Network KPI

Provides:

- Total meters
- Healthy meters
- At-risk meters
- Average signal strength
- Average packet loss
- Average latency

## Rollout KPI

Combines:

```text
Rollout Progress
       +
Vendor Performance
       +
Workforce Data
       +
Material Availability
```

---

# 🤖 Multi-Agent Architecture

## DivyaNetra Supervisor Agent

The Supervisor Agent acts as the orchestrator.

```text
User Request
      ↓
Supervisor Agent
      ↓
Intent Detection
      ↓
Domain Agent Routing
```

### Supported Routes

```text
NETWORK_HEALTH
ROLLOUT_RISK
EXECUTIVE_QUERY
```

---

# 📡 AMI Network Health Swarm

```text
Monitoring Agent
        ↓
Diagnosis Agent
        ↓
Prediction Agent
        ↓
Recommendation Agent
```

## 1. Monitoring Agent

Responsibilities:

- Scan smart meter telemetry
- Count total meters
- Identify at-risk meters
- Calculate at-risk percentage

## 2. Diagnosis Agent

Responsibilities:

- Group problems by region
- Identify affected concentrator
- Determine severity
- Identify probable root cause

Example:

```text
Affected Region: Mumbai West
Concentrator: DC-300
Severity: CRITICAL
```

## 3. Prediction Agent

Calculates:

```text
Signal Risk
+
Packet Loss Risk
+
Latency Risk
=
Network Risk Score
```

Outputs:

- Risk score
- Outage probability
- Confidence score
- Predicted impact

## 4. Recommendation Agent

Example:

```text
Priority: P1 - CRITICAL

Action:
Immediately inspect the concentrator

Crew:
Network Response Crew Alpha
```

---

# 📊 Smart Meter Rollout Risk Swarm

```text
Rollout Progress Agent
          ↓
Vendor Performance Agent
          ↓
Workforce Planning Agent
          ↓
Rollout Risk Agent
          ↓
Rollout Recommendation Agent
```

## Risk Factors

```text
Schedule Delay
+
Vendor SLA
+
Crew Shortage
+
Material Availability
+
Installation Rejection Rate
```

## Risk Levels

```text
Risk Score >= 70 → CRITICAL
Risk Score >= 40 → HIGH
Risk Score >= 20 → MEDIUM
Otherwise        → LOW
```

---

# 💬 Executive Query Agent

Supports questions such as:

```text
What requires immediate attention today?
Which region has the highest network risk?
Which rollout project is delayed?
Which vendor is performing poorly?
```

The Executive Query Agent can analyze:

```text
Network Risk
      +
Rollout Risk
      +
Vendor Risk
      ↓
Executive Insight
```

---

# 👤 Human-in-the-Loop (HITL)

High-impact actions require human approval.

```text
AI Detects Problem
        ↓
AI Diagnoses Problem
        ↓
AI Predicts Risk
        ↓
AI Recommends Action
        ↓
👤 Human Approval
        ↓
Action Agent Executes Workflow
```

---

# 🚀 ACT Layer

After approval:

```text
Human Approval
       ↓
Action Agent
       ↓
┌───────────────┬────────────────┬────────────────┐
│               │                │                │
▼               ▼                ▼
Incident     Work Order      Teams Alert
```

The current implementation simulates:

- ServiceNow incident/work order
- Workforce/crew dispatch
- Microsoft Teams notification

---

# 📜 Governance and Audit

Every agent action is recorded.

Audit information includes:

```text
Timestamp
Agent Name
Action
Details
Status
```

Example audit trail:

```text
Monitoring Agent
→ Network Health Scan

Diagnosis Agent
→ Root Cause Analysis

Prediction Agent
→ Network Risk Prediction

Recommendation Agent
→ Remediation Plan

Action Agent
→ Operational Action Executed
```

---

# 🖥️ Run the Application

Start the Streamlit application:

```cmd
streamlit run app.py
```

The application normally opens at:

```text
http://localhost:8501
```

---

# 🎬 Recommended Demo Flow

## 1. Command Center

Open:

```text
🏠 Command Center
```

Show:

- Total Smart Meters
- At-Risk Meters
- Delayed Projects
- Vendor Risk

Suggested demo statement:

> DivyaNetra provides a unified command center that identifies operational risks across AMI network health and smart meter rollout operations.

---

## 2. AMI Network Health

Open:

```text
📡 AMI Network Health
```

Click:

```text
🚀 Run Network Health Swarm
```

Explain the flow:

1. Monitoring Agent scans telemetry.
2. Diagnosis Agent identifies the affected region and likely concentrator.
3. Prediction Agent calculates outage risk and impact.
4. Recommendation Agent proposes remediation.
5. Human approves the operational action.

Then click:

```text
✅ Approve Operational Action
```

The demo creates:

```text
Incident
   ↓
Work Order
   ↓
Crew Assignment
   ↓
Teams Alert
```

---

## 3. Smart Meter Rollout Risk

Open:

```text
📊 Smart Meter Rollout Risk
```

Click:

```text
🚀 Run Rollout Risk Swarm
```

Explain:

> The rollout swarm combines schedule progress, vendor performance, workforce availability, and material availability to predict project delivery risk.

---

## 4. Executive Query

Open:

```text
💬 Executive Query
```

Ask:

```text
What requires immediate attention today?
```

Explain:

> The Supervisor Agent routes the request to the relevant domain intelligence and produces an executive-level insight.

---

## 5. Audit & Governance

Open:

```text
📜 Audit & Governance
```

Show the recorded agent decisions and actions.

---

# 🔄 Reset the Demo

Stop Streamlit:

```text
CTRL + C
```

Delete the database:

```cmd
del divyanetra.duckdb
```

Recreate the demo data:

```cmd
python setup_data.py
```

Start the application again:

```cmd
streamlit run app.py
```

---

# ❗ Troubleshooting

## Invalid DuckDB Database

Error:

```text
The file divyanetra.duckdb exists, but it is not a valid DuckDB database file
```

Solution:

```cmd
del divyanetra.duckdb
python setup_data.py
```

> Do not manually create an empty `divyanetra.duckdb` file.

---

## Table Does Not Exist

Example:

```text
Table gold_network_kpi does not exist
```

Solution:

```cmd
python setup_data.py
```

Run the setup before starting Streamlit.

---

## Module Not Found

Example:

```text
ModuleNotFoundError: No module named 'duckdb'
```

Solution:

```cmd
pip install -r requirements.txt
```

---

# 🔄 Mapping to Target DivyaNetra / Databricks Architecture

| Target Architecture | Local Capability Demo |
|---|---|
| Databricks Apps | Streamlit |
| Delta Lake | DuckDB |
| Bronze / Silver / Gold | Bronze / Silver / Gold tables |
| Unity Catalog | Simplified local governance and audit |
| Mosaic AI Agent Framework | Python multi-agent architecture |
| Agent Bricks | Supervisor + domain agents |
| Vector Search | Future enhancement |
| Genie | Executive Query Agent |
| Lakeflow Jobs | Manual/on-demand workflow execution |
| ServiceNow | Mock work order |
| WFM | Mock crew dispatch |
| Teams / Slack | Mock notification |
| MLflow | Future enhancement |
| Model Evaluation | Future enhancement |

---

# 🚀 Future Enhancements

## Data Platform

- Delta Lake
- Databricks Unity Catalog
- Databricks Lakeflow
- Databricks Jobs

## Agentic AI

- LLM-powered Supervisor
- Databricks Agent Bricks
- Mosaic AI Agent Framework
- Function Calling
- Agent-to-Agent communication

## AI Intelligence

- Anomaly detection
- Time-series forecasting
- Predictive ML models
- RAG
- Vector Search
- SOP and document grounding

## Integrations

- Actual ServiceNow REST API
- Microsoft Teams Webhook
- Microsoft Graph API
- SAP integration
- WFM API
- CRM API

## Governance

- Unity Catalog permissions
- AI Gateway guardrails
- MLflow tracing
- Agent evaluation
- Model evaluation
- PII masking

---

# 🏁 Summary

DivyaNetra demonstrates a reusable Agentic AI operating model:

```text
                    DIVYANETRA
                         │
                         ▼
                      01 SENSE
              Collect operational signals
                         │
                         ▼
                     02 GROUND
               Bronze → Silver → Gold
                         │
                         ▼
                 03 REASON & DECIDE
                Supervisor + AI Agents
                         │
                         ▼
                      04 ACT
            Human Approval + Workflows
                         │
                         ▼
               GOVERNED OPERATIONAL ACTION
```

## ⭐ Key Demo Value

```text
ONE PLATFORM
        +
MULTIPLE OPERATIONAL DOMAINS
        +
MULTI-AGENT INTELLIGENCE
        +
PREDICTIVE DECISION MAKING
        +
HUMAN CONTROL
        +
AUDITABLE ACTIONS
```

> **DivyaNetra transforms operational data into governed agentic intelligence — detecting risks, diagnosing root causes, predicting impact, recommending actions, and executing controlled workflows through human-approved automation.**
