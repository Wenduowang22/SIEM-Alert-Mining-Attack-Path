"""
安全知识库检索器
内置 ATT&CK 战术、处置建议、合规要求三类安全知识
支持余弦相似度语义检索，为分析结果注入领域知识
"""
import logging
from typing import List, Dict
import numpy as np
from .embedding import EmbeddingService

logger = logging.getLogger(__name__)

# 内置安全知识库（演示版，生产环境可迁移至 PGVector 向量数据库）
BUILTIN_SECURITY_KNOWLEDGE = [
    {
        "type": "mitre_attack",
        "title": "T1021.001 远程桌面协议横向移动",
        "content": "攻击者通过 RDP 3389 端口进行内网横向移动，常见于勒索软件传播，特征为短时间内高频 3389 端口连接尝试",
        "mitre_id": "T1021.001",
    },
    {
        "type": "mitre_attack",
        "title": "T1110 暴力破解",
        "content": "针对 SSH/FTP/数据库等服务的密码暴力枚举，特征为短时间内大量失败登录事件，来源IP集中",
        "mitre_id": "T1110",
    },
    {
        "type": "mitre_attack",
        "title": "T1041 数据渗出",
        "content": "攻击者通过隐蔽通道将窃取的数据外传，常见于攻击收尾阶段，特征为异常大流量外发、非工作时间传输",
        "mitre_id": "T1041",
    },
    {
        "type": "disposal",
        "title": "横向移动事件处置建议",
        "content": "1. 立即隔离受害主机 2. 封禁攻击源IP地址 3. 核查受害主机账号权限 4. 更新防火墙访问控制策略",
    },
    {
        "type": "disposal",
        "title": "暴力破解事件处置建议",
        "content": "1. 封禁攻击源IP 2. 启用登录失败锁定策略 3. 强制相关用户修改弱密码 4. 开启双因素认证",
    },
    {
        "type": "compliance",
        "title": "等保2.0 告警处置要求",
        "content": "需留存告警日志不少于6个月，处置流程需留痕，高危告警需1小时内响应，形成闭环处置记录",
    },
]


class KnowledgeRetriever:
    def __init__(self):
        self.embedding = EmbeddingService()
        self.knowledge_base = BUILTIN_SECURITY_KNOWLEDGE
        self._vec_index = None

    def _build_index(self):
        """构建向量索引，首次调用自动构建"""
        if self._vec_index is None:
            texts = [item["title"] + " " + item["content"] for item in self.knowledge_base]
            self._vec_index = np.array(self.embedding.encode_batch(texts))

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        语义检索相关安全知识
        :param query: 查询文本
        :param top_k: 返回条数
        :return: 按相似度降序排列的知识列表
        """
        self._build_index()
        query_vec = np.array(self.embedding.encode(query))

        # 计算余弦相似度
        scores = np.dot(self._vec_index, query_vec)
        top_indices = scores.argsort()[-top_k:][::-1]

        results = []
        for idx in top_indices:
            item = self.knowledge_base[idx].copy()
            item["similarity_score"] = float(scores[idx])
            results.append(item)
        return results

