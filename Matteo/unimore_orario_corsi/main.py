from flask import Flask, render_template, request
from wtforms import SelectField, validators, Form, StringField, SubmitField
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client()


courses = [{'A': ["09-11","11-13"]},{'B':["09-11","11-13","14-16"]},{'C':["09-11","14-16"]}]


class FormClass(Form):
    #user_uuid = StringField("User UUID", validators=[validators.InputRequired(), validators.UUID("uuid not valid")])
    course_id = SelectField("Course", choices=['A','B','C'], validators=[validators.InputRequired()])
    fascia_oraria = SelectField("Fascia oraria", choices=["09-11","11-13","14-16"], validators=[validators.InputRequired()])
    submit = SubmitField()

@app.route('/', methods=['GET','POST'])
def main_page():
    form = FormClass(request.form)

    if request.method == 'GET':
        return render_template('index.html', form=form)
    
    if form.validate():
        #user_uuid = request.form.to_dict()["user_uuid"]
        course_id = request.form.to_dict()["course_id"]
        fascia_oraria = request.form.to_dict()["fascia_oraria"]
        print(course_id)
        print(fascia_oraria)

        orario_valido = False
        for course in courses:
            if course.get(course_id) == None:
                continue
            else:
                if fascia_oraria in course.get(course_id):
                    orario_valido = True

        if not orario_valido:
            return render_template('index.html', form=form, error="Orario non valido")

        lista_utenti_prenotati = []
        ref = db.collection(course_id).stream()
        for user in ref:
            print(user.id)
            print(user.to_dict()['posto'])
            lista_utenti_prenotati.append({"id":user.id , "posto": user.to_dict()['posto']})

        print(lista_utenti_prenotati)
        return render_template('index.html', form=form, lista=lista_utenti_prenotati)
    
    return render_template('index.html', form=form, error="form non valido")



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)