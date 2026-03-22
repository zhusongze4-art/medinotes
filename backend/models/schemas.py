from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ============ LLM 输出结构 ============

class ClinicalSummary(BaseModel):
    """LLM 生成的结构化临床摘要，SOAP 格式"""
    patient_name: str = Field(description="患者姓名")
    age: Optional[int] = Field(default=None, description="患者年龄")
    subjective: str = Field(description="主观：患者主诉、症状、病史")
    objective: str = Field(description="客观：体检结果、检查数据")
    assessment: str = Field(description="评估：诊断结论")
    plan: str = Field(description="计划：治疗方案、后续步骤")
    medications: List[str] = Field(default_factory=list, description="提及的药物")
    diagnoses: List[str] = Field(default_factory=list, description="诊断列表")


# ============ API 请求模型 ============

class DialogueRequest(BaseModel):
    """POST /api/ingest 的请求体"""
    dialogue: str = Field(description="医患对话原文")


class SearchRequest(BaseModel):
    """POST /api/search/similar 的请求体"""
    query: str = Field(description="搜索关键词或症状描述")
    top_k: int = Field(default=5, description="返回最相似的 K 条记录")


# ============ API 响应模型 ============

class PatientRecord(BaseModel):
    """存储在 Redis 中的完整患者记录"""
    patient_id: str
    summary: ClinicalSummary
    raw_dialogue: str
    created_at: datetime = Field(default_factory=datetime.now)


class PatientListItem(BaseModel):
    """患者列表页展示用的精简结构"""
    patient_id: str
    patient_name: str
    age: Optional[int]
    assessment: str


class AgeStats(BaseModel):
    """年龄统计结果"""
    total: int
    min_age: Optional[int]
    max_age: Optional[int]
    avg_age: Optional[float]


class AgeGroup(BaseModel):
    """年龄分布的单个桶"""
    group: str
    count: int


class MedicationCount(BaseModel):
    """药物频率的单条记录"""
    medication: str
    count: int


class AnalyticsResponse(BaseModel):
    """GET /api/analytics 的完整响应"""
    age_stats: AgeStats
    age_distribution: List[AgeGroup]
    medication_frequency: List[MedicationCount]