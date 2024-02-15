import torch
import cv2
import numpy as np
from PIL import Image
from glob import glob
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks, rotate
from skimage.color import rgb2gray
from nomeroff_net import pipeline
from nomeroff_net.tools import unzip
from strhub.data.module import SceneTextDataModule
from paddleocr import PaddleOCR

# Initialize OCR models and other resources
ocr = PaddleOCR(use_angle_cls=True, lang="en")
parseq = torch.hub.load("baudm/parseq", "parseq", pretrained=True).eval()
img_transform = SceneTextDataModule.get_transform(parseq.hparams.img_size)

# Assuming init_models.py and other necessary modules are correctly set up in your environment
from init_models import upsampler, country_model

# Download models if they don't exist
multiline_number_plate_detection_and_reading = pipeline(
    "multiline_number_plate_detection_and_reading", image_loader="opencv"
)

def preprocess(img):
    rot_angle = 0
    grayscale = rgb2gray(img)
    edges = canny(grayscale, sigma=3.0)
    out, angles, distances = hough_line(edges)
    _, angles_peaks, _ = hough_line_peaks(out, angles, distances, num_peaks=20)
    angle = np.mean(np.rad2deg(angles_peaks))
    
    if 0 <= angle <= 90:
        rot_angle = angle - 90
    elif -45 <= angle < 0:
        rot_angle = angle - 90
    elif -90 <= angle < -45:
        rot_angle = 90 + angle
    if abs(rot_angle) > 20:
        rot_angle = 0
    
    rotated = rotate(img, rot_angle, resize=True) * 255
    rotated = rotated.astype(np.uint8)
    minus = np.abs(int(np.sin(np.radians(rot_angle)) * rotated.shape[0]))
    if rotated.shape[1] / rotated.shape[0] < 3 and minus > 6:
        rotated = rotated[minus:-minus, :, :]
    return rotated

def del_symbols(input_string):
    cleaned_string = ""
    for char in input_string:
        if char not in ("-","#","_","+","=","!","@","$","%","*","&","(",")","^","/","|",";",".",":",",","·","<",">"):
            cleaned_string += char
    return cleaned_string

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
    combined_element = "".join(results_array).replace(" ", "")
    return combined_element, confidences_array

def parseq_finc(img):
    img = img_transform(img).unsqueeze(0)
    logits = parseq(img)
    pred = logits.softmax(-1)
    label, confidence = parseq.tokenizer.decode(pred)
    return label[0], confidence

def calculate_mean(numbers):
    if len(numbers) == 0:
        return None
    return sum(numbers) / len(numbers)

def lp_det_reco(img_path):
    result = multiline_number_plate_detection_and_reading(glob(img_path), matplotlib_show=False)
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
        x_min, y_min, x_max, y_max, _, _ = images_bboxs[0][0]
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
        pro = preprocess(images[0][y_min:y_max, x_min:x_max])

        pro_resized = cv2.resize(pro, (224, 224))

        # country
        pred_country, pred_idx, probs_country = country_model.predict(pro_resized)
        probs_country = f"{probs_country[pred_idx]:.4f}"
        country = (pred_country, probs_country)

        # Enhance img or not
        H, W, _ = pro.shape
        if H >= 100 and H <= 300 and W >= 100 and W <= 300:
            img_enh, _ = upsampler.enhance(pro, outscale=1)
        else:
            img_enh = pro
        img_final = Image.fromarray(img_enh)

        # OCR
        combined_element_without_spaces, conf = '', []
        if country[0] == "CN":
            combined_element_without_spaces, conf = paddle(img_enh, "ch")
        elif country[0] in ["AM", "KG"]:
            if count_lines[0][0] >= 2:
                combined_element_without_spaces, conf = paddle(img_enh, "en")
            else:
                conf = confidences[0][0]
                combined_element_without_spaces = texts[0][0]
        elif country[0] in ["RU", "KZ"]:
            combined_element_without_spaces, conf = paddle(img_enh, "en")
        elif country[0] == "UZ":
            if count_lines[0][0] >= 2:
                combined_element_without_spaces, conf = paddle(img_enh, "en")
            else:
                start = img_enh[:, : int(W // 4.5)]
                end = img_enh[:, int(W // 4.5) :]
                number_plate = [start, end]
                result = []
                for i in range(len(number_plate)):
                    label, confidence = parseq_finc(Image.fromarray(number_plate[i]))
                    conf.append(confidence[0].detach().numpy())
                    result.append(label)
                combined_element_without_spaces = "".join(result)
        else:
            combined_element_without_spaces, conf = paddle(img_enh, "en")

        combined_element_without_spaces = del_symbols(combined_element_without_spaces)
        mean_conf = calculate_mean(conf) if conf else None

        return combined_element_without_spaces, mean_conf, country, img_final
    except Exception as error:
        print(f"An error occurred: {error}")
        return None, None, None, None

result_text, confidence, country_code, cropped_image = lp_det_reco('/home/rikitwiki/Desktop/gts/2773DZE_2773DZE.jpg')
print(lp_det_reco('/home/rikitwiki/Desktop/gts/2773DZE_2773DZE.jpg'))