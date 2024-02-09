# AutoVision
This project performs car license plate recognition, country identification, using various tools and libraries.




## Как начать (Linux)
1
```
git clone git@github.com:PetaBytePro/AutoVision.git
```
2
```
cd AutoVision/
```
3
```
python3 -m venv venv
```
4
```
source venv/bin/activate
```
5

# CPU:
```
  python -m pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
```
# GPU:
```  
  python -m pip install paddlepaddle-gpu -i https://pypi.tuna.tsinghua.edu.cn/simple
```
6
```
pip install -r requirements.txt
python3 setup.py -q develop
```
7 (do it only if you are having an error with "libssl")
```
sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6  -y

wget http://nz2.archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb

sudo dpkg -i libssl1.1_1.1.1f-1ubuntu2.19_amd64.deb
```
8
Insert your path to image, here at the end of the app.py file and do the 11th step:
```
p = lp_det_reco('img_path')
```
9 (put and extract the data zip into the project!!!)
```
https://cloud.sanarip.org/index.php/s/NYpfBa3BSot7APe/download/data.zip
```
10
```
python3 app.py
```

at the and calls lp_det_rec func in which you should paste the path to your image. 

# Licence

### car segmentation and country detection

YOLO ultralytics - AGPL-3.0 License

### OCR

- PaddleOCR - Apache License
  (https://github.com/PaddlePaddle/PaddleOCR)
- ParseQ - Apache License
  (https://github.com/baudm/parseq)

### Photo quality improvement

Original Source:

Real-ESRGAN - BSD 3-Clause License, Xintao Wang (https://github.com/xinntao/Real-ESRGAN)
