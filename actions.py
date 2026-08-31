from datetime import datetime

from database import (
    get_connection,
    next_id,
    add_audit_log
)


def execute_approved_action(
    use_case,
    region,
    severity,
    risk_score,
    root_cause,
    recommended_action,
    crew
):

    # =====================================================
    # CREATE INCIDENT
    # =====================================================

    incident_id = next_id(
        "incidents",
        "incident_id"
    )

    conn = get_connection()

    conn.execute("""
        INSERT INTO incidents
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, [

        incident_id,

        datetime.now(),

        use_case,

        region,

        severity,

        risk_score,

        root_cause,

        "APPROVED"
    ])

    # =====================================================
    # CREATE MOCK SERVICENOW WORK ORDER
    # =====================================================

    work_order_id = next_id(
        "work_orders",
        "work_order_id"
    )

    conn.execute("""
        INSERT INTO work_orders
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [

        work_order_id,

        incident_id,

        datetime.now(),

        region,

        recommended_action,

        crew,

        "DISPATCHED"
    ])

    # =====================================================
    # CREATE MOCK TEAMS ALERT
    # =====================================================

    alert_id = next_id(
        "teams_alerts",
        "alert_id"
    )

    message = (

        f"DivyaNetra Alert: "
        f"Incident {incident_id} approved. "
        f"Work Order {work_order_id} dispatched "
        f"to {crew}."
    )

    conn.execute("""
        INSERT INTO teams_alerts
        VALUES (?, ?, ?, ?)
    """, [

        alert_id,

        datetime.now(),

        message,

        "SENT"
    ])

    conn.close()

    # =====================================================
    # AUDIT
    # =====================================================

    add_audit_log(
        "Action Agent",
        "Operational Action Executed",
        f"Incident {incident_id}, "
        f"Work Order {work_order_id}, "
        f"Crew {crew}"
    )

    return {

        "incident_id":
            incident_id,

        "work_order_id":
            work_order_id,

        "teams_alert":
            message
    }