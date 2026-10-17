"""
Attack behavior analysis module
Process variant analysis, attack path extraction, case query
Core logic from dissertation: Section 4.2 & 4.3 Variant & Repetition Analysis
"""
import pandas as pd

class AttackPathAnalyzer:
    def __init__(self):
        pass

    def get_variant_stats(self, event_log_df: pd.DataFrame) -> dict:
        """
        Calculate process variant statistics
        Corresponds to dissertation: Process Variant Distribution
        """
        # Extract activity sequence per case
        case_sequences = event_log_df.groupby("case_id")["activity"].agg(tuple)
        variant_counts = case_sequences.value_counts()
        
        total_cases = len(case_sequences)
        top10_cases = variant_counts.head(10).sum()
        top20_cases = variant_counts.head(20).sum()
        
        return {
            "total_cases": total_cases,
            "number_of_variants": int(len(variant_counts)),
            "top10_coverage": round(top10_cases / total_cases * 100, 2),
            "top20_coverage": round(top20_cases / total_cases * 100, 2)
        }

    def get_attack_list(self, event_log_df: pd.DataFrame, limit: int = 20) -> list:
        """Get attack case list sorted by alert count (descending)"""
        case_stats = event_log_df.groupby("case_id").agg(
            alert_count=("event_id", "nunique"),
            activity_count=("activity", "nunique"),
            first_time=("timestamp", "min")
        ).reset_index()
        return case_stats.sort_values("alert_count", ascending=False).head(limit).to_dict(orient="records")

    def get_attack_path(self, event_log_df: pd.DataFrame, case_id: str) -> dict:
        """
        Get full attack activity sequence for a specific case ID
        Corresponds to dissertation: Selected Case Comparison
        """
        case_events = event_log_df[event_log_df["case_id"] == case_id].sort_values("timestamp")
        if case_events.empty:
            return {"error": "Case not found"}
        
        activity_sequence = case_events["activity"].tolist()
        
        return {
            "case_id": case_id,
            "alert_count": len(case_events),
            "activity_count": case_events["activity"].nunique(),
            "activity_sequence": activity_sequence,
            "time_span": str(case_events["timestamp"].max() - case_events["timestamp"].min())
        }

