import torch
import os
from basicsr.utils.download_util import load_file_from_url
from init_models import upsampler, country_model

import cv2
import numpy as np
from PIL import Image
from glob import glob
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks
from skimage.transform import rotate
from skimage.color import rgb2gray
from nomeroff_net import pipeline
from nomeroff_net.tools import unzip
from strhub.data.module import SceneTextDataModule
from paddleocr import PaddleOCR


# Initialize OCR models and other resources
ocr = PaddleOCR(use_angle_cls=True, lang="en")
parseq = torch.hub.load("baudm/parseq", "parseq", pretrained=True).eval()
img_transform = SceneTextDataModule.get_transform(parseq.hparams.img_size)

# Download models if they don't exist
multiline_number_plate_detection_and_reading = pipeline(
    "multiline_number_plate_detection_and_reading", image_loader="opencv"
)


# Define a function for preprocessing an image
def preprocess(img):
    # Detect rotation angle
    rot_angle = 0
    grayscale = rgb2gray(img)
    edges = canny(grayscale, sigma=3.0)
    out, angles, distances = hough_line(edges)
    _, angles_peaks, _ = hough_line_peaks(out, angles, distances, num_peaks=20)
    angle = np.mean(np.rad2deg(angles_peaks))

    # Adjust rotation angle
    if 0 <= angle <= 90:
        rot_angle = angle - 90
    elif -45 <= angle < 0:
        rot_angle = angle - 90
    elif -90 <= angle < -45:
        rot_angle = 90 + angle
    if abs(rot_angle) > 20:
        rot_angle = 0

    # Rotate and crop the image
    rotated = rotate(img, rot_angle, resize=True) * 255
    rotated = rotated.astype(np.uint8)
    rotated1 = rotated[:, :, :]
    minus = np.abs(int(np.sin(np.radians(rot_angle)) * rotated.shape[0]))
    if rotated.shape[1] / rotated.shape[0] < 3 and minus > 6:
        rotated1 = rotated[minus:-minus, :, :]
    return rotated1


# Define a function to remove unwanted characters from a string
def del_symbols(input_string):
    cleaned_string = ""
    for char in input_string:
        if char not in (
            "-",
            "#",
            "_",
            "+",
            "=",
            "!",
            "@",
            "$",
            "%",
            "*",
            "&",
            "(",
            ")",
            "^",
            "/",
            "|",
            ";",
            ":",
            ".",
            ",",
            "·",
            "<",
            ">",
        ):
            cleaned_string += char

    return cleaned_string


# PaddleOCR takes cv2 image
def paddle(img, lang):
    recognition = PaddleOCR(use_angle_cls=True, lang=lang, det=False)
    result = recognition.ocr(img)
    results_array = []
    confidences_array = []
    for idx in range(len(result[0])):
        res = result[0][idx][1][0]
        confidence = result[0][idx][1][1]
        results_array.append(res)
        confidences_array.append(confidence)
    combined_element = "".join(results_array)
    final = combined_element.replace(" ", "")

    # returns text and confidential probability
    return final, confidences_array


# Parseq OCR takes PIL image
def parseq_finc(img):
    img = img_transform(img).unsqueeze(0)
    logits = parseq(img)
    pred = logits.softmax(-1)
    label, confidence = parseq.tokenizer.decode(pred)

    return label[0], confidence


def calculate_mean(numbers):
    if len(numbers) == 0:
        return None  # Handle the case of an empty array

    total = sum(numbers)
    mean = total / len(numbers)
    return mean


