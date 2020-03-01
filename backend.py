import numpy as np
import os
import requests
import json


from flask import Flask, request, render_template, url_for, redirect, make_response
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions


# pretrained ResNet50
model = ResNet50(weights='imagenet')
app = Flask(__name__, template_folder='/Users/AaronLopes/Desktop/documents/gt_spring_20/leonardy-kno-da-vibez')
keyword = ''

@app.route("/")
def fileFrontPage():
    return render_template('fileform2.html')

@app.route("/play_music")
def play_music():
    keyword = 'castle'
    print(keyword)
    auth_token = 'BQC-vsg880t2sJsW3B6dkLtTtLxzrsW-Mgd-VYINKx2YR84LS8OpGfy8WduOlGTbHV0h-BZ9ZTZdgF2VdOdPM-csTwdXje6vZkPNkP5He40ABxAAc_WPW_Wlya22TSBqSVWUmMJz3rw4vd_w19ILa05RtlvU9jeKItBJt6c'
    uri = spotify_search(keyword, auth_token)
    spotify_play(uri, auth_token)
    return ''


@app.route("/handleUpload", methods=['POST'])
def handleFileUpload():
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            path = os.path.join('/Users/AaronLopes/Desktop/documents/gt_spring_20/leonardy-kno-da-vibez', photo.filename)
            photo.save(path)
            keyword = label_img(path)
        else:
            keyword = "never gonna give you up"

    return redirect(url_for('fileFrontPage'))

def label_img(path):

    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    yhat = decode_predictions(preds, top=1)[0][0][1]
    print(yhat)
    return yhat


def spotify_search(keyword, auth_token):
    search_url = 'https://api.spotify.com/v1/search'
    search_headers = {'Authorization': 'Bearer ' + auth_token}
    search_params = {'q': keyword, 'type': 'track', 'market': 'US', 'limit': 1}
    r = requests.get(headers = search_headers, url = search_url, params = search_params)
    data = r.json()
    uri = data['tracks']['items'][0]['uri']
    return uri

def spotify_play(uri, auth_token):
    play_url = 'https://api.spotify.com/v1/me/player/play'
    play_headers = {'Authorization': 'Bearer ' + auth_token, 'Accept': 'application/json', 'Content-Type': 'application/json'}
    play_params = {'device_id': '4b3fe332fbd0cf39be3ca5d1bffc6bb4ee49527b'}
    play_payload = {'uris': [uri]}
    r = requests.put(headers = play_headers, url = play_url, params = play_params, data = json.dumps(play_payload))


if __name__ == '__main__':
    app.run()




