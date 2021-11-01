from flask import Flask, request, render_template
from wtforms import Form, StringField, SubmitField, validators, FloatField
from wtforms.fields.core import IntegerField
from marketplace import Marketplace
from requests import post, get
from google.cloud import firestore

app = Flask(__name__)

marketplace = Marketplace()

class SearchForm(Form):
    userId = StringField('User uuid', [validators.UUID(), validators.InputRequired()])
    gameId = StringField('Game uuid', [validators.UUID(), validators.InputRequired()])
    submit = SubmitField(label=('Submit'))

class InsertForm(Form):
    userId = StringField('User uuid:', [validators.UUID(), validators.InputRequired()])
    gameId = StringField('Game uuid:', [validators.UUID(), validators.InputRequired()])
    title = StringField('Title:', [validators.InputRequired(), validators.Length(min=1, max= 250)])
    year = IntegerField('Year:', [validators.NumberRange(min=2010, max=2020)])
    console = StringField('Console:') #, [lambda x: x in ['ps4', 'xbox1', 'switch']])
    price = FloatField('Price:') #, [lambda x: x >= 0.01])
    submit = SubmitField(label=('Submit'))


@app.route('/', methods=['GET'])
def main_page():
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

    
    #Elimino giochi duplicati
    res = []
    for i in games:
        if i not in res:
            res.append(i)

    return render_template('games_list.html', games = res)


@app.route('/view/<string:id>', methods=['GET'])
def view_game_specs(id):
    db = firestore.Client()
    for x in db.collections():
        ref = x.document(id).get()
        if ref.exists:
            return render_template('game_specs.html', game = ref.to_dict())
    return None, 407

@app.route('/search', methods=['GET','POST'])
def search_game():
    form = SearchForm(request.form)
    if request.method == 'GET':
        return render_template('search.html', form = form)
    else:
        if not form.validate():
            return render_template('search.html', form = form, error = "Invalid inputs")

        user = request.form['userId']
        game = request.form['gameId']

        #chiamata all'api
        r = get('http://videogame-2210.appspot.com/api/v1/game/{}/{}'.format(user, game))

        ret_code = r.status_code
        if ret_code == 200:
            json = r.json()
            return render_template('search.html', form = form, json = json, retval= ret_code)

        return render_template('search.html', form = form, error = "Game not found")


@app.route('/insert', methods=['GET','POST'])
def insert_game():
    form = InsertForm(request.form)
    if request.method == 'GET':
        return render_template('insert.html', form = form)
    else:
        if not form.validate():
            return render_template('insert.html', form = form, error = "Invalid inputs")

        user = request.form['userId']
        game = request.form['gameId']

        title = request.form['title']
        year = request.form['year']

        console = request.form['console']
        price = request.form['price']

        # Seconda validazione per quelli particolari

        if console not in ['ps4', 'xbox1', 'switch'] or price == 0:
            return render_template('insert.html', form = form, error = "Invalid inputs")

        json = {
            'title':title,
            'year': year,
            'console': console, 
            'price':price
        }

        #chiamata all'api
        p = post('http://videogame-2210.appspot.com/api/v1/game/{}/{}'.format(user, game), json = json)

        p_code = p.status_code
        
        print('RETURN DA POST: {}'.format(p_code))
        print(p.json())

        if p_code == 201:
            return render_template('insert.html', form = form, retval= p_code)

        return render_template('insert.html', form = form, error = "GENERIC ERROR")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)