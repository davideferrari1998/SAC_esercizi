from flask import Flask, request, render_template
from wtforms import Form, StringField, SubmitField, validators, SelectField
from requests import post, get
from google.cloud import firestore

app = Flask(__name__)

class CourseForm(Form):
    course = SelectField('CORSO:', choices =['A','B','C'], validators=[validators.InputRequired()])
    time_slot = SelectField('FASCIA ORARIA:',choices=["09-11","11-13","14-16"],validators= [validators.InputRequired()])
    submit = SubmitField(label=('Submit'))


@app.route('/', methods=['GET', 'POST'])
def main_page():
    form = CourseForm(request.form)
    if request.method == 'GET':
        return render_template('seats.html', form = form)
    else:
        if not form.validate():
            return render_template('seats.html', form = form, error = "Invalid inputs")

        corso = request.form['course']
        orario = request.form['time_slot']

        if corso == 'A' and orario == "14-16":
            return render_template('seats.html', form = form, error = "INVALID TIME SLOT")
        
        if corso == 'C' and orario == "11-13":
            return render_template('seats.html', form = form, error = "INVALID TIME SLOT")

        utenti = []

        col = "Course" + corso
        db=firestore.Client()
        ref = db.collection(col)
        for r in ref.stream():
            posto = r.to_dict()
            posto['id'] = r.id
            utenti.append(posto)

        return render_template('seats.html', form = form, students = utenti)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)