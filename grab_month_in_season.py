import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
# import webbrowser
# Should you want to view the webpage being used.
from bs4 import BeautifulSoup
import requests
from IPython.display import display
from time import time
started = time()
# Show all the columns in the dataframes below
pd.set_option('display.max_columns', None)
# list of the months games are played 
months = ['october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june']
# create a numpy array to match the count of months, will be used as an indexer
season_range = np.arange(0, 9)
# create a dictionary from with the months list and matching numpy array
season_dict = {key: months[key] for key in season_range}
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
        display('The month selected: {}, {}'.format(input_key, season_dict[input_key]))
        return season_dict[input_key]  # Return the matching key-value pair
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

# Get the URL for the selected month by prompting the user to input a number
selected_month_url = create_url(season_search_by_key(input("num: ")))

# Run a GET request to retrieve the raw HTML data from the selected month's URL
raw_data = run_get_request(selected_month_url)
# Display the retrieved raw HTML data
display(raw_data)

# Extract game dates from the raw data using specified tag and class
game_dates = find_dates(raw_data, 'th', 'left')
# Remove duplicate dates and reset the index for a cleaner DataFrame
games_dates_cleaned = game_dates.drop_duplicates().reset_index().drop("index", axis=1)
# Display the cleaned DataFrame containing unique game dates
display(games_dates_cleaned)

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
display(cleaned_columns)

# Extract the main data for the new DataFrame using the cleaned column names
data_for_new_df = create_data_as_list(raw_data)
# Display the extracted data as a list
display(data_for_new_df)


finished = time()
# Calculate the total time elapsed between the start and finish times
tot_time = (finished - started)

# Print the formatted start time in hours, minutes, and seconds
print("Started running at {}".format(
    str(int(((started % 3600) / 120))) + ":" +  # Calculate and format the hours part
    str(int((started % 3600) / 60)) + ":" +    # Calculate and format the minutes part
    str(int((started % 3600) % 60))            # Calculate and format the seconds part
))

# Print the formatted finish time in hours, minutes, and seconds
print("Finished running at {}".format(
    str(int(((finished % 3600) / 120))) + ":" +  # Calculate and format the hours part
    str(int((finished % 3600) / 60)) + ":" +     # Calculate and format the minutes part
    str(int((finished % 3600) % 60))             # Calculate and format the seconds part
))

# Print the total elapsed runtime formatted in hours, minutes, and seconds
print("\n** Total Elapsed Runtime:", 
    str(int((tot_time / 3600))) + ":" +          # Calculate and format the total hours part
    str(int((tot_time % 3600) / 60)) + ":" +     # Calculate and format the total minutes part
    str(int((tot_time % 3600) % 60))             # Calculate and format the total seconds part
)

