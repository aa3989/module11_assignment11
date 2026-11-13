# app/operations/factory.py

from collections.abc import Callable

from app.models.calculation import CalculationType
from app.operations import add, subtract, multiply, divide


class CalculationFactory:
    OPERATIONS: dict[CalculationType, Callable] = {
        CalculationType.ADD: add,
        CalculationType.SUBTRACT: subtract,
        CalculationType.MULTIPLY: multiply,
        CalculationType.DIVIDE: divide,
    }

    @classmethod
    def get_operation(cls, operation_type):
        try:
            selected_type = CalculationType(operation_type)
            return cls.OPERATIONS[selected_type]
        except (ValueError, KeyError):
            raise ValueError(
                f"Unsupported calculation type: {operation_type}"
            ) from None

    @classmethod
    def calculate(cls, a, b, operation_type):
        operation = cls.get_operation(operation_type)
        return operation(a, b)
