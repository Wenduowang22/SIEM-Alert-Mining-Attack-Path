from .base import BaseAgent
from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processor import AlertDataProcessor


class FeatureEngineerAgent(BaseAgent):
    agent_name = "feature_engineer"

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """案例聚合、特征提取、统计指标计算"""
        data_dir = os.path.dirname(state["raw_alerts_path"])
        processor = AlertDataProcessor(data_dir)
        processor.load_and_preprocess()
        metrics = processor.get_basic_metrics()
        return {
            "_case_count": metrics.get("total_cases", 0),
            "feature_matrix_path": "memory://case_features",
        }

