# app/schemas/calculation.py

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FiniteFloat,
    model_validator,
)

from app.models.calculation import CalculationType


class CalculationCreate(BaseModel):
    a: FiniteFloat = Field(..., strict=True)
    b: FiniteFloat = Field(..., strict=True)
    type: CalculationType

    @model_validator(mode="after")
    def validate_division(self):
        if self.type == CalculationType.DIVIDE and self.b == 0:
            raise ValueError("Cannot divide by zero")
        return self


class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: CalculationType
    result: float

    model_config = ConfigDict(from_attributes=True)
