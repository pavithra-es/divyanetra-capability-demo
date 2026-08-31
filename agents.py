import duckdb
import pandas as pd

from database import (
    DB_NAME,
    add_audit_log
)


# =========================================================
# DATABASE HELPER
# =========================================================

def query_data(query):

    conn = duckdb.connect(DB_NAME)

    df = conn.execute(query).df()

    conn.close()

    return df


# =========================================================
# 01 MONITORING AGENT
# =========================================================

def monitoring_agent():

    df = query_data("""
        SELECT *
        FROM silver_meter_telemetry
    """)

    at_risk_df = df[
        df["health_status"] == "AT_RISK"
    ]

    result = {

        "total_meters": int(len(df)),

        "at_risk_meters":
            int(len(at_risk_df)),

        "healthy_meters":
            int(len(df) - len(at_risk_df)),

        "at_risk_percentage":
            round(
                len(at_risk_df) / len(df) * 100,
                2
            )
    }

    add_audit_log(
        "Monitoring Agent",
        "Network Health Scan",
        f"Scanned {result['total_meters']} meters. "
        f"Detected {result['at_risk_meters']} at-risk meters."
    )

    return result, at_risk_df


# =========================================================
# 02 DIAGNOSIS AGENT
# =========================================================

def diagnosis_agent(at_risk_df):

    if len(at_risk_df) == 0:

        return {

            "severity": "LOW",

            "root_cause":
                "No significant network issue detected",

            "affected_region": None,

            "worst_concentrator": None,

            "affected_meters": 0
        }

    grouped = (

        at_risk_df
        .groupby(
            ["region", "concentrator_id"]
        )
        .size()
        .reset_index(name="affected_meters")
        .sort_values(
            "affected_meters",
            ascending=False
        )
    )

    worst = grouped.iloc[0]

    affected = int(
        worst["affected_meters"]
    )

    if affected > 30:

        severity = "CRITICAL"

    elif affected > 15:

        severity = "HIGH"

    else:

        severity = "MEDIUM"

    root_cause = (

        f"Probable communication degradation "
        f"or Data Concentrator issue at "
        f"{worst['concentrator_id']}"
    )

    result = {

        "severity": severity,

        "root_cause": root_cause,

        "affected_region":
            worst["region"],

        "worst_concentrator":
            worst["concentrator_id"],

        "affected_meters": affected
    }

    add_audit_log(
        "Diagnosis Agent",
        "Root Cause Analysis",
        root_cause
    )

    return result


# =========================================================
# 03 PREDICTION AGENT
# =========================================================

def prediction_agent(at_risk_df):

    if len(at_risk_df) == 0:

        return {

            "risk_score": 0,

            "outage_probability": 0,

            "confidence": 100,

            "predicted_impact": 0
        }

    avg_signal = float(
        at_risk_df[
            "signal_strength"
        ].mean()
    )

    avg_packet_loss = float(
        at_risk_df[
            "packet_loss"
        ].mean()
    )

    avg_latency = float(
        at_risk_df[
            "latency"
        ].mean()
    )

    # =====================================================
    # DEMO RISK MODEL
    # =====================================================

    signal_risk = max(
        0,
        (50 - avg_signal) * 1.2
    )

    packet_risk = min(
        30,
        avg_packet_loss * 1.2
    )

    latency_risk = min(
        25,
        avg_latency / 20
    )

    risk_score = min(
        100,
        round(
            signal_risk
            + packet_risk
            + latency_risk,
            2
        )
    )

    outage_probability = min(
        99,
        round(risk_score + 8, 2)
    )

    confidence = min(
        95,
        round(
            70 + len(at_risk_df) / 5,
            2
        )
    )

    predicted_impact = int(
        len(at_risk_df) * 1.5
    )

    result = {

        "risk_score": risk_score,

        "outage_probability":
            outage_probability,

        "confidence": confidence,

        "predicted_impact":
            predicted_impact
    }

    add_audit_log(
        "Prediction Agent",
        "Network Risk Prediction",
        f"Risk Score={risk_score}, "
        f"Outage Probability={outage_probability}%"
    )

    return result


# =========================================================
# 04 NETWORK RECOMMENDATION AGENT
# =========================================================

