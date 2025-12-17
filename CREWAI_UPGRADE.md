# SWAST Handover Delays - CrewAI Upgrade

## Overview

This document describes the CrewAI upgrade for the SWAST Hospital Handover Delays proof-of-concept application. The upgrade introduces AI-powered healthcare analytics agents that work together to analyze handover delays, monitor performance, and predict future demand.

**Upgrade Date:** December 17, 2025
**Agent ID:** Agent 55
**CrewAI Version:** >=0.86.0
**LangChain OpenAI Version:** >=0.3.0

---

## What's New

### Three Specialized Healthcare Analytics Agents

The CrewAI upgrade introduces three AI agents that collaborate to provide comprehensive handover delay analysis:

#### 1. Handover Data Analyst
- **Role:** Analyzes hospital handover data to identify delays, patterns, and bottlenecks
- **Expertise:** Emergency medical services operations, delay pattern analysis, NHS standards
- **Key Functions:**
  - Calculate key performance metrics (outstanding handovers, average duration, hours lost)
  - Identify delay patterns and peak times
  - Provide data-driven recommendations
  - Compare performance across hospitals and time periods

#### 2. Healthcare Performance Monitor
- **Role:** Real-time performance monitoring and alerting
- **Expertise:** Healthcare operations, KPI tracking, operational impact assessment
- **Key Functions:**
  - Monitor current handover status across all hospitals
  - Alert on critical delays (60+ minutes, 90+ minutes)
  - Track performance vs. 15-minute target
  - Assess operational impact on ambulance availability

#### 3. Predictive Healthcare Analytics Specialist
- **Role:** Forecast future demand and predict bottlenecks
- **Expertise:** Time series forecasting, demand prediction, resource optimization
- **Key Functions:**
  - Predict handover arrivals for next 4-6 hours
  - Identify upcoming high-risk periods
  - Provide proactive resource recommendations
  - Analyze seasonal and time-of-day patterns

---

## Architecture

### Directory Structure

```
swast-agent55/
├── src/
│   └── swast_crew/
│       ├── __init__.py                 # Package initialization
│       ├── crew.py                      # Main crew configuration
│       ├── main.py                      # Entry point
│       ├── config/
│       │   ├── agents.yaml              # Agent definitions
│       │   └── tasks.yaml               # Task definitions
│       └── tools/
│           ├── __init__.py
│           └── handover_tools.py        # Custom tools for data access
├── handover.py                          # Original Streamlit dashboard
├── DataforMock.xlsx                     # Data file
├── requirements.txt                     # Python dependencies
├── pyproject.toml                       # Poetry configuration
├── .env.example                         # Environment variables template
└── CREWAI_UPGRADE.md                    # This document
```

### Custom Tools

Three specialized tools enable agents to access handover data:

1. **HandoverDataTool**: Reads detailed handover data (waiting, completed, current callsigns)
2. **HandoverMetricsTool**: Calculates KPIs and compares to previous periods
3. **HandoverForecastTool**: Accesses forecast data for predictive analysis

---

## Installation

### Prerequisites

