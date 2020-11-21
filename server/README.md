## How to 

Install the dependencies:

    pip install -r requirements.txt


Run the Flask server:

    FLASK_ENV=development FLASK_APP=app.py flask run


From another tab, send the image file in a request:

    curl -X POST -F file=@ISIC_0149568.jpeg http://localhost:5000/predict

It will return the possibility of melanoma predicted by given model.

    {"melanoma_propability":"0.5218048"}