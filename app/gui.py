import tkinter as tk
from tkinter import messagebox
import joblib
import sqlite3
import pandas as pd


MODEL_PATH = r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\model\floor_prediction_model.pkl"
DATABASE_PATH = r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\property_assessments.db"


# ==============================
# LOAD MODEL
# ==============================

model = joblib.load(MODEL_PATH)


# ==============================
# DATABASE CONNECTION
# ==============================

def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# ==============================
# TAX CALCULATION
# ==============================

def calculate_tax(plot_area, floors, location_score):

    base_rate = 10

    floor_factor = 1 + (floors - 1) * 0.15

    location_factor = 1 + (location_score - 1) * 0.10

    tax = plot_area * base_rate * floor_factor * location_factor

    return round(tax, 2)


# ==============================
# SAVE ASSESSMENT
# ==============================

def save_assessment(
    plot_area,
    building_height,
    road_width,
    location_score,
    floors,
    tax
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO assessments
        (
            plot_area,
            building_height,
            road_width,
            location_score,
            predicted_floors,
            estimated_tax
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        plot_area,
        building_height,
        road_width,
        location_score,
        floors,
        tax
    ))

    connection.commit()
    connection.close()


# ==============================
# ASSESS PROPERTY
# ==============================

def assess_property():

    try:

        plot_area = float(plot_area_entry.get())
        building_height = float(height_entry.get())
        road_width = float(road_entry.get())
        location_score = int(location_entry.get())

        if plot_area <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Plot area must be greater than 0."
            )
            return

        if building_height <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Building height must be greater than 0."
            )
            return

        if road_width <= 0:
            messagebox.showerror(
                "Invalid Input",
                "Road width must be greater than 0."
            )
            return

        if location_score < 1 or location_score > 5:
            messagebox.showerror(
                "Invalid Input",
                "Location score must be between 1 and 5."
            )
            return

        input_data = pd.DataFrame([{
            "plot_area": plot_area,
            "building_height": building_height,
            "road_width": road_width,
            "location_score": location_score
        }])

        prediction = model.predict(input_data)

        floors = int(prediction[0])

        tax = calculate_tax(
            plot_area,
            floors,
            location_score
        )

        save_assessment(
            plot_area,
            building_height,
            road_width,
            location_score,
            floors,
            tax
        )

        floors_result.config(
            text=f"Predicted Floors: {floors}"
        )

        tax_result.config(
            text=f"Estimated Property Tax: ₹{tax:,.2f}"
        )

        status_result.config(
            text="Assessment completed and saved successfully!"
        )

        update_dashboard()

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numerical values."
        )

    except Exception as error:

        messagebox.showerror(
            "Error",
            str(error)
        )


# ==============================
# CLEAR
# ==============================

def clear_inputs():

    plot_area_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    road_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)

    floors_result.config(
        text="Predicted Floors: -"
    )

    tax_result.config(
        text="Estimated Property Tax: ₹-"
    )

    status_result.config(
        text="Enter property details"
    )


# ==============================
# DASHBOARD UPDATE
# ==============================

def update_dashboard():

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM assessments"
        )

        total = cursor.fetchone()[0]

        cursor.execute(
            "SELECT SUM(estimated_tax) FROM assessments"
        )

        total_tax = cursor.fetchone()[0]

        cursor.execute(
            "SELECT MAX(predicted_floors) FROM assessments"
        )

        max_floors = cursor.fetchone()[0]

        connection.close()

        if total_tax is None:
            total_tax = 0

        if max_floors is None:
            max_floors = 0

        total_result.config(
            text=str(total)
        )

        tax_total_result.config(
            text=f"₹{total_tax:,.2f}"
        )

        floors_total_result.config(
            text=str(max_floors)
        )

    except Exception:
        pass


# ==============================
# HISTORY WINDOW
# ==============================

