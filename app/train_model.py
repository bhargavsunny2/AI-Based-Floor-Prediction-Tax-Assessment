import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv(
    r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\dataset\property_data.csv"
)

# Input features
X = data[
    [
        "plot_area",
        "building_height",
        "road_width",
        "location_score"
    ]
]

# Target
y = data["floors"]

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model trained successfully!")
print("Accuracy:", round(accuracy * 100, 2), "%")

# Save model
joblib.dump(
    model,
    r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\model\floor_prediction_model.pkl"
)

print("Model saved successfully!")