from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import sqlite3
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)


# Database initialization
def init_db():
    with sqlite3.connect("garden.db") as conn:
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
        conn.commit()


# Weather API configuration
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
ZIP_CODE = "23832"
COUNTRY_CODE = "US"


def get_weather():
    """Get 3-day weather forecast"""
    if not WEATHER_API_KEY:
        return {"error": "Weather API key not configured"}

    url = f"http://api.openweathermap.org/data/2.5/forecast?zip={ZIP_CODE},{COUNTRY_CODE}&appid={WEATHER_API_KEY}&units=imperial"
    try:
        response = requests.get(url)
        data = response.json()

        # Process next 3 days
        forecast = []
        current_date = None
        for item in data["list"]:
            date = datetime.fromtimestamp(item["dt"]).date()
            if current_date != date:
                if len(forecast) >= 3:
                    break
                current_date = date
                forecast.append(
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "temp": item["main"]["temp"],
                        "description": item["weather"][0]["description"],
                        "humidity": item["main"]["humidity"],
                    }
                )
        return forecast
    except Exception as e:
        return {"error": str(e)}


def get_daily_tasks():
    """Generate daily gardening tasks based on date and weather"""
    current_date = datetime.now()
    month = current_date.month
    tasks = []

    # Monthly task generation logic
    if month == 1:  # January
        tasks.append("Start planning your garden layout")
        tasks.append("Order seeds for the upcoming season")
        tasks.append("Begin indoor seed starting for tomatoes and peppers")
        tasks.append("Check stored vegetables for spoilage")
    elif month == 2:  # February
        tasks.append("Continue indoor seed starting")
        tasks.append("Start eggplant and pepper seeds indoors")
        tasks.append("Prepare outdoor beds for early spring planting")
        tasks.append("Plan crop rotation for the season")
    elif month == 3:  # March
        tasks.append("Start tomato seeds indoors")
        tasks.append("Direct sow peas and lettuce")
        tasks.append("Prepare garden beds and add compost")
        tasks.append("Test soil pH and amend if necessary")
    elif month == 4:  # April
        tasks.append("Plant potatoes and onion sets")
        tasks.append("Direct sow carrots and beets")
        tasks.append("Transplant early spring vegetables")
        tasks.append("Set up trellises for climbing plants")
    elif month == 5:  # May
        tasks.append("Transplant tomatoes and peppers after last frost")
        tasks.append("Direct sow beans and corn")
        tasks.append("Begin regular fertilizing schedule")
        tasks.append("Monitor for pest problems")
    elif month == 6:  # June
        tasks.append("Plant successive crops of beans and lettuce")
        tasks.append("Mulch to retain moisture")
        tasks.append("Start harvesting early crops")
        tasks.append("Monitor for disease in humid weather")
    elif month == 7:  # July
        tasks.append("Plant fall crops of carrots and beets")
        tasks.append("Continue succession planting of lettuce")
        tasks.append("Monitor watering needs closely")
        tasks.append("Harvest vegetables regularly")
    elif month == 8:  # August
        tasks.append("Plant fall crops of peas and greens")
        tasks.append("Start fall brassicas indoors")
        tasks.append("Continue harvesting summer crops")
        tasks.append("Save seeds from heirloom vegetables")
    elif month == 9:  # September
        tasks.append("Plant garlic and spring bulbs")
        tasks.append("Continue harvesting warm-season crops")
        tasks.append("Plant cold-hardy vegetables")
        tasks.append("Begin cleanup of spent plants")
    elif month == 10:  # October
        tasks.append("Harvest remaining warm-season crops")
        tasks.append("Plant cover crops in empty beds")
        tasks.append("Clean up diseased plant material")
        tasks.append("Store garden supplies for winter")
    elif month == 11:  # November
        tasks.append("Harvest remaining root crops")
        tasks.append("Add mulch to protect perennials")
        tasks.append("Clean and store garden tools")
        tasks.append("Test soil and add amendments")
    elif month == 12:  # December
        tasks.append("Review garden journal and plan for spring")
        tasks.append("Check stored vegetables")
        tasks.append("Order seed catalogs")
        tasks.append("Maintain winter protection for perennials")

    # Add weather-based tasks
    weather = get_weather()
    if weather and not isinstance(weather, dict):  # Check if weather data is valid
        for day in weather:
            if "temp" in day and day["temp"] < 32:
                tasks.append(
                    f"Frost warning for {day['date']}! Protect sensitive plants"
                )

    return tasks


@app.route("/")
def home():
    weather = get_weather()
    tasks = get_daily_tasks()
    return render_template("index.html", weather=weather, tasks=tasks)


@app.route("/vegetables")
def vegetables():
    with sqlite3.connect("garden.db") as conn:
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        c = conn.cursor()
        c.execute("SELECT * FROM vegetables")
        vegetables = c.fetchall()
    return render_template("vegetables.html", vegetables=vegetables)


@app.route("/vegetable/<int:id>")
def vegetable_detail(id):
    with sqlite3.connect("garden.db") as conn:
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM vegetables WHERE id = ?", (id,))
        vegetable = c.fetchone()
    return render_template("vegetable_detail.html", vegetable=vegetable)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
