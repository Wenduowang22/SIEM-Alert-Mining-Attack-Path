"""
Agent 抽象基类
所有分析 Agent 统一接口，规范日志、错误处理、状态更新
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """所有分析 Agent 的父类"""

    agent_name: str = "base_agent"

    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Agent 核心业务逻辑，子类必须实现
        :param state: 当前工作流全局状态
        :return: 状态增量更新字典
        """
        pass

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        带统一错误处理的执行入口
        所有 Agent 都通过此方法调用，不直接调用 execute
        """
        try:
            logger.info(f"[{self.agent_name}] 节点开始执行")
            # 执行业务逻辑
            result = self.execute(state)
            # 自动追加已完成步骤
            completed_steps = state.get("completed_steps", []) + [self.agent_name]
            result["completed_steps"] = completed_steps
            result["current_step"] = self.agent_name
            logger.info(f"[{self.agent_name}] 节点执行完成")
            return result
        except Exception as e:
            error_msg = f"[{self.agent_name}] 执行异常: {str(e)}"
            logger.error(error_msg, exc_info=True)
            errors = state.get("errors", []) + [error_msg]
            return {
                "errors": errors,
                "current_step": self.agent_name,
            }

