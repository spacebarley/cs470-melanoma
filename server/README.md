## How to 

Install the dependencies:

    pip install -r requirements.txt


Run the Flask server:

    FLASK_ENV=development FLASK_APP=app.py flask run


From another tab, send the image file in a request:

    curl --location --request POST 'localhost:5000/predict' --form 'sex="Male"' --form 'age="20"' --form 'site="head"' --form 'file=@ISIC_0149568.jpeg"'

It will return the possibility of melanoma predicted by given model.

    {"melanoma_probability":"0.5218048"}