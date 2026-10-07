# Appointment Booking System Database Design

## Assumptions

1. The system supports multiple patients.
2. The system supports multiple doctors.
3. Each appointment belongs to exactly one patient and exactly one doctor.
4. Each appointment has a start time and an end time.
5. Cancelled appointments are preserved instead of deleted.
6. A patient can have many appointments.
7. A doctor can have many appointments.
8. Appointment status is tracked explicitly.
9. Authentication payments prescriptions and detailed medical records are outside this mini project scope.
10. Appointment history is preserved by keeping the appointment row and changing its status.

## Schema

### patients

| Column | Type | Constraint |
|---|---|---|
| patient_id | INTEGER | PRIMARY KEY |
| full_name | TEXT | NOT NULL |
| email | TEXT | UNIQUE |
| phone | TEXT |  |
| created_at | TEXT | NOT NULL |

### doctors

| Column | Type | Constraint |
|---|---|---|
| doctor_id | INTEGER | PRIMARY KEY |
| full_name | TEXT | NOT NULL |
| specialty | TEXT |  |
| created_at | TEXT | NOT NULL |

### appointments

| Column | Type | Constraint |
|---|---|---|
| appointment_id | INTEGER | PRIMARY KEY |
| patient_id | INTEGER | NOT NULL FK |
| doctor_id | INTEGER | NOT NULL FK |
| start_time | TEXT | NOT NULL |
| end_time | TEXT | NOT NULL |
| status | TEXT | NOT NULL |
| created_at | TEXT | NOT NULL |

## Relationship Diagram

```text
patients 1 --------< appointments >-------- 1 doctors
```

A patient can have many appointments while every appointment points to one patient

A doctor can have many appointments while every appointment points to one doctor

## Recommended Appointment Status Values

- SCHEDULED
- COMPLETED
- CANCELLED
- NO_SHOW

## Design Decisions

### Why appointments are a separate table

The relationship between a patient and a doctor has its own attributes such as time duration and status so it should be modeled as a separate entity

### Why cancelled appointments are preserved

Deleting cancelled appointments would remove useful booking history and make later auditing harder

### Why foreign keys are used

Foreign keys protect referential integrity and prevent appointments from referencing patients or doctors that do not exist

### Why status is stored on the appointment

The status values are small and stable for this project so a separate status table would add unnecessary complexity

### Why start and end times are stored

Keeping both values makes duration and scheduling validation straightforward

This design is intentionally small because the task focuses on backend foundations rather than a complete medical system
