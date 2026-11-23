"""Tuition fee calculation module."""
from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class Course:
    """A course defined by its credit hours."""
    hours: int


HOUR_RATE = 350
STAFF_DISCOUNT_RATE = 0.5
HIGH_FEE_THRESHOLD = 6000
HIGH_FEE_REDUCTION = 200
SUMMER_FEE = 150


class StudentType(Enum):
    """Supported student categories."""
    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


RATES = {
    StudentType.REGULAR: 1,
    StudentType.STAFF_CHILD: STAFF_DISCOUNT_RATE,
    StudentType.SCHOLARSHIP: 0,
}

LABELS = {
    StudentType.REGULAR: "Student fee",
    StudentType.STAFF_CHILD: "Staff child fee",
    StudentType.SCHOLARSHIP: "Scholarship fee",
}


def tuition_fee(courses, student_type, summer=False, discount=0, extras=()):
    """Calculate the total tuition fee for a student."""
    rate = RATES[student_type]
    total = sum(course.hours * HOUR_RATE * rate for course in courses)

    if total > HIGH_FEE_THRESHOLD:
        total -= HIGH_FEE_REDUCTION
    if summer:
        total += SUMMER_FEE
    total -= discount
    total += sum(extras)
    return total


def report(courses, student_type, summer=False, discount=0):
    """Return a formatted tuition fee report."""
    fee = tuition_fee(courses, student_type, summer, discount)
    lines = [f"{LABELS[student_type]}: {fee}"]
    if fee > HIGH_FEE_THRESHOLD:
        lines.append("High fee")
    return "\n".join(lines)


def process_all(students):
    """Calculate tuition fees for all students."""
    return {
        student["name"]: tuition_fee(
            student["courses"],
            student["type"],
            student["summer"],
        )
        for student in students
    }
