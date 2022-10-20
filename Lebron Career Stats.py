import matplotlib.pyplot as plt
import pandas as pd

# import the needed datasets and place them into DataFrames
# 'cle' shows the statistics for his tenure on the Cleveland Cavaliers
# 'mia' for the Miami Heat
# 'lal' for the Los Angeles Lakers, where he plays now
# using 'index_col=0' specifies the column that will be placed as the index
# for each DataFrame, which is the 'Year' column for each
# This will be put to use later in this exercise
cle = pd.read_csv("CLE Only - LebronJamesCareerStats.csv")
mia = pd.read_csv("MIA Only - LebronJamesCareerStats.csv")
lal = pd.read_csv("LAL Only - LebronJamesCareerStats.csv")

for_merge_suffixes = ("_cle", "_mia")

cle_mia_lal = cle.merge(mia, on=["Year"], suffixes=for_merge_suffixes).merge(lal, on="Year")
# all_teams_sorted =
print(cle_mia_lal.groupby("Team").agg({'PTS': 'sum'}))
# Print each of the newly set DataFrames, I chose to split them up with '__' lines
# Specify each called variable as a string, it will recognize you are instructing display the text in ""
# along with the given info for each variable.
# print(str(cle),
#      '\n____________________\n\n' + str(mia),
#      '\n____________________\n\n' + str(lal))
# short_seasons = 1, 2, 3, 4
# cle_seasons = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
# all_years = cle.iloc[:, 0], mia.iloc[:, 0], lal.iloc[:, 0]
# print(all_years)

# Theoretical merge

# cle_mia_lal = pd.merge(cle, mia)
# print(cle_mia_lal)


# ridership_cal_stations = ridership.merge(cal, on=['year','month','day']) \
# .merge(stations, on='station_id')
# plt.plot(cle_seasons, cle["PTS"], color="gold")
# plt.plot(short_seasons, mia["PTS"], color="black")
# plt.plot(short_seasons, lal["PTS"], color="purple")
# plt.show()
# all_stats = pd.merge(cle, mia)
# print(all_stats)

