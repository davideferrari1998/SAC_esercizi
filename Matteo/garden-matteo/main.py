from flask import Flask, render_template
from google.cloud import firestore
import datetime

app = Flask(__name__)

db = firestore.Client()


@app.route('/', methods=['GET'])
def main_page():
    ref = db.collections()
    semine = list()
    for semina_coll in ref:
        #dettagli_semina = {"date": None, "name": None, "germinazione": None, "crescita": None, "color": None}
        dettagli_semina = dict()
        date = semina_coll.id
        date_semina = datetime.datetime.strptime(date, "%Y-%m-%d")
        date_now = datetime.datetime.now()
        if(date_semina < date_now):
            color = 1
        elif(date_semina < date_now + datetime.timedelta(days=10)):
            color = 2
        else:
            color = 3

        print(semina_coll.id)
        for semina_doc in semina_coll.stream():
            dettagli_semina["date"] = date
            dettagli_semina["color"] = color
            dettagli_semina["name"] = semina_doc.to_dict()["plant"]["name"]
            dettagli_semina["germinazione"] = semina_doc.to_dict()["plant"]["sprout-time"]
            dettagli_semina["crescita"] = semina_doc.to_dict()["plant"]["full-growth"]           
            print(dettagli_semina)
            dets = dettagli_semina.copy()
            semine.append(dets)
    
    return render_template('main_page.html', semine=semine)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)