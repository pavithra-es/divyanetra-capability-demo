import duckdb
from datetime import datetime


DB_NAME = "divyanetra.duckdb"


def get_connection():
    return duckdb.connect(DB_NAME)


def initialize_database():

    conn = get_connection()

    # =====================================================
    # GOVERNANCE / AUDIT TABLE
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            audit_id BIGINT,
            timestamp TIMESTAMP,
            agent_name VARCHAR,
            action VARCHAR,
            details VARCHAR,
            status VARCHAR
        )
    """)

    # =====================================================
    # INCIDENT TABLE
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id BIGINT,
            created_at TIMESTAMP,
            use_case VARCHAR,
            region VARCHAR,
            severity VARCHAR,
            risk_score DOUBLE,
            root_cause VARCHAR,
            status VARCHAR
        )
    """)

    # =====================================================
    # WORK ORDER / SERVICENOW SIMULATION
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS work_orders (
            work_order_id BIGINT,
            incident_id BIGINT,
            created_at TIMESTAMP,
            region VARCHAR,
            action VARCHAR,
            assigned_crew VARCHAR,
            status VARCHAR
        )
    """)

    # =====================================================
    # MOCK TEAMS ALERTS
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS teams_alerts (
            alert_id BIGINT,
            created_at TIMESTAMP,
            message VARCHAR,
            status VARCHAR
        )
    """)

    conn.close()


def next_id(table_name, column_name):

    conn = get_connection()

    result = conn.execute(
        f"""
        SELECT COALESCE(MAX({column_name}), 0) + 1
        FROM {table_name}
        """
    ).fetchone()[0]

    conn.close()

    return int(result)


def add_audit_log(agent_name, action, details, status="SUCCESS"):

    audit_id = next_id("audit_logs", "audit_id")

    conn = get_connection()

    conn.execute("""
        INSERT INTO audit_logs
        VALUES (?, ?, ?, ?, ?, ?)
    """, [
        audit_id,
        datetime.now(),
        agent_name,
        action,
        details,
        status
    ])

    conn.close()


def get_audit_logs():

    conn = get_connection()

    df = conn.execute("""
        SELECT
            timestamp,
            agent_name,
            action,
            details,
            status
        FROM audit_logs
        ORDER BY audit_id DESC
    """).df()

    conn.close()

    return df