import io
import json
import torch

import torch.nn as nn

import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'model')))

from model import MyNetwork

app = Flask(__name__)
CORS(app)

device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Use pt file made by our model
model_path = './trained/efficient_b1_model_final.pt'
model = MyNetwork()
model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
model.eval()

# Transform given image to fit on our model
def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(240),
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

# Make one hot tensors of given metadata
def create_metadata(sex, age, site):
    arr_sex = one_hot_sex(sex)
    arr_age = one_hot_age(age)
    arr_site = one_hot_site(site)
    metadata = np.array(arr_sex + arr_age + arr_site).astype(np.float32)
    return torch.from_numpy(metadata).unsqueeze(0)    

# Apply given data to model, return melanoma possibility
def get_prediction(image_bytes, sex, age, site):
    metadata = create_metadata(sex, age, site)

    # Iterate to give randomly transformed image
    output = 0
    for i in range(10):
        image = transform_image(image_bytes=image_bytes)
        outputs = model(image, metadata)
        output += torch.softmax(outputs, 1).cpu().detach().numpy()[:, 1][0]
    return output / 10


# Get predict message, post melanoma possibility as json
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
