"""
Custom tools for SWAST Handover Analytics
"""
from crewai.tools import BaseTool
from typing import Type, Optional, Dict, Any
from pydantic import BaseModel, Field
import pandas as pd


class HandoverDataInput(BaseModel):
    """Input schema for HandoverDataTool."""
    hospital_name: str = Field(..., description="Name of the hospital to analyze")
    data_file_path: str = Field(default="DataforMock.xlsx", description="Path to the data file")


class HandoverDataTool(BaseTool):
    name: str = "Handover Data Reader"
    description: str = (
        "Reads handover data from the SWAST data file for a specific hospital. "
        "Returns detailed information about waiting handovers, completed handovers, "
        "and current callsigns waiting for handover."
    )
    args_schema: Type[BaseModel] = HandoverDataInput

    def _run(self, hospital_name: str, data_file_path: str = "DataforMock.xlsx") -> str:
        """Execute the tool to read handover data."""
        try:
            # Read various sheets from the Excel file
            waiting_handovers = pd.read_excel(data_file_path, sheet_name='WaitingHandovers')
            current_waiting = pd.read_excel(data_file_path, sheet_name='CurrentWaitingCallsigns')
            completed_24h = pd.read_excel(data_file_path, sheet_name='HospitalHandoversCompleted')

            # Filter for specific hospital if not "All"
            if hospital_name != "All":
                waiting_filtered = waiting_handovers[
                    waiting_handovers['Hospital Attended '] == hospital_name
                ]
                current_filtered = current_waiting[
                    current_waiting['Hospital Attended'] == hospital_name
                ]
                completed_filtered = completed_24h[
                    completed_24h['Hospital Attended'] == hospital_name
                ]
            else:
                waiting_filtered = waiting_handovers
                current_filtered = current_waiting
                completed_filtered = completed_24h

            # Build summary report
            report = f"=== HANDOVER DATA FOR {hospital_name} ===\n\n"

            # Waiting handovers summary
            if not waiting_filtered.empty:
                report += "CURRENT WAITING HANDOVERS:\n"
                for _, row in waiting_filtered.iterrows():
                    report += f"  Hospital: {row['Hospital Attended ']}\n"
                    report += f"  Expected: {row['Expected']}, Inbound: {row['Inbound ']}, "
                    report += f"Arrived: {row['Arrived ']}, Waiting: {row['Waiting']}\n"
                    report += f"  0-15 mins: {row['0 - 15 Mins']}, 15-30 mins: {row['15 - 30 Mins ']}, "
                    report += f"30-60 mins: {row['30 - 60 Mins ']}, 60-90 mins: {row['60 - 90 Mins']}, "
                    report += f"90+ mins: {row['90 + Mins ']}\n\n"

            # Current waiting callsigns
            report += f"CURRENT WAITING CALLSIGNS: {len(current_filtered)}\n"
            if not current_filtered.empty and len(current_filtered) <= 10:
                for _, row in current_filtered.iterrows():
                    report += f"  {row['Callsign']} at {row['Hospital Attended']} - "
                    report += f"Arrived: {row['Arrived Destination Time']} ({row['Current Duration']} mins)\n"

            # 24-hour completed summary
            if not completed_filtered.empty:
                report += f"\n24-HOUR COMPLETED HANDOVERS:\n"
                for _, row in completed_filtered.iterrows():
                    report += f"  Hospital: {row['Hospital Attended']}\n"
                    report += f"  Total Handovers: {row['Handovers']}, Average: {row['Average']} mins, "
                    report += f"Hours Lost: {row['Hours Lost']}\n"
                    report += f"  % within 15 mins: {row['% 15 Mins']}%, % within 30 mins: {row['% 30 Mins']}%\n\n"

            return report

        except Exception as e:
            return f"Error reading handover data: {str(e)}"


class HandoverMetricsInput(BaseModel):
    """Input schema for HandoverMetricsTool."""
    hospital_name: str = Field(..., description="Name of the hospital to analyze")
    data_file_path: str = Field(default="DataforMock.xlsx", description="Path to the data file")


