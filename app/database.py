import sqlite3


DATABASE_PATH = r"C:\Users\sande\OneDrive\Desktop\AI_Floor_Tax_System\property_assessments.db"


def create_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plot_area REAL,
            building_height REAL,
            road_width REAL,
            location_score INTEGER,
            predicted_floors INTEGER,
            estimated_tax REAL
        )
    """)

    connection.commit()
    connection.close()


def save_assessment(
    plot_area,
    building_height,
    road_width,
    location_score,
    predicted_floors,
    estimated_tax
):

    connection = sqlite3.connect(DATABASE_PATH)

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
        predicted_floors,
        estimated_tax
    ))

    connection.commit()
    connection.close()


def get_assessments():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM assessments
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records