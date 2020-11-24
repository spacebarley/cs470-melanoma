import io
import json
import torch

import torch.nn as nn

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from flask_cors import CORS

import timm

app = Flask(__name__)
CORS(app)

model_path = './trained/test.pt'
num_classes = 2
model = timm.create_model('tf_efficientnet_b2_ns', pretrained=True, num_classes=num_classes)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
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


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model(tensor)
    output = torch.softmax(outputs, 1).cpu().detach().numpy()[:, 1][0]
    return output


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        possibility = get_prediction(image_bytes=img_bytes)
        return jsonify({'melanoma_probability': str(possibility)})


if __name__ == '__main__':
    app.run()