def view_history():

    history_window = tk.Toplevel(window)

    history_window.title(
        "Assessment History"
    )

    history_window.geometry(
        "950x550"
    )

    title = tk.Label(
        history_window,
        text="PROPERTY ASSESSMENT HISTORY",
        font=("Arial", 18, "bold")
    )

    title.pack(pady=15)

    history_text = tk.Text(
        history_window,
        width=115,
        height=22,
        font=("Courier New", 10)
    )

    history_text.pack(
        padx=10,
        pady=10
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            plot_area,
            building_height,
            road_width,
            location_score,
            predicted_floors,
            estimated_tax
        FROM assessments
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    if not records:

        history_text.insert(
            tk.END,
            "No assessment records found."
        )

    else:

        header = (
            "ID   Plot Area   Height   Road   "
            "Location   Floors   Tax\n"
        )

        history_text.insert(
            tk.END,
            header
        )

        history_text.insert(
            tk.END,
            "-" * 90 + "\n"
        )

        for record in records:

            history_text.insert(
                tk.END,
                f"{record[0]:<4}"
                f"{record[1]:<12.0f}"
                f"{record[2]:<9.1f}"
                f"{record[3]:<7.1f}"
                f"{record[4]:<11}"
                f"{record[5]:<9}"
                f"₹{record[6]:,.2f}\n"
            )

    history_text.config(
        state="disabled"
    )


# ==============================
# MAIN WINDOW
# ==============================

window = tk.Tk()

window.title(
    "AI Floor & Tax Assessment System"
)

window.geometry(
    "720x760"
)

window.resizable(
    False,
    False
)


# ==============================
# HEADER
# ==============================

title = tk.Label(
    window,
    text="AI FLOOR & TAX ASSESSMENT SYSTEM",
    font=("Arial", 22, "bold")
)

title.pack(pady=20)


subtitle = tk.Label(
    window,
    text="Machine Learning Based Property Assessment",
    font=("Arial", 11)
)

subtitle.pack()


# ==============================
# DASHBOARD
# ==============================

dashboard = tk.Frame(
    window
)

dashboard.pack(
    pady=20
)


# Total assessments

box1 = tk.Frame(
    dashboard,
    width=190,
    height=90,
    relief="solid",
    borderwidth=1
)

box1.grid(
    row=0,
    column=0,
    padx=10
)

box1.pack_propagate(False)

tk.Label(
    box1,
    text="TOTAL ASSESSMENTS",
    font=("Arial", 10, "bold")
).pack(pady=8)

total_result = tk.Label(
    box1,
    text="0",
    font=("Arial", 20, "bold")
)

total_result.pack()


# Total tax

box2 = tk.Frame(
    dashboard,
    width=220,
    height=90,
    relief="solid",
    borderwidth=1
)

box2.grid(
    row=0,
    column=1,
    padx=10
)

box2.pack_propagate(False)

tk.Label(
    box2,
    text="TOTAL ESTIMATED TAX",
    font=("Arial", 10, "bold")
).pack(pady=8)

tax_total_result = tk.Label(
    box2,
    text="₹0.00",
    font=("Arial", 18, "bold")
)

tax_total_result.pack()


# Maximum floors

box3 = tk.Frame(
    dashboard,
    width=190,
    height=90,
    relief="solid",
    borderwidth=1
)

box3.grid(
    row=0,
    column=2,
    padx=10
)

box3.pack_propagate(False)

tk.Label(
    box3,
    text="MAX PREDICTED FLOORS",
    font=("Arial", 10, "bold")
).pack(pady=8)

floors_total_result = tk.Label(
    box3,
    text="0",
    font=("Arial", 20, "bold")
)

floors_total_result.pack()


# ==============================
# INPUT SECTION
# ==============================

input_frame = tk.Frame(
    window
)

input_frame.pack(
    pady=15
)


# Plot area

tk.Label(
    input_frame,
    text="Plot Area (sq.ft):",
    font=("Arial", 12)
).grid(
    row=0,
    column=0,
    padx=15,
    pady=10,
    sticky="w"
)

plot_area_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

plot_area_entry.grid(
    row=0,
    column=1,
    padx=15,
    pady=10
)


# Building height

tk.Label(
    input_frame,
    text="Building Height (m):",
    font=("Arial", 12)
).grid(
    row=1,
    column=0,
    padx=15,
    pady=10,
    sticky="w"
)

height_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

height_entry.grid(
    row=1,
    column=1,
    padx=15,
    pady=10
)


# Road width

tk.Label(
    input_frame,
    text="Road Width (m):",
    font=("Arial", 12)
).grid(
    row=2,
    column=0,
    padx=15,
    pady=10,
    sticky="w"
)

road_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

road_entry.grid(
    row=2,
    column=1,
    padx=15,
    pady=10
)


# Location score

tk.Label(
    input_frame,
    text="Location Score (1-5):",
    font=("Arial", 12)
).grid(
    row=3,
    column=0,
    padx=15,
    pady=10,
    sticky="w"
)

location_entry = tk.Entry(
    input_frame,
    width=25,
    font=("Arial", 12)
)

location_entry.grid(
    row=3,
    column=1,
    padx=15,
    pady=10
)


# ==============================
# BUTTONS
# ==============================

button_frame = tk.Frame(
    window
)

button_frame.pack(
    pady=10
)


tk.Button(
    button_frame,
    text="ASSESS PROPERTY",
    command=assess_property,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10
).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_inputs,
    font=("Arial", 12, "bold"),
    padx=30,
    pady=10
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    button_frame,
    text="VIEW HISTORY",
    command=view_history,
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10
).grid(
    row=0,
    column=2,
    padx=5
)


# ==============================
# RESULT SECTION
# ==============================

result_frame = tk.Frame(
    window,
    relief="solid",
    borderwidth=1,
    padx=30,
    pady=15
)

result_frame.pack(
    pady=15
)


floors_result = tk.Label(
    result_frame,
    text="Predicted Floors: -",
    font=("Arial", 16, "bold")
)

floors_result.pack(
    pady=5
)


tax_result = tk.Label(
    result_frame,
    text="Estimated Property Tax: ₹-",
    font=("Arial", 16, "bold")
)

tax_result.pack(
    pady=5
)


status_result = tk.Label(
    result_frame,
    text="Enter property details",
    font=("Arial", 11)
)

status_result.pack(
    pady=5
)


# ==============================
# INITIAL DASHBOARD DATA
# ==============================

update_dashboard()


# ==============================
# START APPLICATION
# ==============================

window.mainloop()