def network_recommendation_agent(
    diagnosis,
    prediction
):

    if prediction["risk_score"] >= 70:

        priority = "P1 - CRITICAL"

        action = (
            f"Immediately inspect "
            f"{diagnosis['worst_concentrator']} "
            f"and dispatch Network Response Crew Alpha"
        )

        crew = "Network Response Crew Alpha"

    elif prediction["risk_score"] >= 40:

        priority = "P2 - HIGH"

        action = (
            "Perform preventive inspection "
            "within 4 hours"
        )

        crew = "Field Network Maintenance Crew"

    else:

        priority = "P3 - MEDIUM"

        action = (
            "Continue enhanced monitoring"
        )

        crew = "Network Monitoring Team"

    result = {

        "priority": priority,

        "recommended_action": action,

        "crew": crew
    }

    add_audit_log(
        "Network Recommendation Agent",
        "Remediation Plan",
        action
    )

    return result


# =========================================================
# COMPLETE NETWORK HEALTH SWARM
# =========================================================

def run_network_health_swarm():

    monitoring, at_risk_df = monitoring_agent()

    diagnosis = diagnosis_agent(
        at_risk_df
    )

    prediction = prediction_agent(
        at_risk_df
    )

    recommendation = (
        network_recommendation_agent(
            diagnosis,
            prediction
        )
    )

    return {

        "monitoring": monitoring,

        "diagnosis": diagnosis,

        "prediction": prediction,

        "recommendation": recommendation
    }


# =========================================================
# ROLLOUT PROGRESS AGENT
# =========================================================

def rollout_progress_agent():

    df = query_data("""
        SELECT *
        FROM gold_rollout_kpi
    """)

    df["progress_gap"] = (
        df["expected_progress"]
        - df["actual_progress"]
    )

    add_audit_log(
        "Rollout Progress Agent",
        "Rollout Progress Analysis",
        f"Analyzed {len(df)} rollout projects"
    )

    return df


# =========================================================
# VENDOR PERFORMANCE AGENT
# =========================================================

def vendor_performance_agent(df):

    risky = df[

        (df["sla_score"] < 85)

        |

        (df["rejection_rate"] > 10)

    ].copy()

    add_audit_log(
        "Vendor Performance Agent",
        "Vendor SLA Analysis",
        f"Detected {len(risky)} vendor risk areas"
    )

    return risky


# =========================================================
# WORKFORCE AGENT
# =========================================================

def workforce_agent(df):

    df = df.copy()

    df["crew_gap"] = (

        df["planned_crew_count"]
        - df["actual_crew_count"]
    )

    workforce_risk = df[
        df["crew_gap"] > 0
    ]

    add_audit_log(
        "Workforce Planning Agent",
        "Crew Availability Analysis",
        f"{len(workforce_risk)} projects have crew shortages"
    )

    return workforce_risk


# =========================================================
# ROLLOUT RISK PREDICTION AGENT
# =========================================================

def rollout_risk_agent(df):

    results = []

    for _, row in df.iterrows():

        delay_risk = max(
            0,
            row["expected_progress"]
            - row["actual_progress"]
        ) * 4

        vendor_risk = max(
            0,
            90 - row["sla_score"]
        ) * 2

        crew_risk = max(
            0,
            row["planned_crew_count"]
            - row["actual_crew_count"]
        ) * 5

        material_risk = max(
            0,
            90 - row["material_availability"]
        ) * 1.5

        rejection_risk = (
            row["rejection_rate"] * 1.5
        )

        risk_score = min(

            100,

            round(
                delay_risk
                + vendor_risk
                + crew_risk
                + material_risk
                + rejection_risk,
                2
            )
        )

        if risk_score >= 70:

            risk_level = "CRITICAL"

        elif risk_score >= 40:

            risk_level = "HIGH"

        elif risk_score >= 20:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"

        predicted_delay_days = int(
            risk_score / 4
        )

        results.append({

            "project_id":
                row["project_id"],

            "region":
                row["region"],

            "vendor":
                row["vendor"],

            "risk_score":
                risk_score,

            "risk_level":
                risk_level,

            "predicted_delay_days":
                predicted_delay_days
        })

    result_df = pd.DataFrame(results)

    add_audit_log(
        "Rollout Risk Agent",
        "Project Delay Prediction",
        "Calculated rollout risk scores"
    )

    return result_df


# =========================================================
# ROLLOUT RECOMMENDATION AGENT
# =========================================================

