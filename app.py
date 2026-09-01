import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

import os
from database import get_connection

conn = get_connection()
from setup_data import create_lakehouse

DB_FILE = "divyanetra.duckdb"

if not os.path.exists(DB_FILE):
    create_lakehouse()
    
from database import (
    DB_NAME,
    initialize_database,
    get_audit_logs
)

from agents import (

    run_network_health_swarm,

    run_rollout_swarm,

    executive_query_agent,

    supervisor_agent
)

from actions import (
    execute_approved_action
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title="DivyaNetra AI Command Center",

    page_icon="⚡",

    layout="wide"
)


# =========================================================
# INITIALIZATION
# =========================================================

initialize_database()


# =========================================================
# DATABASE QUERY
# =========================================================

def get_data(query):

    conn = duckdb.connect(DB_NAME)

    df = conn.execute(query).df()

    conn.close()

    return df


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("⚡ DIVYANETRA")

st.sidebar.markdown(
    "### Agentic Command Center"
)

page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Command Center",

        "📡 AMI Network Health",

        "📊 Smart Meter Rollout Risk",

        "💬 Executive Query",

        "📜 Audit & Governance",

        "🗄️ Data Explorer" 
    ]
)


# =========================================================
# COMMAND CENTER
# =========================================================

if page == "🏠 Command Center":

    st.title(
        "⚡ DivyaNetra AI Command Center"
    )

    st.caption(
        "Sense → Ground → Reason & Decide → Act"
    )

    try:

        network = get_data("""
            SELECT *
            FROM gold_network_kpi
        """)

        rollout = get_data("""
            SELECT *
            FROM gold_rollout_kpi
        """)

    except Exception:

        st.error(
            "Demo data not found."
        )

        st.code(
            "python setup_data.py"
        )

        st.stop()

    total_meters = int(
        network["total_meters"].sum()
    )

    at_risk = int(
        network["at_risk_meters"].sum()
    )

    delayed_projects = len(

        rollout[
            rollout["schedule_variance"] < 0
        ]
    )

    critical_vendors = len(

        rollout[
            rollout["sla_score"] < 85
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "⚡ Total Smart Meters",
        total_meters
    )

    c2.metric(
        "🔴 At-Risk Meters",
        at_risk
    )

    c3.metric(
        "🟠 Delayed Projects",
        delayed_projects
    )

    c4.metric(
        "🚨 Vendor Risk",
        critical_vendors
    )

    st.divider()

    st.subheader(
        "🤖 DivyaNetra Top AI Insight"
    )

    worst_network = network.sort_values(
        "at_risk_meters",
        ascending=False
    ).iloc[0]

    worst_rollout = rollout.sort_values(
        "schedule_variance"
    ).iloc[0]

    st.error(
        f"""
PRIORITY ATTENTION REQUIRED

📡 Network Risk:
{worst_network['region']}

At-Risk Meters:
{int(worst_network['at_risk_meters'])}

📊 Rollout Risk:
{worst_rollout['region']}

Vendor:
{worst_rollout['vendor']}

Schedule Variance:
{worst_rollout['schedule_variance']}%
"""
    )

    st.subheader(
        "📊 Network Health by Region"
    )

    fig = px.bar(

        network,

        x="region",

        y="at_risk_meters",

        title="At-Risk Smart Meters"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# NETWORK HEALTH PAGE
# =========================================================

elif page == "📡 AMI Network Health":

    st.title(
        "📡 AMI Network Health Agent"
    )

    st.caption(
        "Monitoring → Diagnosis → Prediction → Recommendation → Approval → Action"
    )

    if st.button(
        "🚀 Run Network Health Swarm",
        type="primary"
    ):

        with st.spinner(
            "DivyaNetra agents are analyzing the AMI network..."
        ):

            result = (
                run_network_health_swarm()
            )

            st.session_state[
                "network_result"
            ] = result

    if "network_result" in st.session_state:

        result = st.session_state[
            "network_result"
        ]

        monitoring = result["monitoring"]

        diagnosis = result["diagnosis"]

        prediction = result["prediction"]

        recommendation = result[
            "recommendation"
        ]

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Total Meters",
            monitoring["total_meters"]
        )

        c2.metric(
            "At Risk",
            monitoring["at_risk_meters"]
        )

        c3.metric(
            "Risk Score",
            prediction["risk_score"]
        )

        c4.metric(
            "Outage Probability",
            f"{prediction['outage_probability']}%"
        )

        st.divider()

        st.subheader(
            "🤖 Agent Decisions"
        )

        st.success(
            "👁️ Monitoring Agent completed"
        )

        st.info(
            f"""
🧠 Diagnosis Agent

Root Cause:
{diagnosis['root_cause']}

Region:
{diagnosis['affected_region']}

Concentrator:
{diagnosis['worst_concentrator']}

Severity:
{diagnosis['severity']}
"""
        )

        st.warning(
            f"""
🔮 Prediction Agent

Risk Score:
{prediction['risk_score']}

Predicted Impact:
{prediction['predicted_impact']} meters

Confidence:
{prediction['confidence']}%
"""
        )

        st.success(
            f"""
💡 Recommendation Agent

Priority:
{recommendation['priority']}

Action:
{recommendation['recommended_action']}

Crew:
{recommendation['crew']}
"""
        )

        st.divider()

        st.subheader(
            "👤 Human-in-the-Loop"
        )

        approve = st.button(
            "✅ Approve Operational Action",
            type="primary"
        )

        if approve:

            action_result = (
                execute_approved_action(

                    use_case="AMI Network Health",

                    region=diagnosis[
                        "affected_region"
                    ],

                    severity=diagnosis[
                        "severity"
                    ],

                    risk_score=prediction[
                        "risk_score"
                    ],

                    root_cause=diagnosis[
                        "root_cause"
                    ],

                    recommended_action=
                        recommendation[
                            "recommended_action"
                        ],

                    crew=recommendation[
                        "crew"
                    ]
                )
            )

            st.success(
                "🎉 Action Executed Successfully"
            )

            st.write(
                f"Incident ID: {action_result['incident_id']}"
            )

            st.write(
                f"ServiceNow Work Order: "
                f"{action_result['work_order_id']}"
            )

            st.write(
                "📢 Teams Alert:"
            )

            st.info(
                action_result["teams_alert"]
            )


# =========================================================
# ROLLOUT RISK PAGE
# =========================================================

elif page == "📊 Smart Meter Rollout Risk":

    st.title(
        "📊 Smart Meter Rollout Risk Agent"
    )

    st.caption(
        "Progress → Vendor → Workforce → Prediction → Recommendation"
    )

    if st.button(
        "🚀 Run Rollout Risk Swarm",
        type="primary"
    ):

        with st.spinner(
            "Analyzing rollout projects..."
        ):

            result = run_rollout_swarm()

            st.session_state[
                "rollout_result"
            ] = result

    if "rollout_result" in st.session_state:

        result = st.session_state[
            "rollout_result"
        ]

        rollout_df = result[
            "rollout_data"
        ]

        risk_df = result[
            "risk_data"
        ]

        recommendations = result[
            "recommendations"
        ]

        st.subheader(
            "📈 Rollout Progress"
        )

        st.dataframe(
            rollout_df[[
                "project_id",
                "region",
                "vendor",
                "expected_progress",
                "actual_progress",
                "schedule_variance",
                "sla_score",
                "material_availability",
                "planned_crew_count",
                "actual_crew_count"
            ]],

            use_container_width=True
        )

        st.divider()

        st.subheader(
            "🔮 AI Risk Prediction"
        )

        st.dataframe(
            risk_df,

            use_container_width=True
        )

        fig = px.bar(

            risk_df,

            x="region",

            y="risk_score",

            color="risk_level",

            title="Smart Meter Rollout Risk"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        st.subheader(
            "💡 AI Recommendations"
        )

        st.dataframe(
            recommendations,
            use_container_width=True
        )


# =========================================================
# EXECUTIVE QUERY
# =========================================================

elif page == "💬 Executive Query":

    st.title(
        "💬 DivyaNetra Executive Query Agent"
    )

    st.caption(
        "Ask questions across governed operational data"
    )

    examples = [

        "What requires immediate attention today?",

        "Which region has the highest network risk?",

        "Which rollout project is delayed?",

        "Which vendor is performing poorly?"
    ]

    question = st.text_input(

        "Ask DivyaNetra",

        placeholder=
        "What requires immediate attention today?"
    )

    st.write("Examples:")

    selected_example = st.selectbox(
        "Choose an example",
        [""] + examples
    )

    if selected_example:

        question = selected_example

    if st.button(
        "🤖 Ask DivyaNetra",
        type="primary"
    ):

        if question:

            route = supervisor_agent(
                question
            )

            result = executive_query_agent(
                question
            )

            st.success(
                f"Supervisor Route: {route}"
            )

            st.subheader(
                f"🤖 {result['source']}"
            )

            st.info(
                result["answer"]
            )

        else:

            st.warning(
                "Please enter a question."
            )


# =========================================================
# AUDIT & GOVERNANCE
# =========================================================

elif page == "📜 Audit & Governance":

    st.title(
        "📜 DivyaNetra Governance Rail"
    )

    st.caption(
        "Every agent decision and operational action is auditable"
    )

    logs = get_audit_logs()

    if len(logs) > 0:

        st.dataframe(
            logs,
            use_container_width=True
        )

    else:

        st.info(
            "No audit events yet. Run an agent workflow."
        )

    st.divider()

    st.subheader(
        "🔐 Governance Model"
    )

    st.markdown("""

- **Sense:** Simulated AMI, rollout and vendor data
- **Ground:** Bronze → Silver → Gold tables
- **Reason & Decide:** Supervisor and domain agents
- **Human-in-the-Loop:** Approval required for operational action
- **Act:** Mock ServiceNow, WFM and Teams workflow
- **Audit:** Every agent action is logged
""")
elif page == "🗄️ Data Explorer":

    st.title("🗄️ DivyaNetra Data Explorer")

    tables = [
        "bronze_meter_telemetry",
        "bronze_rollout_progress",
        "bronze_vendor_performance",
        "silver_meter_telemetry",
        "silver_rollout_progress",
        "silver_vendor_performance",
        "gold_network_kpi",
        "gold_rollout_kpi"
    ]

    selected_table = st.selectbox(
        "Select Data Layer / Table",
        tables
    )

    df = conn.execute(
        f"SELECT * FROM {selected_table}"
    ).df()

    st.subheader(f"📊 {selected_table}")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.success(f"Total Records: {len(df)}")    