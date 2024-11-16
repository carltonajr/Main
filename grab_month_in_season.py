# Reads a txt file that has a  script for each month.

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
# import webbrowser
# Should you want to view the webpage being used.
from bs4 import BeautifulSoup
import requests
from IPython.display import display
from time import time
from datetime import timedelta, datetime

started = time()


def files_in_folder(folder_path):
    # define 'files' as a global variable for use outside the function
    global files
    # change the backslashes to forward slashes in the folder path
    folder_path = folder_path.replace('"', '').replace(r"\\", r"/")
    # A 'try:' statement is used to handle exceptions and errors that might occur within
    # its block
    try:
        # Select the files as a list from the folder given by the path
        files = os.listdir(folder_path)

        # Filter out files specifically not other directories using a single line for loop
        files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]

        # Now count the number of files selected by way of 'len()' to see how long the list is
        num_of_files = len(files)
        # Finding the file names 'if' the list length is greater than 0
        display(f"Files found:{num_of_files} in {folder_path}\n")
        # Print files found
        display("Files located:")
        # For loop to iterate over each element in the list
        for name in files:
            # Print the name of the file found
            display(name)
        # Else statement that changes 'files' to a dataframe for folders with more than 15 files
        else:
            # Original  message
            display(f"Files found:{num_of_files} in {folder_path}\n")
            # Turn 'files' into a dataframe with 'num_of_files' as the index column
            files = pd.DataFrame({num_of_files: files})
            # Rename column with file names to 'file_name'
            files.columns = ['file_name']
            # print the 1st five rows of the dataframe 'files'
            display(files)
    # Use an 'except' to give a result of an error message that no files were found
    except FileNotFoundError:
        # Print the message
        display(f"No files found in {folder_path}")


# Show all the columns in the dataframes below
pd.set_option('display.max_columns', None)
# list of the months games are played
months = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']
calendar_month = [10, 11, 12, 1, 2, 3, 4, 5, 6]
# create a numpy array to match the count of months, will be used as an indexer
season_range = np.arange(0, 9)
# create a dictionary from with the months list and matching numpy array
season_dict = {key: months[key] for key in season_range}
months_dict = {key: calendar_month [key] for key in season_range}
print('Please enter a value to select a month from the season:\n{}'.format(season_dict))


# function that runs the get request for the webpage based on the month selected.
def run_get_request(url):
    # website = webbrowser.open(url)
    # Should you want to view the webpage being used.
    # url is created with function 'create_url', get request and save as 'page'
    page = requests.get(url)
    # parse the selected page with an HTML parser from BeautifulSoup
    soup = BeautifulSoup(page.text, 'html.parser')
    # create a place for the found information, searched for by table
    dataset = soup.find('div', class_='table_wrapper')
    # returns the collected info
    return dataset


# Define a function that creates a URL based on the month provided
def create_url(month_value):
    # Display a message indicating which month's link is being created, with the month value capitalized
    display(f'Creating a link for the month of {month_value.capitalize()}')

    # Construct the URL using the provided month value, formatted in lowercase for consistency in the link
    url = f'https://www.basketball-reference.com/leagues/NBA_2023_games-{month_value.lower()}.html'

    # Display a clickable message showing the constructed URL and indicating the month and season it refers to
    display(f'Click to go  {url},' f' showing the month of {month_value.capitalize()} of the 2022-23 NBA Season')

    # Return the constructed URL for further use
    return url


def season_search_by_key(input_key):
    # message to show what was input into the function call
    display('{} was input.'.format(input_key))
    # change input_key to integer as the key values are integer values in a numpy array
    input_key = int(input_key)
    # Check if the provided input_key exists in season_dict
    if input_key in list(season_dict.keys()):
        display('The month selected: {}, {}, {}'.format(input_key, season_dict[input_key], calendar_month[input_key]))
        return [input_key, season_dict[input_key], calendar_month[input_key]]  # Return the matching key-value pair
    else:
        raise ValueError("Input not found in range given.")


# Define a function to find specific dates from the provided HTML data
def find_dates(data, lookfor1, lookfor2):
    # Find all elements with the specified tag (lookfor1) and class (lookfor2) in the data
    new_dates = data.find_all(lookfor1, class_=lookfor2)
    # Extract the text content of each date found and store it in a DataFrame
    df = pd.DataFrame([date.text for date in new_dates])
    # Split the date text into 'weekday', 'date', and 'year' columns using the comma as a separator
    df = df[0].str.split(',', expand=True)
    # Define column names for better readability
    date_columns = ['weekday', 'date', 'year']
    # Set the column names in the DataFrame
    df.columns = date_columns
    # Return the formatted DataFrame containing the date information
    return df


# Define a function to extract data from a dataset as a list
def create_data_as_list(dataset):
    # Find all table data ('td') elements in the dataset
    new_data = dataset.find_all('td')
    # Extract the text content of each 'td' element
    new_data = [data.text for data in new_data]
    # Convert the extracted data into a list
    new_data_as_list = list(new_data)
    # Return the list of extracted data
    return new_data_as_list


# Define a function to extract and clean column names from the provided data
def column_names(data):
    # Create a DataFrame containing the text of each title element found in the data
    df = pd.DataFrame([title.text for title in data])
    # Split the text content into individual strings, using newlines as separators
    df = df[0].str.split('\n', expand=True)
    # Extract the first row and convert the column names to lowercase
    list_names = list(df.iloc[0].str.lower())
    # Return the list of cleaned column names
    return list_names


