import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'
spacer = "\n_________________________________________________________________________\n"

all_coaching = pd.read_csv("Coach Prime Coaching.csv")
print(all_coaching.head(), spacer)

all_coaching["Margin"] = all_coaching['Team Score'] - all_coaching['Opp Score']
print(all_coaching, spacer)

result_all = []
for lab, row in all_coaching.iterrows():
    if row['Margin'] > 0:
        result_all.append("W")

    elif row['Margin'] < 0:
        result_all.append('L')

    else:
        result_all.append("Result Unavailable")

all_coaching["Result"] = result_all
print(all_coaching, spacer)

all_coaching_record = all_coaching.groupby("Result").agg({"Result": "count"})
print("As of 12/2022, Coach Prime's overall record is\n", all_coaching_record, spacer)

season_2020 = all_coaching.loc[all_coaching["Season"] == 2020]
season_2020_record = season_2020.groupby("Result").agg({"Result": "count"})
print("2020 Season\n", season_2020, "\nWin-Loss", season_2020_record, spacer)

season_2021 = all_coaching.loc[all_coaching["Season"] == 2021]
season_2021_record = season_2021.groupby("Result").agg({"Result": "count"})
print("2021 Season\n", season_2021, "\nWin-Loss", season_2021_record, spacer)

season_2022 = all_coaching.loc[all_coaching["Season"] == 2022]
season_2022_record = season_2022.groupby("Result").agg({"Result": "count"})
print("2022 Season\n", season_2022, "\nWin-Loss", season_2022_record, spacer)

all_coaching_record_teams = all_coaching.groupby(["Opponent", "Result"]).agg({"Result": "count"})
print(all_coaching_record_teams)
