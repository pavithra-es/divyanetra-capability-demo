import duckdb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

from database import (
    DB_NAME,
    initialize_database
)


random.seed(42)
np.random.seed(42)


def generate_meter_data():

    rows = []

    regions = [
        "Mumbai North",
        "Mumbai South",
        "Mumbai West",
        "Mumbai Central"
    ]

    concentrator_map = {
        "Mumbai North": "DC-100",
        "Mumbai South": "DC-200",
        "Mumbai West": "DC-300",
        "Mumbai Central": "DC-400"
    }

    for i in range(1, 501):

        region = random.choice(regions)

        concentrator = concentrator_map[region]

        signal_strength = round(
            np.random.uniform(70, 100), 2
        )

        packet_loss = round(
            np.random.uniform(0, 5), 2
        )

        latency = round(
            np.random.uniform(20, 120), 2
        )

        event_type = "NORMAL"

        # =================================================
        # INTENTIONAL DEMO PROBLEM
        # Mumbai West / DC-300
        # =================================================

        if region == "Mumbai West":

            if random.random() < 0.70:

                signal_strength = round(
                    np.random.uniform(15, 45), 2
                )

                packet_loss = round(
                    np.random.uniform(15, 45), 2
                )

                latency = round(
                    np.random.uniform(250, 800), 2
                )

                event_type = "COMMUNICATION_DEGRADATION"

        rows.append({

            "meter_id": f"METER-{i:05d}",

            "region": region,

            "concentrator_id": concentrator,

            "signal_strength": signal_strength,

            "packet_loss": packet_loss,

            "latency": latency,

            "firmware_version": "FW-2.1",

            "event_type": event_type,

            "event_time": datetime.now()
        })

    return pd.DataFrame(rows)


def generate_rollout_data():

    data = [

        {
            "project_id": "PRJ-001",
            "region": "Mumbai North",
            "vendor": "Vendor Alpha",
            "target_meters": 100000,
            "installed_meters": 82000,
            "expected_progress": 80,
            "actual_progress": 82,
            "material_availability": 96,
            "planned_crew_count": 12,
            "actual_crew_count": 12
        },

        {
            "project_id": "PRJ-002",
            "region": "Mumbai South",
            "vendor": "Vendor Beta",
            "target_meters": 80000,
            "installed_meters": 65000,
            "expected_progress": 70,
            "actual_progress": 81,
            "material_availability": 94,
            "planned_crew_count": 10,
            "actual_crew_count": 11
        },

        {
            "project_id": "PRJ-003",
            "region": "Mumbai West",
            "vendor": "Vendor Gamma",
            "target_meters": 100000,
            "installed_meters": 62000,
            "expected_progress": 75,
            "actual_progress": 62,
            "material_availability": 68,
            "planned_crew_count": 12,
            "actual_crew_count": 8
        },

        {
            "project_id": "PRJ-004",
            "region": "Mumbai Central",
            "vendor": "Vendor Alpha",
            "target_meters": 90000,
            "installed_meters": 70000,
            "expected_progress": 72,
            "actual_progress": 78,
            "material_availability": 92,
            "planned_crew_count": 10,
            "actual_crew_count": 10
        }
    ]

    return pd.DataFrame(data)


def generate_vendor_data():

    data = [

        {
            "vendor": "Vendor Alpha",
            "sla_score": 94,
            "installation_quality": 96,
            "rejection_rate": 2,
            "average_installations_per_day": 850
        },

        {
            "vendor": "Vendor Beta",
            "sla_score": 91,
            "installation_quality": 92,
            "rejection_rate": 4,
            "average_installations_per_day": 720
        },

        {
            "vendor": "Vendor Gamma",
            "sla_score": 78,
            "installation_quality": 80,
            "rejection_rate": 14,
            "average_installations_per_day": 420
        }
    ]

    return pd.DataFrame(data)


