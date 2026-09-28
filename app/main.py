import joblib


# Load the trained ML model
model = joblib.load(
    r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\model\floor_prediction_model.pkl"
)


# Tax calculation function
def calculate_tax(plot_area, floors, location_score):

    base_rate = 10

    floor_factor = 1 + (floors - 1) * 0.15

    location_factor = 1 + (location_score - 1) * 0.10

    tax = plot_area * base_rate * floor_factor * location_factor

    return round(tax, 2)


# Property information
plot_area = 2500
building_height = 45
road_width = 12
location_score = 4


# Predict floors
prediction = model.predict([[
    plot_area,
    building_height,
    road_width,
    location_score
]])

floors = int(prediction[0])


# Calculate tax
tax = calculate_tax(
    plot_area,
    floors,
    location_score
)


# Display final result
print("===================================")
print(" AI FLOOR & TAX ASSESSMENT SYSTEM")
print("===================================")

print("\nPROPERTY DETAILS")
print("----------------")
print("Plot Area:", plot_area, "sq.ft")
print("Building Height:", building_height, "m")
print("Road Width:", road_width, "m")
print("Location Score:", location_score)

print("\nASSESSMENT RESULT")
print("-----------------")
print("Predicted Floors:", floors)
print("Estimated Property Tax: ₹", tax)

print("\nAssessment completed successfully!")