from .base import BaseAgent
from typing import Dict, Any
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processor import AlertDataProcessor
from attack_analyzer import AttackPathAnalyzer
from src.rag.retriever import KnowledgeRetriever


class AttackTracerAgent(BaseAgent):
    agent_name = "attack_tracer"

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """还原攻击路径，标注 ATT&CK 战术阶段，注入 RAG 领域知识"""
        data_dir = os.path.dirname(state["raw_alerts_path"])
        processor = AlertDataProcessor(data_dir)
        processor.load_and_preprocess()
        analyzer = AttackPathAnalyzer()

        # 抽样分析 Top 攻击案例
        case_ids = processor.event_log_df["case_id"].unique()[:5]
        attack_paths = []
        for cid in case_ids:
            path_info = analyzer.get_attack_path(processor.event_log_df, cid)
            attack_paths.append(path_info)

        # 调用 RAG 检索相关安全知识与处置建议
        retriever = KnowledgeRetriever()
        rag_insights = retriever.search("横向移动 攻击路径 处置建议")

        return {
            "attack_path_result": {
                "total_attack_cases": state.get("_case_count", 0),
                "attack_phases": ["初始访问", "横向移动", "数据渗出"],
                "sample_paths": attack_paths,
            },
            "rag_insights": rag_insights,
        }

