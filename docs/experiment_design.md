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