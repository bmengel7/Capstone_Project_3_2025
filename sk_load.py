import os
import re
import glob
import pandas as pd
import duckdb

def main():

data_dir = 'data'
duckdb_path = os.path.join(data_dir, 'serial_killers.duckdb')
output_csv_path = os.path.join(data_dir, 'output.csv')

os.makedirs(data_dir, exist_ok=True)

print(f"Connecting to DuckDB at {duckdb_path}...")
    conn = duckdb.connect(duckdb_path)
    
    try:
       
        excel_files = glob.glob(os.path.join(data_dir, '*.xlsx'))

       
        if not excel_files:
            print(f"No Excel files found in {data_dir} directory.")
            return

        print(f"Found {len(excel_files)} Excel files: {[os.path.basename(f) for f in excel_files]}")
        
        print("Processing Excel files...")
        all_dfsts = []  

        for i, excel_file in enumerated(excel_files):
            file_name = os.path.basename(excel_file)
            print(f"Loading {file_name}...")
 
if __name__ == "__main__":  
    main()