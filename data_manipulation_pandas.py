import pandas as pd
import matplotlib.pyplot as plt

# Importing a CSV
movies = pd.read_csv("Test_CSV.csv")
print(movies.head())

vet_visits = pd.read_csv("vet_visits_datacamp_course.csv")
print(vet_visits)


# Dropping Duplicate Names
no_duplicate = vet_visits.drop_duplicates(subset="name")
print("Show the 'vet_visits' DataFrame without duplicate names:")
print(no_duplicate)

# Dropping Duplicate Pairs
no_duplicate_pairs = vet_visits.drop_duplicates(subset=["name", "breed"])
print("Show the 'vet_visits' DataFrame without duplicate names and breeds:")
print(no_duplicate_pairs)

print("Group Summary Calculations using '.groupby()'")
vet_group1 = vet_visits.groupby("breed")["weight_kg"].agg([min, max, sum])
print(vet_group1)

# Proportions of a column
vet_prop = vet_visits["breed"].value_counts(normalize=True)
print("What is the proportion of each dog breed in the DataFrame?")
print(vet_prop)

# Explicit Indexes
print("\nSet the index to the 'name' column:")
vet_index = vet_visits.set_index("name")
print(vet_index)
reset = vet_index.reset_index()
print("\nReset the index to the original setting:")
print(reset)

vet_index_loc = vet_index.loc[["Max", "Stella"]]
print(vet_index_loc)

print("\nSet the index to the 'breed' column:")
vet_index2 = vet_visits.set_index("breed")
print(vet_index2)
reset2 = vet_index2.reset_index()
print("\nReset the index to the original setting:")
print(reset2)
vet_index_loc2 = vet_index2.loc[["Chow Chow", "Chihuahua"]]
print(vet_index_loc2)

# Pivot Tables
vet_visits_pivot = vet_visits.pivot_table(values="weight_kg", index="breed", columns="color")
print(vet_visits_pivot)

chow_to_poodle = vet_visits_pivot.loc["Chow Chow": "Poodle"]
print(chow_to_poodle)

print(vet_visits_pivot.mean(axis="index"))

print(vet_visits_pivot.mean(axis="columns"))

vet_visits.hist(bins=10, legend="breed")
plt.show()

chow_chow = vet_index2.loc[["Chow Chow"]]
print(chow_chow)

chow_chow.plot(x="name",
               y="weight_kg",
               kind="line")
plt.show()

chow_chow.plot(x="name", y="weight_kg", kind="scatter")
plt.show()

avg_weight_by_breed = vet_visits.groupby("breed")["weight_kg"].mean()
print(avg_weight_by_breed)

avg_weight_by_breed.plot(kind="line")
plt.show()

# Functions


def square():

    new_value = 4**2
    print(new_value)


square()