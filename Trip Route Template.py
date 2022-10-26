import pandas as pd
import matplotlib.pyplot as plt


# """This pair of 'print()' statements will give background info"""
# """as well as pose the question for us to find an answer for."""
print("")
print("")
# """We used days to place hold for the graphs later on"""
# We are planning this trip over X days of driving, not including days spent in a destination
days = (1, 2, 3, 4, 5, 6)

# """1st step to answering our question, getting the data to compute with"""
print("-Let's Look at the Route Info Going Through df_1, Indiana-")

# Let's use the imported 'pandas' to import our data in the file, in this case from a CSV File
df_1 = pd.read_csv("df_2.csv")

# We can also import the df_2 route data, but we'll focus on df_1 for now
df_2 = pd.read_csv("df_2.csv")

# --Not a necessary step but I print the '.head()' of the newly imported information,
# --which is stored in a DataFrame upon pandas 'reading' the CSV file path given.
print(df_1.head())
# Now since we know the information came through correctly, I'll go ahead and show the entire dataset
print(df_1)
# Not much extra for this particular dataset ;)

# One thing that is helpful is being able to see the every column in the DataFrame
# lets display all the available columns to see everything we are working with
pd.set_option('display.max_columns', None)
print(df_1)

# To see which is the shorter route we are going to tally up the 2 major stats that can answer our question
# from above, Distance and Time, and we can place this equation into the variable 'df_1_distance'
# To accomplish this, we can select the 2 columns we want to add and send it through a 'cumsum()' call
# This cumulatively adds the values in each row from top to bottom, at the end provides the cumulative sum for
# each column
df_1_distance = df_1[["Distance(mi)", "Time(hrs)"]].cumsum()

# A  simple 'print()' call can confirm if our code is working properly
# Because I added text to print out along with retrieving the 'df_1_distance' variable, you have to specify
# that 'df_1_distance' is classified as a string. Otherwise, an error will occur
pd.set_option('display.max_columns', None)
print("-The total expected time and distance driven when going through df_1:\n" + str(df_1_distance))

# Now that we have completed the process of finding an endpoint for the df_1 data
# we can start to experiment with different ways of visualizing our findings.
# For the time being, we'll use the regular 'plt.plot' which defaults to a line plot
# As for the x and y of the graph, we will refer to 2 different DataFrames we created earlier
# the x: the "Leaving" column of 'df_1'
# the y: the "Distance(mi)" column of 'df_1_distance'
plt.plot(days, df_1_distance["Distance(mi)"])
# Make sure you use 'plt.show()' for the plot you put together to actually show
# plt.show()

# Now that we have df_1 in a good space, let's circle back and do the same to the df_2 DataFrame
# Remember we already imported df_2 so all we have to do down here is put the data into action
pd.set_option('display.max_columns', None)
print(df_2)

df_2_distance = df_2[["Distance(mi)", "Time(hrs)"]].cumsum()
print("-The total expected time and distance driven when going through df_2:\n" + str(df_2_distance))

plt.plot(days, df_2_distance["Distance(mi)"])
plt.title("df_1 Route v df_2 Route")

# We now have calculated the total distance and total time expected for both routes
# Are we able to see both together?
# Certainly we can use a '.merge' to combine the 2 DataFrames into one
# This allows us to see all of our imported information in one place; 'suffixes' gives the ability to distinguish
# which columns go with which DataFrame
# Another thing to keep in mind, merging 2 DataFrames combines them at the 'on' call. But what every is
# put placed in the " on='' " has to be the index of both DataFrames, or it will not work.
print("\n-Cumulative Distance and Time going through df_1:\n" + str(df_1_distance),
      "\n__________\n",
      "\n-Cumulative Distance and Time going through df_2:\n" + str(df_2_distance))
df_2_df_1 = pd.merge(df_1_distance, df_2_distance, left_index=True, right_index=True, suffixes=('_df_1', '_df_2'))
print(df_2_df_1)

# The moment we have done all this work for up to this point. We are about to answer our initial question.
# We can do this by comparing the data we have pulled from each plot separately on the same graph.
# Reminder when plotting 2 graphs together one of the 2 variables have to be the same
# We'll plot the total distance in a scatter plot

plt.scatter(days, df_2_df_1["Distance(mi)_df_1"])
plt.scatter(days, df_2_df_1["Distance(mi)_df_2"])
plt.title("df_1 Route v df_2 Route: Distance in miles")
plt.xlabel("Driving Days")
plt.ylabel("Distance(mi) Driven")
plt.legend(["df_1 Route", "df_2 Route"])
plt.show()

# For the hours graph, we'll use a line plot
plt.plot(days, df_2_df_1["Time(hrs)_df_1"])
plt.plot(days, df_2_df_1["Time(hrs)_df_2"])
plt.title("df_1 Route v df_2 Route: Time in hours")
plt.xlabel("Driving Day")
plt.ylabel("Time(hrs)")
plt.legend(["df_1 Route", "df_2 Route"])
plt.show()

