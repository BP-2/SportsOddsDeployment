import pandas as pd

file_path = 'completeOctNov.csv'  
df = pd.read_csv(file_path)

print("Original columns:", df.columns)

df = df.drop(columns=['PTS.1'])

print("\nData after removing 'PTS.1':")
print(df.head())

output_file = 'cleaned_data.csv'  
df.to_csv(output_file, index=False)

print(f"\nCleaned data has been saved to '{output_file}'.")