def create_lakehouse():

    initialize_database()

    conn = duckdb.connect(DB_NAME)

    # =====================================================
    # 01 SENSE / BRONZE
    # =====================================================

    meter_df = generate_meter_data()

    rollout_df = generate_rollout_data()

    vendor_df = generate_vendor_data()

    conn.register("meter_df", meter_df)

    conn.execute("""
        CREATE OR REPLACE TABLE bronze_meter_telemetry AS
        SELECT *
        FROM meter_df
    """)

    conn.unregister("meter_df")

    conn.register("rollout_df", rollout_df)

    conn.execute("""
        CREATE OR REPLACE TABLE bronze_rollout_progress AS
        SELECT *
        FROM rollout_df
    """)

    conn.unregister("rollout_df")

    conn.register("vendor_df", vendor_df)

    conn.execute("""
        CREATE OR REPLACE TABLE bronze_vendor_performance AS
        SELECT *
        FROM vendor_df
    """)

    conn.unregister("vendor_df")

    # =====================================================
    # 02 GROUND / SILVER
    # =====================================================

    conn.execute("""
        CREATE OR REPLACE TABLE silver_meter_telemetry AS
        SELECT
            meter_id,
            region,
            concentrator_id,
            CAST(signal_strength AS DOUBLE) AS signal_strength,
            CAST(packet_loss AS DOUBLE) AS packet_loss,
            CAST(latency AS DOUBLE) AS latency,
            firmware_version,
            event_type,
            event_time,

            CASE
                WHEN signal_strength < 50
                  OR packet_loss > 10
                  OR latency > 200
                THEN 'AT_RISK'

                ELSE 'HEALTHY'
            END AS health_status

        FROM bronze_meter_telemetry

        WHERE meter_id IS NOT NULL
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE silver_rollout_progress AS
        SELECT
            *,
            actual_progress - expected_progress
                AS schedule_variance,

            target_meters - installed_meters
                AS remaining_meters

        FROM bronze_rollout_progress
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE silver_vendor_performance AS
        SELECT *
        FROM bronze_vendor_performance
    """)

    # =====================================================
    # GOLD BUSINESS KPIs
    # =====================================================

    conn.execute("""
        CREATE OR REPLACE TABLE gold_network_kpi AS

        SELECT

            region,

            COUNT(*) AS total_meters,

            SUM(
                CASE
                    WHEN health_status = 'HEALTHY'
                    THEN 1
                    ELSE 0
                END
            ) AS healthy_meters,

            SUM(
                CASE
                    WHEN health_status = 'AT_RISK'
                    THEN 1
                    ELSE 0
                END
            ) AS at_risk_meters,

            ROUND(
                AVG(signal_strength),
                2
            ) AS avg_signal_strength,

            ROUND(
                AVG(packet_loss),
                2
            ) AS avg_packet_loss,

            ROUND(
                AVG(latency),
                2
            ) AS avg_latency

        FROM silver_meter_telemetry

        GROUP BY region
    """)

    conn.execute("""
        CREATE OR REPLACE TABLE gold_rollout_kpi AS

        SELECT

            r.project_id,
            r.region,
            r.vendor,
            r.target_meters,
            r.installed_meters,
            r.expected_progress,
            r.actual_progress,
            r.schedule_variance,
            r.remaining_meters,
            r.material_availability,
            r.planned_crew_count,
            r.actual_crew_count,

            v.sla_score,
            v.installation_quality,
            v.rejection_rate,
            v.average_installations_per_day

        FROM silver_rollout_progress r

        LEFT JOIN silver_vendor_performance v

        ON r.vendor = v.vendor
    """)

    conn.close()

    print("==============================================")
    print("DivyaNetra Demo Data Created Successfully")
    print("==============================================")

    print("Bronze Layer:")
    print(" - bronze_meter_telemetry")
    print(" - bronze_rollout_progress")
    print(" - bronze_vendor_performance")

    print()
    print("Silver Layer:")
    print(" - silver_meter_telemetry")
    print(" - silver_rollout_progress")
    print(" - silver_vendor_performance")

    print()
    print("Gold Layer:")
    print(" - gold_network_kpi")
    print(" - gold_rollout_kpi")


if __name__ == "__main__":

    create_lakehouse()