import pandas as pd
import numpy as np

def normalize_metrics(df, metrics):
    """
    Normalize metrics to 0-1 range
    Some metrics should be minimized (lower is better), others maximized (higher is better)
    """
    
    # Define which metrics should be MINIMIZED (lower is better)
    minimize_metrics = {
        "sec",           # Specific Energy Consumption - lower is better
        "leakage",       # Leakage - lower is better
        "velocity_uniformity"  # Standard deviation - lower (more uniform) is better
    }
    
    # Define which metrics should be MAXIMIZED (higher is better)
    maximize_metrics = {
        "fad_efficiency",      # FAD Efficiency - higher is better
        "pressure_stability",  # Pressure difference - depends on context
        "running_stability"    # Running time ratio - higher is better
    }
    
    data = df[metrics].copy()
    
    print("\n=== NORMALIZATION PROCESS ===\n")
    
    for col in metrics:
        col_data = data[col].values
        min_val = col_data.min()
        max_val = col_data.max()
        
        if max_val == min_val:
            data[col] = 0.5  # If all values are the same, set to 0.5
            print(f"✓ {col:25s}: All values same ({min_val})")
        else:
            # Normalize to 0-1
            normalized = (col_data - min_val) / (max_val - min_val)
            
            # If metric should be MINIMIZED, invert it (so lower values get higher scores)
            if col in minimize_metrics:
                normalized = 1 - normalized
                metric_type = "MINIMIZE (inverted)"
            else:
                metric_type = "MAXIMIZE"
            
            data[col] = normalized
            
            print(f"✓ {col:25s}: {metric_type:20s} | range [{min_val:.4f}, {max_val:.4f}]")
    
    print()
    return data