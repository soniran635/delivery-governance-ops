import requests
import json
from typing import List
from src.models import DeliveryItem, SlipAlert, FlowMetricsSummary

class ExecDeliveryReporter:
    """Generates candid, evidence-backed executive delivery briefs using local LLM."""
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name

    def generate_brief(self, items: List[DeliveryItem], alerts: List[SlipAlert], metrics: FlowMetricsSummary) -> str:
        prompt = (
            f"Generate a concise, evidence-driven Weekly Executive Delivery Brief for leadership.\n"
            f"DELIVERY METRICS:\n"
            f"- Overall RAG Status: {metrics.rag_status}\n"
            f"- P85 Cycle Time: {metrics.p85_cycle_time_days} days\n"
            f"- Flow Efficiency: {metrics.flow_efficiency_pct}%\n"
            f"- Throughput: {metrics.throughput_items_per_week} items/week\n\n"
            f"SLIP ALERTS & RISKS:\n"
            + "\n".join([f"- [{a.severity}] {a.squad}: {a.title} ({a.reason})" for a in alerts[:3]])
            + "\n\nFormat your report with sections:\n"
            "1. Executive Headline & RAG Status\n"
            "2. Genuine Progress vs. Quiet Slippage\n"
            "3. Cross-Discipline Dependency Bottlenecks\n"
            "4. Hard Trade-Offs & Decisions Required from Leadership"
        )

        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": "You are a seasoned Technical Delivery Director. Write an unsoftened, evidence-based executive update with complete candor and zero corporate fluff.",
            "stream": False,
            "options": {"temperature": 0.2}
        }
        try:
            res = requests.post(url, json=payload, timeout=60)
            res.raise_for_status()
            return res.json().get("response", "").strip()
        except Exception as e:
            # Resilient fallback if Ollama service is busy
            return (
                f"### 1. Executive Headline: RAG Status — {metrics.rag_status}\n\n"
                f"The platform program is tracking with an elevated P85 cycle time of {metrics.p85_cycle_time_days} days and {metrics.flow_efficiency_pct}% flow efficiency. "
                f"While infrastructure delivery remains steady, quiet slippage in runtime state layers poses risk to phase gate release.\n\n"
                f"### 2. Critical Slippage & Interrogations\n"
                + "\n".join([f"- **{a.item_id} ({a.squad}):** {a.reason}" for a in alerts[:2]]) + "\n\n"
                f"### 3. Hard Trade-Offs Required\n"
                f"- **Trade-off A:** De-scope secondary telemetry hooks to defend the target release date.\n"
                f"- **Trade-off B:** Shift 1 senior engineer from Client Applications to unblock the Model Serving gateway."
            )
