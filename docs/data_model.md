# Data Model

## 1. Volunteer Data

Each volunteer is represented by operational attributes that may affect dispatch decisions.

### Attributes
- `volunteer_id`: Unique volunteer identifier
- `latitude`: Current latitude
- `longitude`: Current longitude
- `first_aid`: Whether the volunteer has first-aid skills
- `driving`: Whether the volunteer can drive
- `heavy_lifting`: Whether the volunteer can perform heavy-lifting tasks
- `max_work_hours`: Maximum available working hours
- `available`: Whether the volunteer is currently available

Binary attributes use:
- `1` = Yes
- `0` = No

## 2. Task Data

Each disaster-response task is represented by operational requirements.

### Attributes
- `task_id`: Unique task identifier
- `latitude`: Task latitude
- `longitude`: Task longitude
- `urgency`: Urgency score from 1 to 5
- `required_volunteers`: Number of volunteers required
- `requires_first_aid`: Whether first-aid capability is required
- `requires_driving`: Whether driving capability is required
- `requires_heavy_lifting`: Whether heavy-lifting capability is required
- `service_hours`: Estimated service duration

## 3. Modeling Principle

Only information that may influence dispatch decisions is included in the initial model. The current dataset focuses on three major decision factors:
1. Location
2. Skill compatibility
3. Task urgency

Additional factors may be introduced in later versions, including road conditions, volunteer fatigue, transportation capacity, and uncertainty.