- Python 3.10 or higher
- OpenAI API key

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/colygon/handover_poc.git
   cd handover_poc
   git checkout crewai-upgrade
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or using Poetry:
   ```bash
   poetry install
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. **Verify installation:**
   ```bash
   python -m swast_crew.main --help
   ```

---

## Usage

### Running the Analytics Crew

#### Analyze All Hospitals
```bash
python -m swast_crew.main
```

#### Analyze Specific Hospital
```bash
python -m swast_crew.main "Royal Devon and Exeter Hospital"
```

#### Using Poetry Scripts
```bash
poetry run swast-crew
poetry run swast-crew "Royal Devon and Exeter Hospital"
```

### Running the Original Streamlit Dashboard

The original Streamlit dashboard remains fully functional:

```bash
streamlit run handover.py
```

### Advanced Usage

#### Train the Crew
```bash
python -m swast_crew.main train 5  # Train for 5 iterations
```

#### Replay a Task
```bash
python -m swast_crew.main replay <task_id>
```

#### Test the Crew
```bash
python -m swast_crew.main test 3 gpt-4o-mini
```

---

## Integration with Existing Dashboard

The CrewAI upgrade complements the existing Streamlit dashboard:

- **Dashboard**: Provides real-time visual monitoring and reporting
- **CrewAI Agents**: Provide AI-powered analysis, insights, and recommendations

Both systems read from the same data file (`DataforMock.xlsx`), ensuring consistency.

### Future Integration Ideas

1. **Embedded Agent Insights**: Display agent analysis directly in the Streamlit dashboard
2. **Alert System**: Use agents to generate alerts shown in the dashboard
3. **Automated Reports**: Generate periodic reports using agent analysis
4. **Interactive Q&A**: Allow users to ask questions about handover data via chat interface

---

## Configuration

### Agent Configuration (agents.yaml)

Define agent roles, goals, and backstories. Customize to match your organization's needs.

### Task Configuration (tasks.yaml)

Define analysis tasks with:
- Detailed descriptions
- Expected outputs
- Input parameters (hospital name, time periods, etc.)

### LLM Configuration (crew.py)

Default model: `gpt-4o-mini`

To use a different model, edit `src/swast_crew/crew.py`:
```python
self.llm = ChatOpenAI(
    model="gpt-4o",  # or "gpt-4-turbo", etc.
    temperature=0.7
)
```

---

## Dependencies

### Core Dependencies

- **crewai>=0.86.0**: AI agent framework
- **langchain-openai>=0.3.0**: OpenAI integration for LangChain
- **python-dotenv>=1.0.0**: Environment variable management

### Existing Dependencies

- **streamlit**: Web dashboard framework
- **pandas**: Data manipulation
- **plotly**: Interactive visualizations
- **openpyxl**: Excel file reading

---

## Data Sources

The system reads from `DataforMock.xlsx` with the following sheets:

- **Hospitals**: List of hospitals
- **metrics**: Key performance indicators
- **Graph**: Historical handover completion data
- **Forecast**: Predicted arrivals
- **WaitingHandovers**: Current waiting status by hospital
- **CurrentWaitingCallsigns**: Individual ambulance callsigns waiting
- **HospitalHandoversCompleted**: 24-hour completed handover summary
- **HospitalHandoverCompletedByHour**: Hourly breakdown
- **LongestCompletedHandover**: Top longest delays

### Adapting to Real Data

To use real data sources:

1. Update `handover_tools.py` to read from your SQL database, API, or other data source
2. Maintain the same data structure or update tool output formatting
3. Consider real-time data feeds for live monitoring

---

## Example Output

When you run the crew, you'll receive comprehensive analysis including:

### Handover Data Analyst Output
```
=== HANDOVER DELAY ANALYSIS ===

Summary Statistics:
- Total Outstanding: 12 handovers
- Average Duration: 28 minutes (target: 15 minutes)
- Hours Lost Today: 15.5 hours

Identified Patterns:
- Peak delays occur between 14:00-16:00
- Royal Devon & Exeter shows highest delays (avg 35 mins)
- 45% of handovers exceed 15-minute target

Recommendations:
1. Increase hospital capacity during 14:00-16:00 peak
2. Investigate process bottlenecks at Royal Devon & Exeter
3. Consider additional handover bays at high-delay sites
```

### Performance Monitor Output
```
=== REAL-TIME PERFORMANCE MONITORING ===

Critical Alerts:
- 3 handovers exceeding 90 minutes (CRITICAL)
- Average handover time 32 minutes (above 30-min threshold)

Current Status:
- 12 outstanding handovers across all hospitals
- Deteriorating: Average increased by 8 mins in last hour

Operational Impact:
- Estimated 6 ambulances delayed
- 15.5 hours of capacity lost today

Immediate Actions:
1. Prioritize 3 critical 90+ minute handovers
2. Request additional discharge capacity
3. Alert operational managers
```

### Predictive Analyst Output
```
=== HANDOVER DEMAND FORECAST ===

Next 6 Hours Forecast:
14:00-15:00: 18 arrivals (HIGH)
15:00-16:00: 22 arrivals (CRITICAL)
16:00-17:00: 19 arrivals (HIGH)
17:00-18:00: 14 arrivals (MODERATE)
18:00-19:00: 12 arrivals (MODERATE)
19:00-20:00: 10 arrivals (NORMAL)

