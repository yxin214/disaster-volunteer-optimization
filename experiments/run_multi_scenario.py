from pathlib import Path
from math import radians, sin, cos, sqrt, atan2
import random
import pandas as pd
from ortools.linear_solver import pywraplp
from itertools import combinations


BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "results" / "multi_scenario"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_tasks(num_tasks, rng):
    tasks = []

    for j in range(1, num_tasks + 1):
        tasks.append(
            {
                "task_id": f"T{j:02d}",
                "latitude": rng.uniform(23.96, 24.00),
                "longitude": rng.uniform(121.59, 121.63),
                "urgency": rng.randint(1, 5),
                "required_volunteers": rng.randint(1, 3),
                "requires_first_aid": rng.randint(0, 1),
                "requires_driving": rng.randint(0, 1),
                "requires_heavy_lifting": rng.randint(0, 1),
                "service_hours": rng.randint(1, 4),
            }
        )

    return pd.DataFrame(tasks)

def calculate_volunteer_count(tasks, supply_ratio):
    total_demand = int(
        tasks["required_volunteers"].sum()
    )

    num_volunteers = max(
        1,
        round(total_demand * supply_ratio)
    )

    return num_volunteers, total_demand

def generate_volunteers(num_volunteers, rng):
    volunteers = []

    for i in range(1, num_volunteers + 1):
        volunteers.append(
            {
                "volunteer_id": f"V{i:02d}",
                "latitude": rng.uniform(23.96, 24.00),
                "longitude": rng.uniform(121.59, 121.63),
                "first_aid": rng.randint(0, 1),
                "driving": rng.randint(0, 1),
                "heavy_lifting": rng.randint(0, 1),
                "max_work_hours": rng.randint(4, 8),
                "available": 1,
            }
        )

    return pd.DataFrame(volunteers)

