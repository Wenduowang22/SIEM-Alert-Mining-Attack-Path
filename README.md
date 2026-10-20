# SIEM 安全告警挖掘与攻击路径分析平台

基于多智能体编排的企业级安全告警智能分析平台，将流程挖掘技术引入 SIEM 告警分析场景，通过 LangGraph 驱动 7 个专业 Agent 协同工作，自动挖掘攻击行为模式、还原攻击链路、实现告警降噪，有效降低安全分析师的误报处理负担。

项目源自硕士学位研究课题，已完成完整工程化封装，可直接集成部署至企业安全运营体系。

## ✨ 核心特性
- 🧠 **多智能体编排引擎**：基于 LangGraph 状态机构建 7 个专业 Agent 流水线，覆盖编排调度、数据清洗、特征工程、流程挖掘、攻击溯源、误报研判、报告生成全链路，节点解耦、可扩展、可追溯
- 📊 **流程挖掘攻击建模**：基于 PM4Py 实现 DFG 直接跟随图、过程树、Petri 网多维度攻击行为建模，自动挖掘攻击者横向移动路径与行为模式
- ⚡ **高性能数据处理**：基于 DuckDB 列式引擎处理百万级告警日志，支持多源数据归一化清洗、案例聚合、特征工程全流程
- 🌐 **标准化 API 服务**：基于 FastAPI 封装标准化 REST 接口，配套可视化 Web 演示页面，实现从原始告警输入到攻击路径输出的全链路自动化
- 🔄 **状态机驱动架构**：统一 AgentState 共享状态，支持条件路由、异常重试、流式进度推送，分析过程全链路可观测
- 🛡️ **生产级工程规范**：统一 Agent 抽象基类、标准化错误处理、增量状态更新机制，符合企业级项目设计范式

## 🏗️ 系统架构
### 7-Agent 协同工作流
Orchestrator 编排调度 Agent
↓
DataCleaner 数据清洗 Agent
↓
FeatureEngineer 特征工程 Agent
↓
ProcessMiner 流程挖掘建模 Agent
↓
AttackTracer 攻击溯源还原 Agent
↓
FalsePositiveJudge 误报研判过滤 Agent
↓
ReportGenerator 分析报告输出 Agent
基于 LangGraph StateGraph 状态图编排，全链路通过 AgentState 共享数据，支持同步批量执行与流式实时推送两种运行模式。

## 🛠️ 技术栈
| 类别 | 技术 |
|------|------|
| 核心语言 | Python 3.10+ |
| 多智能体编排 | LangGraph、LangChain Core |
| 流程挖掘 | PM4Py（Process Mining） |
| Web 框架 | FastAPI + Uvicorn |
| 数据引擎 | DuckDB、Pandas、NumPy |
| 工程化 | Git、Docker 支持 |

## 📈 效果验证
基于 Microsoft GUIDE 160 万条真实安全告警数据集完成效果验证：
- 误告警过滤率达 **90%+**
- 告警降噪倍数约 **10 倍**
- 从海量原始告警中精准筛选出 **1692 个真实攻击案例**

## 🚀 快速开始
### 环境安装
```bash
# 克隆仓库
git clone https://github.com/Wenduowang22/SIEM-Alert-Mining-Attack-Path.git
cd SIEM-Alert-Mining-Attack-Path

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
from src.agents.workflow import AlertAnalysisWorkflow

# 初始化工作流
wf = AlertAnalysisWorkflow()

# 执行完整分析
result = wf.run(
    task_id="task_001",
    data_path="data/sample_alerts.csv"
)

# 查看结果
print(f"分析告警数: {result['cleaned_alerts_count']}")
print(f"真实攻击案例: {result['real_attack_cases']}")
print(f"置信度: {result['confidence_score']}")

启动API服务
python run.py
接口文档地址：http://localhost:8000/docs

📁 项目结构
SIEM-Alert-Mining-Attack-Path/
├── src/
│   ├── agents/              # 多智能体工作流模块
│   │   ├── base.py             # Agent 抽象基类
│   │   ├── state.py            # 工作流共享状态定义
│   │   ├── orchestrator.py     # 编排调度 Agent
│   │   ├── data_cleaner.py     # 数据清洗 Agent
│   │   ├── feature_engineer.py # 特征工程 Agent
│   │   ├── process_miner.py    # 流程挖掘 Agent
│   │   ├── attack_tracer.py    # 攻击溯源 Agent
│   │   ├── false_positive_judge.py # 误报研判 Agent
│   │   ├── report_generator.py # 报告生成 Agent
│   │   └── workflow.py         # 工作流编排引擎
│   ├── data_processor.py    # 告警数据预处理
│   ├── process_miner.py     # 流程挖掘核心算法
│   ├── attack_analyzer.py   # 攻击路径分析
│   └── evaluator.py         # 效果评估
├── api/                    # FastAPI 接口层
├── data/                   # 测试数据目录
├── requirements.txt        # 依赖清单
├── run.py                  # 服务启动入口
└── README.md
## 📧 联系方式

- Wenduo Wang
- wenduowang22@163.com
