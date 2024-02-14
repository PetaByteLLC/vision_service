from ultralytics import YOLO
from PIL import Image
import matplotlib.pyplot as plt

model = YOLO('/home/rikitwiki/Desktop/best.pt')

results = model('/home/rikitwiki/Desktop/gts/01D194VB_0_unknown.jpeg')

if len(results) > 0:
    boxes = results[0].boxes
    if len(boxes.xyxy) > 0:
        xmin, ymin, xmax, ymax = boxes.xyxy[0].cpu().numpy()

        img_path = '/home/rikitwiki/Desktop/gts/01D194VB_0_unknown.jpeg'
        img = Image.open(img_path)

        license_plate_img = img.crop((xmin, ymin, xmax, ymax))

        plt.figure(figsize=(10, 5))
        plt.imshow(img)
        plt.title("Изображение с обнаруженным номером машины")
        plt.axis('off')
        plt.show()

        plt.figure(figsize=(5, 2.5))
        plt.imshow(license_plate_img)
        plt.title("Обрезанный номерной знак")
        plt.axis('off')
        plt.show()
else:
    print("Номерные знаки не обнаружены.")