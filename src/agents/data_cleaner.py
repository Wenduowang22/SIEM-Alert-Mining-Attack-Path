from .base import BaseAgent
from typing import Dict, Any
import sys
import os

# 导入原有核心模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processor import AlertDataProcessor


class DataCleanerAgent(BaseAgent):
    agent_name = "data_cleaner"

    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """调用原有数据处理模块，完成告警清洗、去重、归一化"""
        # 原类接收数据目录，内部自动拼接文件名
        data_dir = os.path.dirname(state["raw_alerts_path"])
        processor = AlertDataProcessor(data_dir)
        # 调用原类的真实加载方法
        processor.load_and_preprocess()
        cleaned_count = len(processor.event_log_df)
        return {
            "cleaned_alerts_count": cleaned_count,
            "_processor_ref": processor,  # 内存传递给下游节点复用
        }

