Max_Grade = 100
Min_Grade = 0
A_Grade = 90
B_Grade = 80
C_Grade = 70
D_Grade = 60


def letter_grade(score):
    if score < Min_Grade or score > Max_Grade:
        raise ValueError("Score must be between 0 and 100")

    if score >= A_Grade:
        return "A"

    elif score >= B_Grade:
        return "B"

    elif score >= C_Grade:
        return "C"

    elif score >= D_Grade:
        return "D"

    else:
        return "F"
