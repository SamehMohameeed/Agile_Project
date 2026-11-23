from enum import Enum
from dataclasses import dataclass

@dataclass(frozen=True)
class Course:
    hours: int

HOUR_RATE = 350
STAFF_DISCOUNT_RATE = 0.5
HIGH_FEE_THRESHOLD = 6000
HIGH_FEE_REDUCTION = 200
SUMMER_FEE = 150

class StudentType(Enum):
    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3
    

RATES = {
    StudentType.REGULAR: 1,
    StudentType.STAFF_CHILD: STAFF_DISCOUNT_RATE,
    StudentType.SCHOLARSHIP: 0,
}


def tuition_fee(courses, student_type, summer=False, discount=0, extras=()):

    rate = RATES[student_type]
    total = sum(course.hours * HOUR_RATE * rate for course in courses)
    
    if total > HIGH_FEE_THRESHOLD:
        total = total - HIGH_FEE_REDUCTION
    if summer :
        total = total + SUMMER_FEE
    total -= discount
    total += sum(extras)
    return total

def report(courses, student_type, summer=False, discount=0):
    fee = tuition_fee(courses, student_type, summer, discount)
    if student_type == StudentType.REGULAR:
        print("Student fee: " + str(fee))
    elif student_type == StudentType.STAFF_CHILD:
        print("Staff child fee: " + str(fee))
    if fee > HIGH_FEE_THRESHOLD:
        print("High fee")
    return fee

def process_all(students):
    for student in students:
        if student["type"] == StudentType.REGULAR:
            fee = tuition_fee(student["courses"], StudentType.REGULAR, student["summer"])
        if student["type"] == StudentType.STAFF_CHILD:
            fee = tuition_fee(student["courses"], StudentType.STAFF_CHILD, student["summer"])
        print(student["name"], fee)
