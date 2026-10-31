
import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ------------------------------------------------
# CONFIGURATION
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "campus_energy.db"

app = FastAPI(
    title="Campus Energy Management System",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

BUILDINGS = [
    ("Engineering Block", 25),
    ("Library", 15),
    ("Administrative Block", 10),
    ("Laboratories", 20),
    ("Hostel Block", 30)
]


# ------------------------------------------------
# DATABASE
# ------------------------------------------------

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS buildings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                solar_capacity_kw REAL NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS energy_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                building_id INTEGER NOT NULL,
                timestamp TEXT NOT NULL,

                voltage_v REAL,
                current_a REAL,
                active_power_kw REAL,
                energy_kwh REAL,
                frequency_hz REAL,
                power_factor REAL,
                apparent_power_kva REAL,

                solar_power_kw REAL,
                grid_power_kw REAL,
                temperature_c REAL,

                FOREIGN KEY(building_id) REFERENCES buildings(id)
            )
        """)

        for name, capacity in BUILDINGS:
            conn.execute("""
                INSERT OR IGNORE INTO buildings
                (name, solar_capacity_kw)
                VALUES (?, ?)
            """, (name, capacity))

        count = conn.execute(
            "SELECT COUNT(*) FROM energy_readings"
        ).fetchone()[0]

        # Generate demonstration data only once
        if count == 0:

            building_rows = conn.execute(
                "SELECT id FROM buildings"
            ).fetchall()

            now = datetime.now()

            for day in range(7):
                date = now.date() - timedelta(days=6-day)

                for building in building_rows:
                    building_id = building["id"]

                    for interval in range(4):

                        voltage = round(random.uniform(220, 240), 2)
                        current = round(random.uniform(5, 25), 2)
                        power_factor = round(random.uniform(0.85, 0.99), 2)
                        frequency = round(random.uniform(49.8, 50.2), 2)

                        # Single-phase apparent power
                        apparent_power = voltage * current / 1000

                        # Active power = Apparent power x PF
                        active_power = apparent_power * power_factor

                        solar = round(random.uniform(1, 8), 2)
                        grid = round(max(active_power - solar, 0), 2)

                        energy = round(
                            active_power * 6, 2
                        )

                        temperature = round(
                            random.uniform(25, 36), 2
                        )

                        timestamp = (
                            datetime.combine(date, datetime.min.time())
                            + timedelta(hours=interval * 6)
                        )

                        conn.execute("""
                            INSERT INTO energy_readings (
                                building_id,
                                timestamp,
                                voltage_v,
                                current_a,
                                active_power_kw,
                                energy_kwh,
                                frequency_hz,
                                power_factor,
                                apparent_power_kva,
                                solar_power_kw,
                                grid_power_kw,
                                temperature_c
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            building_id,
                            timestamp.isoformat(timespec="seconds"),
                            voltage,
                            current,
                            active_power,
                            energy,
                            frequency,
                            power_factor,
                            apparent_power,
                            solar,
                            grid,
                            temperature
                        ))

        conn.commit()


initialize_database()


# ------------------------------------------------
# HOME DASHBOARD
# ------------------------------------------------

@app.get("/")
async def home():
    return {
        "message": "Campus Energy Monitoring API is running!"
    }


@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


# ------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------

@app.get("/api/health")
async def health():
    return {
        "status": "online",
        "application": "Campus Energy Management System"
    }


# ------------------------------------------------
# CAMPUS OVERVIEW
# ------------------------------------------------

