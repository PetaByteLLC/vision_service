from typing import Tuple, Union

from .ai_service.app_gts import lp_det_reco
from .ai_service.car_attributes import predict_image
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.insert(0, "src/web_service/vision_service")


def process_image(img_path: str) -> Union[dict, Tuple]:
    """
    Description: Processes an image to detect a car and its attributes, as well as the license plate.
    params:
        img_path: A string representing the path to the image file.
    return: A dictionary with data if a car is not detected, or a tuple containing the license plate information and car attributes.
    """
    # car_attributes = predict_image(img_path)
    try:
        lp = lp_det_reco(img_path)
        logger.info(f"Recognition result: {lp}")
        return lp
    except Exception as e:
        raise e
