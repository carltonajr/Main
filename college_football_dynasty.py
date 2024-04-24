import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import numpy as np
from IPython.display import display
# **Please note there is a 3 year -hiatus- due to changing gaming systems**
# *Conferences accurate as of 2012 NCAA Football Season*


def find_rivals(df, column):
    rivals = df[column].value_counts()
    big_rivals = {}
    for opponent, count in rivals.items():
        if count >= 3:
            big_rivals.update({opponent: count})
    return big_rivals


def count_values_sort(data, column):
    return data[column].value_counts().sort_index()


def change_for_machine_learning(df):
    for column in df.columns:
        if df.loc[:, column].dtype != int:
            df.loc[:, column] = df[column].astype('category')
        for column in df.columns:
            if df[column].dtype == 'category':
                df.loc[:, column] = df[column].cat.codes
    return df


def get_result(df, column):
    result = []
    for lab, row in df.iterrows():
        if row[column] > 0:
            result.append("W")
        elif row[column] < 0:
            result.append('L')
        else:
            raise ValueError("Game score could not be interpreted.")
    df['Win/Loss'] = result
    return df


def update_rankings(df, column):
    top_25_rank = []
    for lab, row in df.iterrows():
        if row[column] == '-':
            top_25_rank.append(0)
        else:
            top_25_rank.append(row[column])
    return pd.DataFrame({'Opp Rank': top_25_rank})


def offensive_style_ran(df, column, new_column):
    one_back_offense_years = '2008|2009|2012'
    spread_offense_years = '2013|2014|2015'

    offense_style = ['one_back', 'spread']
    find_offense_style = [
        (df[column].apply(lambda x: any(year in x for year in one_back_offense_years.split('|')))),
        (df[column].apply(lambda x: any(year in x for year in spread_offense_years.split('|'))))
    ]

    df.loc[:, new_column] = np.select(find_offense_style, offense_style, default='Unavailable')
    return df


# Read the desired Excel file and save it under 'stats'
stats = pd.read_excel("Simple Stats - NCAA Football Game Dynasty.xlsx")
display(stats)

stats['Opp Rank'] = update_rankings(stats, 'Opp Rank')
display(stats.tail(10))

display(count_values_sort(update_rankings(stats, 'Opp Rank'), 'Opp Rank'))

stats = get_result(stats, 'Final Margin')
display(stats.tail())

display(count_values_sort(stats, 'Season'))
display(count_values_sort(stats, 'Conference'))

display(count_values_sort(stats, ['Ranked Opp?', 'Conference']))

info = stats[["Season", "Opponent", "Conference", "Opp Rank", "Traveled Distance (mi)",
              "Home Team", "Stadium Capacity", "Time of Season"]]
season_play = stats[["Opponent", "Home Team", "Stadium Capacity", "F Player Score",
                     "F Opp Score", "Time of Season"]]
stats_calculations = stats[["Season", "Opponent", "Conference", "H Player Score", "F Player Score",
                            "H Opp Score", "F Opp Score", "Half Margin", "Final Margin"]]

# prediction_target
y = stats['Stadium Capacity']

