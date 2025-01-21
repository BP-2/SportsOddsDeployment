import pandas as pd

input_file = 'merged_data_time.csv' 

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


df = pd.read_csv(input_file)

output_data = []

for _, row in df.iterrows():
    game_name = row['Game Name']
    visitor_team, home_team = game_name.split(' v ')

    visitor_team_full = team_name_mapping.get(visitor_team, visitor_team) 
    home_team_full = team_name_mapping.get(home_team, home_team)
    
    away_odds = f"+{row['Away Odds']}" if row['Away Odds'] > 0 else f"{row['Away Odds']}"
    home_odds = f"+{row['Home Odds']}" if row['Home Odds'] > 0 else f"{row['Home Odds']}"
    

    cutoff_date = row['Cutoff Date']
    
    output_data.append([visitor_team_full, home_team_full, away_odds, home_odds, cutoff_date])

output_df = pd.DataFrame(output_data, columns=['Visitor/Neutral', 'Home/Neutral', 'AwayOdds', 'HomeOdds', 'Cutoff Date'])

output_file = 'jan_transformed_odds_with_full_team_names.csv'  
output_df.to_csv(output_file, index=False)

print(f"Transformed data with full team names saved to {output_file}")
