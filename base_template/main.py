from flask import Flask, render_template, request
from google.cloud import firestore
from wtforms import SelectField, validators, Form, StringField, SubmitField

app = Flask(__name__)

db = firestore.Client()

@app.route('/', methods=['GET'])
def main_page():
    ...

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)