# prediction_features
X = stats.drop('Stadium Capacity', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

train_data = X_train.join(y_train)

train_data.sample(5, replace=False)

display(train_data[train_data['Time of Season'] == 'Bowl Season'])

plt.figure(figsize=(15, 10))
sns.scatterplot(x='Traveled Distance (mi)', y='Stadium Capacity', data=train_data, hue='Conference', palette='coolwarm')

display(train_data.corr(numeric_only=True))

conference_dummies = pd.get_dummies(train_data['Conference'])
conference_dummies = pd.DataFrame(conference_dummies)
display(conference_dummies)

train_data = pd.concat([train_data, conference_dummies] , axis=1)
display(train_data.head())

display(change_for_machine_learning(train_data))

# Create a dataframe containing each of the teams coached
# This gives us something for the function to look over.
home_teams = ["Jackson State", "Kansas", "Maryland"]

# Now, we want to calculate how many home and away games coached.
# 1st create variables for each game type
home_games, away_games = 0, 0

# Then we use a for loop to search through the "Home Team" column for matches to the values in 'home_teams'
# If the value matches add 1 to 'home_games', otherwise add 1 to 'away_games'
for index, row in info.iterrows():
    if pd.Series(home_teams).isin([row["Home Team"]]).any():
        home_games += 1
    else:
        away_games += 1


# this gives us the total amount of games coached
all_games = len(info)
home_game_percentage = ((home_games / all_games) * 100).__round__(2)
away_game_percentage = ((away_games / all_games) * 100).__round__(2)
home_away = (f"Since starting coaching at: {home_teams} of {all_games} games coached;"
             f"A total of {home_games} games {home_game_percentage}% were coached at home versus "
             f"{away_games} away or neutral site games {away_game_percentage}% of the time. "
             f"(Including Bowl Season and Championship Weekends).\n")
display(home_away)

win_count, loss_count = 0, 0

for lab, row in stats_calculations.iterrows():
    if row['Final Margin'] > 0:
        win_count += 1
    else:
        loss_count += 1
percent_win_loss = (win_count / all_games) * 100
win_loss = (f"With {all_games} games coached, the overall coaching record is: "
            f"{win_count} wins - {loss_count} losses and a win percentage of {percent_win_loss}%")
display(win_loss)

match_up = find_rivals(stats, "Opponent")
selected_big_rivals = stats_calculations[stats_calculations['Opponent'].isin(match_up.keys())]
display(selected_big_rivals)

# How many PPG do the teams score and give up based on what conference their opponent is in?
conference_avg = stats_calculations.groupby('Conference')[['F Player Score', 'F Opp Score']].mean().round(1)
display(conference_avg)

# How many PPG do the teams score and give up based on what part of the season
time_of_season_avg = season_play.groupby('Time of Season')[['F Player Score', 'F Opp Score']].mean().round(2)
display(time_of_season_avg)


# Use pandas 'set_option' to display all the columns in the subsequent dataframes
pd.set_option('display.max_columns', None)

travel_ranked_opps = pd.DataFrame(info[info['Opp Rank']  != 0]
                                  [['Traveled Distance (mi)', 'Opponent', 'Opp Rank']])
display(travel_ranked_opps['Opponent'].value_counts().sort_values())

coached_team_conference = ["FCS", "BIG 12", "BIG TEN"]
conferences_prob = (stats_calculations['Conference'].value_counts() / stats_calculations['Conference'].value_counts().sum()) * 100
display(conferences_prob)

# Calculate how many opponents are specifically power 5 conference teams
# We can use a similar formula from the home games/ away games for loop with a few tweaks
power_5_conferences = ["ACC", "BIG TEN", "BIG 12", "PAC-12", "SEC"]
power_5_opponents, non_power_5 = 0, 0
avg_power_5_opp = []
for index, row in info.iterrows():
    if pd.Series(power_5_conferences).isin([row["Conference"]]).any():
        power_5_opponents += 1
        avg_power_5_opp.append(row)
    else:
        non_power_5 += 1

prob_of_power_5 = power_5_opponents / all_games
rounded_prob_of_power_5 = round(prob_of_power_5, 3) * 100
display(rounded_prob_of_power_5)

big_3 = ["BIG TEN", "BIG 12", "SEC"]
big_3_opponents = 0
for index, row in info.iterrows():
    if pd.Series(big_3).isin([row["Conference"]]).any():
        big_3_opponents += 1

prob_of_big_3 = big_3_opponents / all_games
rounded_prob_of_big_3 = round(prob_of_big_3, 3)
big_3_power_5 = big_3_opponents / power_5_opponents
rounded_big_3_power_5 = round(big_3_power_5, 3)
display(rounded_big_3_power_5 * 100)

halftime_correlation = stats_calculations['H Player Score'].corr(stats_calculations['Half Margin'])
final_correlation = stats_calculations['F Player Score'].corr(stats_calculations['Final Margin'])
halftime_final_correlation = stats_calculations['Half Margin'].corr(stats_calculations['Final Margin'])
opp_correlation_half = stats_calculations['H Opp Score'].corr(stats_calculations['Half Margin'])
opp_correlation_final = stats_calculations['F Opp Score'].corr(stats_calculations['Final Margin'])
correlations = [halftime_correlation, final_correlation, halftime_final_correlation, opp_correlation_half]
display(correlations)

one_score_half = stats_calculations[stats_calculations['Half Margin'] <= 3]
blowouts = stats_calculations[stats_calculations['Final Margin'] >= 35]
one_score_games = stats_calculations[stats_calculations["Final Margin"] <= 3]
power_5_blowouts = blowouts[blowouts["Conference"].isin(coached_team_conference)]

sns.catplot(x='Season', y='H Player Score', data=stats_calculations, hue='Conference', kind='bar')
plt.show()

stats_calculations.loc[:, 'Season'] = stats_calculations['Season'].astype('string')

stats_calculations = offensive_style_ran(stats_calculations, 'Season', 'offensive_style')
display(stats_calculations.tail())

high_scoring_outputs = stats_calculations[['F Player Score', 'Opponent', 'Conference', 'Final Margin']]\
    .sort_values(['F Player Score'], ascending=False)

points_56_plus = high_scoring_outputs[high_scoring_outputs['F Player Score'] >= 56]
display(points_56_plus)

display(points_56_plus["Conference"].value_counts())

display(points_56_plus[["F Player Score", "Final Margin"]].mean().round(2))

points_28_less = high_scoring_outputs[high_scoring_outputs['F Player Score'] <= 28]
display(points_28_less)

display(points_28_less[["F Player Score", "Final Margin"]].mean().round(2))

display(points_28_less["Conference"].value_counts())


bowl_season = season_play[season_play["Time of Season"] == "Bowl Season"]
display(bowl_season['Time of Season'].count())

display(bowl_season['Home Team'].unique())

bowl_season_ppg = bowl_season[["F Player Score", "F Opp Score"]].mean().round(2)
display(bowl_season_ppg)

bowl_season_crowd_size = bowl_season[["Stadium Capacity"]].mean()
display(bowl_season_crowd_size.astype('int'))

stadium_sizes = season_play[["Opponent", "Stadium Capacity", "F Player Score", "F Opp Score", 'Home Team']]\
    .set_index('Stadium Capacity').sort_index(ascending=False)
display(stadium_sizes)

avg_scoring_by_stadiums = stadium_sizes.groupby(['Stadium Capacity', 'Home Team'])[['F Player Score', 'F Opp Score']]\
    .mean().round(2)
display(avg_scoring_by_stadiums)

stadiums_100k = stadium_sizes[stadium_sizes.index >= 100000].drop('Home Team', axis=1)
display(stadiums_100k[['F Player Score', 'F Opp Score']].mean().round(2))

avg_stadium_size = stadium_sizes.reset_index()
display(avg_stadium_size[["Stadium Capacity"]].mean().round().astype('int'))


cheap_tix, mid_tix, expensive_tix = 25, 85, 150
ticket_price_breakdown = {"Nosebleed Tickets": cheap_tix, "Mid-Level Tickets": mid_tix,
                          "Lower Level Tickets": expensive_tix}
display(ticket_price_breakdown)

tix_nose, tix_mid, tix_up_close = [], [], []

for lab, row in info.iterrows():
    if row["Home Team"] == "National Championship":
        tix_nose.append(cheap_tix * 15)
        tix_mid.append(mid_tix * 6)
        tix_up_close.append(expensive_tix * 8)
    elif row["Time of Season"] != "Regular Season":
        tix_nose.append(cheap_tix * 4)
        tix_mid.append(mid_tix * 4)
        tix_up_close.append(expensive_tix * 4)
    elif row["Conference"] == "SEC" or row["Conference"] == "BIG TEN" or row["Conference"] == "BIG 12":
       tix_nose.append(cheap_tix * 3)
       tix_mid.append(mid_tix * 3)
       tix_up_close.append(expensive_tix * 3)

    elif row["Conference"] == "ACC" or row["Conference"] == "PAC-12":
        tix_nose.append(cheap_tix * 2)
        tix_mid.append(mid_tix * 2)
        tix_up_close.append(expensive_tix * 2)
    else:
        tix_nose.append(cheap_tix)
        tix_mid.append(mid_tix)
        tix_up_close.append(expensive_tix)

info = info.loc[:, 'Nosebleed Pricing'] == tix_nose
info = info.loc[:, 'Mid-Level Pricing'] == tix_mid
info = info.loc[:, 'Lower Level Pricing'] == tix_up_close

display(info['Lower Level Pricing'].value_counts())

ticket_pricing = info[["Season", "Opponent", "Conference", "Stadium Capacity", "Time of Season",
                       "Nosebleed Pricing", "Mid-Level Pricing", "Lower Level Pricing"]]
# stadium_breakdown = ticket_pricing.drop(["Home Team", "Time of Season"], axis=1)
# Let's say all stadium had a standard breakdown of 20/30/50 seating arrangements
# print(divider, ticket_pricing.head(), divider)
nose_seating = (ticket_pricing["Stadium Capacity"] * .50).astype(int)
mid_level_seating = (ticket_pricing["Stadium Capacity"] * .30).astype(int)
lower_level_seating = (ticket_pricing["Stadium Capacity"] * .20).astype(int)
# pd.set_option('display.max_rows', None)
ticket_pricing["Nosebleed Seats Count"] = nose_seating
ticket_pricing["Mid-Level Seats Count"] = mid_level_seating
ticket_pricing["Lower Level Seats Count"] = lower_level_seating

games_tickets_gross = ticket_pricing[["Season", "Conference", "Opponent", "Stadium Capacity", "Time of Season"]]
games_tickets_gross["Nosebleeds Gross"] = (ticket_pricing["Nosebleed Seats Count"] * ticket_pricing["Nosebleed Seating"])
games_tickets_gross["Mid-Level Gross"] = (ticket_pricing["Mid-Level Seats Count"] * ticket_pricing["Mid-Level Seating"])
games_tickets_gross["Lower Level Gross"] = (ticket_pricing["Lower Level Seats Count"] * ticket_pricing["Lower Level Seating"])
# print(games_tickets_gross.tail(), games_tickets_gross.sort_values("Stadium Capacity"), sep="\n\n")

avg_tickets_gross_conference = games_tickets_gross.groupby(["Conference", "Season"])\
[["Nosebleeds Gross", "Mid-Level Gross", "Lower Level Gross"]].mean().sort_values("Conference")
# print(avg_tickets_gross_conference.sort_values("Conference"))

total_avg_tickets_gross = games_tickets_gross.groupby(["Season", "Conference"])\
    [["Nosebleeds Gross", "Mid-Level Gross", "Lower Level Gross"]].sum().mean(axis=1)
# print(total_avg_tickets_gross)

games_tickets_gross_100k = games_tickets_gross[games_tickets_gross["Stadium Capacity"] >= 100000]
total_avg_tickets_gross_100k = games_tickets_gross_100k.groupby\
    (["Season", "Conference"])[["Nosebleeds Gross", "Mid-Level Gross", "Lower Level Gross"]]\
    .sum().mean(axis=1).astype(int)
# print(games_tickets_gross_100k, total_avg_tickets_gross_100k, sep="\n\n\n")

total_avg_tickets_gross_millions = (total_avg_tickets_gross / 1000000).round(2)
# print(total_avg_tickets_gross_millions)

post_season_tickets = games_tickets_gross[games_tickets_gross["Time of Season"] != "Reg Season"]
avg_post_season_tickets = post_season_tickets.groupby("Time of Season")\
    [["Nosebleeds Gross", "Mid-Level Gross", "Lower Level Gross"]].sum().mean(axis=1).astype(int)
post_season_avg_tickets_gross_millions = (avg_post_season_tickets / 1000000).round(2)
# print(post_season_avg_tickets_gross_millions, avg_post_season_tickets, sep="\n\n\n")

post_season_avg_tickets_conference = post_season_tickets.groupby(["Conference"])\
[["Nosebleeds Gross", "Mid-Level Gross", "Lower Level Gross"]].mean().sort_values("Conference").astype(int)
post_season_counts = post_season_tickets["Time of Season"].value_counts().sort_values(ascending=False)
# print(post_season_avg_tickets_conference)

# print(type(avg_post_season_tickets))
avg_post_season_tickets = pd.DataFrame(avg_post_season_tickets)

bowl_season_ticket_numbers = avg_post_season_tickets.iloc[0, 0]
post_season_ticket_numbers = avg_post_season_tickets.iloc[1, 0]

bowl_vs_post_percent = ((bowl_season_ticket_numbers / post_season_ticket_numbers) * 100).round(3)
bowl_vs_post = f"Post Season and Bowl Season Games played:\n{post_season_counts}"
# print(bowl_vs_post)

unique_opps = info["Opponent"].unique()
unique_opps_count = info["Opponent"].nunique()
