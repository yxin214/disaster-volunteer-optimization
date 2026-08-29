from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"

TASKS_FILE = DATA_DIR / "tasks.csv"
TASK_COMPARISON_FILE = RESULTS_DIR / "task_level_comparison.csv"

GREEDY_ASSIGNMENT_FILE = RESULTS_DIR / "greedy_assignment.csv"
OPTIMIZATION_ASSIGNMENT_FILE = RESULTS_DIR / "optimization_assignment.csv"

OUTPUT_FILE = RESULTS_DIR / "method_comparison.csv"

def load_data():
    tasks = pd.read_csv(TASKS_FILE)
    greedy = pd.read_csv(GREEDY_ASSIGNMENT_FILE)
    optimization = pd.read_csv(OPTIMIZATION_ASSIGNMENT_FILE)

    return tasks, greedy, optimization

def evaluate_method(assignments, tasks):
    evaluation = []

    for _, task in tasks.iterrows():
        task_id = task["task_id"]
        required = int(task["required_volunteers"])

        assigned_count = len(
            assignments[
                assignments["task_id"] == task_id
            ]
        )

        completed = assigned_count >= required

        evaluation.append(
            {
                "task_id": task_id,
                "urgency": task["urgency"],
                "required_volunteers": required,
                "assigned_volunteers": assigned_count,
                "completed": completed,
            }
        )

    return pd.DataFrame(evaluation)

def calculate_metrics(assignments, evaluation):
    total_distance = assignments["distance_km"].sum()

    completed_tasks = int(
        evaluation["completed"].sum()
    )

    total_tasks = len(evaluation)

    completion_rate = (
        completed_tasks / total_tasks
        if total_tasks > 0
        else 0
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

    return {
        "total_distance_km": total_distance,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "urgency_weighted_completion": weighted_completion,
    }

def build_task_comparison(
    tasks,
    greedy_evaluation,
    optimization_evaluation
):
    comparison = tasks[
        ["task_id", "urgency", "required_volunteers"]
    ].copy()

    comparison["greedy_assigned"] = (
        greedy_evaluation[
            "assigned_volunteers"
        ].values
    )

    comparison["greedy_completed"] = (
        greedy_evaluation[
            "completed"
        ].values
    )

    comparison["optimization_assigned"] = (
        optimization_evaluation[
            "assigned_volunteers"
        ].values
    )

    comparison["optimization_completed"] = (
        optimization_evaluation[
            "completed"
        ].values
    )

    return comparison

def percentage_change(new_value, old_value):
    if old_value == 0:
        return None

    return (
        (new_value - old_value)
        / old_value
        * 100
    )

if __name__ == "__main__":
    tasks, greedy, optimization = load_data()

    greedy_evaluation = evaluate_method(
        greedy,
        tasks
    )

    optimization_evaluation = evaluate_method(
        optimization,
        tasks
    )

    greedy_metrics = calculate_metrics(
        greedy,
        greedy_evaluation
    )

    optimization_metrics = calculate_metrics(
        optimization,
        optimization_evaluation
    )

    comparison = pd.DataFrame(
        [
            {
                "method": "Greedy",
                **greedy_metrics,
            },
            {
                "method": "Optimization",
                **optimization_metrics,
            },
        ]
    )

    print("\nMethod Comparison:")
    print(comparison)

    comparison.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nComparison saved to: "
        f"{OUTPUT_FILE}"
    )    

    task_comparison = build_task_comparison(
        tasks,
        greedy_evaluation,
        optimization_evaluation
    )

    print("\nTask-Level Comparison:")
    print(task_comparison)

    task_comparison.to_csv(
        TASK_COMPARISON_FILE,
        index=False
    )    

    distance_change = percentage_change(
        optimization_metrics["total_distance_km"],
        greedy_metrics["total_distance_km"],
    )

    weighted_change = percentage_change(
        optimization_metrics[
            "urgency_weighted_completion"
        ],
        greedy_metrics[
            "urgency_weighted_completion"
        ],
    )

    print("\nRelative Changes:")

    if distance_change is not None:
        print(
            f"Travel distance change: "
            f"{distance_change:+.2f}%"
        )

    if weighted_change is not None:
        print(
            f"Urgency-weighted completion change: "
            f"{weighted_change:+.2f}%"
        )    