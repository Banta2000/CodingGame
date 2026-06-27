# myInput = input()
myInput = "rizzo succo formaggio"


# Assuming e_Prices and i_Prices are given as strings of numbers separated by spaces
e_Prices = "100 200 300"
i_Prices = "50 100 150"

# Convert the string of prices into lists of integers
export_prices = list(map(int, e_Prices.split()))
import_prices = list(map(int, i_Prices.split()))

# Calculate the sum of export and import prices
sum_export = sum(export_prices)
sum_import = sum(import_prices)

# Calculate terms of trade as a percentage
terms_of_trade = (sum_export / sum_import) * 100

# Round down to the nearest integer
terms_of_trade = int(terms_of_trade)

print(terms_of_trade)
