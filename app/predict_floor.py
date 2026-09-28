import joblib

# Load the trained model
model = joblib.load(
    r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\model\floor_prediction_model.pkl"
)

# New property details
plot_area = 2500
building_height = 45
road_width = 12
location_score = 4

# Predict number of floors
prediction = model.predict([[
    plot_area,
    building_height,
    road_width,
    location_score
]])

print("NEW PROPERTY")
print("--------------------")
print("Plot Area:", plot_area, "sq.ft")
print("Building Height:", building_height, "m")
print("Road Width:", road_width, "m")
print("Location Score:", location_score)

print("\nPredicted Floors:", prediction[0])