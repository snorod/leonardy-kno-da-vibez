import numpy as np
import os

from flask import Flask, request, render_template, url_for, redirect
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions


# pretrained ResNet50
model = ResNet50(weights='imagenet')
app = Flask(__name__)

@app.route("/")
def fileFrontPage():
    return render_template('fileform.html')

@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            photo.save(os.path.join('/Users/AaronLopes/Desktop/documents/gt_spring_20/leonardy-kno-da-vibez', photo.filename))
    return redirect(url_for('fileFrontPage'))

#tbd
def label_img(path):
    # set path
    img_path = path

    # import image, resize
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    yhat= decode_predictions(preds, top=3)