class HandoverMetricsTool(BaseTool):
    name: str = "Handover Metrics Calculator"
    description: str = (
        "Calculates key performance metrics for hospital handovers including total outstanding, "
        "current average duration, hours lost, and comparison to previous periods."
    )
    args_schema: Type[BaseModel] = HandoverMetricsInput

    def _run(self, hospital_name: str, data_file_path: str = "DataforMock.xlsx") -> str:
        """Execute the tool to calculate metrics."""
        try:
            # Read metrics sheet
            metrics_df = pd.read_excel(data_file_path, sheet_name='metrics')

            # Filter for hospital
            hospital_metrics = metrics_df[metrics_df['Hospital Attended'] == hospital_name]

            if hospital_metrics.empty:
                return f"No metrics found for hospital: {hospital_name}"

            # Extract key metrics
            total_outstanding = hospital_metrics[
                hospital_metrics['Metric'] == 'Total Outstanding'
            ].iloc[0]
            current_avg = hospital_metrics[
                hospital_metrics['Metric'] == 'Current Handover Average Mins'
            ].iloc[0]
            hours_lost = hospital_metrics[
                hospital_metrics['Metric'] == 'Hours Lost to Handovers Over 15 Mins'
            ].iloc[0]

            # Build metrics report
            report = f"=== KEY METRICS FOR {hospital_name} ===\n\n"
            report += f"TOTAL OUTSTANDING HANDOVERS:\n"
            report += f"  Current: {int(total_outstanding['Value'])}\n"
            report += f"  Previous (1 hour ago): {int(total_outstanding['Previous'])}\n"
            report += f"  Change: {int(total_outstanding['Value']) - int(total_outstanding['Previous'])}\n\n"

            report += f"CURRENT HANDOVER AVERAGE:\n"
            report += f"  Current: {int(current_avg['Value'])} minutes\n"
            report += f"  Previous (1 hour ago): {int(current_avg['Previous'])} minutes\n"
            report += f"  Change: {int(current_avg['Value']) - int(current_avg['Previous'])} minutes\n"

            # Performance assessment
            if int(current_avg['Value']) <= 15:
                report += f"  STATUS: MEETING TARGET (15 min target)\n\n"
            elif int(current_avg['Value']) <= 30:
                report += f"  STATUS: MODERATE DELAYS (above 15 min target)\n\n"
            else:
                report += f"  STATUS: CRITICAL DELAYS (significantly above target)\n\n"

            report += f"HOURS LOST TODAY (>15 mins):\n"
            report += f"  Current: {int(hours_lost['Value'])} hours\n"
            report += f"  Previous (yesterday): {int(hours_lost['Previous'])} hours\n"
            report += f"  Change: {int(hours_lost['Value']) - int(hours_lost['Previous'])} hours\n"

            return report

        except Exception as e:
            return f"Error calculating metrics: {str(e)}"


class HandoverForecastInput(BaseModel):
    """Input schema for HandoverForecastTool."""
    hospital_name: str = Field(..., description="Name of the hospital to analyze")
    data_file_path: str = Field(default="DataforMock.xlsx", description="Path to the data file")


class HandoverForecastTool(BaseTool):
    name: str = "Handover Forecast Reader"
    description: str = (
        "Reads forecast data for predicted handover arrivals. Returns predictions "
        "for the next several hours to support proactive resource planning."
    )
    args_schema: Type[BaseModel] = HandoverForecastInput

    def _run(self, hospital_name: str, data_file_path: str = "DataforMock.xlsx") -> str:
        """Execute the tool to read forecast data."""
        try:
            # Read forecast sheet
            forecast_df = pd.read_excel(data_file_path, sheet_name='Forecast')

            # Filter for hospital
            hospital_forecast = forecast_df[forecast_df['Hospital Attended'] == hospital_name]

            if hospital_forecast.empty:
                return f"No forecast data found for hospital: {hospital_name}"

            # Read historical data for context
            graph_df = pd.read_excel(data_file_path, sheet_name='Graph')
            hospital_historical = graph_df[graph_df['Hospital Attended'] == hospital_name]

            # Build forecast report
            report = f"=== HANDOVER FORECAST FOR {hospital_name} ===\n\n"
            report += "PREDICTED ARRIVALS (Next Hours):\n"

            for _, row in hospital_forecast.iterrows():
                report += f"  {row['Arrived Destination Resolved']}: {int(row['y'])} predicted arrivals\n"

            # Add context from recent actuals
            if not hospital_historical.empty:
                recent_avg = hospital_historical['Number of Handovers'].mean()
                forecast_avg = hospital_forecast['y'].mean()

                report += f"\nFORECAST ANALYSIS:\n"
                report += f"  Recent average: {recent_avg:.1f} handovers/hour\n"
                report += f"  Forecast average: {forecast_avg:.1f} handovers/hour\n"

                if forecast_avg > recent_avg * 1.2:
                    report += f"  ALERT: Forecast shows 20%+ increase in demand\n"
                elif forecast_avg > recent_avg * 1.1:
                    report += f"  WARNING: Forecast shows moderate increase in demand\n"
                else:
                    report += f"  INFO: Forecast shows stable demand\n"

            return report

        except Exception as e:
            return f"Error reading forecast data: {str(e)}"
