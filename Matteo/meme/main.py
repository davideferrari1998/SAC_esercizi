from flask import Flask, render_template, request
from requests import get
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client()

@app.route('/', methods=['GET'])
def main_page():
    tags = set()
    for x in db.collections():
        for y in x.stream():
            info = y.to_dict()
            for tag in info['tags']:
                tags.add(tag)
    return render_template('index.html', tags=tags)

@app.route('/view/<string:tag>', methods=['GET'])
def load_meme_by_tag(tag):
    r = get(f'https://exam-15-06-20.appspot.com/api/v1/memesByTag/{tag}')
    memes = r.json()
    return render_template('meme.html', memes=memes, tag=tag)

@app.route('/view_spec/<string:tag>/<string:title>', methods=['GET'])
def load_meme_info(tag, title):
    r = get(f'https://exam-15-06-20.appspot.com/api/v1/memesByTag/{tag}')
    memes = r.json()
    for meme in memes:
        print(meme)
        if meme['title'] == title:
            return render_template('meme_info.html', meme=meme)
    return {'error':'An error occured'}, 404


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)