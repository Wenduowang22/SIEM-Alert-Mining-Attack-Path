# SIEM-Alert-Mining-Attack-Path
基于流程挖掘（Process Mining）的 SIEM 安全告警分析引擎。针对企业 SIEM 告警量爆炸、误报率高、分析师效率低的痛点，将告警组织为事件序列，自动挖掘攻击行为模式、识别攻击路径、实现告警降噪。

> 核心算法源自硕士学位论文研究，已完成工程化封装与服务化改造，可直接集成部署。

## ✨ 核心功能
- 🧹 **多源告警预处理**：告警去重、事件归一化、案例筛选、特征工程
- 🔍 **流程挖掘建模**：基于 DFG / 过程树 / Petri 网挖掘攻击行为链路
- 🎯 **真实攻击识别**：从海量告警中筛选真实攻击案例，过滤 90%+ 误告警
- 🛤️ **攻击路径分析**：自动还原攻击活动序列，识别横向移动模式
- 🌐 **REST API 服务**：基于 FastAPI 封装标准化接口，可直接集成进安全平台
- 📊 **可视化演示**：内置 Web 演示页面，直观展示分析结果

## 🛠️ 技术栈
| 类别 | 技术 |
|------|------|
| 开发语言 | Python 3.10+ |
| Web 框架 | FastAPI + Uvicorn |
| 流程挖掘 | PM4Py 2.7.23.3 |
| 数据引擎 | DuckDB, Pandas |
| 可视化 | 原生 HTML + CSS |
| 数据集 | Microsoft GUIDE Security Alert Dataset |

## 🚀 快速开始
### 环境要求
- Python 3.10+
- macOS / Linux / Windows

### 安装运行
1. 克隆仓库
```bash
git clone https://github.com/Wenduowang22/SIEM-Alert-Mining-Attack-Path.git
cd SIEM-Alert-Mining-Attack-Path

