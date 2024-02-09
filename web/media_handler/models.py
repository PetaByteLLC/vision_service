from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Float
from web.database.base_model import AbstractBase, Base
from web.media_handler.schemas import MediaSchema

from datetime import datetime


class Media(AbstractBase):
    """
    The Media class you've provided is a SQLAlchemy ORM model for a database table named "media".
    It is designed to store various attributes of media, specifically related to car information.\
    This class extends AbstractBase, which implies it inherits common base properties for ORM models.
    The __pydantic_model__ attribute indicates the use of Pydantic models for data validation and serialization.
    Here's an overview of each attribute and the to_read_model method:
    """
    __tablename__ = "media"
    __pydantic_model__ = MediaSchema

    url: Mapped[str] = mapped_column(String(500), nullable=True)
    car_type_body: Mapped[str] = mapped_column(String(500), nullable=True)
    car_type_body_score: Mapped[str] = mapped_column(Float(), nullable=True)
    car_color: Mapped[str] = mapped_column(String(500), nullable=True)
    car_color_score: Mapped[str] = mapped_column(Float(), nullable=True)
    car_brand: Mapped[str] = mapped_column(String(500), nullable=True)
    car_brand_score: Mapped[str] = mapped_column(Float(), nullable=True)
    license_plate_number: Mapped[str] = mapped_column(String(500), nullable=True)
    license_plate_number_score: Mapped[str] = mapped_column(Float(), nullable=True)
    license_plate_country: Mapped[str] = mapped_column(String(500), nullable=True)
    license_plate_country_score: Mapped[str] = mapped_column(Float(), nullable=True)

    def to_read_model(self):
        return self.__pydantic_model__(
            id=self.id,
            url=self.url,
            result=self.result,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
