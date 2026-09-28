import pandas as pd

data = pd.read_csv(
    r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\dataset\property_data.csv"
)

print("Dataset loaded successfully!")

print("\nNumber of rows:", len(data))
print("Number of columns:", len(data.columns))

print("\nColumn names:")
print(data.columns.tolist())

print("\nFirst 5 records:")
print(data.head())