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
import json
import firebase_admin
from firebase_admin import credentials, firestore

from datetime import datetime, timezone, timedelta

# grabbing the API key from environment variable
load_dotenv()  
API_KEY = os.getenv("CLOUD_API_KEY")
if not API_KEY:
    raise ValueError("API key is not set in the .env file.")

API_URL = "https://sports-api.cloudbet.com/pub/v2/odds/competitions/basketball-usa-nba" #endpoint


firebase_private_key = os.getenv('FIREBASE_ADMIN_AUTH')
if firebase_private_key is None:
    raise ValueError("Firebase admin private key not found in environment variables.")

cred = credentials.Certificate(json.loads(firebase_private_key))
firebase_admin.initialize_app(cred)
db = firestore.client()

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
        events = data.get("events", [])
        
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
                
                # Check if both home and away teams exist and are valid
                if home_team == "Unknown" or away_team == "Unknown":
                    continue  
                
                # Extract moneyline odds for the main period
                main_period = markets.get("period=ot&period=ft", {}) # gross
                selections = main_period.get("selections", [])
                
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
        
def fetch_nba_moneyline_odds_json():
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
        
        today_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        tomorrow_date = (datetime.now(timezone.utc) + timedelta(days=1)).strftime("%Y-%m-%d")
        today_tomorrow_games = []
        
        for event in events:
            game_name = event.get("name", "Unknown")
            cutoff_time = event.get("cutoffTime", "Unknown")
            home_team = event.get("home", {}).get("name", "Unknown") if event.get("home") else "Unknown"
            away_team = event.get("away", {}).get("name", "Unknown") if event.get("away") else "Unknown"
            markets = event.get("markets", {}).get("basketball.moneyline", {}).get("submarkets", {})
            
            main_period = markets.get("period=ot&period=ft", {})
            selections = main_period.get("selections", [])
            
            home_odds = "N/A"
            away_odds = "N/A"

            if home_team == "Unknown" or away_team == "Unknown":
                    continue  
            
            for selection in selections:
                outcome = selection.get("outcome", "Unknown")
                price = selection.get("price", "N/A")
                if outcome == "home":
                    home_odds = decimal_to_american(price)
                elif outcome == "away":
                    away_odds = decimal_to_american(price)
            
            if cutoff_time.startswith(today_date) or cutoff_time.startswith(tomorrow_date):
                today_tomorrow_games.append({
                    "Game Name": game_name,
                    "Home Team": home_team,
                    "Away Team": away_team,
                    "Cutoff Time": cutoff_time,
                    "Home Odds": home_odds,
                    "Away Odds": away_odds
                })
        
        if today_tomorrow_games:
            filename = f"{today_date}_and_{tomorrow_date}_moneyline.json"
            with open(filename, "w", encoding="utf-8") as json_file:
                json.dump(today_tomorrow_games, json_file, indent=4)
            send_data_to_firebase(today_tomorrow_games, "daily-games-odds")
            print(f"Today's and tomorrow's game data saved to {filename}")
        else:
            print("No games with today's or tomorrow's cutoff time found.")
    else:
        print(f"Error fetching data. HTTP Status Code: {response.status_code}")
        print(response.text)

def send_data_to_firebase(data, collection_name):
    today = datetime.now().strftime("%Y-%m-%d")  
    doc_ref = db.collection(collection_name).document(f"{today}-gameOdds")
    doc_ref.set({"games": data})  


def decimal_to_american(decimal_odds):
    try:
        decimal_odds = float(decimal_odds)  # Ensure it's a float
        if decimal_odds >= 2.0:
            return int(100 * (decimal_odds - 1))
        else:
            return int(-100 / (decimal_odds - 1))
    except (ValueError, TypeError, ZeroDivisionError):
        return "N/A"  # Handle invalid values safely

# fetch_nba_moneyline_odds()
fetch_nba_moneyline_odds_csv()

fetch_nba_moneyline_odds_json()