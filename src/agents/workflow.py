"""
LangGraph 工作流编排引擎
将 7 个 Agent 组装为状态机流水线，支持同步执行和流式推送
"""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import AnalysisState
from .orchestrator import OrchestratorAgent
from .data_cleaner import DataCleanerAgent
from .feature_engineer import FeatureEngineerAgent
from .process_miner import ProcessMinerAgent
from .attack_tracer import AttackTracerAgent
from .false_positive_judge import FalsePositiveJudgeAgent
from .report_generator import ReportGeneratorAgent


class AlertAnalysisWorkflow:
    """告警智能分析工作流引擎"""

    def __init__(self):
        # 1. 初始化所有 Agent 实例
        self.orchestrator = OrchestratorAgent()
        self.data_cleaner = DataCleanerAgent()
        self.feature_engineer = FeatureEngineerAgent()
        self.process_miner = ProcessMinerAgent()
        self.attack_tracer = AttackTracerAgent()
        self.fp_judge = FalsePositiveJudgeAgent()
        self.report_gen = ReportGeneratorAgent()

        # 2. 创建状态图
        self.graph = StateGraph(AnalysisState)
        self._build_nodes_and_edges()

        # 3. 配置内存检查点（支持会话记忆）
        self.checkpointer = MemorySaver()
        self.app = self.graph.compile(checkpointer=self.checkpointer)

    def _build_nodes_and_edges(self):
        """注册所有节点，并定义流水线执行顺序"""
        # 注册节点
        self.graph.add_node("orchestrator", self.orchestrator.run)
        self.graph.add_node("data_cleaner", self.data_cleaner.run)
        self.graph.add_node("feature_engineer", self.feature_engineer.run)
        self.graph.add_node("process_miner", self.process_miner.run)
        self.graph.add_node("attack_tracer", self.attack_tracer.run)
        self.graph.add_node("fp_judge", self.fp_judge.run)
        self.graph.add_node("report_generator", self.report_gen.run)

        # 设置入口节点
        self.graph.set_entry_point("orchestrator")

        # 线性流水线连接（顺序执行）
        self.graph.add_edge("orchestrator", "data_cleaner")
        self.graph.add_edge("data_cleaner", "feature_engineer")
        self.graph.add_edge("feature_engineer", "process_miner")
        self.graph.add_edge("process_miner", "attack_tracer")
        self.graph.add_edge("attack_tracer", "fp_judge")
        self.graph.add_edge("fp_judge", "report_generator")
        self.graph.add_edge("report_generator", END)

    def run(self, task_id: str, data_path: str, thread_id: str = "default") -> dict:
        """
        同步执行完整工作流
        :param task_id: 任务ID
        :param data_path: 告警数据文件路径
        :param thread_id: 会话线程ID，用于记忆
        :return: 最终完整状态
        """
        initial_state = {
            "task_id": task_id,
            "raw_alerts_path": data_path,
            "data_source": "csv",
            "current_step": "init",
            "completed_steps": [],
            "errors": [],
            "retry_count": 0,
        }
        config = {"configurable": {"thread_id": thread_id}}
        return self.app.invoke(initial_state, config=config)

    def stream(self, task_id: str, data_path: str, thread_id: str = "stream"):
        """
        流式逐节点返回状态，用于前端实时进度展示
        """
        initial_state = {
            "task_id": task_id,
            "raw_alerts_path": data_path,
            "data_source": "csv",
            "current_step": "init",
            "completed_steps": [],
            "errors": [],
            "retry_count": 0,
        }
        config = {"configurable": {"thread_id": thread_id}}
        return self.app.stream(initial_state, config=config)

