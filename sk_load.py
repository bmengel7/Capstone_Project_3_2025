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
                    
                 # Added a column indicating the source file to track data provenance
                df['source_file'] = file_name
                all_dfs.append(df)
                print(f"  Loaded {len(df)} rows with {len(df.columns)} columns")
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
            
            #exit if no data is loaded from excel    
        if not all_dfs:
            print("No data loaded from Excel files.")
            return

           
        combined_df = pd.concat(all_dfs, ignore_index=True)
        print(f"Combined DataFrame has {len(combined_df)} rows and {len(combined_df.columns)} columns.")

        conn.register("combined_data", combined_df)
        
        conn.execute("DROP TABLE IF EXISTS serial")
        
        conn.execute("CREATE TABLE serial AS SELECT * FROM combined_data")
if __name__ == "__main__":  
    main()