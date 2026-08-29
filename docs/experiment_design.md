# Experiment Design

## 1. Objective

The experiment compares a greedy nearest-assignment baseline with the proposed optimization-based volunteer dispatch model. The purpose is to evaluate whether global optimization can improve disaster-response resource allocation when volunteer resources are limited.

## 2. Compared Methods

### Greedy Baseline
Tasks are processed sequentially in descending order of urgency. For each task, the nearest available and eligible volunteers are selected.

### Optimization Model
All volunteer-task assignments are considered simultaneously using a binary integer programming model.

The model jointly considers:
- Task urgency
- Travel distance
- Personnel requirements
- Volunteer availability
- Working-time feasibility
- Skill coverage

## 3. Evaluation Metrics

The methods are evaluated using:
- Total travel distance
- Number of completed tasks
- Task completion rate
- Urgency-weighted completion rate

## 4. Initial Experimental Setting

The initial experiment uses:
- 10 volunteers
- 5 disaster-response tasks
- Three skill categories
- Task urgency scores ranging from 1 to 5
- Geographic travel distances calculated using the Haversine formula

This small instance is used to verify model correctness before larger-scale experiments are conducted.

## 5. Research Question

Does global optimization produce better overall disaster-response resource allocation than sequential greedy assignment, particularly under limited volunteer resources?

## 6. Initial Case Study Results

In the initial synthetic scenario containing 10 volunteers and 5 disaster-response tasks, the greedy baseline completed 4 of 5 tasks, while the optimization model successfully completed all 5 tasks.

The greedy method produced a total volunteer travel distance of 14.92 km, whereas the optimization model reduced the total travel distance to 12.03 km, corresponding to an approximately 19.37% reduction. The task completion rate increased from 80% to 100%, while the urgency-weighted completion rate increased from 89.47% to 100%.

At the task level, the greedy method failed to serve Task T04 because volunteer resources had already been allocated to earlier tasks. In contrast, the optimization model considered all assignments simultaneously and reallocated volunteers globally, allowing all tasks to be completed with a lower total travel distance.

These preliminary results demonstrate the potential advantage of global optimization over sequential greedy assignment. However, the current result is based on a single synthetic instance and should be treated as a proof-of-concept rather than a general performance conclusion.

## 7. Multi-Scenario Experimental Results

To evaluate the robustness of the proposed optimization model, three volunteer supply conditions were tested: resource-rich, balanced, and resource-scarce. Each scenario contained 30 randomly generated problem instances, resulting in 90 instances and 180 method evaluations across the greedy and optimization approaches.

Across all three supply conditions, the optimization model achieved higher average task completion rates and urgency-weighted completion rates than the greedy baseline.

Under the resource-rich condition, task completion increased from 96.33% to 99.67%, while urgency-weighted completion increased from 97.90% to 99.89%. The optimization model also reduced average travel distance from 18.88 km to 17.00 km.

Under the balanced condition, the optimization model produced the largest improvement in task completion, increasing the completion rate from 87.33% to 98.33%. Urgency-weighted completion also increased from 93.04% to 99.21%. This improvement required a moderate increase in average travel distance from 21.18 km to 22.04 km, illustrating a trade-off between service coverage and travel cost.

Under the resource-scarce condition, the optimization model improved task completion from 64.00% to 72.67% and urgency-weighted completion from 78.66% to 85.89%, while slightly reducing average travel distance from 16.77 km to 16.42 km.

The results indicate that global optimization provides limited additional benefit when volunteer resources are abundant, because the greedy baseline can already satisfy most tasks. In contrast, its advantage becomes substantially more pronounced when resources are constrained. The largest improvement was observed in the balanced condition, where allocation decisions were sufficiently constrained to make local greedy choices consequential, while enough resources remained for improved global coordination to recover additional tasks.

The optimization model also exhibited consistently lower standard deviations in both completion rate and urgency-weighted completion across all three scenarios, suggesting more stable performance across randomly generated problem instances.

These findings suggest that the value of global optimization is particularly significant when available resources are constrained enough to require careful allocation, but not so scarce that unmet demand becomes unavoidable.