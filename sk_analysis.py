import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def analyze_serial_killers():
    """
    Generate comprehensive analysis and visualization of serial killer data,
    avoiding the 'Possible victims' and 'Years active' columns.
    """
    # Create output directories
    os.makedirs('data/reports', exist_ok=True)
    os.makedirs('data/charts', exist_ok=True)
    
    # Load the data
    print("Loading data from CSV...")
    try:
        df = pd.read_csv('data/output.csv')
        print(f"Loaded {len(df)} rows with {len(df.columns)} columns")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Created an overview of the dataset
    print("\nGenerating analysis report...")
    
# Create a timestamp for the report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Start the report
    report = f"""# Serial Killer Data Analysis Report
Generated: {timestamp}

# Dataset Overview
- Total records: {len(df)}
- Total columns: {len(df.columns)}

"""
    
    # 1. TEMPORAL ANALYSIS
    report += "\n## Temporal Analysis\n\n"
    
    # Calculate activity period statistics using from_year and to_year
    if all(col in df.columns for col in ['from_year', 'to_year']):
        # Basic statistics on time periods
        from_year_stats = df['from_year'].describe().to_dict()
        to_year_stats = df['to_year'].describe().to_dict()
        
        report += f"### Activity Period Statistics\n"
        report += f"- Earliest recorded activity start: {int(from_year_stats['min'])}\n"
        report += f"- Latest recorded activity start: {int(from_year_stats['max'])}\n"
        report += f"- Earliest recorded activity end: {int(to_year_stats['min'])}\n"
        report += f"- Latest recorded activity end: {int(to_year_stats['max'])}\n"
        report += f"- Median activity start year: {int(from_year_stats['50%'])}\n"
        report += f"- Median activity end year: {int(to_year_stats['50%'])}\n\n"
        