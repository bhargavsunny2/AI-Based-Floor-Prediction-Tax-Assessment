def calculate_tax(plot_area, floors, location_score):

    base_rate = 10

    floor_factor = 1 + (floors - 1) * 0.15

    location_factor = 1 + (location_score - 1) * 0.10

    tax = plot_area * base_rate * floor_factor * location_factor

    return round(tax, 2)


# Example property
plot_area = 2500
floors = 4
location_score = 4

tax = calculate_tax(
    plot_area,
    floors,
    location_score
)

print("PROPERTY TAX ASSESSMENT")
print("------------------------")
print("Plot Area:", plot_area, "sq.ft")
print("Floors:", floors)
print("Location Score:", location_score)

print("\nEstimated Property Tax: ₹", tax)