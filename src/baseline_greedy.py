from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

VOLUNTEERS_FILE = DATA_DIR / "volunteers.csv"
TASKS_FILE = DATA_DIR / "tasks.csv"
DISTANCE_FILE = DATA_DIR / "distance_matrix.csv"

RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

ASSIGNMENT_OUTPUT = (RESULTS_DIR / "greedy_assignment.csv")
EVALUATION_OUTPUT = (RESULTS_DIR / "greedy_evaluation.csv")

def load_data():
    volunteers = pd.read_csv(VOLUNTEERS_FILE)
    tasks = pd.read_csv(TASKS_FILE)

    distance_matrix = pd.read_csv(
        DISTANCE_FILE,
        index_col="volunteer_id"
    )

    return volunteers, tasks, distance_matrix

def is_skill_compatible(volunteer, task):
    if (
        task["requires_first_aid"] == 1
        and volunteer["first_aid"] != 1
    ):
        return False

    if (
        task["requires_driving"] == 1
        and volunteer["driving"] != 1
    ):
        return False

    if (
        task["requires_heavy_lifting"] == 1
        and volunteer["heavy_lifting"] != 1
    ):
        return False

    return True

def greedy_assignment(volunteers, tasks, distance_matrix):
    assignments = []
    assigned_volunteers = set()

    # Higher urgency tasks are handled first
    tasks_sorted = tasks.sort_values(
        by="urgency",
        ascending=False
    )

    for _, task in tasks_sorted.iterrows():
        task_id = task["task_id"]
        required = int(task["required_volunteers"])

        candidates = []

        for _, volunteer in volunteers.iterrows():
            volunteer_id = volunteer["volunteer_id"]

            # Skip unavailable volunteers
            if volunteer["available"] != 1:
                continue

            # Skip already assigned volunteers
            if volunteer_id in assigned_volunteers:
                continue

            # Skip volunteers without enough available time
            if volunteer["max_work_hours"] < task["service_hours"]:
                continue

            # Skip incompatible skills
            if not is_skill_compatible(volunteer, task):
                continue

            distance = distance_matrix.loc[
                volunteer_id,
                task_id
            ]

            candidates.append(
                (volunteer_id, distance)
            )

        # Sort candidates by distance
        candidates.sort(key=lambda x: x[1])

        selected = candidates[:required]

        for volunteer_id, distance in selected:
            assignments.append(
                {
                    "volunteer_id": volunteer_id,
                    "task_id": task_id,
                    "distance_km": distance,
                    "urgency": task["urgency"],
                }
            )

            assigned_volunteers.add(volunteer_id)

    return pd.DataFrame(assignments)

def evaluate_assignment(result, tasks):
    evaluation = []

    for _, task in tasks.iterrows():
        task_id = task["task_id"]

        assigned_count = len(
            result[result["task_id"] == task_id]
        )

        required_count = int(
            task["required_volunteers"]
        )

        completed = assigned_count >= required_count

        evaluation.append(
            {
                "task_id": task_id,
                "urgency": task["urgency"],
                "required_volunteers": required_count,
                "assigned_volunteers": assigned_count,
                "completed": completed,
            }
        )

    return pd.DataFrame(evaluation)

if __name__ == "__main__":
    volunteers, tasks, distance_matrix = load_data()

    result = greedy_assignment(
        volunteers,
        tasks,
        distance_matrix
    )

    evaluation = evaluate_assignment(
        result,
        tasks
    )

    print("\nGreedy Assignment Result:")
    print(result)

    print("\nTask Evaluation:")
    print(evaluation)

    total_distance = result["distance_km"].sum()

    completed_tasks = evaluation["completed"].sum()
    total_tasks = len(evaluation)

    print("\nSummary")
    print(f"Total travel distance: {total_distance:.2f} km")
    print(
        f"Completed tasks: "
        f"{completed_tasks}/{total_tasks}"
    )

    completed_urgency = evaluation.loc[
        evaluation["completed"],
        "urgency"
    ].sum()

    total_urgency = evaluation["urgency"].sum()

    weighted_completion = (
        completed_urgency / total_urgency
        if total_urgency > 0
        else 0
    )

    print(
        f"Urgency-weighted completion: "
        f"{weighted_completion:.2%}"
    )   

    result.to_csv(
    ASSIGNMENT_OUTPUT,
    index=False
    )

    evaluation.to_csv(
        EVALUATION_OUTPUT,
        index=False
    )

    print(
        f"\nAssignment saved to: "
        f"{ASSIGNMENT_OUTPUT}"
    )

    print(
        f"Evaluation saved to: "
        f"{EVALUATION_OUTPUT}"
    )