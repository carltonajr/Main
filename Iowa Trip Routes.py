import pandas as pd
import matplotlib.pyplot as plt

print("We are planning to drive from Charlotte, North Carolina to Fairfield, Iowa. "
      "\nWe have narrowed the GPS directions to 2 options. "
      "\nOne going North then West, hitting Indianapolis, Indiana. "
      "\nThe other route starts out West then swings North passing through Nashville, Tennessee.")
print("-What is the shorter route to Fairfield, Iowa, based on the two routes given?\n\n")

print("-Let's Look at the Route Info Going Through Indianapolis, Indiana-")
# 1st lets use the imported 'pandas' to import our data in the file "Through_Indianapolis.csv"
indianapolis = pd.read_csv("Iowa Trip Files/Through_Indianapolis.csv")
# We can also import the Nashville route data, but we'll focus on Indianapolis for now
nashville = pd.read_csv("Iowa Trip Files/Through_Nashville.csv")
# Not a necessary step but I print the '.head()' of the newly imported information,
# which is stored in a DataFrame upon pandas 'reading' the CSV file path given.
print(indianapolis.head())
# Now since we know the information came through correctly, I'll go ahead and show the entire dataset
print(indianapolis)
# lol not much extra for this particular file ;)

# One thing that is helpful is being able to see the every column in the DataFrame
# lets display all the available columns to see everything we are working with
pd.set_option('display.max_columns', None)
print(indianapolis)

# now that can see everything, how about some math
# To see which is the shorter route we are going to tally up the 2 major stats that can answer our question
# from above, Distance and Time, and we can place this equation into the variable 'indianapolis_distance'
# To accomplish this, we can select the 2 columns we want to add and send it through a 'cumsum()' call
# This cumulatively adds the values in each row from top to bottom, at the end provides the cumulative sum for
# each column
indianapolis_distance = indianapolis[["Distance(mi)", "Time(hrs)"]].cumsum()

# A  simple 'print()' call can confirm if our code is working properly
# Because I added text to print out along with retrieving the 'indianapolis_distance' variable, you have to specify
# that 'indianapolis_distance' is classified as a string. Otherwise, an error will occur
print("-The total expected time and distance driven when going through Indianapolis:\n" + str(indianapolis_distance))

# Now that we have completed the process of finding an endpoint for the Indianapolis data
# we can start to experiment with different ways of visualizing our findings.
# For the time being, we'll use the regular 'plt.plot' which defaults to a line plot
# As for the x and y of the graph, we will refer to 2 different DataFrames we created earlier
# the x: the "Leaving" column of 'indianapolis'
# the y: the "Distance(mi)" column of 'indianapolis_distance'
plt.plot(indianapolis["Leaving"], indianapolis_distance["Distance(mi)"])
plt.title("Indianapolis Route Graphed")
# Make sure you use 'plt.show()' for the plot you put together to actually show
plt.show()

# Now that we have Indianapolis in a good space, let's circle back and do the same to the Nashville DataFrame
# Remember we already imported Nashville so all we have to do down here is put the data into action
pd.set_option('display.max_columns', None)
print(nashville)

nashville_distance = nashville[["Distance(mi)", "Time(hrs)"]].cumsum()
print("-The total expected time and distance driven when going through Nashville:\n" + str(nashville_distance))

plt.plot(nashville["Leaving"], nashville_distance["Distance(mi)"])
plt.title("Nashville Route Graphed")
plt.show()
# We now have calculated the total distance and total time expected for both routes
# Are we able to see both together?
# Certainly we can use a '.merge' to combine the 2 DataFrames into one
# This allows us to see all of our imported information in one place; 'suffixes' gives the ability to distinguish
# which columns go with which DataFrame
# Another thing to keep in mind, merging 2 DataFrames combines them at the 'on' call. But what every is
# put placed in the " on='' " has to be the index of both DataFrames, or it will not work.
print("\n-Cumulative Distance and Time going through Indianapolis:\n" + str(indianapolis_distance),
      "\n__________\n",
      "\n-Cumulative Distance and Time going through Nashville:\n" + str(nashville_distance))

nashville_indianapolis = pd.merge(indianapolis_distance, nashville_distance, left_index=True, right_index=True)
print(nashville_indianapolis)

# The moment we have done all this work for up to this point. We are about to answer our initial question.
# We can do this by comparing the data we have pulled from each plot separately on the same graph.
# Reminder when plotting 2 graphs together one of the 2 variables have to be the same
# We'll plot the total distance in a scatter plot
days = (1, 2, 3, 4, 5, 6)
plt.scatter(days, nashville_indianapolis["Distance(mi)_x"])
plt.scatter(days, nashville_indianapolis["Distance(mi)_y"])
plt.title("Indianapolis Route v Nashville Route: Distance in miles")
plt.xlabel("Driving Day")
plt.ylabel("Distance(mi)")
plt.show()

# For the hours graph, we'll use a line plot
plt.plot(days, nashville_indianapolis["Time(hrs)_x"])
plt.plot(days, nashville_indianapolis["Time(hrs)_y"])
plt.title("Indianapolis Route v Nashville Route: Time in hours")
plt.xlabel("Driving Day")
plt.ylabel("Time(hrs)")
plt.show()

print("\nBased on the data composed in this exercise, the expected shorter route is going through "
      "Indianapolis, Indiana as opposed to going through Nashville, Tennessee")
