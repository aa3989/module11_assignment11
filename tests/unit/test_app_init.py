# tests/unit/test_app_init.py

import runpy
from pathlib import Path
from unittest.mock import patch

import app


def test_init_db():
    """Verify database initialization creates tables."""
    with patch.object(app.Base.metadata, "create_all") as mock_create:
        app.init_db()

    mock_create.assert_called_once_with(bind=app.engine)


def test_drop_db():
    """Verify database cleanup drops tables."""
    with patch.object(app.Base.metadata, "drop_all") as mock_drop:
        app.drop_db()

    mock_drop.assert_called_once_with(bind=app.engine)



def test_app_main():
    """Verify running app/__init__.py initializes the database."""
    app_init_path = Path(app.__file__)

    with patch("sqlalchemy.schema.MetaData.create_all") as mock_create:
        runpy.run_path(str(app_init_path), run_name="__main__")

    # Verify create_all was called exactly once.
    mock_create.assert_called_once()

    # Verify the database engine was provided.
    call_kwargs = mock_create.call_args.kwargs
    assert "bind" in call_kwargs

    # Verify the correct database URL was used.
    assert str(call_kwargs["bind"].url) == str(app.engine.url)

