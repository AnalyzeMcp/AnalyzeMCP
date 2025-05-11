from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

from ..ai.models import ProtocolAnalyzer
from ..data.processor import DataProcessor

app = FastAPI(
    title="AnalyzeMCP API",
    description="API for Machine Control Protocol Analysis",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProtocolData(BaseModel):
    protocol_type: str
    timestamp: datetime
    packet_size: int
    payload: Dict[str, Any]

class AnalysisResult(BaseModel):
    analysis: List[Dict[str, Any]]
    insights: List[str]
    recommendations: List[str]

# Dependency Injection
def get_analyzer():
    model = ProtocolAnalyzer()
    return model

def get_processor():
    processor = DataProcessor()
    return processor

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_protocol(
    data: List[ProtocolData],
    analyzer: ProtocolAnalyzer = Depends(get_analyzer),
    processor: DataProcessor = Depends(get_processor)
) -> AnalysisResult:
    try:
        # Preprocess data
        processed_data = processor.preprocess_protocol_data([d.dict() for d in data])
        
        # Perform analysis
        analysis_results = analyzer.analyze(processed_data)
        
        # Generate insights and recommendations
        insights = analyzer.generate_insights(analysis_results)
        recommendations = analyzer.generate_recommendations(analysis_results)
        
        return AnalysisResult(
            analysis=analysis_results,
            insights=insights,
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/metrics")
async def get_metrics(
    analyzer: ProtocolAnalyzer = Depends(get_analyzer)
) -> Dict[str, Any]:
    try:
        return analyzer.get_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))