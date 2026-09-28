import os
import sys

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from src.models import DeliveryItem, FlowMetricsSummary
from src.slip_detector import DeliverySlipDetector
from src.exec_reporter import ExecDeliveryReporter

st.set_page_config(page_title="Delivery-Governance-Ops | AI Delivery Intelligence", layout="wide", page_icon="🧭")

st.title("🧭 Delivery-Governance-Ops: Engineering Intelligence & Slip Detection")
st.markdown("**Flow Metrics Telemetry | Quiet Slip Interrogator | Automated Executive Briefs** | *100% Free & Open-Source*")

# Mock telemetry across EY platform layers
sample_items = [
    DeliveryItem(
        item_id="INFRA-204",
        title="vLLM GPU Multi-Node Cluster Scaling",
        squad="GPU/K8s Infra",
        status="In_Progress",
        committed_date="2026-09-22",
        in_flight_days=8,
        estimate_days=3,
        active_coding_hours=12.0,
        idle_wait_hours=32.0,
        dependency_ids=[]
    ),
    DeliveryItem(
        item_id="MODEL-109",
        title="Dynamic Semantic Routing & Quota Gateway",
        squad="Model Serving & Routing",
        status="Blocked",
        committed_date="2026-09-25",
        in_flight_days=5,
        estimate_days=4,
        active_coding_hours=16.0,
        idle_wait_hours=18.0,
        blocked_reason="Gated waiting on GPU Cluster networking configuration",
        dependency_ids=["INFRA-204"]
    ),
    DeliveryItem(
        item_id="AGENT-301",
        title="Multi-Turn Agent Memory & State Persistence",
        squad="Agent Orchestration",
        status="In_Progress",
        committed_date="2026-09-26",
        in_flight_days=4,
        estimate_days=5,
        active_coding_hours=24.0,
        idle_wait_hours=6.0,
        dependency_ids=[]
    ),
    DeliveryItem(
        item_id="CLIENT-402",
        title="Audit-Grade Compliance Traceability Viewer",
        squad="Client Applications",
        status="In_Review",
        committed_date="2026-09-24",
        in_flight_days=6,
        estimate_days=5,
        active_coding_hours=28.0,
        idle_wait_hours=8.0,
        dependency_ids=["AGENT-301"]
    )
]

detector = DeliverySlipDetector()
reporter = ExecDeliveryReporter()

tab1, tab2, tab3 = st.tabs([
    "🚨 Standup Interrogator & Quiet Slippage",
    "📈 Flow Metrics & Squad Telemetry",
    "📋 AI Executive Delivery Brief"
])

# ----------------- TAB 1: STANDUP INTERROGATOR -----------------
with tab1:
    st.subheader("Daily Standup Interrogation Board")
    st.caption("Surfacing quietly slipping commitments, flow bottlenecks, and evidence-backed questions.")

    alerts = detector.audit_commitments(sample_items)
    
    st.error(f"⚠️ {len(alerts)} High-Risk Delivery Slippages Detected Across Active Sprints")

    for a in alerts:
        with st.expander(f"[{a.severity}] {a.item_id}: {a.title} ({a.squad})", expanded=True):
            st.markdown(f"**Observed Evidence:** {a.reason}")
            st.info(f"🎤 **Recommended Standup Interrogation Question:**\n\n*{a.standup_interrogation_question}*")
            st.markdown(f"**Intervention Plan:** {a.recommended_intervention}")

# ----------------- TAB 2: FLOW METRICS -----------------
with tab2:
    st.subheader("Objective Flow Telemetry")
    st.caption("Replacing story points with cycle time distribution and flow efficiency.")

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.metric(label="P50 Cycle Time", value="3.8 Days")
    with f2:
        st.metric(label="P85 Cycle Time", value="7.2 Days", delta="+1.4d slip risk", delta_color="inverse")
    with f3:
        st.metric(label="Flow Efficiency", value="46.5%", delta="-8% (Wait waste)")
    with f4:
        st.metric(label="Throughput", value="14 Items/Wk")

    st.divider()

    st.markdown("### Work-In-Progress (WIP) Health by Squad")
    wip_df = pd.DataFrame([
        {
            "Item ID": item.item_id,
            "Title": item.title,
            "Squad": item.squad,
            "Status": item.status,
            "In-Flight": f"{item.in_flight_days} days",
            "Estimate": f"{item.estimate_days} days",
            "Active Hours": f"{item.active_coding_hours}h",
            "Idle/Wait Hours": f"{item.idle_wait_hours}h"
        }
        for item in sample_items
    ])
    st.dataframe(wip_df, use_container_width=True, hide_index=True)

# ----------------- TAB 3: AI EXECUTIVE DELIVERY BRIEF -----------------
with tab3:
    st.subheader("Automated Executive Delivery Brief (WBR/MBR)")
    st.caption("Unsoftened delivery status generated directly from flow telemetry via local Ollama.")

    metrics = FlowMetricsSummary(
        p50_cycle_time_days=3.8,
        p85_cycle_time_days=7.2,
        p95_cycle_time_days=11.4,
        flow_efficiency_pct=46.5,
        throughput_items_per_week=14,
        rag_status="AMBER"
    )

    if st.button("⚡ Generate Candid Executive Brief via Local LLM", type="primary"):
        with st.spinner("Analyzing sprint telemetry and synthesizing executive brief..."):
            brief = reporter.generate_brief(sample_items, alerts, metrics)
            st.markdown(brief)
