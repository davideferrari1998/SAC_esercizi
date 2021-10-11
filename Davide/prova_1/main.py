from re import template
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return render_template('greetings.html', rec="Davide")

@app.route('/greetings/<rec>', methods=['GET'])
def hello_2(rec):
    print(request.args)
    return render_template('greetings.html', rec=rec)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port="8080", debug=True)


