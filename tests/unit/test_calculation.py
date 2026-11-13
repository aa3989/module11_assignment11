# tests/unit/test_calculation.py

import math

import pytest
from pydantic import ValidationError

from app.models.calculation import CalculationType
from app.operations.factory import CalculationFactory
from app.schemas.calculation import CalculationCreate
from app.models.calculation import Calculation

@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("Add", 10, 5, 15),
        ("Sub", 10, 5, 5),
        ("Multiply", 10, 5, 50),
        ("Divide", 10, 5, 2),
        ("Add", -5, 3, -2),
        ("Multiply", 2.5, 4, 10),
    ],
)
def test_calculation_factory(operation, a, b, expected):
    result = CalculationFactory.calculate(a, b, operation)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "operation,expected_type",
    [
        ("Add", CalculationType.ADD),
        ("Sub", CalculationType.SUBTRACT),
        ("Multiply", CalculationType.MULTIPLY),
        ("Divide", CalculationType.DIVIDE),
    ],
)
def test_valid_calculation_schema(operation, expected_type):
    calculation = CalculationCreate(
        a=10,
        b=5,
        type=operation,
    )

    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == expected_type


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"a": 10, "b": 5, "type": "Power"},
        {"a": 10, "b": 0, "type": "Divide"},
        {"a": "hello", "b": 5, "type": "Add"},
        {"a": "10", "b": 5, "type": "Add"},
        {"a": math.inf, "b": 5, "type": "Add"},
        {"a": 10, "b": math.nan, "type": "Add"},
        {"a": 10, "type": "Add"},
    ],
)
def test_invalid_calculation_schema(invalid_data):
    with pytest.raises(ValidationError):
        CalculationCreate(**invalid_data)


def test_factory_rejects_invalid_operation():
    with pytest.raises(ValueError, match="Unsupported"):
        CalculationFactory.get_operation("Power")


def test_factory_rejects_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        CalculationFactory.calculate(10, 0, "Divide")


def test_factory_selects_correct_function():
    operation = CalculationFactory.get_operation("Add")

    assert operation(7, 3) == 10

def test_calculation_repr():
    calculation = Calculation(
        a=10,
        b=5,
        type="Add",
        result=15,
    )
    calculation.id = 1

    text = repr(calculation)

    assert "Calculation" in text
    assert "Add" in text
    assert "15" in text
