from pathlib import Path
import pandas as pd

from run_multi_scenario import (
    generate_tasks,
    calculate_volunteer_count,
    generate_volunteers,
    build_distance_matrix,
    optimization_assignment,
    evaluate,
)

import random

BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_DIR = (
    BASE_DIR
    / "results"
    / "sensitivity"
)

RESULTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

ALPHA_VALUES = [
    0.5,
    1.0,
    2.0,
    5.0,
    10.0,
    20.0,
    50.0,
]

BETA = 1.0

SUPPLY_RATIO = 1.0
NUM_TASKS = 10
REPETITIONS = 30

def run_sensitivity_analysis():
    results = []

    for seed in range(REPETITIONS):
        rng = random.Random(seed)

        tasks = generate_tasks(
            NUM_TASKS,
            rng,
        )

        num_volunteers, total_demand = (
            calculate_volunteer_count(
                tasks,
                SUPPLY_RATIO,
            )
        )

        volunteers = generate_volunteers(
            num_volunteers,
            rng,
        )

        distance_matrix = (
            build_distance_matrix(
                volunteers,
                tasks,
            )
        )

        for alpha in ALPHA_VALUES:
            assignment = (
                optimization_assignment(
                    volunteers,
                    tasks,
                    distance_matrix,
                    alpha=alpha,
                    beta=BETA,
                )
            )

            metrics = evaluate(
                assignment,
                tasks,
            )

            results.append(
                {
                    "seed": seed,
                    "alpha": alpha,
                    "beta": BETA,
                    "supply_ratio":
                        SUPPLY_RATIO,
                    "num_tasks":
                        NUM_TASKS,
                    "num_volunteers":
                        num_volunteers,
                    "total_demand":
                        total_demand,
                    **metrics,
                }
            )     

    return pd.DataFrame(results)      

if __name__ == "__main__":
    results = (
        run_sensitivity_analysis()
    )

    results_file = (
        RESULTS_DIR
        / "sensitivity_results.csv"
    )

    results.to_csv(
        results_file,
        index=False,
    )

    metrics = [
        "total_distance_km",
        "completion_rate",
        "urgency_weighted_completion",
        "distance_per_completed_task",
        "distance_per_completed_urgency",
    ]

    summary = (
        results.groupby("alpha")[metrics]
        .agg(["mean", "std"])
        .round(4)
    )    

    summary.columns = [
        f"{metric}_{stat}"
        for metric, stat
        in summary.columns
    ]

    summary = summary.reset_index()     

    summary_file = (
        RESULTS_DIR
        / "sensitivity_summary.csv"
    )

    summary.to_csv(
        summary_file,
        index=False,
    )

    print("\nSensitivity Summary:")
    print(summary.to_string(index=False))

    print(
        f"\nSummary saved to: "
        f"{summary_file}"
    )       

    print(
        f"\nTotal rows: {len(results)}"
    )

    print(
        f"Results saved to: "
        f"{results_file}"
    )         