def rollout_recommendation_agent(
    rollout_df,
    risk_df
):

    merged = rollout_df.merge(

        risk_df,

        on=[
            "project_id",
            "region",
            "vendor"
        ]
    )

    recommendations = []

    for _, row in merged.iterrows():

        actions = []

        if row["risk_score"] >= 70:

            actions.append(
                "Immediate management escalation"
            )

        if row["actual_crew_count"] < row["planned_crew_count"]:

            crew_needed = (

                row["planned_crew_count"]
                - row["actual_crew_count"]
            )

            actions.append(
                f"Add {crew_needed} installation crews"
            )

        if row["material_availability"] < 80:

            actions.append(
                "Escalate material shortage"
            )

        if row["sla_score"] < 85:

            actions.append(
                f"Raise SLA alert for {row['vendor']}"
            )

        if not actions:

            actions.append(
                "Continue normal rollout monitoring"
            )

        recommendations.append({

            "project_id":
                row["project_id"],

            "region":
                row["region"],

            "recommendation":
                " | ".join(actions)
        })

    result_df = pd.DataFrame(
        recommendations
    )

    add_audit_log(
        "Rollout Recommendation Agent",
        "Recovery Plan",
        "Generated rollout remediation recommendations"
    )

    return result_df


# =========================================================
# COMPLETE ROLLOUT SWARM
# =========================================================

def run_rollout_swarm():

    rollout_df = rollout_progress_agent()

    vendor_performance_agent(
        rollout_df
    )

    workforce_agent(
        rollout_df
    )

    risk_df = rollout_risk_agent(
        rollout_df
    )

    recommendations = (
        rollout_recommendation_agent(
            rollout_df,
            risk_df
        )
    )

    return {

        "rollout_data":
            rollout_df,

        "risk_data":
            risk_df,

        "recommendations":
            recommendations
    }


# =========================================================
# EXECUTIVE QUERY AGENT
# =========================================================

def executive_query_agent(question):

    question_lower = question.lower()

    # -----------------------------------------------------
    # NETWORK INSIGHT
    # -----------------------------------------------------

    network = query_data("""
        SELECT *
        FROM gold_network_kpi
        ORDER BY at_risk_meters DESC
    """)

    # -----------------------------------------------------
    # ROLLOUT INSIGHT
    # -----------------------------------------------------

    rollout = query_data("""
        SELECT *
        FROM gold_rollout_kpi
        ORDER BY schedule_variance ASC
    """)

    total_at_risk = int(
        network["at_risk_meters"].sum()
    )

    worst_network = network.iloc[0]

    worst_rollout = rollout.iloc[0]

    # -----------------------------------------------------
    # SIMPLE INTENT ROUTING
    # -----------------------------------------------------

    if any(word in question_lower for word in [
        "network",
        "meter",
        "outage",
        "signal"
    ]):

        answer = f"""
NETWORK HEALTH INSIGHT

Highest Risk Region:
{worst_network['region']}

At-Risk Meters:
{int(worst_network['at_risk_meters'])}

Average Signal Strength:
{worst_network['avg_signal_strength']}

Recommended Priority:
Immediate investigation.
"""

        source = "Network Health Agent"

    elif any(word in question_lower for word in [
        "rollout",
        "project",
        "delay",
        "vendor"
    ]):

        answer = f"""
ROLLOUT INSIGHT

Highest Risk Project:
{worst_rollout['project_id']}

Region:
{worst_rollout['region']}

Vendor:
{worst_rollout['vendor']}

Expected Progress:
{worst_rollout['expected_progress']}%

Actual Progress:
{worst_rollout['actual_progress']}%

Schedule Variance:
{worst_rollout['schedule_variance']}%
"""

        source = "Rollout Risk Agent"

    else:

        answer = f"""
DIVYANETRA EXECUTIVE PRIORITY

1. Network Risk:
{worst_network['region']}

At-Risk Meters:
{int(worst_network['at_risk_meters'])}

2. Rollout Risk:
{worst_rollout['region']}

Vendor:
{worst_rollout['vendor']}

Schedule Variance:
{worst_rollout['schedule_variance']}%

RECOMMENDATION:

Prioritize {worst_network['region']} for
network remediation and operational recovery.
"""

        source = (
            "Cross-Domain Executive Intelligence"
        )

    add_audit_log(
        "Executive Query Agent",
        "Executive Question Answered",
        f"Question: {question}"
    )

    return {

        "source": source,

        "answer": answer
    }


# =========================================================
# SUPERVISOR AGENT
# =========================================================

def supervisor_agent(request):

    request_lower = request.lower()

    if any(word in request_lower for word in [
        "network",
        "meter",
        "signal",
        "outage"
    ]):

        route = "NETWORK_HEALTH"

    elif any(word in request_lower for word in [
        "rollout",
        "project",
        "vendor",
        "delay"
    ]):

        route = "ROLLOUT_RISK"

    else:

        route = "EXECUTIVE_QUERY"

    add_audit_log(
        "DivyaNetra Supervisor Agent",
        "Request Routing",
        f"Request routed to {route}"
    )

    return route