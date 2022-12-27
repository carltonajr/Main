import pandas as pd
import matplotlib.pyplot as plt

shows = pd.read_csv("YFBP all eps.csv")
# this prints the first 5 rows from the dataset
print(shows.head())

# now show the entire dataset
print(shows)

print(shows["Views"].max())

# splitting the dataset in two using .loc
front_half_shows = shows.loc[shows["Episode"] >= 45]
back_half_shows = shows.loc[shows["Episode"] <= 46]
print("____________________\n", front_half_shows, "\n", "\n____________________\n",
      back_half_shows)
views = shows.set_index("Views").sort_index()

all_views = shows[["Views"]].cumsum()
print("\nHow many views in total did YFBP get from the episodes collectively?\n", all_views)
print("Total ", all_views.iloc[-1])

long_ep = shows.set_index(["Length(mins)", "Title"]).sort_index(ascending=False)
print(long_ep)

long_ep_views = long_ep.groupby("Length(mins)")["Views"].agg([min, max])
print(long_ep_views)

best_eps = shows[shows['Views'] >= 2000]
print(best_eps)

ep_sets_totals = shows.groupby("Ep Set")["Views"].cumsum()
print("Ep Sets:", ep_sets_totals)

colors, sizes = [], []
# Iterate over rows of shows
for lab, row in shows.iterrows():
    if row['Views'] >= 2000:
        colors.append("gold")
        sizes.append(350)

    elif 1999 < row['Views'] >= 1700:
        colors.append("blue")
        sizes.append(300)

    elif 1699 < row['Views'] >= 1400:
        colors.append("green")
        sizes.append(250)
    else:
        colors.append("red")
        sizes.append(200)

plt.style.use('Solarize_Light2')
plt.scatter(shows["Title"], shows["Length(mins)"], c=colors, edgecolor="black", s=sizes, marker="*")
plt.xlabel("Title")
plt.xticks(rotation=90)
plt.tick_params(left=False, bottom=False)
plt.ylabel("Length of Episode")
plt.title("YFBP Episode Titles by Total Length of Episode")
plt.show()


