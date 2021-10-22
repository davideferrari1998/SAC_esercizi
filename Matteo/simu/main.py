from flask import Flask, render_template, request
from requests import get
from wtforms import Form, StringField, DateField, SubmitField, validators

app = Flask(__name__)

class SearchForm(Form):
    userId = StringField('User uuid', [validators.UUID(), validators.InputRequired()])
    date = DateField('Date', [validators.InputRequired()], format='%Y-%m-%d')
    submit = SubmitField(label=('Submit'))


@app.route('/', methods=['GET','POST'])
def main_page():
    print('main_page function')
    form = SearchForm(request.form)

    if request.method == 'GET':        
        return render_template('index.html', form=form)
    else:
        if not form.validate():
            return render_template('index.html', form=form, error="uuid not valid or date not valid, date should be YYYY-MM-DD")

        user_uuid = request.form.to_dict()['userId']
        date = request.form.to_dict()['date']
        
        print(user_uuid)
        print(date)

        r1 = get(f'https://simulazione-matteo.nw.r.appspot.com/api/v1/travel/{user_uuid}/{date}')
        r2 = get(f'https://simulazione-matteo.nw.r.appspot.com/api/v1/friends/{user_uuid}/{date}')

        print(r1.status_code)
        print(r1.json())
        print(r2.status_code)
        print(r2.json())
        return render_template('index.html', form=form, list1=r1.json(), list2=r2.json())


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)