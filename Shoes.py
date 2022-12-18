import pandas as pd
import matplotlib.pyplot as plt

shoes = pd.read_csv("Shoes.csv")
print("show the 'shoes' file")
print(shoes)

print(shoes.shape)

colors = []

# Iterate over rows of shoes
# This 'for' call does a check with each row in the 'shoes' DataFrame
# When running it reads the 'Brand' column of each row and assigns the given color based on what is read
# When the 'for' is executing: Row 1, read the column labeled "Brand", what have been assigned for the given result?
# based on the reading result, the color assigned will be shown for this particular piece of data when the data is
# being visualized
for lab, row in shoes.iterrows():
    if row['Brand'] == "Jordan":
        colors.append("red")
    elif row['Brand'] == "Nike":
        colors.append("orange")
    else:
        colors.append("black")

index_shoes = shoes.set_index(["Colorway", "Model"]).sort_index()
print(index_shoes)

shoe_priced = shoes.set_index("Colorway").sort_index()
print(shoe_priced)

print(shoes.groupby("Model")["Purchase Price"].cumsum())

shoe_priced.plot(kind="bar")
plt.show()

# Create a scatter plot of duration versus release_year
plt.scatter(shoes['Model'], shoes['Purchase Price'], c=colors)

# Create a title and axis labels
plt.title("Shoe Model v Purchase Price")
plt.xlabel("Model")
plt.ylabel("Purchase Price")

# Show the plot
plt.show()
