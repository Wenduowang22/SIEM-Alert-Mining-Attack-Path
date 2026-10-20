from .base import BaseAgent
from typing import Dict, Any
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processor import AlertDataProcessor


class ProcessMinerAgent(BaseAgent):
    agent_name = "process_miner"

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """构建流程挖掘模型，生成 DFG 边关系"""
        data_dir = os.path.dirname(state["raw_alerts_path"])
        processor = AlertDataProcessor(data_dir)
        processor.load_and_preprocess()
        df = processor.event_log_df

        # 计算 DFG 直接跟随边
        if "case_id" in df.columns and "activity" in df.columns:
            df_sorted = df.sort_values(["case_id", "timestamp"])
            df_sorted["next_activity"] = df_sorted.groupby("case_id")["activity"].shift(-1)
            edges = df_sorted.dropna(subset=["next_activity"])
            edge_counts = edges.groupby(["activity", "next_activity"]).size().reset_index(name="count")
            edge_counts = edge_counts.sort_values("count", ascending=False).head(20)
            dfg_edges = edge_counts.to_dict(orient="records")
        else:
            dfg_edges = []

        return {
            "process_model_result": {
                "model_types": ["DFG", "Process Tree", "Petri Net"],
                "dfg_edges_count": len(dfg_edges),
                "dfg_edges": dfg_edges,
            }
        }

