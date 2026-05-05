from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Central registry for all ORM models.
    Every model must inherit from this Base.
    """
    pass
