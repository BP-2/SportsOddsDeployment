import os
import pandas as pd
import math 

def decimal_to_american(decimal_odds):
    if pd.isna(decimal_odds) or math.isnan(decimal_odds):
        return 0 
    try:
        if decimal_odds >= 2.0:
            return int(100 * (decimal_odds - 1))
        else:
            return int(-100 / (decimal_odds - 1))
    except ZeroDivisionError: # should not hit here
        return None

def process_csv_files(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    for filename in os.listdir(folder_path):
        if filename.endswith("moneyline.csv"):
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(folder_path, filename.replace(".csv", "_american.csv"))
            print(f"Processing file: {filename}")
            try:
                df = pd.read_csv(input_file) 
                df["Home Odds"] = df["Home Odds"].apply(decimal_to_american)    
                df["Away Odds"] = df["Away Odds"].apply(decimal_to_american)
                
                df = df[['Game Name','Away Team','Home Team','Cutoff Time','Away Odds', 'Home Odds',]]
                df.to_csv(output_file, index=False)
                print(f"Saved converted file as: {output_file}\n")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    folder = "Moneyline" 
    process_csv_files(folder)
