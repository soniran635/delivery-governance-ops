from pydantic import BaseModel, Field
from typing import List, Optional

class DeliveryItem(BaseModel):
    item_id: str
    title: str
    squad: str  # 'GPU/K8s Infra', 'Model Serving & Routing', 'Agent Orchestration', 'Client Applications'
    status: str  # 'Backlog', 'In_Progress', 'Blocked', 'In_Review', 'Done'
    committed_date: str
    in_flight_days: int
    estimate_days: int
    active_coding_hours: float
    idle_wait_hours: float
    blocked_reason: Optional[str] = None
    dependency_ids: List[str] = []

class SlipAlert(BaseModel):
    item_id: str
    title: str
    squad: str
    severity: str  # 'CRITICAL_SLIP', 'HIGH_RISK', 'WATCHLIST'
    reason: str
    standup_interrogation_question: str
    recommended_intervention: str

class FlowMetricsSummary(BaseModel):
    p50_cycle_time_days: float
    p85_cycle_time_days: float
    p95_cycle_time_days: float
    flow_efficiency_pct: float
    throughput_items_per_week: int
    rag_status: str  # 'RED', 'AMBER', 'GREEN'
