# Imports
import pandas as pd
import numpy as np
import os
import time

# new function
def new_season_ingestion():
    # variable to hold the opponent names for verification while inserting new data
    opponents = pd.read_csv(f"Insert path Opponents.csv")
  
    # Update the values to strings
    opponents['Opponent'] = opponents['Opponent'].astype('string')
  
    # Split the team names
    # Example: 
    # 'BOS Celtics'
    # 'BOS' 'Celtics' 
    change_team_names = opponents['Opponent'].str.split(' ', expand=True)
  
    # Rename columns and make 'change_team_names' a dataframe
    change_team_names.columns = ['opp_id', 'opp_name']
    change_team_names = pd.DataFrame(change_team_names)
    # Empty list for new row inputs
    new_row = []
  
    # Empty dataframe to store new inputs before adding to the existing data
    new_season = pd.DataFrame()
  
    # Columns for 'new_season'
    columns = ['season', 'game', 'opp_id', 'opp_name', 'home_away', 'talons_score', 'opp_score']

    # Grab CSV file with existing data
    data_path = f"Insert path for the season you are adding to.csv"
  
    # Grab time stamp and display the last time the file was updated
    modification_time = os.path.getmtime(data_path)
    print(f"This dataset was last updated: {time.ctime(modification_time)}")

    # Load data to 'current_data'
    current_data = pd.read_csv(data_path)

    # last_game grabs the last line in the loaded dataframe 'current_data'
    last_game = current_data.tail(1)
  
    # grab which game of the season 'last_game' is
    last_game_num = current_data['game'].iloc[-1]
  
    # next_game for the team
    next_game = last_game_num + 1

    # Print the previous game making it easier to find the next game up.
    print(last_game)
    print(last_game_num)
  
    # display how many games are left in the regular season
    remaining = 82 - last_game_num
    print(f"Games remaining: {remaining}")

    while True:
        # If the amount of games to be added is more than 82 (the games in the regular season)
        # do not advance
        games = int(input("How many games are you inputting? "))
        game_index = np.arange(next_game, games + next_game)
        if game_index[-1] > 82 or games > 82:
            print(f"Based on number of games being added, the season will be {game_index[-1]} games\n"
                  f"which is longer than 82 games.\nPlease adjust the amount of games being added.")
        else:
            print(f"Last game to be input: {game_index[-1]}")
            break
    
    # for loop to input values that make up 'new_row' for the amount of times requested
    for i in game_index:
        # which game you are inputting.
        print(f"Game {i}")
        
        # Input the opponent faced 
        opponent = input("Opponent Abbreviation: ").upper()

        # Use 'search' to match up the input with the correct opponent mascot
        # from when the team names were split
        def search(value):
            results = change_team_names[change_team_names['opp_id'].str.contains(value, case=False)]
            name_results = list(results['opp_name'])
            if len(results) == 0:
                name_results = "Did not find anything with that title."
            return name_results

        # Search and select the found value
        opp_name = search(opponent)
        opp_name = opp_name[0]

        # Input whether the game was at home or away
        # do not advance if the input does not match 'home' or 'away'
        while True:
            home = "H"
            away = "A"
            home_away = input("Input H for Home game / A for Away: ").upper()
            if home_away == home or home_away == away:
                break
            else:
                print("Invalid input. Please enter H for Home game or A for Away game.")

        # Input the team score then the opponents score
        # do not advance if the inputs match are or too large/ too small
        while True:
            print("Paladins Score: ")
            talons_score = int(input())
            print("Opponent Score: ")
            opp_score = int(input())
            if opp_score == talons_score:
                print("Opponent score cannot be the same oas the Talons Score")
            elif 300 > talons_score > 1 and 300 > opp_score > 1:
                break
            else:
                print("Invalid final scores. Please input scores for each team.")

        # Complete a new row input and append it to the empty datafrane to populate.
        new_row.append([2019, i, opponent, opp_name, home_away, talons_score, opp_score])
        new_season = pd.DataFrame(new_row, columns=columns)

    # Return populated dataset that needs to be added to existing dataset
    return new_season

# Variable for the newly input data for a quick view before committing
update_data = new_season_ingestion()
print(update_data)

# Confirm the season you are adding to is correct  
year = int(input("Please confirm the the year:"))

# path to existing data
path = f"Insert path {year}.csv"

# Read, concatenate together, and save to the file name to finish update.
data = pd.read_csv(path)
data = pd.concat([data, update_data])
data.to_csv(path, index=False)

# Print the last time the file was updated and preview the updated data to confirm the changes.
updated_time = os.path.getmtime(path)
print(f"Insert path {year}.csv: {time.ctime(updated_time)}")
save_correctly = pd.read_csv(path, index_col='season')
print(save_correctly.tail())
