from typing import List
from src.models import DeliveryItem, SlipAlert

class DeliverySlipDetector:
    """Algorithmic engine to detect quiet slippage, flow bottlenecks,

    and cross-discipline handoff blockers before sprint end.
    """
    def audit_commitments(self, items: List[DeliveryItem]) -> List[SlipAlert]:
        alerts = []
        item_map = {item.item_id: item for item in items}

        for item in items:
            if item.status == "Done":
                continue

            # 1. Detect Quiet Slippage: In-flight age > 1.7x of engineering estimate
            if item.status == "In_Progress" and item.in_flight_days > (item.estimate_days * 1.7):
                slip_days = item.in_flight_days - item.estimate_days
                alerts.append(SlipAlert(
                    item_id=item.item_id,
                    title=item.title,
                    squad=item.squad,
                    severity="CRITICAL_SLIP",
                    reason=f"In flight for {item.in_flight_days} days against a {item.estimate_days}-day estimate (+{slip_days} days slippage).",
                    standup_interrogation_question=(
                        f"Standup Question for {item.squad}: This was sized for {item.estimate_days} days but has been in progress for {item.in_flight_days} days. "
                        f"What specific technical complexity was uncovered, and can we split out the remaining unblocked scope today?"
                    ),
                    recommended_intervention="Decompose remaining work into an atomic story; agree on a firm exit date or de-scope."
                ))

            # 2. Detect Low Flow Efficiency (Blocked / Idle Waiting)
            total_hours = item.active_coding_hours + item.idle_wait_hours
            if total_hours > 0:
                efficiency = round((item.active_coding_hours / total_hours) * 100, 1)
                if efficiency < 30.0 and item.status == "In_Progress":
                    alerts.append(SlipAlert(
                        item_id=item.item_id,
                        title=item.title,
                        squad=item.squad,
                        severity="HIGH_RISK",
                        reason=f"Flow efficiency is only {efficiency}% ({item.idle_wait_hours} hrs waiting vs {item.active_coding_hours} hrs active work).",
                        standup_interrogation_question=(
                            f"Standup Question: Why is {item.item_id} spending {efficiency}% time in active progress? "
                            f"Who or what environment dependency is stalling this work?"
                        ),
                        recommended_intervention="Escalate cross-team unblocker with tech leads immediately."
                    ))

            # 3. Detect Dependency Chain Risk (Downstream Blocking)
            for dep_id in item.dependency_ids:
                if dep_id in item_map:
                    dep_item = item_map[dep_id]
                    if dep_item.status in ["Blocked", "In_Progress"] and dep_item.in_flight_days > dep_item.estimate_days:
                        alerts.append(SlipAlert(
                            item_id=item.item_id,
                            title=item.title,
                            squad=item.squad,
                            severity="HIGH_RISK",
                            reason=f"Blocked by upstream dependency {dep_item.item_id} ({dep_item.squad}) which is already slipping.",
                            standup_interrogation_question=f"Cross-Squad Sync: {item.squad} is gated waiting on {dep_item.item_id}. What is the exact handoff date?",
                            recommended_intervention="Schedule an emergency 15-min handoff alignment between squad leads."
                        ))

        return alerts
