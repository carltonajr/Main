# Import module
from tkinter import *
import pandas as pd
import numpy as np

run = True


years = np.arange(2028, 2044)


while run:
    # Create object
    root = Tk()

    # Adjust size
    root.geometry("500x450")

    # Change the label text
    def show():
        global run
        label.config(text=clicked.get())
        label.pack()
        year = int(clicked.get())
        data_path = f"{year}"
        info_path = ""
        root.destroy()
        info = pd.read_csv(info_path)
        season = pd.read_csv(data_path, index_col='season')
        season_info = pd.DataFrame(info[info.season == year])
        print(season)
        all_nba = int(season_info['1st-all-nba'].iloc[0] +
                      season_info['2nd-all-nba'].iloc[0] +
                      season_info['3rd-all-nba'].iloc[0])

        pd.set_option('display.max_columns', None)
        if season_info['won_finals'].iloc[0] == 'y':
            opps = season_info['opponent'].iloc[0]

            print(f"Talons won the {year} NBA Championship against {opps}!")
        else:
            print(f"Talons did not win the {year} NBA Championship.")
        print(f"They had {all_nba} player(s) on the 3 All NBA Teams.")
        print(season_info)
        run = False
        return

    # datatype of menu text
    clicked = StringVar()

    # initial menu text
    clicked.set("Choose Below")

    # Create Dropdown menu
    drop = OptionMenu(root, clicked, *years)
    drop.pack()

    # Create Label
    label = Label(root, text=" ")

    # Create button, it will change label text
    Button(root, text="View Season Data", command=show).pack()
    # Execute tkinter
    root.mainloop()
    break
