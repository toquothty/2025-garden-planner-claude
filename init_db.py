import sqlite3
from datetime import datetime

# Vegetable data for Virginia Zone 7A
VEGETABLES = [
    {
        "name": "Tomatoes",
        "sow_type": "Transplant",
        "days_to_harvest": 75,
        "plant_spacing": 24,
        "seed_depth": 0.25,
        "sow_start": "March 15",
        "sow_end": "April 30",
        "harvest_start": "June 1",
        "harvest_end": "October 15",
        "image_url": "https://images.unsplash.com/photo-1592841200221-a6898f307baa",
    },
    {
        "name": "Green Beans",
        "sow_type": "Direct Sow",
        "days_to_harvest": 55,
        "plant_spacing": 4,
        "seed_depth": 1.0,
        "sow_start": "April 15",
        "sow_end": "July 31",
        "harvest_start": "June 10",
        "harvest_end": "September 30",
        "image_url": "https://images.unsplash.com/photo-1574963835594-61eede2070dc",
    },
    {
        "name": "Bell Peppers",
        "sow_type": "Transplant",
        "days_to_harvest": 70,
        "plant_spacing": 18,
        "seed_depth": 0.25,
        "sow_start": "March 15",
        "sow_end": "April 30",
        "harvest_start": "June 15",
        "harvest_end": "October 15",
        "image_url": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83",
    },
    {
        "name": "Lettuce",
        "sow_type": "Direct Sow",
        "days_to_harvest": 45,
        "plant_spacing": 6,
        "seed_depth": 0.25,
        "sow_start": "March 1",
        "sow_end": "April 15",
        "harvest_start": "April 15",
        "harvest_end": "June 1",
        "image_url": "https://images.unsplash.com/photo-1622205313162-be1d5712a43f",
    },
    {
        "name": "Carrots",
        "sow_type": "Direct Sow",
        "days_to_harvest": 70,
        "plant_spacing": 3,
        "seed_depth": 0.5,
        "sow_start": "March 15",
        "sow_end": "July 31",
        "harvest_start": "May 24",
        "harvest_end": "October 15",
        "image_url": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37",
    },
    {
        "name": "Cucumbers",
        "sow_type": "Direct Sow",
        "days_to_harvest": 60,
        "plant_spacing": 12,
        "seed_depth": 1.0,
        "sow_start": "April 15",
        "sow_end": "July 15",
        "harvest_start": "June 14",
        "harvest_end": "September 15",
        "image_url": "https://images.unsplash.com/photo-1589621316382-008455b857cd",
    },
    {
        "name": "Zucchini",
        "sow_type": "Direct Sow",
        "days_to_harvest": 50,
        "plant_spacing": 24,
        "seed_depth": 1.0,
        "sow_start": "April 15",
        "sow_end": "July 31",
        "harvest_start": "June 4",
        "harvest_end": "September 30",
        "image_url": "https://images.unsplash.com/photo-1563252722-6434563a985d",
    },
    {
        "name": "Broccoli",
        "sow_type": "Transplant",
        "days_to_harvest": 65,
        "plant_spacing": 18,
        "seed_depth": 0.5,
        "sow_start": "March 1",
        "sow_end": "April 15",
        "harvest_start": "May 5",
        "harvest_end": "June 19",
        "image_url": "https://images.unsplash.com/photo-1584270354949-c26b0d5b4a0c",
    },
]


def init_db():
    # Connect to database
    conn = sqlite3.connect("garden.db")
    c = conn.cursor()

    # Create vegetables table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS vegetables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sow_type TEXT NOT NULL,
            days_to_harvest INTEGER,
            plant_spacing INTEGER,
            seed_depth FLOAT,
            sow_start_date TEXT,
            sow_end_date TEXT,
            harvest_start_date TEXT,
            harvest_end_date TEXT,
            image_url TEXT
        )
    """
    )

    # Clear existing data
    c.execute("DELETE FROM vegetables")

    # Insert vegetable data
    for veg in VEGETABLES:
        c.execute(
            """
            INSERT INTO vegetables (
                name, sow_type, days_to_harvest, plant_spacing, seed_depth,
                sow_start_date, sow_end_date, harvest_start_date, harvest_end_date, image_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                veg["name"],
                veg["sow_type"],
                veg["days_to_harvest"],
                veg["plant_spacing"],
                veg["seed_depth"],
                veg["sow_start"],
                veg["sow_end"],
                veg["harvest_start"],
                veg["harvest_end"],
                veg["image_url"],
            ),
        )

    # Commit changes and close connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized with vegetable data.")
