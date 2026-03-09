from src.excel_parser import parse_excel
from src.feature_engineering import calculate_features
from src.normalization import normalize_metrics
from src.ahp_weights import get_weights
from src.ranking_engine import rank_machines

def run_pipeline(file):
    df = parse_excel(file)
    
    print("Parsed data:")
    print(df)
    
    df = calculate_features(df)
    
    print("\nAfter feature engineering:")
    print(df)
    
    # ---- DYNAMICALLY SELECT AVAILABLE METRICS ----
    available_metrics = [
        "sec",
        "leakage",
        "fad_efficiency",
        "pressure_stability",
        "velocity_uniformity",
        "running_stability"
    ]
    
    # Filter to only metrics that exist in the dataframe
    metrics = [m for m in available_metrics if m in df.columns]
    
    print(f"\nUsing metrics: {metrics}")
    
    if not metrics:
        raise ValueError("No valid metrics found in the dataset")
    
    scaled = normalize_metrics(df, metrics)
    
    weights = get_weights()
    
    scores = rank_machines(scaled, metrics, weights)
    
    df["performance_score"] = scores
    
    result = df.sort_values("performance_score", ascending=False)
    
    # ---- RESET INDEX TO START FROM 1 ----
    result = result.reset_index(drop=True)
    result.index = result.index + 1
    
    return result