from flask import Flask, render_template, request
from google.cloud import firestore
import datetime

app = Flask(__name__)

db = firestore.Client()

@app.route('/', methods=['GET'])
def main_page():

    today = datetime.datetime.now()

    # semina = [{'name':....., 'date':....., 'full-growth':....., 'sprout-time':....., 'color':....}]
    semine = list()

    for col in db.collections():

        date = col.id
        date_semina = datetime.datetime.strptime(date, "%d-%m-%Y")
        if date_semina < today:
            color = 1
        elif date_semina < (today + datetime.timedelta(days=10)):
            color = 2
        else:
            color = 3

        for doc in col.stream():
            plant = dict()
            ref = doc.to_dict()
            plant['name'] = ref['plant']['name']
            plant['date'] = date_semina.strftime("%d-%m-%Y")
            plant['full-growth'] = ref['plant']['full-growth']
            plant['sprout-time'] = ref['plant']['sprout-time']
            plant['color'] = color

            semine.append(plant)
        
    return render_template('semine.html', semine = semine)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)