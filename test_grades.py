import pytest

from grades import letter_grade


def test_ninety_is_an_a():
    assert letter_grade(90) == "A"

def test_eighty_nine_is_a_b():
    assert letter_grade(89) == "B"

def test_below_sixty_fails():
    assert letter_grade(59) == "F"

def test_score_above_100_is_rejected():
    with pytest.raises(ValueError):
        letter_grade(101)
        
def test_score_is_0_is_a_f():
    assert letter_grade(0) == "F"

def test_score_is_100_is_an_a():
    assert letter_grade(100) == "A"
    
def test_score_is_60_is_a_d():
    assert letter_grade(60) == "D"

def test_score_is_70_is_a_c():
    assert letter_grade(70) == "C"
    
def test_score_is_negative_1_is_rejected():
    with pytest.raises(ValueError):
        letter_grade(-1)
    