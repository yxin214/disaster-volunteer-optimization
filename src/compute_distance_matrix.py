from pathlib import Path
import pandas as pd
from math import radians, sin, cos, sqrt, atan2

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

VOLUNTEERS_FILE = DATA_DIR / "volunteers.csv"
TASKS_FILE = DATA_DIR / "tasks.csv"
OUTPUT_FILE = DATA_DIR / "distance_matrix.csv"

def load_data():
    volunteers = pd.read_csv(VOLUNTEERS_FILE)
    tasks = pd.read_csv(TASKS_FILE)

    return volunteers, tasks

def validate_data(volunteers, tasks):
    # Check missing values
    if volunteers.isnull().any().any():
        raise ValueError("Volunteer data contains missing values.")

    if tasks.isnull().any().any():
        raise ValueError("Task data contains missing values.")

    # Check duplicate IDs
    if volunteers["volunteer_id"].duplicated().any():
        raise ValueError("Duplicate volunteer IDs found.")

    if tasks["task_id"].duplicated().any():
        raise ValueError("Duplicate task IDs found.")

    # Check binary columns
    volunteer_binary_columns = [
        "first_aid",
        "driving",
        "heavy_lifting",
        "available",
    ]

    for column in volunteer_binary_columns:
        if not volunteers[column].isin([0, 1]).all():
            raise ValueError(f"{column} must contain only 0 or 1.")

    task_binary_columns = [
        "requires_first_aid",
        "requires_driving",
        "requires_heavy_lifting",
    ]

    for column in task_binary_columns:
        if not tasks[column].isin([0, 1]).all():
            raise ValueError(f"{column} must contain only 0 or 1.")

    # Check urgency range
    if not tasks["urgency"].between(1, 5).all():
        raise ValueError("Task urgency must be between 1 and 5.")

    # Check positive values
    if not (volunteers["max_work_hours"] > 0).all():
        raise ValueError("max_work_hours must be positive.")

    if not (tasks["required_volunteers"] > 0).all():
        raise ValueError("required_volunteers must be positive.")

    if not (tasks["service_hours"] > 0).all():
        raise ValueError("service_hours must be positive.")

    print("Data validation passed.")

def haversine_distance(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * c    

def build_distance_matrix(volunteers, tasks):
    distance_matrix = pd.DataFrame(
        index=volunteers["volunteer_id"],
        columns=tasks["task_id"],
        dtype=float,
    )

    for _, volunteer in volunteers.iterrows():
        for _, task in tasks.iterrows():
            distance = haversine_distance(
                volunteer["latitude"],
                volunteer["longitude"],
                task["latitude"],
                task["longitude"],
            )

            distance_matrix.loc[
                volunteer["volunteer_id"],
                task["task_id"]
            ] = distance

    return distance_matrix

if __name__ == "__main__":
    volunteers, tasks = load_data()

    validate_data(volunteers, tasks)

    distance_matrix = build_distance_matrix(volunteers, tasks)

    print("\nDistance Matrix (km):")
    print(distance_matrix.round(2))

    distance_matrix.to_csv(OUTPUT_FILE)

    print(f"\nDistance matrix saved to: {OUTPUT_FILE}")