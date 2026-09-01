import duckdb

# Connect to DuckDB database
conn = duckdb.connect("divyanetra.duckdb")

# List all tables
print("\n===================================")
print("ALL TABLES")
print("===================================")

tables = conn.execute("""
    SHOW TABLES
""").fetchall()

for table in tables:
    print(table[0])


# Function to display table data
def show_table(table_name):
    print("\n\n===================================")
    print(f"TABLE: {table_name}")
    print("===================================")

    result = conn.execute(f"""
        SELECT *
        FROM {table_name}
        LIMIT 10
    """).df()

    print(result.to_string(index=False))


# Bronze Tables
show_table("bronze_meter_telemetry")
show_table("bronze_rollout_progress")
show_table("bronze_vendor_performance")


# Silver Tables
show_table("silver_meter_telemetry")
show_table("silver_rollout_progress")
show_table("silver_vendor_performance")


# Gold Tables
show_table("gold_network_kpi")
show_table("gold_rollout_kpi")


conn.close()