High-Risk Period: 14:00-17:00
- 20%+ increase vs. recent average
- Recommend pre-positioning resources
- Alert hospital discharge coordinators

Resource Recommendations:
- Add 2 handover bays during 14:00-17:00
- Ensure discharge coordinators available
- Consider diversion protocols if capacity limited
```

---

## Troubleshooting

### Common Issues

#### OpenAI API Key Not Found
```
Error: OpenAI API key not configured
```
**Solution:** Ensure `.env` file exists with `OPENAI_API_KEY=your_key_here`

#### Import Errors
```
ModuleNotFoundError: No module named 'crewai'
```
**Solution:** Install dependencies with `pip install -r requirements.txt`

#### Data File Not Found
```
FileNotFoundError: DataforMock.xlsx
```
**Solution:** Ensure you run commands from the repository root directory

#### Rate Limiting
```
RateLimitError: You exceeded your current quota
```
**Solution:** Check OpenAI account credits or reduce request frequency

---

## Performance Considerations

### API Costs

- Each crew run makes multiple LLM API calls (one per agent/task)
- Using `gpt-4o-mini` is cost-effective for most analyses
- For higher quality analysis, consider `gpt-4o` or `gpt-4-turbo`

### Execution Time

- Full crew run: 30-90 seconds (depends on data size and LLM response time)
- Individual agent tasks: 10-30 seconds each
- Sequential processing ensures logical task flow

### Optimization Tips

1. **Use gpt-4o-mini** for routine analysis
2. **Cache results** for frequently accessed data
3. **Batch hospital analyses** rather than one-by-one
4. **Limit tool calls** by preprocessing data when possible

---

## Security Considerations

### API Key Protection

- Never commit `.env` file to version control
- Use environment variables in production
- Rotate API keys regularly

### Data Privacy

- Current mock data contains no real patient information
- When using real data, ensure GDPR/HIPAA compliance
- Consider data anonymization for agent training

### Access Control

- Restrict access to production systems
- Implement audit logging for agent actions
- Review agent outputs before acting on recommendations

---

## Roadmap

### Planned Enhancements

1. **Real-time Integration**: Connect to live data feeds
2. **Advanced Forecasting**: Machine learning models for prediction
3. **Multi-hospital Optimization**: Agent coordination across facilities
4. **Automated Alerting**: SMS/email alerts for critical situations
5. **Natural Language Interface**: Chat with agents about handover data
6. **Historical Analysis**: Trend analysis over weeks/months
7. **Resource Optimization**: AI-powered staffing recommendations

### Contributing

This is an open-source proof of concept. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## Credits

- **Original Project**: SWAST Data Science Team
- **CrewAI Upgrade**: Agent 55
- **Framework**: CrewAI by [Crew AI](https://www.crewai.com/)
- **LLM Provider**: OpenAI

---

## License

This project maintains the original license from the SWAST handover_poc repository.

---

## Support

For questions or issues:

1. Check the troubleshooting section above
2. Review CrewAI documentation: https://docs.crewai.com/
3. Open an issue on GitHub
4. Contact: data.science@swast.nhs.uk

---

## Appendix: Agent Collaboration Flow

```
User Request
    ↓
Handover Data Analyst
    ├── Reads data using HandoverDataTool
    ├── Calculates metrics using HandoverMetricsTool
    ├── Analyzes patterns and trends
    └── Outputs: Comprehensive analysis report
    ↓
Performance Monitor
    ├── Receives context from Data Analyst
    ├── Monitors real-time metrics
    ├── Identifies critical situations
    └── Outputs: Performance monitoring report with alerts
    ↓
Predictive Analyst
    ├── Receives context from previous agents
    ├── Reads forecast data
    ├── Predicts future demand
    └── Outputs: Forecast report with recommendations
    ↓
Final Combined Report
```

The sequential process ensures each agent builds on the previous agent's insights, creating a comprehensive, actionable analysis.

---

**End of Documentation**
