import pandas as pd
from sklearn.preprocessing import LabelEncoder

def engineer_ml_features(df):
    df = df.copy()
    
    # Derived operational logistics ratios
    df['expected_velocity_kmh'] = df['distance_km'] / (df['expected_time_hours_clean'] + 1e-5)
    df['payload_intensity'] = df['package_weight_kg'] * df['distance_km']
    
    # Categorical string encoders
    categorical_columns = ['delivery_partner', 'package_type', 'vehicle_type', 'delivery_mode', 'region', 'weather_condition']
    encoders = {}
    
    for col in categorical_columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
        
    return df, encoders
