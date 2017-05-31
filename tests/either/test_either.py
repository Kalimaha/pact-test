from pact_test.either import *


def test_left_value():
    l = Left(42)
    assert l.value == 42


def test_right_value():
    r = Right(42)
    assert r.value == 42


def test_concat_right():
    out = minus_one(45) >> minus_one >> minus_one
    assert out.value == 42


def test_concat_left():
    out = minus_one(1) >> one_divided_by
    assert out.value == "Division by zero."


def test_break_the_chain():
    out = minus_one(1) >> one_divided_by >> minus_one
    assert out.value == "Division by zero."


def test_multiple_parameters():
    out = minus_one(9).concat(my_sum, 5)
    assert out.value == 13


def minus_one(value):
    return Right(value - 1)


def one_divided_by(value):
    try:
        result = Right(1 / value)
    except ZeroDivisionError:
        result = Left("Division by zero.")
    return result


def my_sum(a, b):
    return Right(a + b)
