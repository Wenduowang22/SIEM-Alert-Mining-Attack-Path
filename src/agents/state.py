"""
工作流共享状态定义
贯穿所有 Agent 的统一数据结构，LangGraph 通过它实现节点间数据传递
"""
from typing import TypedDict, List, Dict


class AnalysisState(TypedDict):
    """安全告警分析工作流全链路状态"""
    #  输入层 
    task_id: str
    data_source: str
    raw_alerts_path: str

    # 中间产物 
    cleaned_alerts_count: int
    process_model_result: Dict
    attack_path_result: Dict
    rag_insights: List[Dict]

    #  控制字段 
    current_step: str
    completed_steps: List[str]
    retry_count: int
    errors: List[str]
    confidence_score: float

    #  最终输出 
    final_report: Dict
    false_positive_count: int
    real_attack_cases: int

