from re import L
from flask import Flask, render_template, request
from requests import get
from wtforms import Form, StringField, DateField, SubmitField, validators
from google.cloud import firestore

app = Flask(__name__)

class SearchForm(Form):

    user_id = StringField('USER ID:',[validators.UUID(), validators.InputRequired()])
    submit = SubmitField(label='SUBMIT')


@app.route('/', methods = ['GET'])
def main_page():
    return render_template('index.html')


@app.route('/search', methods = ['GET', 'POST'])
def search_function():
    form = SearchForm(request.form)

    if request.method == 'GET':
        return render_template('search.html', form = form)
    else:
        if not form.validate():
            return render_template('search.html', form = form, error = "Invalid USER ID")

    user = request.form['user_id']
    db = firestore.Client()
    travels = []
    ref= db.collection(f'{user}')

    for t in ref.stream():
        json = t.to_dict()
        json['date'] = t.id
        travels.append(json)

    return render_template('search.html', form = form, travels = travels)



@app.route('/find', methods = ['GET','POST'])
def find_function():
    form = SearchForm(request.form)

    if request.method == 'GET':
        return render_template('find.html', form = form)
    else:
        if not form.validate():
            return render_template('find.html', form = form, error = "Invalid USER ID")


    user = request.form['user_id']
    #Richiesta all'api
    r = get('http://travel-2510.appspot.com/api/v1/travel/friends/{}'.format(user))

    users = r.json()

    if r.status_code == 405:
        return render_template('find.html', form = form, msg = r.text)

    return render_template('find.html', form = form, users = users)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)