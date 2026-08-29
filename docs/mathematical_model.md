# Mathematical Model

## 1. Overview

The disaster volunteer dispatch problem is formulated as a binary integer optimization problem. The model determines the assignment of available volunteers to disaster-response tasks while considering travel distance, task urgency, personnel requirements, skill requirements, and volunteer availability. The objective is to allocate limited volunteer resources efficiently while prioritizing critical disaster-response tasks.

## 2. Sets

Let:
- \(V = \{1,2,\ldots,n\}\): set of volunteers
- \(T = \{1,2,\ldots,m\}\): set of disaster-response tasks

Indices:
- \(i \in V\): volunteer index
- \(j \in T\): task index

## 3. Parameters

The following parameters are known before optimization:
- \(d_{ij}\): travel distance from volunteer \(i\) to task \(j\)
- \(u_j\): urgency score of task \(j\)
- \(r_j\): required number of volunteers for task \(j\)
- \(a_i\): availability of volunteer \(i\), where 1 indicates available and 0 indicates unavailable
- \(h_i\): maximum available working hours of volunteer \(i\)
- \(s_j\): estimated service duration of task \(j\)

## 4. Decision Variables

### Volunteer Assignment
\[
x_{ij} =
\begin{cases}
1, & \text{if volunteer } i \text{ is assigned to task } j \\
0, & \text{otherwise}
\end{cases}
\]

### Task Completion
\[
y_j =
\begin{cases}
1, & \text{if task } j \text{ is completed} \\
0, & \text{otherwise}
\end{cases}
\]

where:
\[
x_{ij}, y_j \in \{0,1\}
\]

## 5. Objective Function

The model seeks to prioritize urgent disaster-response tasks while reducing unnecessary volunteer travel.

The objective is formulated as:
\[
\max
\left(
\alpha \sum_{j \in T} u_j y_j
-
\beta \sum_{i \in V}\sum_{j \in T} d_{ij}x_{ij}
\right)
\]

where:
- \(\alpha\) controls the importance of task urgency and completion.
- \(\beta\) controls the importance of travel distance.

The first term rewards the completion of high-urgency tasks, while the second term penalizes excessive volunteer travel.

## 6. Constraints

### 6.1 One-Task-Per-Volunteer Constraint
Each volunteer can be assigned to at most one task:
\[
\sum_{j \in T} x_{ij} \leq 1
\qquad \forall i \in V
\]

### 6.2 Volunteer Availability Constraint
Unavailable volunteers cannot be assigned:
\[
x_{ij} \leq a_i
\qquad \forall i \in V,\; j \in T
\]

### 6.3 Task Staffing and Completion Constraint
Volunteers are assigned to a task only when the task is completed, and the required personnel count must be satisfied:
\[
\sum_{i \in V} x_{ij}
=
r_j y_j
\qquad \forall j \in T
\]

If \(y_j=1\), exactly \(r_j\) volunteers must be assigned.
If \(y_j=0\), no volunteers are assigned to the task.

### 6.4 Working-Time Feasibility Constraint

A volunteer cannot be assigned to a task whose service duration exceeds the volunteer's available working time:
\[
x_{ij}=0
\qquad
\text{if } s_j>h_i
\]

### 6.5 Skill Coverage Constraints

Let:
- \(f_i\): 1 if volunteer \(i\) has first-aid skills
- \(d_i\): 1 if volunteer \(i\) has driving skills
- \(l_i\): 1 if volunteer \(i\) has heavy-lifting capability

Let:
- \(F_j\): 1 if task \(j\) requires first-aid capability
- \(D_j\): 1 if task \(j\) requires driving capability
- \(L_j\): 1 if task \(j\) requires heavy-lifting capability

For every completed task requiring a particular skill, at least one assigned volunteer must possess that skill.

First aid:
\[
\sum_{i \in V} f_i x_{ij}
\geq
F_j y_j
\qquad \forall j \in T
\]

Driving:
\[
\sum_{i \in V} d_i x_{ij}
\geq
D_j y_j
\qquad \forall j \in T
\]

Heavy lifting:
\[
\sum_{i \in V} l_i x_{ij}
\geq
L_j y_j
\qquad \forall j \in T
\]

## 7. Model Assumptions

The initial optimization model makes the following simplifying assumptions:
1. Volunteer and task locations are known before dispatch.
2. Travel distance is estimated using geographic distance and does not yet account for road-network disruptions.
3. Each volunteer can participate in at most one task during a single optimization period.
4. Each completed task requires a fixed number of volunteers.
5. A required skill must be covered by at least one assigned volunteer.
6. Task urgency is represented using a predefined score from 1 to 5.
7. Travel conditions and task requirements are deterministic during each optimization run.

These assumptions provide a controlled baseline formulation. Future extensions may incorporate road accessibility, dynamic task arrivals, uncertainty, volunteer fatigue, transportation capacity, and repeated dispatch periods.