# Problem Definition

## 1. Background

During large-scale disasters such as floods, earthquakes, and typhoons, many rescue and recovery tasks may occur simultaneously. These tasks can include first aid, supply delivery, debris removal, evacuation assistance, and infrastructure recovery. At the same time, available volunteer resources are limited. Volunteers may differ in their locations, skills, availability, and capabilities, while disaster-response tasks may have different urgency levels, personnel requirements, and skill requirements. Therefore, assigning volunteers based only on proximity or first-come-first-served rules may not produce an effective overall response. This project studies how optimization methods can support volunteer dispatch and resource allocation under limited resources and multiple operational constraints.

## 2. Problem Scenario

Consider a disaster-affected region containing a set of pending response tasks and a limited set of available volunteers.

Each volunteer is characterized by:
- Current location
- Available skills
- Availability
- Service capacity

Each disaster-response task is characterized by:
- Location
- Urgency level
- Required number of volunteers
- Required skills
- Estimated service time

The system must determine which volunteers should be assigned to which tasks while considering both operational efficiency and disaster-response priorities.

## 3. Model Inputs

The optimization model considers two major types of input data.

### Volunteer Information
- Volunteer ID
- Current location
- Skill set
- Availability
- Maximum working time

### Task Information
- Task ID
- Task location
- Urgency level
- Required number of volunteers
- Required skills
- Estimated service duration

The travel distance or travel time between each volunteer and task is also considered.

## 4. Expected Output

The model generates a volunteer-task assignment plan specifying:
- Which volunteers are assigned to each task
- Which tasks are prioritized
- Which volunteers remain unassigned or on standby
- Which tasks cannot be served under the current resource limitations

The output should support decision-makers in allocating limited volunteer resources more effectively.

## 5. Research Question

How can limited volunteer resources be allocated to disaster-response tasks while jointly considering task urgency, travel cost, and skill requirements?

The goal is to develop an optimization-based dispatch framework that prioritizes critical disaster-response tasks while reducing unnecessary volunteer travel and ensuring that task skill requirements are satisfied.

## 6. Why Optimization?

Simple dispatch strategies, such as assigning the nearest available volunteer to each task, make decisions locally and sequentially. However, a locally optimal assignment may lead to poor overall resource allocation. For example, assigning the closest volunteer to one task may prevent that volunteer from serving another task where their skills or location would provide greater overall value. Optimization provides a systematic approach for considering all volunteer-task assignments simultaneously and finding a solution that better balances multiple objectives and constraints.