def create_df(value, num_of_elements):
    num_rows = len(value) // num_of_elements
    rows = []
    for i in range(num_rows):
        row = value[i * num_of_elements: (i + 1) * num_of_elements]
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


def update_column_names(df, column, new_name):
    df.rename(columns={column: new_name}, inplace=True)
    return df


def change_data_type(df, column, new_type):
    df[column] = df[column].astype(new_type)
    return df


# Get the URL for the selected month by prompting the user to input a number
selected_month = season_search_by_key(input("num: "))
print(selected_month)

selected_month_url = create_url(selected_month[1])

# Run a GET request to retrieve the raw HTML data from the selected month's URL
raw_data = run_get_request(selected_month_url)
# Display the retrieved raw HTML data
display(raw_data)

# Extract game dates from the raw data using specified tag and class
game_dates = find_dates(raw_data, 'th', 'left')
# Remove duplicate dates and reset the index for a cleaner DataFrame
game_dates_cleaned = game_dates.drop_duplicates().reset_index().drop("index", axis=1)
# Display the cleaned DataFrame containing unique game dates
display(game_dates_cleaned)

# Find the header elements in the raw data to use as column names
headers = raw_data.find_all('thead')

# Extract and display the column names using the headers
columns = column_names(headers)
display(columns)

# Define a list of unwanted column names for cleaning purposes
clean_the_column_names = ['\xa0', 'notes', '', 'date']
# Filter out the unwanted column names and keep the cleaned list of column names
cleaned_columns = list(filter(lambda x: x not in clean_the_column_names, columns))
# Display the final list of cleaned column names
cleaned_columns[2] = 'away_pts'
cleaned_columns[4] = 'home_pts'

# Extract the main data for the new DataFrame using the cleaned column names
data_for_new_df = create_data_as_list(raw_data)
# Display the extracted data as a list
display(len(data_for_new_df))

values_to_remove = ['', 'Box Score', 'OT', '2OT', '3OT']
data_for_new_df = list(filter(lambda x: x not in values_to_remove, data_for_new_df))
display(len(data_for_new_df))


standard_data = create_df(data_for_new_df, 8)
standard_data.columns = cleaned_columns
standard_data['start (et)'] = standard_data['start (et)'].str.replace('p', '', regex=False)
# standard_data['24hr start'] = pd.to_datetime(standard_data['start (et)'], format='%I:%M %p')
display(standard_data.head(25))

display("All times are Eastern Standard Time.")
game_dates['len. of game'] = standard_data['log']
game_dates['start_time'] = standard_data['start (et)']
game_dates = change_data_type(game_dates, 'weekday', 'string')
game_dates = change_data_type(game_dates, 'date', 'string')
game_dates = change_data_type(game_dates, 'year', 'int')
game_dates = change_data_type(game_dates, 'len. of game', 'string')
print(game_dates.dtypes)


month = execute()
files_in_folder("folder path")
new_csv = pd.read_csv("new file path")
print(new_csv.tail())


def create_date_time(df):
    class DateOfGame:
        def __init__(self, day, month, year, hour, minute):
            self.day = day
            self.month = month
            self.year = year
            self.hour = hour
            self.minute = minute

    dates = []
    # %Y-%m-%dT%H:%M:%S
    for lab, row in df.iterrows():
        date_split = row['date'].split(' ')
        start_time_split = row['start (et)'].split(':')
        hour, minutes = int(start_time_split[0]) + 12, int(start_time_split[1])
        date_num = int(date_split[2])
        select_day = DateOfGame(date_num, month[2], row['year'], hour, minutes)
        as_datetime = datetime(select_day.year, select_day.month, select_day.day, select_day.hour,
                               select_day.minute)
        dates.append(as_datetime.isoformat())
    iso_dates = pd.DataFrame(dates)
    print(iso_dates)
    return iso_dates


new_csv['calendar_info'] = create_date_time(new_csv)
print(new_csv.tail())
print(new_csv.info())
breakpoint()
# new_csv.to_csv("newdata_insertmonth.csv")


finished = time()
# Calculate the total time elapsed between the start and finish times
tot_time = (finished - started)

# Print the formatted start time in hours, minutes, and seconds
print("Started running at {}".format(
    str(int(((started % 3600) / 120))) + ":" +  # Calculate and format the hours part
    str(int((started % 3600) / 60)) + ":" +  # Calculate and format the minutes part
    str(int((started % 3600) % 60))  # Calculate and format the seconds part
))

# Print the formatted finish time in hours, minutes, and seconds
print("Finished running at {}".format(
    str(int(((finished % 3600) / 120))) + ":" +  # Calculate and format the hours part
    str(int((finished % 3600) / 60)) + ":" +  # Calculate and format the minutes part
    str(int((finished % 3600) % 60))  # Calculate and format the seconds part
))

# Print the total elapsed runtime formatted in hours, minutes, and seconds
print("\n** Total Elapsed Runtime:",
      str(int((tot_time / 3600))) + ":" +  # Calculate and format the total hours part
      str(int((tot_time % 3600) / 60)) + ":" +  # Calculate and format the total minutes part
      str(int((tot_time % 3600) % 60))  # Calculate and format the total seconds part
      )
