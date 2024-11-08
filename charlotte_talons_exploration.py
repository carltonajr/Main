# Impport necessary libraries and options
import numpy as np
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# Define preferences for plotting later on
talons_color = '#87D5FF'
opps_color = '#FF3E00'
plt.figure(figsize=(15, 6))

data_years = np.arange(2028, 2043)
for i in  data_years:
    path = f'/kaggle/input/2035-season/Charlotte Talons {i} Season.csv'
    print(i)

# All of the functions to be used are stored below, along with its purpose.

# -new_dataframe - Create new dataframe

# -scoring_results - Scoring difference

# -game_win_loss - Win / Loss

# -team_conference - Opp Conference

# -team_division - Opp Division

# -rival_opps - Rivalry?

# -new_year_data - New data for dataset

# -load_data_csv - Load the CSV file

# -fix_columns - Update column names

# -choose_year - Choose a season from 'available_years' to select the data from that season

def new_dataframe(values, values2):
    """Use concatenation to merge uploaded data.
    
    Args:
        values: 1st Dataset
        values_2: Data to be merged
    
    Returns:
        Full dataset with new data added.
    """
    dataset = pd.concat([values, values2])
    return dataset


def scoring_results(values, values_2):
    """Calculate the point spread from each game through subtracting
    opponent scores from the team scores

    Args:
        values: Team score value
        values_2: opponent score value

    Returns:
        Difference of the 2 values, stored in a DataFrame"""
    point_spread = values - values_2
    return pd.DataFrame(point_spread)



def game_win_loss(values):
    """Assign win or loss based on the value

        Args:
            values: value to determine win or loss

        Returns:
            string 'win' or 'loss' """
    result = ['win' if diff > 0 else 'loss' for diff in values]
    return result

def team_conference(values):
    """Assign 'Conference' value for each team based on if the team name is
    saved in 'eastern_conference'

        Args:
            values: Team name value to be searched for in 'eastern-conference'

        Returns:
            Conference name to then add to the dataset, 'eastern' or 'western'"""
    eastern_conference = ('BAL Barons|BKN Nets|BOS Celtics|NY Knicks|PHI 76ers|WAS Wizards'
                          '|CHI Bulls|CLE Cavaliers|DET Pistons|IND Pacers|NAS Stars|TOR Raptors'
                          '|ATL Hawks|CHA Hornets|MIA Heat|ORL Magic|VIR Storm')
    conference = ['eastern' if opp in eastern_conference else 'western' for opp in values]
    return conference


def team_division(values):
    """Assign 'Division' value for each team based on which division the team name is stored'

        Args:
        
        values: Team name value to be searched for in each 'division'

        Returns:
            Division name to then add to the dataset"""
    atlantic_div = 'BAL Barons|BKN Nets|BOS Celtics|NY Knicks|PHI 76ers|WAS Wizards'
    central_div = 'CHI Bulls|CLE Cavaliers|DET Pistons|IND Pacers|NAS Stars|TOR Raptors'
    southeast_div = 'ATL Hawks|CHA Hornets|MIA Heat|ORL Magic|VIR Storm'
    pacific_div = 'GS Warriors|LA Clippers|LA Lakers|PHX Suns|SAC Kings|UTA Jazz'
    northwest_div = 'DEN Nuggets|KC Knights|MIL Bucks|MIN Timberwolves|POR Blazers|STL Sound'
    southwest_div = 'DAL Mavericks|HOU Rockets|MEM Grizzlies|NOLA Pelicans|OKC Thunder|SAN Spurs'
    league_divisions = ['atlantic', 'central', 'southeast', 'pacific', 'northwest', 'southwest']
    division = [
        (values.str.contains(atlantic_div)),
        (values.str.contains(central_div)),
        (values.str.contains(southeast_div)),
        (values.str.contains(pacific_div)),
        (values.str.contains(northwest_div)),
        (values.str.contains(southwest_div))
    ]
    team = np.select(division, league_divisions, default='Other')
    return team

