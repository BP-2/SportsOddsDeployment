import os
import glob
import pandas as pd

def load_and_process_csv_files(directory):
    file_pattern = os.path.join(directory, '**', '*moneyline_american.csv')  
    csv_files = glob.glob(file_pattern, recursive=True)
    
    all_dataframes = []

    for csv_file in csv_files:
        print(f"Processing file: {csv_file}")
        
        df = pd.read_csv(csv_file)
        
        df['Cutoff Time'] = pd.to_datetime(df['Cutoff Time'])
        df['Cutoff Date'] = df['Cutoff Time'].dt.date
        
        all_dataframes.append(df)

    combined_df = pd.concat(all_dataframes, ignore_index=True)

    combined_df.sort_values(by=['Game Name', 'Cutoff Time'], ascending=[True, False], inplace=True)

    combined_df.drop_duplicates(subset=['Away Team', 'Home Team', 'Cutoff Date'], keep='first', inplace=True)

    return combined_df

def main():
    directory = './' 

    result_df = load_and_process_csv_files(directory)

    print("Final DataFrame:")
    print(result_df)

    result_df.to_csv('merged_data.csv', index=False)
    result_df.sort_values(by=['Cutoff Time'], ascending=[True], inplace=True)
    result_df.to_csv('merged_data_time.csv', index=False)


if __name__ == "__main__":
    main()