def lp_det_reco(img_path):
    result = multiline_number_plate_detection_and_reading(
        glob(img_path), matplotlib_show=False
    )
    (
        images,
        images_bboxs,
        images_points,
        images_zones,
        region_ids,
        region_names,
        count_lines,
        confidences,
        texts,
    ) = unzip(result)

    try:
        # lp lines
        x_min, y_min, x_max, y_max, _, _ = images_bboxs[0][0]
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
        pro = preprocess(images[0][y_min:y_max, x_min:x_max])
        try:
            if count_lines[0][0] == 1:
                pro = images_zones[0][0].astype("uint8")
        except:
            pass
        pro_resized = cv2.resize(pro, (224, 224))

        # country
        pred_country, pred_idx, probs_country = country_model.predict(pro_resized)
        probs_country = f"{probs_country[pred_idx]:.4f}"
        country = (pred_country, probs_country)

        # enchance img or not
        H, W, _ = pro.shape
        if H >= 100 and H <= 300 and W >= 100 and W <= 300:
            img_enh, _ = upsampler.enhance(pro, outscale=1)
        else:
            img_enh = pro
        img_final = Image.fromarray(img_enh)
        H, W, _ = img_enh.shape
        # OCR
        match country[0]:
            # OCR if this is Chinese license plate
            case "CN":
                combined_element_without_spaces, conf = paddle(img_enh, "ch")
                combined_element_without_spaces = del_symbols(
                    combined_element_without_spaces
                )
                if (
                    combined_element_without_spaces[0] == "0"
                    or combined_element_without_spaces[1] == "0"
                ):
                    combined_element_without_spaces = (
                        combined_element_without_spaces.replace("0", "Q", 1)
                    )

            # OCR if this is Kyrgyz license plate
            case "AM":
                # Use paddleOCR if squared number plate
                if count_lines[0][0] >= 2:
                    square_w = int(W / 2.7)  # Adjust the size as needed
                    square_h = int(H / 2)
                    black_square = np.zeros((square_h, square_w, 3), dtype=np.uint8)
                    img_enh[(-square_h):, :square_w] = black_square
                    combined_element_without_spaces, conf = paddle(img_enh, "en")
                    combined_element_without_spaces = del_symbols(
                        combined_element_without_spaces
                    ).replace("KG", "")
                else:
                    # Takes values from nomeroff-net
                    conf = confidences[0][0]
                    combined_element_without_spaces = texts[0][0]

            case "KG":
                # Use paddleOCR if squared number plate
                if count_lines[0][0] >= 2:
                    square_w = int(W / 2.7)  # Adjust the size as needed
                    square_h = int(H / 2)
                    black_square = np.zeros((square_h, square_w, 3), dtype=np.uint8)
                    img_enh[(-square_h):, :square_w] = black_square
                    combined_element_without_spaces, conf = paddle(img_enh, "en")
                    combined_element_without_spaces = del_symbols(
                        combined_element_without_spaces
                    ).replace("KG", "")
                    Kg_new_put = [i for i in combined_element_without_spaces]
                    if Kg_new_put[0] == "G":
                        Kg_new_put[0] = "0"
                    try:
                        if (
                            Kg_new_put[0] == "0"
                            and int(Kg_new_put[1])
                            and len(Kg_new_put) >= 6
                            and Kg_new_put[1] != "0"
                        ):
                            Kg_new_put.insert(2, "KG")
                    except:
                        pass
                    combined_element_without_spaces = "".join(Kg_new_put[:])
                else:
                    # Takes values from nomeroff-net
                    conf = confidences[0][0]
                    combined_element_without_spaces = texts[0][0]
                    Kg_new_put = [i for i in combined_element_without_spaces]
                    if Kg_new_put[0] == "G":
                        Kg_new_put[0] = "0"
                    try:
                        if (
                            Kg_new_put[0] == "0"
                            and int(Kg_new_put[1])
                            and len(Kg_new_put) >= 6
                            and Kg_new_put[1] != "0"
                        ):
                            Kg_new_put.insert(2, "KG")
                    except:
                        pass

                    combined_element_without_spaces = "".join(Kg_new_put[:])

            # OCR if this is Russian and Kazakhstan license plates
            case "RU" | "KZ":
                # Use paddleOCR if squared number plate
                if count_lines[0][0] >= 2:
                    combined_element_without_spaces, conf = paddle(img_enh, "en")
                    combined_element_without_spaces = (
                        combined_element_without_spaces.replace("KZ", "")
                    )
                else:
                    # Takes values from nomeroff-net
                    conf = confidences[0][0]
                    combined_element_without_spaces = texts[0][0]

            case "UZ":
                # Use paddleOCR if squared number plate
                if count_lines[0][0] >= 2:
                    combined_element_without_spaces, conf = paddle(img_enh, "en")
                else:
                    # Number plates divide into 2 parts and use pareq
                    start = img_enh[:, : int(W // 4.5)]
                    end = img_enh[:, int(W // 4.5) :]
                    number_plate = [start, end]
                    result = []
                    conf = []
                    for i in range(len(number_plate)):
                        label, confidence = parseq_finc(
                            Image.fromarray(number_plate[i])
                        )
                        for j in range(len(confidence[0])):
                            confidence_var = confidence[0].detach().numpy()[j]
                        conf.append(confidence_var)
                        result.append(label)
                    combined_element = "".join(result)
                    combined_element_without_spaces = combined_element.replace(
                        "G", "0", 2
                    )

            # OCR if this is other country license plates
            case _:
                # Use paddleOCR if squared number plate
                if count_lines[0][0] >= 2:
                    combined_element_without_spaces, conf = paddle(img_enh, "en")
                else:
                    # Use pareq
                    image_final = Image.fromarray(img_enh)
                    label, confidence = parseq_finc(image_final)
                    conf = []
                    for i in range(len(confidence[0])):
                        confidence_var = confidence[0].detach().numpy()[i]
                        conf.append(confidence_var)
                    combined_element_without_spaces = label

        combined_element_without_spaces = del_symbols(combined_element_without_spaces)
        conf = calculate_mean(conf)
    except Exception as error:
        combined_element_without_spaces = None
        img_final = None
        conf = None
        country = None

    return combined_element_without_spaces, conf, country, img_final


# result_text, confidence, country_code, cropped_image = lp_det_reco('/home/rikitwiki/Desktop/gts/2773DZE_2773DZE.jpg')
# print(lp_det_reco('/home/rikitwiki/Desktop/gts/2773DZE_2773DZE.jpg'))
