import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from feature_engineering import engineer_ml_features

def execute_model_training():
    print("Initializing Predictive Diagnostic Risk Engine...")
    cleaned_csv = "data/processed/delivery_logistics_cleaned.csv"
    
    if not os.path.exists(cleaned_csv):
        raise FileNotFoundError(f"Processed file '{cleaned_csv}' not found. Run src/data_pipeline.py first.")
        
    df = pd.read_csv(cleaned_csv)
    processed_df, encoders = engineer_ml_features(df)
    
    features = [
        'delivery_partner', 'package_type', 'vehicle_type', 'delivery_mode', 
        'region', 'weather_condition', 'distance_km', 'package_weight_kg', 
        'expected_time_hours_clean', 'delivery_cost', 'expected_velocity_kmh', 'payload_intensity'
    ]
    
    X = processed_df[features]
    y = processed_df['target_delayed']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set dimensions: {X_train.shape}, Test set dimensions: {X_test.shape}")
    
    # Fit the multi-tree random forest ensemble model
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("Model training complete.")
    
    # Evaluate score metrics
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    print("\nModel Evaluation Summary Report:")
    print(classification_report(y_test, preds))
    print(f"Area Under ROC Curve (ROC-AUC): {roc_auc_score(y_test, probs):.4f}")
    
    # Print root-cause metric ranks
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    
    print("\nRoot-Cause Variance Signatures (Feature Importance Ranking):")
    for rank, idx in enumerate(sorted_idx):
        print(f" Rank {rank+1}: Feature '{features[idx]}' ({importances[idx]:.4%})")

if __name__ == "__main__":
    execute_model_training()
