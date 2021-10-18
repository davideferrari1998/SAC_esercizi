from flask import Flask, request, render_template
from wtforms import Form, StringField, SubmitField, validators, FloatField
from wtforms.fields.core import IntegerField
from marketplace import Marketplace
from requests import post, get
from google.cloud import firestore

app = Flask(__name__)

class SearchForm(Form):
    userId = StringField('User uuid', [validators.UUID(), validators.InputRequired()])
    gameId = StringField('Game uuid', [validators.UUID(), validators.InputRequired()])
    submit = SubmitField(label=('Submit'))

class InsertForm(Form):
    userId = StringField('User uuid', [validators.UUID(), validators.InputRequired()])
    gameId = StringField('Game uuid', [validators.UUID(), validators.InputRequired()])
    title = StringField('Title', [validators.InputRequired()])
    year = IntegerField('Year', [validators.NumberRange(min=2010, max=2020)])
    console = StringField('Console', [lambda x: x in ['ps4', 'xbox_one', 'switch', 'xbox_x', 'xbox_s', 'ps5']])
    price = FloatField('Price', [lambda x: x>= 0])
    submit = SubmitField(label=('Submit'))

@app.route('/', methods=['GET'])
def main_page():
    print('main_page function')
    return render_template('index.html')

@app.route('/view', methods=['GET'])
def view_games():
    db = firestore.Client()
    games = []
    for x in db.collections():
        for doc in x.stream():
            dict = doc.to_dict()
            dict['id'] = doc.id
            games.append(dict)
    return render_template('games_list.html', games=games)

@app.route('/view/<string:id>', methods=['GET'])
def view_game_specs(id):
    db = firestore.Client()
    for x in db.collections():
        ref = x.document(id).get()
        if ref.exists:
            print(ref.to_dict())
            return render_template('game_spec.html', game=ref.to_dict())
    return None, 407

@app.route('/search', methods=['GET', 'POST'])
def search_game():
    form = SearchForm()
    if request.method == 'GET':
        print('get request to search.html')
        return render_template('search.html', form=form)
    else:
        print('post request to search.html')
        userId = request.form['userId']
        gameId = request.form['gameId']
        print('user: {}'.format(userId))
        print('game: {}'.format(gameId))
        print(request.root_url)
        
        #target url endpoint: https://game-market-app.nw.r.appspot.com

        r = get('https://game-market-app.nw.r.appspot.com/api/v1/game/{}/{}'.format(userId, gameId))
        ret_code = r.status_code
        print('get to API, code: {}'.format(ret_code))
        if ret_code == 200:
            print(ret_code)
            json = r.json()
            print(json)
            return render_template('search.html', retval=ret_code, form=form, x=json)
        print(ret_code)
        return render_template('search.html', error=ret_code, form=form)

@app.route('/insert', methods=['GET', 'POST'])
def insert_game():
    form = InsertForm()
    if request.method == 'GET':
        print('get request to insert.html')
        return render_template('insert.html', form=form)
    else:
        print('post request to insert.html')
        userId = request.form['userId']
        gameId = request.form['gameId']
        
        json={
            'title':request.form['title'],
            'year':request.form['year'],
            'console':request.form['console'],
            'price':request.form['price']
        }
        print(request.root_url)

        #target url endpoint: https://game-market-app.nw.r.appspot.com
        
        r = post('https://game-market-app.nw.r.appspot.com/api/v1/game/{}/{}'.format(userId, gameId), json=json)
        ret_code = r.status_code
        print('get to API, code: {}'.format(ret_code))
        if ret_code == 201:
            print(ret_code)
            return render_template('insert.html', retval=ret_code, form=form)
        print(ret_code)
        return render_template('insert.html', error=ret_code, form=form)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)