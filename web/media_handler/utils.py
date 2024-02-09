import os
import secrets
from typing import Tuple, Any, Union
import aiofiles

import base64
from io import BytesIO

from web.ai_service.app_gts import lp_det_reco
from web.ai_service.car_attributes import predict_image
from web.media_handler.schemas import CarAttributes

RANDOM_STRING_CHARS = "1234567890QWERTYUIOPASDFGHJKLZXCVBNM"


def get_random_string(length, allowed_chars=RANDOM_STRING_CHARS) -> str:
    """
    Description: Generates a random string of a specified length using the provided characters.
    params:
        length: An integer specifying the length of the random string to generate.
        allowed_chars: A string containing characters that may be used in the random string. Defaults to a predefined string of uppercase letters and numbers.
    return: A string representing the randomly generated string.
    """
    return "".join(secrets.choice(allowed_chars) for i in range(length))

async def save_file_websocket_connection(file):
    unique_code = get_random_string(length=6)
    filepath = f"web/media/{unique_code}/{file}"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    url: str = str(filepath.replace("web/", ""))

    async with aiofiles.open(filepath, "wb") as buffer:
        await buffer.write(await file.read())

    return url, filepath


async def save_binary(file_base64: str, filename: str) -> Tuple[str, str]:
    """
    Description: Asynchronously saves a base64-encoded image to a directory, generating a unique filename.
    params:
       file_base64: The base64-encoded content of the image to be saved.
       filename: The original filename of the image.
    return: A tuple containing the URL and filepath of the saved file. The URL is a relative path excluding the "web/" prefix.
    """
    unique_code = get_random_string(length=6)
    filepath = f"web/media/{unique_code}_{filename}"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    url: str = str(filepath.replace("web/", ""))

    image_data = base64.b64decode(file_base64)
    buffer = BytesIO(image_data)

    async with aiofiles.open(filepath, "wb") as file:
        await file.write(buffer.getvalue())

    return url, filepath

async def save_file(file) -> Tuple[str, str]:

    """
    Description: Asynchronously saves a file to a directory, generating a unique filename.
    params:
        file: The file to be saved.
    return: A tuple containing the URL and filepath of the saved file. The URL is a relative path excluding the "web/" prefix.
    """

    unique_code = get_random_string(length=6)
    filepath = f"web/media/{unique_code}_{file.filename}"

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    url: str = str(filepath.replace("web/", ""))
    buffer = BytesIO()
    file.save(buffer, format=file.format)

    async with aiofiles.open(filepath, "wb") as file:
        await file.write(buffer.getvalue())

    return url, filepath


async def process_image(img_path: str) -> Union[dict, Tuple]:
    """
    Description: Processes an image to detect a car and its attributes, as well as the license plate.
    params:
        img_path: A string representing the path to the image file.
    return: A dictionary with data if a car is not detected, or a tuple containing the license plate information and car attributes.
    """
    car_attributes = predict_image(img_path)
    lp = lp_det_reco(img_path)
    print(lp)
    return lp, car_attributes


def get_value(result: str, index: int, subindex: Union[int, None] = None) -> Any:
    """
    Description: Retrieves a value from a nested structure based on provided indices.
    params:
        result: The nested structure (e.g., a list of lists) to retrieve the value from.
        index: The primary index to access the top-level list.
        subindex: An optional secondary index to access a nested list.
    return: The retrieved value, or None if indices are out of range.
    """
    if (
        index < len(result) and result[index] is not None and
        (subindex is None or (isinstance(result[index], tuple) and subindex < len(result[index])))
    ):
        return result[index][subindex] if subindex is not None else result[index]
    return None


def get_float_value(result, index: int, subindex: Union[int, None] = None) -> Any:
    """
    Description: Retrieves a float value from a nested structure based on provided indices.
    params:
        result: The nested structure to retrieve the value from.
        index: The primary index to access the top-level list.
        subindex: An optional secondary index to access a nested list.
    return: The retrieved float value, or None if indices are out of range or if the value cannot be converted to float.
    """
    value = get_value(result, index, subindex)
    return float(value) if value is not None else None


def format_data(result: tuple) -> Union[CarAttributes, dict]:
    """
    Description: Formats the result from image processing into a CarAttributes
    Generates a CarAttributes object based on the result of image processing.

    :param result: tuple with image processing results
    :return: object CarAttributes | dict with error message
    """

    if None in result[0]:
        return {"message": "Invalid image size. Please higher image quality"}

    return CarAttributes(
        license_plate_number=get_value(result[0], 0),
        license_plate_number_score=get_float_value(result[0], 1),
        license_plate_country=get_value(result[0], 2, 0),
        license_plate_country_score=get_float_value(result[0], 2, 1),
        car_brand=get_value(result[1], 0),
        car_brand_score=get_float_value(result[1], 1),
        car_color=get_value(result[1], 2),
        car_color_score=get_float_value(result[1], 3),
        car_type_body=get_value(result[1], 4),
        car_type_body_score=get_float_value(result[1], 5),
    )
