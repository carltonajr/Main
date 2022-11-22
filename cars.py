import pandas as pd
import matplotlib.pyplot as plt

cars = pd.read_csv("10_cars.csv")
print(cars)
pd.set_option('display.max_columns', None)

rank_sort = cars.set_index("Rank").sort_index()
print(rank_sort)

reset = cars.reset_index()
print("\nReset the index to the original setting:")
print(reset)

car_type = cars[["Type", "Model"]].sort_values("Type")
print(car_type)

print(cars['Type'].value_counts())

cars["Avg Market Price"] = [80000, 92000, 150000, 75000, 95000, 65000, 14500, 40000, 400000, 12000]
print(cars)

plt.scatter(cars["Model"], cars["Avg Market Price"])
plt.xlabel("Car Model")
plt.ylabel("Avg Market Price")
plt.xticks(rotation=90)
plt.title("My Top 10 Cars Up for Purchase")
plt.show()
