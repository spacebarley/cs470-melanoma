import io
import json
import torch

import torch.nn as nn

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS
from efficientnet_pytorch import EfficientNet
import numpy as np

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'model')))

from model.our_model_revise import MyNetwork
import timm

app = Flask(__name__)
CORS(app)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

model_path = './trained/fourth_model.pt'
model = MyNetwork()
model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
num_classes = 2
# model = timm.create_model('tf_efficientnet_b2_ns', pretrained=True, num_classes=num_classes)
# model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def one_hot_sex(sex):
    if sex.lower() == "male":
        return [1, 0]
    else:
        return [0, 1]

def one_hot_age(age):
    arr = [0] * 10
    arr[int(int(age)/10)] = 1
    return arr

def one_hot_site(site):
    if site in "head/neck":
        return [1, 0, 0, 0, 0, 0]
    elif site in "upper extremity":
        return [0, 1, 0, 0, 0, 0]
    elif site in "lower extremity":
        return [0, 0, 1, 0, 0, 0]
    elif site in "torso":
        return [0, 0, 0, 1, 0, 0]
    elif site in "palms/soles":
        return [0, 0, 0, 0, 1, 0]
    elif site in "oral/genital":
        return [0, 0, 0, 0, 0, 1]
    else: assert(0)

def get_prediction(image_bytes, sex, age, site):
    arr_sex = one_hot_sex(sex)
    arr_age = one_hot_age(age)
    arr_site = one_hot_site(site)
    metadata = np.array(arr_sex + arr_age + arr_site).astype(np.float32)
    metadata = torch.from_numpy(metadata).unsqueeze(0)

    # Iterate to give randomly transformed image
    output = 0
    for i in range(10):
        image = transform_image(image_bytes=image_bytes)
        outputs = model(image, metadata)
        output += torch.softmax(outputs, 1).cpu().detach().numpy()[:, 1][0]
    return output / 10


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        sex = request.form['sex']
        age = request.form['age']
        site = request.form['site']
        possibility = get_prediction(img_bytes, sex, age, site)
        return jsonify({'melanoma_probability': str(possibility)})


if __name__ == '__main__':
    app.run()
