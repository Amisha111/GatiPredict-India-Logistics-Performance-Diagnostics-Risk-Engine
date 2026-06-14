import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from feature_engineering import engineer_ml_features

def build_diagnostic_visualizations():
    print("Generating programmatic visualization reports...")
    db_path = "database/logistics_warehouse.db"
    output_dir = "notebooks"
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Warehouse tracking index '{db_path}' not found. Execute src/data_pipeline.py first.")
        
    os.makedirs(output_dir, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM india_logistics_warehouse", conn)
    conn.close()
    
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'figure.figsize': (10, 6), 'axes.labelsize': 12, 'axes.titlesize': 14})
    
    # Plot 1: SLA Breach Rates by Carrier
    df_partner = df.groupby('delivery_partner')['target_delayed'].mean().reset_index()
    df_partner['sla_breach_rate_pct'] = df_partner['target_delayed'] * 100
    df_partner = df_partner.sort_values(by='sla_breach_rate_pct', ascending=False)
    
    plt.figure()
    sns.barplot(data=df_partner, x='sla_breach_rate_pct', y='delivery_partner', palette='viridis')
    plt.title('SLA Breach Rate (%) by Delivery Partner (India Region)', weight='bold', pad=15)
    plt.xlabel('SLA Breach Rate (%)')
    plt.ylabel('Delivery Partner')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'carrier_sla_breach_rate.png'), dpi=300)
    plt.close()
    
    # Plot 2: Delay Propensity by Weather Patterns
    df_weather = df.groupby('weather_condition')['target_delayed'].mean().reset_index()
    df_weather['sla_breach_rate_pct'] = df_weather['target_delayed'] * 100
    df_weather = df_weather.sort_values(by='sla_breach_rate_pct', ascending=False)
    
    plt.figure(figsize=(10, 5))
    sns.barplot(data=df_weather, x='weather_condition', y='sla_breach_rate_pct', palette='flare')
    plt.title('Impact of Weather Conditions on Delivery Delays', weight='bold', pad=15)
    plt.xlabel('Weather Condition')
    plt.ylabel('SLA Breach Rate (%)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'weather_delay_impact.png'), dpi=300)
    plt.close()
    
    # Plot 3: ML Variable Ranks
    processed_df, _ = engineer_ml_features(df)
    features = [
        'delivery_partner', 'package_type', 'vehicle_type', 'delivery_mode', 
        'region', 'weather_condition', 'distance_km', 'package_weight_kg', 
        'expected_time_hours_clean', 'delivery_cost'
    ]
    X = processed_df[features]
    y = processed_df['target_delayed']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X, y)
    
    df_imp = pd.DataFrame({
        'Feature': features,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=True)
    
    plt.figure()
    sns.barplot(data=df_imp, x='Importance', y='Feature', palette='crest_r')
    plt.title('Root-Cause Diagnostics: Feature Importance Ranking', weight='bold', pad=15)
    plt.xlabel('Relative Information Gain / Importance Weight')
    plt.ylabel('Operational Variable')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bottleneck_feature_importance.png'), dpi=300)
    plt.close()
    
    print(f"Visual dashboard configuration compiled. Charts exported to the '{output_dir}/' folder.")

if __name__ == "__main__":
    build_diagnostic_visualizations()
