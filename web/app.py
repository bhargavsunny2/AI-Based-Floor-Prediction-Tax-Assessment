from flask import Flask, render_template, request
import joblib
import pandas as pd
import sqlite3
import os

app = Flask(__name__)

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "floor_prediction_model.pkl"
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "property_assessments.db"
)


# ==========================================
# LOAD MACHINE LEARNING MODEL
# ==========================================

model = joblib.load(MODEL_PATH)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plot_area REAL NOT NULL,
            building_height REAL NOT NULL,
            road_width REAL NOT NULL,
            location_score INTEGER NOT NULL,
            predicted_floors INTEGER NOT NULL,
            estimated_tax REAL NOT NULL
        )
    """)

    connection.commit()

    connection.close()


# ==========================================
# TAX CALCULATION
# ==========================================

def calculate_tax(
    plot_area,
    floors,
    location_score
):

    base_rate = 10

    floor_factor = (
        1 + (floors - 1) * 0.15
    )

    location_factor = (
        1 + (location_score - 1) * 0.10
    )

    tax = (
        plot_area
        * base_rate
        * floor_factor
        * location_factor
    )

    return round(tax, 2)


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    initialize_database()

    return render_template(
        "index.html",
        predicted_floors=None,
        estimated_tax=None,
        error=None
    )


# ==========================================
# PROPERTY ASSESSMENT
# ==========================================

@app.route(
    "/assess",
    methods=["POST"]
)
def assess():

    try:

        # Make sure database/table exists
        initialize_database()

        # --------------------------------------
        # Read input values
        # --------------------------------------

        plot_area = float(
            request.form.get("plot_area", 0)
        )

        building_height = float(
            request.form.get(
                "building_height",
                0
            )
        )

        road_width = float(
            request.form.get(
                "road_width",
                0
            )
        )

        location_score = int(
            request.form.get(
                "location_score",
                0
            )
        )


        # --------------------------------------
        # Validate input
        # --------------------------------------

        if plot_area <= 0:

            raise ValueError(
                "Plot area must be greater than 0."
            )


        if building_height <= 0:

            raise ValueError(
                "Building height must be greater than 0."
            )


        if road_width <= 0:

            raise ValueError(
                "Road width must be greater than 0."
            )


        if (
            location_score < 1
            or location_score > 4
        ):

            raise ValueError(
                "Location score must be between 1 and 4."
            )


        # --------------------------------------
        # Prepare ML input
        # --------------------------------------

        input_data = pd.DataFrame([
            {
                "plot_area": plot_area,
                "building_height": building_height,
                "road_width": road_width,
                "location_score": location_score
            }
        ])


        # --------------------------------------
        # Predict floors
        # --------------------------------------

        predicted_floors = int(
            model.predict(
                input_data
            )[0]
        )


        # --------------------------------------
        # Calculate tax
        # --------------------------------------

        estimated_tax = calculate_tax(
            plot_area,
            predicted_floors,
            location_score
        )


        # --------------------------------------
        # Save assessment
        # --------------------------------------

        connection = get_db_connection()

        connection.execute(
            """
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
            """,
            (
                plot_area,
                building_height,
                road_width,
                location_score,
                predicted_floors,
                estimated_tax
            )
        )

        connection.commit()

        connection.close()


        # --------------------------------------
        # Display result
        # --------------------------------------

        return render_template(
            "index.html",
            predicted_floors=predicted_floors,
            estimated_tax=estimated_tax,
            error=None
        )


    except Exception as error:

        return render_template(
            "index.html",
            predicted_floors=None,
            estimated_tax=None,
            error=str(error)
        )


# ==========================================
# HISTORY
# ==========================================

@app.route("/history")
def history():

    try:

        # Make sure database/table exists
        initialize_database()

        connection = get_db_connection()

        records = connection.execute(
            """
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
            """
        ).fetchall()

        connection.close()

        return render_template(
            "history.html",
            records=records
        )

    except Exception as error:

        return render_template(
            "history.html",
            records=[],
            error=str(error)
        )


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    initialize_database()

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
