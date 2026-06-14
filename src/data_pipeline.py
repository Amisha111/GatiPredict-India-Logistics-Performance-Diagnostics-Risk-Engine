import os
import sqlite3
import pandas as pd

def run_etl_pipeline():
    print("Starting data ingestion and processing pipeline...")
    raw_csv = "Delivery_Logistics.csv"
    db_dir = "database"
    db_path = os.path.join(db_dir, "logistics_warehouse.db")
    schema_path = os.path.join(db_dir, "schema.sql")
    analytical_path = os.path.join(db_dir, "analytical_queries.sql")
    
    if not os.path.exists(raw_csv):
        raise FileNotFoundError(f"Source file '{raw_csv}' must be present in the root directory.")
        
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)
    
    # Load and clean timestamp data records
    df = pd.read_csv(raw_csv)
    df.columns = [col.strip() for col in df.columns]
    
    # Parse out numeric hours from the timestamp string anomalies
    df['delivery_time_hours_clean'] = df['delivery_time_hours'].apply(lambda x: int(str(x).split('.')[-1]))
    df['expected_time_hours_clean'] = df['expected_time_hours'].apply(lambda x: int(str(x).split('.')[-1]))
    df['target_delayed'] = df['delayed'].apply(lambda x: 1 if str(x).strip().lower() == 'yes' else 0)
    
    # Export clean backup version
    df.to_csv("data/processed/delivery_logistics_cleaned.csv", index=False)
    print("Cleaned data file exported to 'data/processed/delivery_logistics_cleaned.csv'")
    
    # Connect and initialize relational SQLite model database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(schema_path, 'r') as schema_file:
        cursor.executescript(schema_file.read())
        
    # Append structured rows into the staging layer
    df.to_sql('india_logistics_warehouse', conn, if_exists='append', index=False)
    conn.commit()
    print(f"Relational staging completed. Seeded {len(df)} entries into '{db_path}'.")
    
    # Perform operational diagnostic test print
    print("\nRunning Staging KPI Query Verification (Top 5 Regional Carriers by Delay Rate):")
    with open(analytical_path, 'r') as query_file:
        queries = query_file.read().split(';')
        sample_kpi = pd.read_sql_query(queries[0], conn)
        print(sample_kpi.head(5).to_string())
        
    conn.close()

if __name__ == "__main__":
    run_etl_pipeline()
