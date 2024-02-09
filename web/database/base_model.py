from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AbstractBase(Base):
    """
    The provided code defines an abstract base class AbstractBase for SQLAlchemy ORM models.
    This class is designed to be inherited by other SQLAlchemy models and provides a common set of attributes and an abstract method.
    Here's a breakdown of its components:
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    @abstractmethod
    def to_read_model(self):
        raise NotImplementedError
