# tests/integration/test_calculation.py

import pytest

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models.calculation import Calculation
from app.operations.factory import CalculationFactory
from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead,
)


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        ("Add", 10, 5, 15),
        ("Sub", 10, 5, 5),
        ("Multiply", 10, 5, 50),
        ("Divide", 10, 5, 2),
    ],
)
def test_save_calculation(
    db_session, operation, a, b, expected
):
    data = CalculationCreate(
        a=a,
        b=b,
        type=operation,
    )

    result = CalculationFactory.calculate(
        data.a,
        data.b,
        data.type,
    )

    record = Calculation(
        a=data.a,
        b=data.b,
        type=data.type.value,
        result=result,
    )

    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)

    assert record.id is not None
    assert record.a == pytest.approx(a)
    assert record.b == pytest.approx(b)
    assert record.type == operation
    assert record.result == pytest.approx(expected)

    stored = db_session.scalar(
        select(Calculation).where(
            Calculation.id == record.id
        )
    )

    assert stored is not None
    assert stored.result == pytest.approx(expected)


def test_calculation_read_schema(db_session):
    record = Calculation(
        a=20,
        b=4,
        type="Divide",
        result=5,
    )

    db_session.add(record)
    db_session.commit()
    db_session.refresh(record)

    response = CalculationRead.model_validate(record)

    assert response.id == record.id
    assert response.a == 20
    assert response.b == 4
    assert response.type.value == "Divide"
    assert response.result == 5

    assert "password_hash" not in response.model_dump()


@pytest.mark.parametrize(
    "operation,a,b,result",
    [
        ("Power", 2, 3, 8),
        ("Divide", 10, 0, 0),
    ],
)
def test_database_rejects_invalid_calculation(
    db_session, operation, a, b, result
):
    record = Calculation(
        a=a,
        b=b,
        type=operation,
        result=result,
    )

    db_session.add(record)

    with pytest.raises(IntegrityError):
        db_session.commit()

    db_session.rollback()

    assert db_session.scalar(
        select(Calculation)
    ) is None
