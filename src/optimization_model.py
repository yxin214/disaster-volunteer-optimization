from pathlib import Path
import pandas as pd
from ortools.linear_solver import pywraplp

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"

VOLUNTEERS_FILE = DATA_DIR / "volunteers.csv"
TASKS_FILE = DATA_DIR / "tasks.csv"
DISTANCE_FILE = DATA_DIR / "distance_matrix.csv"

OUTPUT_FILE = RESULTS_DIR / "optimization_assignment.csv"

def load_data():
    volunteers = pd.read_csv(VOLUNTEERS_FILE)
    tasks = pd.read_csv(TASKS_FILE)

    distance_matrix = pd.read_csv(
        DISTANCE_FILE,
        index_col="volunteer_id"
    )

    return volunteers, tasks, distance_matrix

def solve_optimization(volunteers, tasks, distance_matrix, alpha=10.0, beta=1.0):
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if solver is None:
        raise RuntimeError("SCIP solver is not available.")
    
    volunteer_ids = volunteers["volunteer_id"].tolist()
    task_ids = tasks["task_id"].tolist()

    x = {}

    for volunteer_id in volunteer_ids:
        for task_id in task_ids:
            x[volunteer_id, task_id] = solver.BoolVar(
                f"x_{volunteer_id}_{task_id}"
            )

    y = {}

    for task_id in task_ids:
        y[task_id] = solver.BoolVar(
            f"y_{task_id}"
        )   

    for volunteer_id in volunteer_ids:
        solver.Add(
            sum(
                x[volunteer_id, task_id]
                for task_id in task_ids
            ) <= 1
        ) 

    for _, volunteer in volunteers.iterrows():
        volunteer_id = volunteer["volunteer_id"]

        if volunteer["available"] != 1:
            for task_id in task_ids:
                solver.Add(
                    x[volunteer_id, task_id] == 0
                ) 

    for _, volunteer in volunteers.iterrows():
        volunteer_id = volunteer["volunteer_id"]

        for _, task in tasks.iterrows():
            task_id = task["task_id"]

            if (
                task["service_hours"]
                > volunteer["max_work_hours"]
            ):
                solver.Add(
                    x[volunteer_id, task_id] == 0
                )    

    for _, task in tasks.iterrows():
        task_id = task["task_id"]
        required = int(task["required_volunteers"])

        solver.Add(
            sum(
                x[volunteer_id, task_id]
                for volunteer_id in volunteer_ids
            )
            ==
            required * y[task_id]
        )             

    for _, task in tasks.iterrows():
        task_id = task["task_id"]

        if task["requires_first_aid"] == 1:
            solver.Add(
                sum(
                    volunteers.loc[
                        volunteers["volunteer_id"]
                        == volunteer_id,
                        "first_aid"
                    ].iloc[0]
                    * x[volunteer_id, task_id]
                    for volunteer_id in volunteer_ids
                )
                >= y[task_id]
            )    

    for _, task in tasks.iterrows():
        task_id = task["task_id"]

        if task["requires_driving"] == 1:
            solver.Add(
                sum(
                    volunteers.loc[
                        volunteers["volunteer_id"]
                        == volunteer_id,
                        "driving"
                    ].iloc[0]
                    * x[volunteer_id, task_id]
                    for volunteer_id in volunteer_ids
                )
                >= y[task_id]
            )

        if task["requires_heavy_lifting"] == 1:
            solver.Add(
                sum(
                    volunteers.loc[
                        volunteers["volunteer_id"]
                        == volunteer_id,
                        "heavy_lifting"
                    ].iloc[0]
                    * x[volunteer_id, task_id]
                    for volunteer_id in volunteer_ids
                )
                >= y[task_id]
            )    
     
    urgency_reward = sum(
        alpha
        * task["urgency"]
        * y[task["task_id"]]
        for _, task in tasks.iterrows()
    )            

    travel_cost = sum(
        beta
        * distance_matrix.loc[
            volunteer_id,
            task_id
        ]
        * x[volunteer_id, task_id]
        for volunteer_id in volunteer_ids
        for task_id in task_ids
    )     

    solver.Maximize(
        urgency_reward - travel_cost
    )       

    status = solver.Solve() 

    assignments = []

    if status in (
        pywraplp.Solver.OPTIMAL,
        pywraplp.Solver.FEASIBLE,
    ):
        for volunteer_id in volunteer_ids:
            for task_id in task_ids:
                if (
                    x[
                        volunteer_id,
                        task_id
                    ].solution_value()
                    > 0.5
                ):
                    assignments.append(
                        {
                            "volunteer_id": volunteer_id,
                            "task_id": task_id,
                            "distance_km":
                                distance_matrix.loc[
                                    volunteer_id,
                                    task_id
                                ],
                        }
                    )                                               

        print("\nCompleted Tasks:")

        for task_id in task_ids:
            if y[task_id].solution_value() > 0.5:
                print(f"{task_id}: completed")
            else:
                print(f"{task_id}: not completed")

    else:
        print("No feasible solution found.")

    return pd.DataFrame(assignments), solver  

if __name__ == "__main__":
    RESULTS_DIR.mkdir(exist_ok=True)

    volunteers, tasks, distance_matrix = load_data()

    result, solver = solve_optimization(
        volunteers,
        tasks,
        distance_matrix
    )

    print("\nOptimization Assignment:")
    print(result)

    if not result.empty:
        total_distance = result["distance_km"].sum()

        print(
            f"\nTotal travel distance: "
            f"{total_distance:.2f} km"
        )

        result.to_csv(
            OUTPUT_FILE,
            index=False
        )

        print(
            f"Assignment saved to: "
            f"{OUTPUT_FILE}"
        )

    print(
        f"\nObjective value: "
        f"{solver.Objective().Value():.2f}"
    )              