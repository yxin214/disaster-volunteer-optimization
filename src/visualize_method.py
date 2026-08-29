from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = (
    BASE_DIR
    / "docs"
    / "figures"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "method_overview.png"
)


def add_box(
    ax,
    x,
    y,
    width,
    height,
    title,
    subtitle=None,
):
    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02",
        linewidth=1.5,
        fill=False,
    )

    ax.add_patch(box)

    if subtitle is None:
        ax.text(
            x + width / 2,
            y + height / 2,
            title,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

    else:
        ax.text(
            x + width / 2,
            y + height * 0.62,
            title,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
        )

        ax.text(
            x + width / 2,
            y + height * 0.30,
            subtitle,
            ha="center",
            va="center",
            fontsize=9,
        )


def add_arrow(
    ax,
    start,
    end,
):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops={
            "arrowstyle": "->",
            "linewidth": 1.5,
        },
    )


if __name__ == "__main__":
    fig, ax = plt.subplots(
        figsize=(10, 10)
    )

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # Disaster scenario
    add_box(
        ax,
        3.0,
        10.3,
        4.0,
        1.0,
        "Disaster Scenario",
        "Volunteer Supply & Task Demand",
    )

    # Input data
    add_box(
        ax,
        3.0,
        8.3,
        4.0,
        1.0,
        "Volunteer & Task Data",
        "Location · Skills · Urgency · Staffing · Working Hours",
    )

    # Modeling
    add_box(
        ax,
        3.0,
        6.3,
        4.0,
        1.0,
        "Distance & Feasibility Modeling",
        "Travel Distance · Availability · Skill & Time Feasibility",
    )

    # Greedy
    add_box(
        ax,
        0.8,
        4.1,
        3.2,
        1.1,
        "Greedy Baseline",
        "Sequential Local Assignment",
    )

    # Optimization
    add_box(
        ax,
        6.0,
        4.1,
        3.2,
        1.1,
        "Optimization Model",
        "Binary Integer Optimization",
    )

    # Assignment
    add_box(
        ax,
        3.0,
        2.1,
        4.0,
        1.0,
        "Volunteer–Task Assignment",
        "Dispatch Decisions",
    )

    # Evaluation
    add_box(
        ax,
        3.0,
        0.2,
        4.0,
        1.0,
        "Performance Evaluation",
        "Completion · Urgency-Weighted Completion · Travel Efficiency",
    )

    # Vertical arrows
    add_arrow(
        ax,
        (5.0, 10.3),
        (5.0, 9.3),
    )

    add_arrow(
        ax,
        (5.0, 8.3),
        (5.0, 7.3),
    )

    # Branch to methods
    add_arrow(
        ax,
        (4.5, 6.3),
        (2.4, 5.2),
    )

    add_arrow(
        ax,
        (5.5, 6.3),
        (7.6, 5.2),
    )

    # Methods to assignment
    add_arrow(
        ax,
        (2.4, 4.1),
        (4.3, 3.1),
    )

    add_arrow(
        ax,
        (7.6, 4.1),
        (5.7, 3.1),
    )

    # Assignment to evaluation
    add_arrow(
        ax,
        (5.0, 2.1),
        (5.0, 1.2),
    )

    fig.tight_layout()

    fig.savefig(
        OUTPUT_FILE,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

    print(
        f"Figure saved to: {OUTPUT_FILE}"
    )