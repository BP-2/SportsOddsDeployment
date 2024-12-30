import pandas as pd
from datetime import datetime, timedelta

odds_file = 'transformed_odds_with_full_team_names.csv'  
odds_data = pd.read_csv(odds_file)

game_details_file = 'preMergeOctDates.csv'  
game_details_data = pd.read_csv(game_details_file)

odds_data.columns = odds_data.columns.str.strip()
game_details_data.columns = game_details_data.columns.str.strip()

game_details_data['Date'] = pd.to_datetime(game_details_data['Date'], errors='coerce')
odds_data['Cutoff Date'] = pd.to_datetime(odds_data['Cutoff Date'], errors='coerce')

def teams_match(row_odds, row_game_details):
    odds_teams = sorted([row_odds['Visitor/Neutral'], row_odds['Home/Neutral']])
    game_teams = sorted([row_game_details['Visitor/Neutral'], row_game_details['Home/Neutral']])
    
    return odds_teams == game_teams

def dates_within_one_day(row_odds, row_game_details):
    date_diff = abs((row_game_details['Date'] - row_odds['Cutoff Date']).days)
    return date_diff <= 1

merged_data = []

for _, odds_row in odds_data.iterrows():
    for _, game_row in game_details_data.iterrows():
        if teams_match(odds_row, game_row) and dates_within_one_day(odds_row, game_row):
            merged_row = {
                'Visitor/Neutral': odds_row['Visitor/Neutral'],
                'PTS': game_row['PTS'],
                'Home/Neutral': odds_row['Home/Neutral'],
                'PTS2': game_row['PTS2'],
                'AwayOdds': odds_row['AwayOdds'],
                'HomeOdds': odds_row['HomeOdds'],
                'Date': game_row['Date'],
                'Start (ET)': game_row['Start (ET)'],
                'Attend.': game_row['Attend.'],
                'LOG': game_row['LOG'],
                'Arena': game_row['Arena'],
            }
            merged_data.append(merged_row)

merged_df = pd.DataFrame(merged_data)

merged_df.to_csv('merged_games_with_odds.csv', index=False)

print("Merged data has been saved to 'merged_games_with_odds.csv'.")
