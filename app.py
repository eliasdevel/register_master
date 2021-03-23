from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.sensors_database


@app.route('/')
def index():
    return render_template('list.html', sensors=db.sensors.find())


@app.route('/sensors', methods=['GET', 'POST'])
def insert():
    if request.method == 'GET':
        return render_template('form.html', sensor=None)
    elif request.method == 'POST':
        db.sensors.insert(request_to_sensor())
        return redirect('/')


@app.route('/sensors/<_id>', methods=['GET', 'POST'])
def update(_id):
    if request.method == 'GET':
        return render_template('form.html', sensor=db.sensors.find_one({"_id": ObjectId(_id)}))
    elif request.method == 'POST':
        db.sensors.update_one({"_id": ObjectId(_id)}, {'$set': request_to_sensor()})
        return redirect('/')


@app.route('/delete/<_id>')
def delete(_id):
    print(_id)
    db.sensors.remove({"_id": ObjectId(_id)})
    return redirect('/')


def request_to_sensor():
    return {'nome': request.form.get('nome'),
            'id_485': request.form.get('id_485'),
            'aciona_saida': request.form.get('aciona_saida'),
            'valor_acionamento': request.form.get('valor_acionamento'),
            'valor_ideal': request.form.get('valor_ideal')}


if __name__ == '__main__':
    app.run(debug=True)
