from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    BASE_DIR
    / "results"
    / "multi_scenario"
    / "multi_scenario_results.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "figures"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

SCENARIO_ORDER = [
    "resource_rich",
    "balanced",
    "resource_scarce",
]

SCENARIO_LABELS = [
    "Resource-rich\n(R = 1.3)",
    "Balanced\n(R = 1.0)",
    "Resource-scarce\n(R = 0.7)",
]

def plot_metric(
    results,
    metric,
    ylabel,
    title,
    filename,
    ylim=None,
):
    summary = (
        results.groupby(
            ["scenario", "method"]
        )[metric]
        .agg(["mean", "std"])
        .reset_index()
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    x_positions = list(
        range(len(SCENARIO_ORDER))
    )

    for method in [
        "Greedy",
        "Optimization",
    ]:
        means = []
        stds = []

        for scenario in SCENARIO_ORDER:
            row = summary[
                (summary["scenario"] == scenario)
                & (summary["method"] == method)
            ]

            means.append(
                row["mean"].iloc[0]
            )

            stds.append(
                row["std"].iloc[0]
            )

        ax.errorbar(
            x_positions,
            means,
            yerr=stds,
            marker="o",
            capsize=4,
            label=method,
        )

    ax.set_xticks(
        x_positions,
        SCENARIO_LABELS
    )

    ax.set_xlabel(
        "Volunteer Supply Condition"
    )

    if ylim is not None:
        ax.set_ylim(ylim)

    ax.set_ylabel(ylabel)

    ax.set_title(title)

    ax.legend()

    ax.grid(
        axis="y",
        alpha=0.3
    )

    fig.tight_layout()

    output_path = (
        OUTPUT_DIR / filename
    )

    fig.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(
        f"Figure saved to: "
        f"{output_path}"
    ) 

if __name__ == "__main__":
    results = pd.read_csv(
        RESULTS_FILE
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

    summary.columns = [
        f"{metric}_{stat}"
        for metric, stat in summary.columns
    ]

    summary = summary.reset_index()

    summary_file = (
        BASE_DIR
        / "results"
        / "multi_scenario"
        / "summary_results.csv"
    )

    summary.to_csv(summary_file, index=False)

    print(
        f"Summary saved to: "
        f"{summary_file}"
    )    

    plot_metric(
        results=results,
        metric="completion_rate",
        ylabel="Task Completion Rate",
        title=(
            "Task Completion Rate "
            "under Different Supply Conditions"
        ),
        filename="completion_rate.png",
        ylim=(0.5, 1.05),
    )   

    plot_metric(
        results=results,
        metric="urgency_weighted_completion",
        ylabel=(
            "Urgency-Weighted "
            "Completion Rate"
        ),
        title=(
            "Urgency-Weighted Completion "
            "under Different Supply Conditions"
        ),
        filename="urgency_weighted_completion.png",
        ylim=(0.5, 1.05),
    )

    plot_metric(
        results=results,
        metric="distance_per_completed_task",
        ylabel="Distance per Completed Task (km)",
        title=(
            "Travel Efficiency "
            "under Different Supply Conditions"
        ),
        filename="distance_per_completed_task.png",
    )          