import sqlite3
import pandas as pd
import os


def to_datetime(dataset, column):
    dataset[column] = dataset[column].astype('string')
    dataset[column] = pd.to_datetime(dataset[column])
    return dataset


path = input("Please enter CSV file name or path: ").replace('"', '').replace(r"\\", r"/")
data = pd.read_csv(path)
game_id = []


def get_game_id():
    global game_id
    data.columns = data.columns.str.lower()
    data.columns = data.columns.str.replace(" ", "_")
    data.columns = data.columns.str.replace("/", "_")
    for i in data.index:
        game_id.append(f"s28_g{i}")

    return game_id


data.index = get_game_id()
print(f"Columns for the new table:\n{list(data.columns)}")
file_name = input("Please enter database file name to save as: ")
db_name = f"{file_name}.db"
print(f"Searching for file named {db_name}, will create a new one if not found.")


def sqlite_connection_create_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS game_info
                  (game_id, opponent, home_away, talons_score, opp_score)''')
    cursor.close()
    conn.close()


files = None


def files_in_folder():
    # define 'files' as a global variable for use outside the function
    global files
    folder_path = ''
    # Select the files as a list from the folder given by the path
    files = os.listdir(folder_path)

    # Filter out files specifically not other directories using a single line for loop
    files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]

    # Now count the number of files selected by way of 'len()' to see how long the list is
    num_of_files = len(files)
    print(f"Files found:{num_of_files} in {folder_path}\n")
    # For loop to iterate over each element in the list
    # Turn 'files' into a dataframe with 'num_of_files' as the index column
    files = pd.DataFrame({num_of_files: files})
    # Rename column with file names to 'file_name'
    files.columns = ['file_name']
    files_list = files
    file_type = r".db$"
    results = files_list[files_list['file_name'].str.contains(file_type, case=True, regex=True)]
    if len(results) == 0:
        raise ValueError("Did not find any '.db' files.")
    else:
        print(f"{len(results)} database files were found")
    return results


database_files = files_in_folder()


def file_select(value):
    while True:
        if value == 1:
            value = db_name
        results = database_files[database_files["file_name"].str.contains(value, case=False)]
        if len(value) == 0:
            print(results)
            value = input("no search value entered, please enter one the available options (Case Sensitive):\n")
        elif len(results) == 0:
            results = f"No files found with {value}"
        elif len(results) == 1:
            return results
        else:
            print(results)
            value = input("Found more than one file, please enter one the available options(Case Sensitive):\n")


pd.set_option('display.max_columns', None)

print(sqlite_connection_create_table())

search_results = file_select(input("Select a file (Case Sensitive)\n[To select the newly created file enter 1]\n:"))

connected_database_file = search_results['file_name'].astype('string')
print(connected_database_file)

#     cursor.execute('''SELECT * FROM game_info''')
#
#     rows = cursor.fetchall()
#     fetched = []
#     for row in pd.DataFrame(rows):
#         print(row)
#         fetched.append(row)
