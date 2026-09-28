import pandas as pd
import random

random.seed(42)

data = []

for i in range(200):
    plot_area = random.randint(700, 4000)
    building_height = random.randint(10, 80)
    road_width = random.randint(6, 20)
    location_score = random.randint(1, 5)

    # Calculate sample authorized floors
    floors = min(
        int(building_height / 10),
        int(road_width / 3) + location_score
    )

    floors = max(1, min(floors, 8))

    data.append([
        plot_area,
        building_height,
        road_width,
        location_score,
        floors
    ])

df = pd.DataFrame(
    data,
    columns=[
        "plot_area",
        "building_height",
        "road_width",
        "location_score",
        "floors"
    ]
)

df.to_csv(
    r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\dataset\property_data.csv",
    index=False
)

print("Dataset created successfully!")
print("Number of records:", len(df))
print("\nFirst 10 records:")
print(df.head(10))