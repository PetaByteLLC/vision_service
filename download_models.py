from basicsr.utils.download_util import load_file_from_url
import os
from fastai.learner import load_learner
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
from ultralytics import YOLO
import zipfile


def download_model(model_url, model_name):
    model_path = os.path.join('weights', model_name + '.pt')
    if not os.path.isfile(model_path):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        for url in model_url:
            model_path = load_file_from_url(
                url=url, model_dir=os.path.join(ROOT_DIR, 'weights'), progress=True, file_name=None)
    return model_path

data_path = os.path.join('.','data','models','Detector','yolov8','yolov8s-2023-02-11.pt')
if not os.path.isfile(data_path):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = load_file_from_url(
        url='https://cloud.sanarip.org/index.php/s/NYpfBa3BSot7APe/download/data.zip', model_dir=os.path.join(ROOT_DIR), progress=True, file_name=None)

delete_data = 'data.zip'
if os.path.isfile(delete_data):
    with zipfile.ZipFile('data.zip', 'r') as zip_ref:
        zip_ref.extractall()
if os.path.isfile(delete_data):
    os.remove(delete_data)

# Define and download models fro car attributes
car_brand_name = 'export_car_brand.pkl'
car_brand_url = ['https://cloud.sanarip.org/index.php/s/d5kmzHgz7fPLL2A/download/export_car_brand.pkl']
car_color_name = 'export_car_color_detection.pkl'
car_color_url = ['https://cloud.sanarip.org/index.php/s/eNTc9Bcc29xQwrp/download/export_car_color_detection.pkl']
car_type_name = 'export_car_body.pkl'
car_type_url = ['https://cloud.sanarip.org/index.php/s/yAmf3gzSRoFZgmx/download/export_car_body.pkl']
yolov8_name = 'yolov8x.pt'
yolov8_url = ['https://cloud.sanarip.org/index.php/s/c8LByRzRc7MGWnB/download/yolov8x.pt']
truck_brand_name = 'export_truck_brand.pkl'
truck_brand_url = ['https://cloud.sanarip.org/index.php/s/7tmD8GBH9SRqA4W/download/export_truck_brand.pkl']

# ls
country_model = 'country_model_v7am.pkl'
file_url = ['https://cloud.sanarip.org/index.php/s/TbMfZgdDrbRLe7g/download/country_model_v7am.pk1']
model_name = 'RealESRGAN_x4plus'
model_url = ['https://cloud.sanarip.org/index.php/s/2XfFdM4CJt52rmm/download/RealESRGAN_x4plus.pth']


car_brand_path = download_model(car_brand_url, car_brand_name)
car_color_path = download_model(car_color_url, car_color_name)
car_type_path = download_model(car_type_url, car_type_name)
yolov8_path = download_model(yolov8_url, yolov8_name)
truck_brand_path = download_model(truck_brand_url, truck_brand_name)
MODEL = yolov8_path

model = YOLO(MODEL)
model.fuse()

country_model_path = download_model(file_url, country_model)
real_esrgan_model_path = download_model(model_url, model_name)

learn_car_brand = load_learner(car_brand_path)
learn_car_color = load_learner(car_color_path)
learn_car_body = load_learner(car_type_path)
country_model = load_learner(country_model_path)
learn_truck_brand = load_learner(truck_brand_path)

model_RDB =RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
upsampler = RealESRGANer(
    scale=4,
    model_path=real_esrgan_model_path,
    dni_weight=None,
    model=model_RDB,
    tile=0,
    tile_pad=10,
    pre_pad=0,
    half=False,
    gpu_id=None)