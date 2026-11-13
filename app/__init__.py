from app.database import Base, engine
import app.models  # Register model tables with Base.metadata


def init_db():
    Base.metadata.create_all(bind=engine)


def drop_db():
    Base.metadata.drop_all(bind=engine)


if __name__ == "__main__":
    init_db()
