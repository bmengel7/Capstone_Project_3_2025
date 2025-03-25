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
         # Dropping existing table to avoid conflicts
        conn.execute("DROP TABLE IF EXISTS serial")
        # set up to permanent table from the temporary data
        conn.execute("CREATE TABLE serial AS SELECT * FROM combined_data")
        
        # counting rows, function key, tables
        row_count = conn.execute("SELECT COUNT(*) FROM serial").fetchone()[0]
        print(f"Created 'serial' table with {row_count} rows")
        # Process Years active column to extract temporal information
        column_info = conn.execute("PRAGMA table_info(serial)").fetchall()
        column_names = [col[1] for col in column_info]
        
        years_active_col = None
        for col in column_names:
            if "year" in col.lower() and "active" in col.lower():
                years_active_col = col
                break

        if years_active_col:
            print(f"\nFound 'Years active' column: {years_active_col}")
            quoted_col = f'"{years_active_col}"'


            conn.execute(f"""
                -- Add new columns to store extracted year values
                ALTER TABLE serial ADD COLUMN from_year VARCHAR;
                ALTER TABLE serial ADD COLUMN to_year VARCHAR;
                
                -- Pattern 1: Extract starting year from patterns like "1984 to 1990", "1984-1990"
                -- The regex captures a 4-digit year followed by various separator formats
                UPDATE serial 
                SET from_year = regexp_extract({quoted_col}, '(\d{{4}})\s*(?:to|–|—|-)', 1)
                WHERE from_year IS NULL AND regexp_matches({quoted_col}, '(\d{{4}})\s*(?:to|–|—|-)');
                
                -- Pattern 2: For single year entries (no range), extract that year as the start year
                UPDATE serial 
                SET from_year = regexp_extract({quoted_col}, '(\d{{4}})', 1)
                WHERE from_year IS NULL AND regexp_matches({quoted_col}, '(\d{{4}})');
                
                -- Extract ending year from patterns like "1984 to 1990", "1984-1990"
                -- The regex captures a 4-digit year that follows various separator formats
                UPDATE serial 
                SET to_year = regexp_extract({quoted_col}, '(?:to|–|—|-)\s*(\d{{4}})', 1)
                WHERE to_year IS NULL AND regexp_matches({quoted_col}, '(?:to|–|—|-)\s*(\d{{4}})');
                
                -- For single year entries, use the same year as both start and end
                UPDATE serial 
                SET to_year = from_year
                WHERE to_year IS NULL AND from_year IS NOT NULL;
                
                -- Convert the extracted string years to integers for calculations
                ALTER TABLE serial ALTER COLUMN from_year TYPE INTEGER USING CAST(from_year AS INTEGER);
                ALTER TABLE serial ALTER COLUMN to_year TYPE INTEGER USING CAST(to_year AS INTEGER);
                
                -- Calculate the duration of activity (inclusive of both start and end years)
                ALTER TABLE serial ADD COLUMN active_duration INTEGER;
                UPDATE serial SET active_duration = to_year - from_year + 1
                WHERE from_year IS NOT NULL AND to_year IS NOT NULL;
            """)
        
            print("Successfully added from_year, to_year, and active_duration columns")
            
        possible_victims_col = None
        for col in column_names:
            if "victim" in col.lower() and ("possible" in col.lower() or "potential" in col.lower()):
                possible_victims_col = col
                break

        if possible_victims_col:
            print(f"\nFound victims column: {possible_victims_col}")
            quoted_victims_col = f'"{possible_victims_col}"'

            conn.execute(f"""
                -- Add column to store whether more victims are possible
                ALTER TABLE serial ADD COLUMN more_victims_possible VARCHAR;
                
                -- Default assumption is 'No'
                UPDATE serial SET more_victims_possible = 'No';
                
                -- If the victim count contains '+', set to 'Yes'
                UPDATE serial 
                SET more_victims_possible = 'Yes' 
                WHERE {quoted_victims_col} LIKE '%+%';
                
                -- Handle NULL values explicitly
                UPDATE serial
                SET more_victims_possible = 'No'
                WHERE {quoted_victims_col} IS NULL;
            """)
            
            yes_count = conn.execute("SELECT COUNT(*) FROM serial WHERE more_victims_possible = 'Yes'").fetchone()[0]
            no_count = conn.execute("SELECT COUNT(*) FROM serial WHERE more_victims_possible = 'No'").fetchone()[0]
            print(f"more_victims_possible counts: Yes: {yes_count}, No: {no_count}")

            print("\nProcessing number_possible_victims column...")
            
            conn.execute("ALTER TABLE serial ADD COLUMN number_possible_victims INTEGER")
            
            victims_df = conn.execute(f"""
                SELECT ROWID, {quoted_victims_col}, more_victims_possible 
                FROM serial
                WHERE more_victims_possible = 'Yes'
            """).fetchdf()
        
        

if __name__ == "__main__":  
    main()