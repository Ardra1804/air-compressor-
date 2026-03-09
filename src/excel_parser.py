import pandas as pd
import re

def clean(text):
    if pd.isna(text):
        return ""
    return str(text).strip().lower()

def parse_excel(file):
    """
    Advanced parser that extracts full machine names from multiple rows
    """
    df = pd.read_excel(file, header=None)
    
    print(f"\n=== EXCEL ANALYSIS ===")
    print(f"Shape: {len(df)} rows x {len(df.columns)} columns\n")
    
    # Print first 15 rows to understand structure
    print("First 15 rows structure:")
    for i in range(min(15, len(df))):
        row_preview = []
        for j in range(min(10, len(df.columns))):
            val = str(df.iloc[i, j])[:20]
            row_preview.append(f"C{j}:{val}")
        print(f"Row {i}: {row_preview}")
    print()
    
    # ---- STEP 1: FIND ALL MACHINE IDENTIFIERS AND NAMES ----
    machine_rows = {}  # {row_number: [machine_data]}
    
    # Search for rows that contain machine identifiers
    for i in range(len(df)):
        row_data = []
        has_machine = False
        
        for j in range(1, len(df.columns)):  # Skip column A
            cell = str(df.iloc[i, j]).strip()
            cell_lower = cell.lower()
            
            # Check for any machine pattern
            if any(pattern in cell_lower for pattern in ["air compressor", "ash ac", "ahp", "compressor"]):
                row_data.append((j, cell))
                has_machine = True
        
        if has_machine:
            machine_rows[i] = row_data
            print(f"Machine identifiers at row {i}: {[cell for _, cell in row_data]}")
    
    if not machine_rows:
        raise ValueError("❌ No machines found in spreadsheet")
    
    # ---- STEP 2: SELECT THE BEST MACHINE ROW ----
    # Prefer the row with the most detailed names
    best_row = max(machine_rows.keys(), key=lambda x: sum(len(cell) for _, cell in machine_rows[x]))
    
    machine_cols = [col for col, _ in machine_rows[best_row]]
    machines = [cell for _, cell in machine_rows[best_row]]
    
    print(f"\n✓ Using row {best_row} as machine row")
    print(f"  Machines: {machines}")
    print(f"  Columns: {machine_cols}\n")
    
    # ---- STEP 3: AUTO-DETECT DATA START ROW ----
    data_start_row = best_row + 1
    
    # ---- STEP 4: AUTO-DETECT PARAMETER ROWS ----
    param_rows = {}
    param_labels = {
        "rated_fad": ["rated", "fad", "capacity", "air flow", "l/s"],
        "actual_fad": ["actual", "fad", "capacity"],
        "leakage": ["leakage"],
        "sec": ["sec"],
        "load_pressure": ["loading pressure", "load pressure", "set point"],
        "unload_pressure": ["unloading pressure", "unload pressure"],
        "running_time": ["running time", "total running"],
        "loading_time": ["loading time", "total loading"],
    }
    
    for i in range(data_start_row, len(df)):
        label = clean(str(df.iloc[i, 0]))
        
        for param_name, keywords in param_labels.items():
            if any(keyword in label for keyword in keywords):
                if param_name not in param_rows:
                    param_rows[param_name] = i
                    print(f"✓ {param_name:20s} @ row {i}: {str(df.iloc[i, 0])[:40]}")
    
    print()
    
    # ---- STEP 5: AUTO-DETECT VELOCITY ROWS ----
    velocity_rows = []
    for i in range(data_start_row, len(df)):
        label = clean(str(df.iloc[i, 0]))
        if re.search(r"velocity|v\d+", label):
            velocity_rows.append(i)
    
    if velocity_rows:
        print(f"✓ Velocity rows: {velocity_rows}\n")
    
    # ---- STEP 6: EXTRACT DATA ----
    records = []
    
    print(f"✓ Extracting data for {len(machines)} machines:")
    for machine_name, col_idx in zip(machines, machine_cols):
        row_data = {"machine": machine_name}
        
        # Extract all detected parameters
        for param_name, param_row in param_rows.items():
            try:
                value = df.iloc[param_row, col_idx]
                row_data[param_name] = value
            except:
                row_data[param_name] = None
        
        # Extract velocity values
        for idx, vel_row in enumerate(velocity_rows):
            try:
                value = df.iloc[vel_row, col_idx]
                row_data[f"v{idx+1}"] = value
            except:
                row_data[f"v{idx+1}"] = None
        
        records.append(row_data)
        print(f"  ✓ {machine_name}")
    
    # Create DataFrame
    dataset = pd.DataFrame(records)
    
    # Convert numeric columns
    for col in dataset.columns:
        if col != "machine":
            dataset[col] = pd.to_numeric(dataset[col], errors="coerce")
    
    print(f"\n=== FINAL DATASET ===")
    print(f"Shape: {dataset.shape}")
    print(f"Columns: {dataset.columns.tolist()}\n")
    print(dataset)
    print()
    
    return dataset