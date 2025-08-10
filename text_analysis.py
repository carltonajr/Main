from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


songs = pd.read_csv("kendrick_songs.csv", index_col='year')
songs = songs.fillna("no feature")


sample = songs.sample(n=3, replace=False)
songs_select = []
reviews = []


def populate():
    for i in sample['title']:
        songs_select.append(i)
        print(f"Song Name: {i}\nPaste lyrics here: ")
        song_lyrics = input("""""")
        if len(song_lyrics) < 1:
            continue
        reviews.append(song_lyrics)


populate()
breakpoint()
# Analyze sentiment
polarities = []
for review in reviews:
    blob = TextBlob(review)
    polarity = blob.sentiment.polarity
    polarities.append(polarity)
    print(f"Review: {review}\nPolarity Score: {polarity}\n")

# Visualization
plt.figure(figsize=(10, 5))
plt.bar(songs_select, polarities, color='skyblue')
plt.axhline(0, color='black', linestyle='--')
plt.title("Sentiment Polarity of Movie Reviews")
plt.xlabel("Review Index")
plt.ylabel("Polarity (-1 = negative, 1 = positive)")

plt.show()