def rival_opps(team):
    """Assign 'Division' value for each team based on which division the team name is stored'

    Args:
        values (str): Team name value to be searched for in the 'rivals' string

    Returns:
        Whether the opponent is a rival team"""
    rivals = 'CHA Hornets|ORL Magic|ATL Hawks|NY Knicks|DAL Mavericks|GS Warriors'
    rival_teams = ['Y' if opp in rivals else 'N' for opp in team]
    return rival_teams




def fix_columns(df):
    """Alters column names to make them easier to use
    
    Args:
        df (DataFrame): name of the variable the dataframe is saved as
    
    Returns:
        Lowercase column names with no '_' in place for spaces and slashes. 
    """
    for col in df.columns:
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.replace('/', '_')
    return df

    
def upload_max_data():
    """Function that streamlines uploading the next season played in the dataset
        Args:
            path (str): The location of the file.

        Returns:
            DataFrame matching the format of the existing data, allowing for easy concatenation
        """
    holdinglist = []
    for i in data_years:
        path = f'/kaggle/input/2035-season/Charlotte Talons {i} Season.csv'
        upload = pd.read_csv(path, index_col='Game')
        
        upload['season'] = i
        upload['score_diff'] = upload['Talons Score'] - upload['OPP Score']
        upload['result'] = game_win_loss(upload['score_diff'])
        upload['conference'] = team_conference(upload['Opponent'])
        upload['division'] = team_division(upload['Opponent'])
        upload['rivalry'] = rival_opps(upload['Opponent'])
        holdinglist.append(upload)
    
    all_seasons = pd.concat(holdinglist, ignore_index=True)

    return all_seasons


all_data = upload_max_data()
print(all_data.tail())


print(all_data.season.value_counts())
print(all_data.info())
all_data = fix_columns(all_data)

# Clean it Up & Show it Off
# 
# With **all_data** defined, display the points per game spread by **'opponent'** and **'division'** they play in.
# Plot with a scatter plot for both the talons scoring and opponent scoring.

ppg = pd.DataFrame(all_data.groupby(['opponent'])[['talons_score', 'opp_score']].mean().round(3))
print(ppg)


talons_color = '#87D5FF'
opps_color = '#FF3E00'
plt.figure(figsize=(15, 6))
sns.set_style('whitegrid')
plt.xticks(rotation=75)
sns.scatterplot(data=ppg, x='opponent', y='talons_score', color='#87D5FF')
sns.scatterplot(data=ppg, x='opponent', y='opp_score', color='#FF3E00')
plt.title(f'Points Per Game Spread for Each Team in all_data')
plt.show()


sns.catplot(data=all_data, x='season', y='talons_score',hue='season', col='division', palette='dark',native_scale=True)
plt.show()

all_data['stand_dev_talons'] = all_data.groupby('opponent')['talons_score'].transform(lambda x: x.std())

unique_stand_devs = pd.DataFrame(all_data[['opponent','stand_dev_talons']].drop_duplicates(inplace=False)).reset_index()
unique_stand_devs['std_rank'] = unique_stand_devs.sort_values('stand_dev_talons', ascending=False).reset_index().index + 1
unique_stand_devs = unique_stand_devs.set_index('std_rank')
unique_stand_devs_top_10 = unique_stand_devs[unique_stand_devs.index <= 10]

print(unique_stand_devs_top_10)

plt.figure(figsize=(15, 6))
sns.set_style('whitegrid')
plt.xticks(rotation=90)
sns.barplot(data=unique_stand_devs, x='opponent', y='stand_dev_talons')
plt.show()


game_end = []
for lab, row in all_data.iterrows():
    if row['result'] == 'win' and row['score_diff'] > 10:
        game_end.append('big win')

    elif row['result'] == 'win' and row['score_diff'] <= 3:
        game_end.append('one_score win')
    
    elif row['result'] == 'loss':
        game_end.append('Loss')

    else:
        game_end.append("win")
        

all_data['game_ending'] = game_end
print(all_data.value_counts('result'))

# all_data.to_csv('all_data_data.csv')