@app.get("/api/overview")
async def overview():

    with get_connection() as conn:

        building_count = conn.execute(
            "SELECT COUNT(*) FROM buildings"
        ).fetchone()[0]

        reading_count = conn.execute(
            "SELECT COUNT(*) FROM energy_readings"
        ).fetchone()[0]

        stats = conn.execute("""
            SELECT
                AVG(voltage_v) AS voltage,
                AVG(current_a) AS current,
                AVG(active_power_kw) AS active_power,
                SUM(energy_kwh) AS energy,
                AVG(frequency_hz) AS frequency,
                AVG(power_factor) AS power_factor,
                AVG(apparent_power_kva) AS apparent_power,
                AVG(solar_power_kw) AS solar,
                AVG(grid_power_kw) AS grid
            FROM energy_readings
        """).fetchone()

        return {
            "total_buildings": building_count,
            "total_readings": reading_count,
            "voltage_v": round(stats["voltage"] or 0, 2),
            "current_a": round(stats["current"] or 0, 2),
            "active_power_kw": round(stats["active_power"] or 0, 2),
            "energy_kwh": round(stats["energy"] or 0, 2),
            "frequency_hz": round(stats["frequency"] or 0, 2),
            "power_factor": round(stats["power_factor"] or 0, 2),
            "apparent_power_kva": round(stats["apparent_power"] or 0, 2),
            "solar_power_kw": round(stats["solar"] or 0, 2),
            "grid_power_kw": round(stats["grid"] or 0, 2)
        }


# ------------------------------------------------
# BUILDING LIST
# ------------------------------------------------

@app.get("/api/buildings")
async def buildings():

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT id, name, solar_capacity_kw
            FROM buildings
            ORDER BY id
        """).fetchall()

        return [dict(row) for row in rows]


# ------------------------------------------------
# DAILY ENERGY SUMMARY
# ------------------------------------------------

@app.get("/api/daily")
async def daily_summary():

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                DATE(timestamp) AS date,
                AVG(voltage_v) AS voltage_v,
                AVG(current_a) AS current_a,
                AVG(active_power_kw) AS active_power_kw,
                SUM(energy_kwh) AS energy_kwh,
                AVG(frequency_hz) AS frequency_hz,
                AVG(power_factor) AS power_factor,
                AVG(apparent_power_kva) AS apparent_power_kva,
                SUM(solar_power_kw) AS solar_power_kw,
                SUM(grid_power_kw) AS grid_power_kw
            FROM energy_readings
            GROUP BY DATE(timestamp)
            ORDER BY date
        """).fetchall()

        return [dict(row) for row in rows]


# ------------------------------------------------
# RECENT READINGS
# ------------------------------------------------

@app.get("/api/readings")
async def recent_readings():

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT
                e.id,
                e.timestamp,
                b.name AS building,
                e.voltage_v,
                e.current_a,
                e.active_power_kw,
                e.energy_kwh,
                e.frequency_hz,
                e.power_factor,
                e.apparent_power_kva,
                e.solar_power_kw,
                e.grid_power_kw,
                e.temperature_c
            FROM energy_readings e
            JOIN buildings b ON b.id = e.building_id
            ORDER BY e.timestamp DESC, e.id DESC
            LIMIT 50
        """).fetchall()

        return [dict(row) for row in rows]


# ------------------------------------------------
# INDIVIDUAL BUILDING PARAMETERS
# ------------------------------------------------

@app.get("/api/buildings/{building_id}/readings")
async def building_readings(building_id: int):

    with get_connection() as conn:

        building = conn.execute(
            "SELECT id FROM buildings WHERE id = ?",
            (building_id,)
        ).fetchone()

        if not building:
            raise HTTPException(
                status_code=404,
                detail="Building not found"
            )

        rows = conn.execute("""
            SELECT *
            FROM energy_readings
            WHERE building_id = ?
            ORDER BY timestamp DESC
            LIMIT 50
        """, (building_id,)).fetchall()

        return [dict(row) for row in rows]


# ------------------------------------------------
# API INFORMATION
# ------------------------------------------------

@app.get("/api")
async def api_information():
    return {
        "application": "Campus Energy Management System",
        "electrical_parameters": [
            "Voltage (V)",
            "Current (A)",
            "Active Power (kW)",
            "Energy (kWh)",
            "Frequency (Hz)",
            "Power Factor",
            "Apparent Power (kVA)"
        ],
        "endpoints": [
            "/api/health",
            "/api/overview",
            "/api/buildings",
            "/api/daily",
            "/api/readings",
            "/docs"
        ]
    }
