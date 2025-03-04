#########################################################
# cloud_odds.py returns the moneyline odds from todays games using cloud_odds.py.  I am unsure 
# which sports book it uses, but it is almost exactly correct with most major sports books.
#
#
# NOTE: Lots more functionality within API for sports https://www.cloudbet.com/api/?urls.primaryName=Feed 
#
#########################################################

import requests
from dotenv import load_dotenv
import os
import csv
from datetime import datetime
from pprint import pprint


# grabbing the API key from environment variable
load_dotenv()  
API_KEY = os.getenv("CLOUD_API_KEY")
if not API_KEY:
    raise ValueError("API key is not set in the .env file.")

API_URL = "https://sports-api.cloudbet.com/pub/v2/odds/competitions/basketball-usa-nba" #endpoint

# Logs todays odds to a csv
def fetch_nba_moneyline_odds_csv():
    params = {"markets": "basketball.moneyline"}
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }

    response = requests.get(API_URL, headers=headers, params=params) # grab response

    if response.status_code == 200: # if it returned succesfully
        data = response.json()
        #print(data)
        events = data.get("events", [])
        print(events)
        if not events:
            print("No NBA moneyline odds available.") # really we should never reach here
            return
        # creating a unique data file to save data
        current_date = datetime.now().strftime("%Y-%m-%d")
        filename = f"{current_date}_moneyline.csv"
        
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Game Name", "Home Team", "Away Team", "Cutoff Time", "Home Odds", "Away Odds"])
            
            # Cycle through the returned json
            for event in events:
                game_name = event.get("name", "Unknown")
                cutoff_time = event.get("cutoffTime", "Unknown")
                home_team = event.get("home", {}).get("name", "Unknown") if event.get("home") else "Unknown"
                away_team = event.get("away", {}).get("name", "Unknown") if event.get("away") else "Unknown"
                markets = event.get("markets", {}).get("basketball.moneyline", {}).get("submarkets", {})
                print("BASKETBALL")
                print_nested(event.get("markets", {}))
                print("MARKETS")
                print_nested(markets)

                over_under = event.get("markets", {}).get("basketball.spread", {}).get("submarkets", {})
                print(over_under)
                # Check if both home and away teams exist and are valid
                if home_team == "Unknown" or away_team == "Unknown":
                    continue  
                
                # Extract moneyline odds for the main period
                main_period = markets.get("period=ot&period=ft", {}) # gross
                selections = main_period.get("selections", [])
                
                over_under_main_period = over_under.get("period=ot&period=ft", {})
                selections_over_under = over_under_main_period.get("selections", [])
                # test_price = selections_over_under.get("price", "N/A")
                # print(over_under_main_period)
                # print(test_price)
                home_odds = "N/A"
                away_odds = "N/A"
                
                # Find home and away odds
                for selection in selections:
                    outcome = selection.get("outcome", "Unknown")
                    price = selection.get("price", "N/A")
                    if outcome == "home":
                        home_odds = price
                    elif outcome == "away":
                        away_odds = price
                
                # Write it
                writer.writerow([game_name, home_team, away_team, cutoff_time, home_odds, away_odds])
        
        print(f"Data has been saved to {filename}")
    else:
        print(f"Error fetching data. HTTP Status Code: {response.status_code}")
        print(response.text)
        
# Prints out today's moneyline odds. Almost identical to the above function
def fetch_nba_moneyline_odds():
    params = {"markets": "basketball.moneyline"}
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }

    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        events = data.get("events", [])
        
        if not events:
            print("No NBA moneyline odds available.")
            return
        
        print("NBA Moneyline Odds:\n")
        for event in events:
            game_name = event.get("name", "Unknown")
            cutoff_time = event.get("cutoffTime", "Unknown")
            home_team = event.get("home", {}).get("name", "Unknown") if event.get("home") else "Unknown"
            away_team = event.get("away", {}).get("name", "Unknown") if event.get("away") else "Unknown"
            markets = event.get("markets", {}).get("basketball.moneyline", {}).get("submarkets", {})
            
            main_period = markets.get("period=ot&period=ft", {})
            selections = main_period.get("selections", [])
            if(game_name != "Unknown" and home_team != "Unknown"): # Here we check for the other entries that are not moneyline and ignore them
                print(f"Game: {game_name}")
                print(f"  Home Team: {home_team}")
                print(f"  Away Team: {away_team}")
                print(f"  Cutoff Time: {cutoff_time}")
                print("  Odds:")
            
            if selections:
                for selection in selections:
                    outcome = selection.get("outcome", "Unknown")
                    price = selection.get("price", "N/A")
                    team = "Home" if outcome == "home" else "Away" if outcome == "away" else "Unknown"
                    print(f"    {team}: {price}")
                print("\n" + "-" * 40 + "\n")
    else:
        print(f"Error fetching data. HTTP Status Code: {response.status_code}")
        print(response.text)

def print_nested(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print("  " * indent + f"{key}:")
            print_nested(value, indent + 1)
    elif isinstance(data, list):
        for i, value in enumerate(data):
            print("  " * indent + f"[{i}]:")
            print_nested(value, indent + 1)
    else:
        print("  " * indent + str(data))



# fetch_nba_moneyline_odds()
fetch_nba_moneyline_odds_csv()