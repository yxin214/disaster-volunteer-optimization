# Greedy Baseline Method

## 1. Purpose

A greedy nearest-assignment strategy is implemented as a baseline for evaluating the optimization model. The baseline simulates a simple dispatch rule that may be used in practice when decisions are made sequentially without global optimization.

## 2. Assignment Strategy

Tasks are processed in descending order of urgency.

For each task, the algorithm:
1. Identifies currently available volunteers.
2. Removes volunteers who have already been assigned.
3. Removes volunteers whose available working time is shorter than the estimated task duration.
4. Removes volunteers who do not satisfy the required skills.
5. Sorts the remaining volunteers by travel distance.
6. Assigns the nearest volunteers until the required personnel count is reached.

## 3. Evaluation Metrics

The baseline is evaluated using:
- Total travel distance
- Number of completed tasks
- Task completion rate
- Urgency-weighted completion rate

## 4. Limitation

The greedy method makes assignments sequentially and locally. Although each assignment may appear optimal at the time it is made, the resulting overall allocation is not guaranteed to be globally optimal. A volunteer selected for one task may be more valuable for another task later in the assignment process. This limitation motivates the development of a global optimization model.