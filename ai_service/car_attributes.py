import os
from ultralytics import YOLO
from fastai.vision.all import *
import numpy as np
from PIL import Image

HOME = os.getcwd()

# import supervision
from supervision.draw.color import ColorPalette
from supervision.video.source import get_video_frames_generator
from supervision.tools.detections import Detections, BoxAnnotator
from download_models import learn_car_body, learn_car_brand, learn_car_color, model, learn_truck_brand


# dict maping class_id to class_name
CLASS_NAMES_DICT = model.model.names


# Cropping function
def crop_detections(frame, detections):
    cropped_images = []
    for detection in [detections[0]]:
        # Extracting the bounding box coordinates from the detection array
        x1, y1, x2, y2 = detection[0], detection[1], detection[2], detection[3]
        cropped_image = frame[int(y1) : int(y2), int(x1) : int(x2)]
        cropped_images.append(cropped_image)
    return cropped_images


def predict_image(img_path):
    SOURCE_VIDEO_PATH = img_path

    # create frame generator
    generator = get_video_frames_generator(SOURCE_VIDEO_PATH)
    # create instance of BoxAnnotator
    box_annotator = BoxAnnotator(
        color=ColorPalette(), thickness=4, text_thickness=4, text_scale=2
    )
    # acquire first video frame
    iterator = iter(generator)
    frame = next(iterator)
    # model prediction on single frame and conversion to supervision Detections
    results = model(frame)
    detections = Detections(
        xyxy=results[0].boxes.xyxy.cpu().numpy(),
        confidence=results[0].boxes.conf.cpu().numpy(),
        class_id=results[0].boxes.cls.cpu().numpy().astype(int),
    )

    # Filter detections for car, truck, bus, and train classes
    relevant_classes = ['car', 'truck', 'bus', 'train']
    relevant_class_ids = [k for k, v in CLASS_NAMES_DICT.items() if v.lower() in relevant_classes]
    relevant_detections = [det for det in detections if det[2] in relevant_class_ids]

    # Find the largest detection among the relevant classes
    largest_detection = None
    max_area = 0
    for det in relevant_detections:
        x1, y1, x2, y2 = det[0]
        area = (x2 - x1) * (y2 - y1)
        if area > max_area:
            max_area = area
            largest_detection = det

    # Proceed only if a detection is found
    if largest_detection:
        # format custom label for the largest detection
        labels = [f"{CLASS_NAMES_DICT[largest_detection[2]]} {largest_detection[1]:0.2f}"]

        # annotate and display frame with only the largest detection
        frame = box_annotator.annotate(
            frame=frame, detections=[largest_detection], labels=labels
        )
    else:
        return False

    cropped_frames = crop_detections(frame, detections.xyxy)

    img = cropped_frames[0][:, :, ::-1]

    # Resize the image (if necessary)
    img = Image.fromarray(img)

    # img.convert("L")

    img_resized = img.resize((224, 224))

    img_resized_gray = img_resized.convert('L')
    img_resized_gray = img_resized.convert('L')

    img_resized_np_brand = np.array(img_resized_gray)
    img_resized_np = np.array(img_resized)
    # Predict
    pred_class, pred_idx, probs = learn_car_brand.predict(img_resized_np_brand)
    pred_class_color, pred_idx_color, probs_color = learn_car_color.predict(
        img_resized_np
    )
    pred_class_body, pred_idx_body, probs_body = learn_car_body.predict(img_resized_np_brand)
    pred_class_truck, pred_idx_truck, probs_truck = learn_truck_brand.predict(img_resized_np_brand)

    return (
        pred_class,
        f"{probs[pred_idx]:.4f}",
        pred_class_color,
        f"{probs_color[pred_idx_color]:.4f}",
        pred_class_body,
        f"{probs_body[pred_idx_body]:.4f}",
        pred_class_truck,
        f"{probs[pred_idx_truck]:.4f}",
    )


# Example usage
# print(predict_image('test.jpeg'))
