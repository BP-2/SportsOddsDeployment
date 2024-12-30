import pandas as pd

# Load the odds data (CSV with visitor/home teams and odds)
odds_file = 'transformed_odds_with_full_team_names.csv'  # Path to your odds data CSV file
odds_data = pd.read_csv(odds_file)

# Load the game details data (CSV with date, teams, and other game info)
game_details_file = 'preMergeOctDates.csv'  # Path to your game details CSV file
game_details_data = pd.read_csv(game_details_file)

# Inspect the data (optional)
print("Odds Data:")
print(odds_data.head())

print("\nGame Details Data:")
print(game_details_data.head())

# Clean up any extra spaces in the column names if necessary
odds_data.columns = odds_data.columns.str.strip()
game_details_data.columns = game_details_data.columns.str.strip()

# Merge the data on 'Visitor/Neutral' (from odds_data) with 'Visitor/Neutral' (from game_details_data)
# Also on 'Home/Neutral' (from odds_data) with 'Home/Neutral' (from game_details_data)
# Finally, merge based on 'PTS' (from odds_data) with 'PTS' (from game_details_data)
merged_data = pd.merge(odds_data, game_details_data, 
                       left_on=['Visitor/Neutral', 'Home/Neutral', 'PTS'], 
                       right_on=['Visitor/Neutral', 'Home/Neutral', 'PTS'],
                       how='inner')

# Inspect the merged data (optional)
print("\nMerged Data:")
print(merged_data.head())

# Save the merged data to a new CSV file
merged_data.to_csv('merged_games_with_odds.csv', index=False)

print("\nMerged data has been saved to 'merged_games_with_odds.csv'.")
