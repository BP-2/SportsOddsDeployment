import pandas as pd

# Define the input file
input_file = 'oddsDatesLateDec.csv'  # Replace with your actual input file path

# Define the mapping from abbreviations to full team names
team_name_mapping = {
    'IND Pacers': 'Indiana Pacers',
    'NO Pelicans': 'New Orleans Pelicans',
    'ORL Magic': 'Orlando Magic',
    'NY Knicks': 'New York Knicks',
    'BOS Celtics': 'Boston Celtics',
    'MIN Timberwolves': 'Minnesota Timberwolves',
    'SA Spurs': 'San Antonio Spurs',
    'POR Trail Blazers': 'Portland Trail Blazers',
    'DAL Mavericks': 'Dallas Mavericks',
    'MEM Grizzlies': 'Memphis Grizzlies',
    'LA Lakers': 'Los Angeles Lakers',
    'DET Pistons': 'Detroit Pistons',
    'MIA Heat': 'Miami Heat',
    'WAS Wizards': 'Washington Wizards',
    'PHX Suns': 'Phoenix Suns',
    'GSW Warriors': 'Golden State Warriors',
    'CHA Hornets': 'Charlotte Hornets',
    'CLE Cavaliers': 'Cleveland Cavaliers',
    'ATL Hawks': 'Atlanta Hawks',
    'SAS Spurs': 'San Antonio Spurs',
    'LAC Clippers': 'Los Angeles Clippers',
    'MIL Bucks': 'Milwaukee Bucks',
    'CHI Bulls': 'Chicago Bulls',
    'TOR Raptors': 'Toronto Raptors',
    'BKN Nets': 'Brooklyn Nets',
    'SAC Kings': 'Sacramento Kings',
    'HOU Rockets': 'Houston Rockets',
    'UTA Jazz': 'Utah Jazz',
    'OKC Thunder': 'Oklahoma City Thunder',
    'PHI 76ers': 'Philadelphia 76ers',
    'BOS Celtics': 'Boston Celtics',
    'POR Trail Blazers': 'Portland Trail Blazers',
    'NY Knicks': 'New York Knicks',
    'MEM Grizzlies': 'Memphis Grizzlies',
    'TOR Raptors': 'Toronto Raptors',
    'SAC Kings': 'Sacramento Kings',
    'DET Pistons': 'Detroit Pistons',
    'MIA Heat': 'Miami Heat',
    'WAS Wizards': 'Washington Wizards'
}


# Read the data into a pandas DataFrame
df = pd.read_csv(input_file)

# Initialize an empty list to store the transformed rows
output_data = []

# Loop through each row of the input DataFrame
for _, row in df.iterrows():
    # Parse the game name to get the visitor and home teams
    game_name = row['Game Name']
    visitor_team, home_team = game_name.split(' v ')

    # Replace the abbreviated team names with full names
    visitor_team_full = team_name_mapping.get(visitor_team, visitor_team)  # Use abbreviation if not found
    home_team_full = team_name_mapping.get(home_team, home_team)  # Use abbreviation if not found
    
    # Extract the away and home odds, and add '+' or '-' signs if needed
    away_odds = f"+{row['Away Odds']}" if row['Away Odds'] > 0 else f"{row['Away Odds']}"
    home_odds = f"+{row['Home Odds']}" if row['Home Odds'] > 0 else f"{row['Home Odds']}"
    

    # Extract the cutoff date
    cutoff_date = row['Cutoff Date']
    
    # Append the transformed data to the output list
    output_data.append([visitor_team_full, home_team_full, away_odds, home_odds, cutoff_date])

# Create a DataFrame for the output
output_df = pd.DataFrame(output_data, columns=['Visitor/Neutral', 'Home/Neutral', 'AwayOdds', 'HomeOdds', 'Cutoff Date'])

# Save the output data to a CSV file
output_file = 'transformed_odds_with_full_team_names.csv'  # Replace with your desired output file path
output_df.to_csv(output_file, index=False)

print(f"Transformed data with full team names saved to {output_file}")
