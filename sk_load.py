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
        all_dfs = []  
        #inserted python to use excel files for program
        for i, excel_file in enumerate(excel_files):
            file_name = os.path.basename(excel_file)
            print(f"Loading {file_name}...")
             
            try:
                
                if i == 0:
                    df = pd.read_excel(excel_file)
                    if df.empty:
                        print(f"Warning: {file_name} is empty, skipping")
                        continue
                    
                    headers = df.columns.tolist()
                else:
                    
                    df = pd.read_excel(excel_file, header=None, names=headers)
                   
                    df = df.iloc[1:]
 
if __name__ == "__main__":  
    main()