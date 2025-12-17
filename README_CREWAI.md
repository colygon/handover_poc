# SWAST Handover Delays - CrewAI Edition

## Quick Start

This repository has been upgraded with AI-powered healthcare analytics agents using CrewAI.

### Installation

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

### Run AI Analytics

```bash
# Analyze all hospitals
python -m swast_crew.main

# Analyze specific hospital
python -m swast_crew.main "Royal Devon and Exeter Hospital"
```

### Run Original Dashboard

```bash
streamlit run handover.py
```

### What You Get

Three specialized AI agents analyze your handover data:

1. **Data Analyst**: Identifies delay patterns and calculates metrics
2. **Performance Monitor**: Alerts on critical delays in real-time
3. **Predictive Analyst**: Forecasts future demand and bottlenecks

### Documentation

See [CREWAI_UPGRADE.md](CREWAI_UPGRADE.md) for complete documentation.

### Agent 55

Upgraded by Agent 55 - December 2025
