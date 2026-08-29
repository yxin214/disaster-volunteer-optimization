from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

RESULTS_FILE = (
    BASE_DIR
    / "results"
    / "sensitivity"
    / "sensitivity_results.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "figures"
    / "sensitivity"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

def plot_sensitivity(
    results,
    metric,
    ylabel,
    title,
    filename,
    ylim=None,
):
    summary = (
        results.groupby("alpha")[metric]
        .agg(["mean", "std"])
        .reset_index()
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    ax.errorbar(
        summary["alpha"],
        summary["mean"],
        yerr=summary["std"],
        marker="o",
        capsize=4,
    )

    ax.set_xscale("log")

    ax.set_xticks(
        summary["alpha"]
    )

    ax.set_xticklabels(
        [
            str(value)
            for value in summary["alpha"]
        ]
    )

    ax.set_xlabel(
        "Urgency Priority Weight (α)"
    )

    ax.set_ylabel(ylabel)

    ax.set_title(title)

    if ylim is not None:
        ax.set_ylim(ylim)

    ax.grid(
        axis="y",
        alpha=0.3,
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

    plot_sensitivity(
        results=results,
        metric="completion_rate",
        ylabel="Task Completion Rate",
        title=(
            "Sensitivity of Task Completion "
            "to Urgency Priority Weight"
        ),
        filename=(
            "alpha_completion_rate.png"
        ),
        ylim=(0.3, 1.05),
    )    

    plot_sensitivity(
        results=results,
        metric=(
            "urgency_weighted_completion"
        ),
        ylabel=(
            "Urgency-Weighted Completion Rate"
        ),
        title=(
            "Sensitivity of Urgency-Weighted "
            "Completion to Priority Weight"
        ),
        filename=(
            "alpha_urgency_completion.png"
        ),
        ylim=(0.4, 1.05),
    )    

    plot_sensitivity(
        results=results,
        metric="total_distance_km",
        ylabel="Total Travel Distance (km)",
        title=(
            "Sensitivity of Travel Distance "
            "to Urgency Priority Weight"
        ),
        filename=(
            "alpha_travel_distance.png"
        ),
    )    