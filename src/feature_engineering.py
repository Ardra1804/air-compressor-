import numpy as np
import pandas as pd

def calculate_features(df):
    """
    Calculate derived features from raw metrics
    """
    
    # FAD efficiency: actual_fad / rated_fad (higher is better)
    if "actual_fad" in df.columns and "rated_fad" in df.columns:
        df["fad_efficiency"] = df["actual_fad"] / df["rated_fad"]
    else:
        df["fad_efficiency"] = 0
    
    # Pressure stability: difference between unload and load pressure
    # Lower difference = more stable (better)
    if "unload_pressure" in df.columns and "load_pressure" in df.columns:
        df["pressure_stability"] = df["unload_pressure"] - df["load_pressure"]
    else:
        df["pressure_stability"] = 0
    
    # Velocity uniformity: standard deviation of velocity readings
    # LOWER std = more uniform (better)
    velocity_cols = [c for c in df.columns if c.startswith("v")]
    if velocity_cols:
        df["velocity_uniformity"] = df[velocity_cols].std(axis=1)
    else:
        df["velocity_uniformity"] = 0
    
    # Running stability: ratio of running time to loading time
    # Higher ratio = more stable (better)
    if "running_time" in df.columns and "loading_time" in df.columns:
        # Avoid division by zero
        df["running_stability"] = df["running_time"] / df["loading_time"].replace(0, 1)
    else:
        df["running_stability"] = 0
    
    # Replace NaN and Inf values with 0
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)
    
    return df