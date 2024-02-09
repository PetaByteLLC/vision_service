from dataclasses import dataclass
from pydantic import BaseModel
from enum import Enum


"""
The provided code defines several Pydantic models and an Enum related to media handling in a web application,
as well as a dataclass for car attributes.
Here's a breakdown of each component:
"""


class MediaType(Enum):
    PHOTO = 1
    VIDEO = 2


class MediaSchema(BaseModel):
    id: int
    url: str
    result: int
    created_at: str
    updated_at: str


class MediaCreateSchema(BaseModel):
    url: str
    result: int


class MediaUpdateSchema(BaseModel):
    title: str
    url: str
    media_type: MediaType
    result: int


class MediaDetailSchema(BaseModel):
    id: int
    title: str
    url: str
    media_type: MediaType
    result: int


@dataclass
class CarAttributes:
    license_plate_number: str
    license_plate_number_score: float
    license_plate_country: str
    license_plate_country_score: float
    car_brand: str
    car_brand_score: float
    car_color: str
    car_color_score: float
    car_type_body: str
    car_type_body_score: float