def haversine_distance(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius_km * c

def build_distance_matrix(volunteers, tasks):
    matrix = pd.DataFrame(
        index=volunteers["volunteer_id"],
        columns=tasks["task_id"],
        dtype=float,
    )

    for _, volunteer in volunteers.iterrows():
        for _, task in tasks.iterrows():
            matrix.loc[
                volunteer["volunteer_id"],
                task["task_id"]
            ] = haversine_distance(
                volunteer["latitude"],
                volunteer["longitude"],
                task["latitude"],
                task["longitude"],
            )

    return matrix

def greedy_assignment(volunteers, tasks, distance_matrix):
    assignments = []
    assigned_volunteers = set()

    tasks_sorted = tasks.sort_values(
        ["urgency", "task_id"],
        ascending=[False, True],
    )

    for _, task in tasks_sorted.iterrows():
        task_id = task["task_id"]
        required = int(task["required_volunteers"])

        candidates = []

        for _, volunteer in volunteers.iterrows():
            volunteer_id = volunteer["volunteer_id"]

            if volunteer_id in assigned_volunteers:
                continue

            if (
                volunteer["max_work_hours"]
                < task["service_hours"]
            ):
                continue

            distance = distance_matrix.loc[
                volunteer_id,
                task_id
            ]

            candidates.append(
                (volunteer_id, distance)
            )

        selected = find_nearest_feasible_team(
            candidates,
            required,
            volunteers,
            task
        )

        if selected is None:
            continue

        for volunteer_id, distance in selected:
            assignments.append(
                {
                    "volunteer_id": volunteer_id,
                    "task_id": task_id,
                    "distance_km": distance,
                }
            )

            assigned_volunteers.add(volunteer_id)

    return pd.DataFrame(
        assignments,
        columns=[
            "volunteer_id",
            "task_id",
            "distance_km",
        ],
    )

def team_covers_required_skills(
    selected_ids,
    volunteers,
    task
):
    selected = volunteers[
        volunteers["volunteer_id"].isin(selected_ids)
    ]

    if task["requires_first_aid"] == 1:
        if selected["first_aid"].sum() < 1:
            return False

    if task["requires_driving"] == 1:
        if selected["driving"].sum() < 1:
            return False

    if task["requires_heavy_lifting"] == 1:
        if selected["heavy_lifting"].sum() < 1:
            return False

    return True

def find_nearest_feasible_team(
    candidates,
    required,
    volunteers,
    task
):
    best_team = None
    best_distance = float("inf")

    for team in combinations(
        candidates,
        required
    ):
        volunteer_ids = [
            item[0]
            for item in team
        ]

        if not team_covers_required_skills(
            volunteer_ids,
            volunteers,
            task
        ):
            continue

        total_distance = sum(
            item[1]
            for item in team
        )

        if total_distance < best_distance:
            best_distance = total_distance
            best_team = team

    return best_team

def optimization_assignment(
    volunteers,
    tasks,
    distance_matrix,
    alpha=10.0,
    beta=1.0,
):
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if solver is None:
        raise RuntimeError(
            "SCIP solver is not available."
        )

    volunteer_ids = volunteers[
        "volunteer_id"
    ].tolist()

    task_ids = tasks[
        "task_id"
    ].tolist()

    volunteer_lookup = volunteers.set_index(
        "volunteer_id"
    )

    x = {
        (i, j): solver.BoolVar(f"x_{i}_{j}")
        for i in volunteer_ids
        for j in task_ids
    }

    y = {
        j: solver.BoolVar(f"y_{j}")
        for j in task_ids
    }

    # One task per volunteer
    for i in volunteer_ids:
        solver.Add(
            sum(x[i, j] for j in task_ids) <= 1
        )

    # Working-time feasibility
    for i in volunteer_ids:
        for _, task in tasks.iterrows():
            j = task["task_id"]

            if (
                volunteer_lookup.loc[
                    i,
                    "max_work_hours"
                ]
                < task["service_hours"]
            ):
                solver.Add(x[i, j] == 0)

    # Staffing and skill coverage
    for _, task in tasks.iterrows():
        j = task["task_id"]
        required = int(
            task["required_volunteers"]
        )

        solver.Add(
            sum(
                x[i, j]
                for i in volunteer_ids
            )
            == required * y[j]
        )

        if task["requires_first_aid"] == 1:
            solver.Add(
                sum(
                    volunteer_lookup.loc[
                        i,
                        "first_aid"
                    ] * x[i, j]
                    for i in volunteer_ids
                )
                >= y[j]
            )

        if task["requires_driving"] == 1:
            solver.Add(
                sum(
                    volunteer_lookup.loc[
                        i,
                        "driving"
                    ] * x[i, j]
                    for i in volunteer_ids
                )
                >= y[j]
            )

        if task["requires_heavy_lifting"] == 1:
            solver.Add(
                sum(
                    volunteer_lookup.loc[
                        i,
                        "heavy_lifting"
                    ] * x[i, j]
                    for i in volunteer_ids
                )
                >= y[j]
            )    

    urgency_reward = sum(
        alpha
        * task["urgency"]
        * y[task["task_id"]]
        for _, task in tasks.iterrows()
    )

    travel_cost = sum(
        beta
        * distance_matrix.loc[i, j]
        * x[i, j]
        for i in volunteer_ids
        for j in task_ids
    )

    solver.Maximize(
        urgency_reward - travel_cost
    )

    status = solver.Solve()

    assignments = []

    if status not in (
        pywraplp.Solver.OPTIMAL,
        pywraplp.Solver.FEASIBLE,
    ):
        return pd.DataFrame(
            columns=[
                "volunteer_id",
                "task_id",
                "distance_km",
            ]
        )

    for i in volunteer_ids:
        for j in task_ids:
            if x[i, j].solution_value() > 0.5:
                assignments.append(
                    {
                        "volunteer_id": i,
                        "task_id": j,
                        "distance_km":
                            distance_matrix.loc[i, j],
                    }
                )

    return pd.DataFrame(assignments)    

def evaluate(assignments, tasks):
    completed_tasks = 0
    completed_urgency = 0

    total_urgency = tasks["urgency"].sum()

    for _, task in tasks.iterrows():
        task_id = task["task_id"]
        required = int(
            task["required_volunteers"]
        )

        assigned_count = len(
            assignments[
                assignments["task_id"]
                == task_id
            ]
        )

        if assigned_count >= required:
            completed_tasks += 1
            completed_urgency += task["urgency"]

    total_tasks = len(tasks)

    total_distance = (
        assignments["distance_km"].sum()
        if not assignments.empty
        else 0
    )

    distance_per_completed_task = (
        total_distance / completed_tasks
        if completed_tasks > 0
        else 0
    )

    distance_per_completed_urgency = (
        total_distance / completed_urgency
        if completed_urgency > 0
        else 0
    )

    return {
        "completed_tasks": completed_tasks,
        "completed_urgency": completed_urgency,
        "completion_rate":
            completed_tasks / total_tasks,
        "urgency_weighted_completion":
            completed_urgency / total_urgency,
        "total_distance_km": total_distance,
        "distance_per_completed_task":
            distance_per_completed_task,
        "distance_per_completed_urgency":
            distance_per_completed_urgency,
    }

def run_experiments():
    scenarios = {
        "resource_rich": 1.3,
        "balanced": 1.0,
        "resource_scarce": 0.7,
    }

    num_tasks = 10
    repetitions = 30

    results = []

    for scenario_name, supply_ratio in scenarios.items():
        for seed in range(repetitions):
            rng = random.Random(seed)

            tasks = generate_tasks(
                num_tasks,
                rng
            )

            num_volunteers, total_demand = (
                calculate_volunteer_count(
                    tasks,
                    supply_ratio
                )
            )

            volunteers = generate_volunteers(
                num_volunteers,
                rng
            )

            distance_matrix = (
                build_distance_matrix(
                    volunteers,
                    tasks
                )
            )

            greedy = greedy_assignment(
                volunteers,
                tasks,
                distance_matrix
            )

            optimization = (
                optimization_assignment(
                    volunteers,
                    tasks,
                    distance_matrix
                )
            )

            greedy_metrics = evaluate(
                greedy,
                tasks
            )

            optimization_metrics = evaluate(
                optimization,
                tasks
            )

            for method, metrics in [
                ("Greedy", greedy_metrics),
                (
                    "Optimization",
                    optimization_metrics
                ),
            ]:
                results.append(
                    {
                        "scenario": scenario_name,
                        "supply_ratio":
                            supply_ratio,
                        "seed": seed,
                        "num_tasks":
                            num_tasks,
                        "num_volunteers":
                            num_volunteers,
                        "total_demand":
                            total_demand,
                        "method": method,
                        **metrics,
                    }
                )

    return pd.DataFrame(results)            

if __name__ == "__main__":
    results = run_experiments()

    output_file = (
        RESULTS_DIR
        / "multi_scenario_results.csv"
    )

    summary = (
        results.groupby(
            ["scenario", "method"]
        )
        [
            [
                "total_distance_km",
                "completion_rate",
                "urgency_weighted_completion",
                "distance_per_completed_task",
                "distance_per_completed_urgency",
            ]
        ]
        .agg(["mean", "std"])
        .round(4)
    )

    print("\nSummary:")
    print(summary.to_string())    

    results.to_csv(
        output_file,
        index=False
    )

    print("\nExperiments completed.")
    print(f"Total rows: {len(results)}")
    print(f"Results saved to: {output_file}")