# app/models/calculation.py

from enum import Enum

from sqlalchemy import Column, Float, Integer, String, CheckConstraint

from app.database import Base


class CalculationType(str, Enum):
    ADD = "Add"
    SUBTRACT = "Sub"
    MULTIPLY = "Multiply"
    DIVIDE = "Divide"


class Calculation(Base):
    __tablename__ = "calculations"

    id = Column(Integer, primary_key=True, index=True)
    a = Column(Float, nullable=False)
    b = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)
    result = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "type IN ('Add', 'Sub', 'Multiply', 'Divide')",
            name="valid_calculation_type",
        ),
        CheckConstraint(
            "type != 'Divide' OR b != 0",
            name="no_division_by_zero",
        ),
    )

    def __repr__(self):
        return (
            f"<Calculation(id={self.id}, "
            f"type={self.type}, result={self.result})>"
        )
