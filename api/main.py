"""
FastAPI main entry point
Expose process mining capabilities as REST API services
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import tempfile

from src.data_processor import AlertDataProcessor
from src.process_miner import AttackProcessMiner
from src.attack_analyzer import AttackPathAnalyzer
from src.evaluator import ModelEvaluator

app = FastAPI(
    title="SIEM Alert Mining & Attack Path System",
    description="基于流程挖掘的安全告警分析引擎 | 硕士论文工程化实现",
    version="1.0.0"
)

# Mount static demo page
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize all modules globally
processor = AlertDataProcessor()
miner = AttackProcessMiner()
analyzer = AttackPathAnalyzer()
evaluator = ModelEvaluator()

# Auto-load sample data when service starts
@app.on_event("startup")
def load_sample_data():
    sample_path = "data/sample_alerts.csv"
    if os.path.exists(sample_path):
        processor.load_and_preprocess(sample_path)
        miner.format_event_log(processor.event_log_df)

@app.get("/", response_class=HTMLResponse)
def root():
    """Service homepage"""
    return """
    <h1>SIEM 安全告警挖掘与攻击路径分析系统</h1>
    <p>📚 基于硕士论文：A Process Mining Approach to Analysing Cybersecurity Attack Behaviour</p>
    <p>🔌 接口文档：<a href="/docs">/docs</a></p>
    <p>📊 演示页面：<a href="/static/demo.html">/static/demo.html</a></p>
    """

@app.get("/api/metrics", summary="获取整体分析指标")
def get_metrics():
    """Return dataset scale and false positive reduction metrics"""
    return evaluator.get_full_summary(processor)

@app.get("/api/attacks", summary="获取攻击案例列表")
def get_attack_list(limit: int = 20):
    """Get top N attack cases sorted by alert count"""
    return analyzer.get_attack_list(processor.event_log_df, limit)

@app.get("/api/attack/{case_id}", summary="查询单个攻击路径")
def get_attack_path(case_id: str):
    """Get full activity sequence for a specific case ID"""
    return analyzer.get_attack_path(processor.event_log_df, case_id)

@app.get("/api/dfg/top", summary="获取 Top 跨活动转换关系")
def get_top_dfg_edges(top_n: int = 10):
    """Get most frequent cross-activity transitions"""
    edges = miner.get_cross_activity_edges(top_n)
    return edges.to_dict(orient="records")

@app.post("/api/upload", summary="上传自定义告警 CSV")
async def upload_alert_file(file: UploadFile = File(...)):
    """Upload custom alert CSV file for analysis"""
    content = await file.read()
    
    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        df = processor.load_and_preprocess(tmp_path)
        miner.format_event_log(df)
        return {
            "status": "success",
            "metrics": evaluator.get_full_summary(processor)
        }
    finally:
        os.unlink(tmp_path)

