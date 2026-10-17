"""
API data schema definitions
Used for request/response type validation
"""
from pydantic import BaseModel
from typing import List

class AttackPathResponse(BaseModel):
    case_id: str
    alert_count: int
    activity_count: int
    activity_sequence: List[str]
    time_span: str

class MetricsResponse(BaseModel):
    number_of_cases: int
    number_of_events: int
    number_of_activities: int
    false_positive_reduction_rate: str
    noise_reduction_factor: float

