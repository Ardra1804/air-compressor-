import numpy as np

def get_weights():
    """
    Return AHP weights for each metric (sum to 1.0)
    
    Weights based on importance:
    - SEC (40%): Most important - directly impacts energy costs
    - Leakage (20%): Important - affects efficiency
    - FAD Efficiency (15%): Capacity utilization
    - Pressure Stability (10%): Operational reliability
    - Velocity Uniformity (10%): Performance quality
    - Running Stability (5%): Consistency
    """
    weights = {
        "sec": 0.40,
        "leakage": 0.20,
        "fad_efficiency": 0.15,
        "pressure_stability": 0.10,
        "velocity_uniformity": 0.10,
        "running_stability": 0.05
    }
    
    print("✓ Weights assigned:")
    for metric, weight in weights.items():
        print(f"  {metric:25s}: {weight:.2%}")
    print()
    
    return weights