"""
Data processing module for GUIDE security alert logs
Handles data loading, deduplication, case filtering and event log construction
Core logic from dissertation: Section 3.1 Dataset and Preprocessing
"""
import duckdb
import pandas as pd
from pathlib import Path

class AlertDataProcessor:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.con = duckdb.connect()
        self.event_log_df = None
        self.case_summary_df = None

    def load_and_preprocess(self, dataset_path: str = None):
        """
        Load GUIDE dataset, deduplicate records, filter TruePositive incidents
        and build process mining event log.
        Fully consistent with dissertation filtering rules.
        """
        if dataset_path is None:
            dataset_path = str(self.data_dir / "sample_alerts.csv")
        
        sql_safe_path = str(dataset_path).replace("'", "''")
        
        # Step 1: Deduplicate alert records (Id + AlertId unique key)
        self.con.execute(f"""
            CREATE OR REPLACE TEMP TABLE alert_events AS
            SELECT
                CAST(Id AS VARCHAR) AS case_id,
                CAST(AlertId AS VARCHAR) AS event_id,
                TRY_CAST(Timestamp AS TIMESTAMP) AS timestamp,
                COALESCE(
                    NULLIF(CAST(Category AS VARCHAR), ''),
                    NULLIF(CAST(AlertTitle AS VARCHAR), ''),
                    'Unknown Activity'
                ) AS activity,
                CAST(AlertTitle AS VARCHAR) AS alert_title,
                CAST(MitreTechniques AS VARCHAR) AS mitre_techniques,
                CAST(DetectorId AS VARCHAR) AS detector_id,
                CAST(IncidentGrade AS VARCHAR) AS incident_grade,
                CAST(OrgId AS VARCHAR) AS org_id,
                CAST(IncidentId AS VARCHAR) AS incident_id
            FROM read_csv_auto('{sql_safe_path}', header=true)
            WHERE CAST(IncidentGrade AS VARCHAR) = 'TruePositive'
              AND Id IS NOT NULL
              AND AlertId IS NOT NULL
              AND Timestamp IS NOT NULL
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY Id, AlertId
                ORDER BY Timestamp, CAST(Category AS VARCHAR), CAST(AlertTitle AS VARCHAR)
            ) = 1
        """)

        # Step 2: Filter cases: 1-100 alerts, at least 1 distinct activity
        self.con.execute("""
            CREATE OR REPLACE TEMP TABLE multi_activity_cases AS
            SELECT case_id
            FROM alert_events
            GROUP BY case_id
            HAVING COUNT(*) BETWEEN 1 AND 100
               AND COUNT(DISTINCT activity) >= 1
        """)

        # Step 3: Build final ordered event log
        self.event_log_df = self.con.execute("""
            SELECT e.*
            FROM alert_events e
            INNER JOIN multi_activity_cases m ON e.case_id = m.case_id
            ORDER BY e.case_id, e.timestamp, e.event_id
        """).df()
        
        # Build final case summary
        self.case_summary_df = self.con.execute("""
            SELECT 
                e.case_id,
                COUNT(*) AS number_of_events,
                COUNT(DISTINCT activity) AS number_of_activities
            FROM alert_events e
            INNER JOIN multi_activity_cases m ON e.case_id = m.case_id
            GROUP BY e.case_id
        """).df()
        
        return self.event_log_df

    def get_basic_metrics(self) -> dict:
        """Return basic dataset metrics consistent with dissertation results"""
        if self.event_log_df is None:
            return {}
        return {
            "number_of_cases": int(self.event_log_df["case_id"].nunique()),
            "number_of_events": int(len(self.event_log_df)),
            "number_of_activities": int(self.event_log_df["activity"].nunique()),
            "avg_events_per_case": round(self.event_log_df.groupby("case_id")["event_id"].count().mean(), 2)
        }

