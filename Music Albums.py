import pandas as pd
import matplotlib.pyplot as plt

albums = pd.read_csv("Music Albums.csv")
print("Original imported CSV file as a DataFrame:")
print(albums)

show_only = "Let's only show "
see = "Let's see "

print(see + "the 'albums' DataFrame indexed by 'Artist' and 'Album':")
albums_sort = albums.set_index(["Artist", "Album"])
print(albums_sort)

reset = albums_sort.reset_index()
print("\nReset the index to the original setting:")
print(reset)

kanye_kendrick_loc = albums_sort.loc[["Kanye West", "Kendrick Lamar"]]
print(show_only + "Kendrick Lamar and Kanye West albums:")
print(kanye_kendrick_loc)

print(see + "the length of each album as the index:")
length_index = albums.set_index(["# of Songs", "Album"]).sort_index()
print(length_index)

print(show_only + "albums that are the deluxe version in the library:")
deluxe = albums[albums["Deluxe Version"] == "Y"]
print(deluxe)

artist_album_date = albums_sort.loc[:, "Release Date"]
print(show_only + "the current index along with the release date column:")
print(artist_album_date)

albums_sort["15 Songs+"] = albums_sort["# of Songs"] >= 15
print(see + "the DataFrame updated with the new column")
print(albums_sort)

sort_15 = albums_sort.loc[:, "# of Songs": "15 Songs+"]
print(show_only + "the current index along with the columns from '# of Songs' to '15 Songs+':")
print(sort_15)

longest = pd.read_csv("album_longest.csv")
print(longest)

print(see + "the artists sorted together by name and show their album with the most songs on it using booleans:")
j_cole = albums[albums["Artist"] == "J. Cole"]
print(j_cole)
j_cole_length = j_cole.sort_values("# of Songs", ascending=False)
j_cole_longest = j_cole_length.iloc[0]
print(j_cole_longest)

kendrick = albums[albums["Artist"] == "Kendrick Lamar"]
print(kendrick)
kendrick_length = kendrick.sort_values("# of Songs", ascending=False)
kendrick_longest = kendrick_length.iloc[0]
print(kendrick_longest)

kanye = albums[albums["Artist"] == "Kanye West"]
print(kanye)
kanye_length = kanye.sort_values("# of Songs", ascending=False)
kanye_longest = kanye_length.iloc[0]
print(kanye_longest)

busta = albums[albums["Artist"] == "Busta Rhymes"]
print(busta)
busta_length = busta.sort_values("# of Songs", ascending=False)
busta_longest = busta_length.iloc[0]
print(busta_longest)

print(see + "a list of the longest albums from each artist in a list below:")
longest_album_each = [j_cole_longest, kendrick_longest, kanye_longest, busta_longest]
print(longest_album_each)

longest_album_tog = albums.groupby("Artist")["# of Songs"].max()
print(longest_album_tog)

print(see + "the DataFrame with the release dates and album names as the index")
dates = albums.set_index(["Release Date", "Album"])
print(dates)

# Slicing a time series using a boolean call, dataframe is not indexed or sorted
albums_date_bool = albums[(albums["Release Date"] >= "2010-01-01") & (albums["Release Date"] <= "2019-12-31")]
print(albums_date_bool)

# Set date as the index and sort the index
albums_release = albums.set_index("Release Date").sort_index()

print("Use .loc[] to show the albums released in the years 2016 and 2017")
print(albums_release.loc["2016":"2017"])

print("Use .loc[] to subset temperatures_ind for rows from Sep 2010 to Jan 2018")
print(albums_release.loc["2010-09":"2018-01", "Artist":"Album"])

print("Now let's use a bar plot to show the 'albums_release' info.")
albums_release_plot = albums_release.groupby("Album")["Artist"].max()
print(albums_release_plot)

albums_release["# of Songs"].hist()
plt.show()
