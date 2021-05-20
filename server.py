import time
from datetime import datetime

import pyowm
from flask import Flask, request, abort


app = Flask(__name__)
db = [
    {
        'name': 'Jack',
        'text': 'Hello',
        'time': time.time()
    },
    {
        'name': 'Mary',
        'text': 'Jack',
        'time': time.time()
    },
]

db_uniq = ['Jack', 'Mary']
db_bot = []

owm = pyowm.OWM('44fadb596090cc2d098c0cc30da68f2b')
mgr = owm.weather_manager()


# while True:
#    db.append({
#        'name': 'Bot',
#       'text': 'Напишите /help для помощи.',
#        'time': time.time(),
#    })
#    time.sleep(30)

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
def status():
    dt = datetime.now()
    return {
        'status': True,
        'name': 'Skillbox Messenger',
        'time1': time.time(),
        'quantity_messages': db.index(db[-1]) + 1,
        'quantity_users': db_uniq.index((db_uniq[-1])) + 1,
    }


@app.route("/send", methods=['POST'])
def send():
    data = request.json
    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if not 0 < len(name) <= 64:
        return abort(400)
    if not 0 < len(text) <= 10000:
        return abort(400)

    db.append({
        'name': name,
        'text': text,
        'time': time.time()
    })
    if name not in db_uniq:
        db_uniq.append(name)

    if text == '/help':
        db.append({
            'name': 'Bot',
            'text': 'Привет, я бот и я умею показывать погоду напишите /weather',
            'time': time.time(),
        })
    if text == '/weather':
        db.append({
            'name': 'Bot',
            'text': 'Напишите в каком городе находитесь в формате "Я тут - \'Город\'',
            'time': time.time(),
        })
    if 'Я тут - ' in str(text):
        place = text[8:]
        observation = mgr.weather_at_place(place)
        w = observation.weather
        db.append({
            'name': 'Bot',
            'text': str(w.detailed_status) + ' и температура ' +  str(w.temperature('celsius')['temp']),
            'time': time.time(),
        })
    return {}


@app.route("/messages")
def messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    filtered_messages = []

    for message in db:
        if message['time'] > after:
            filtered_messages.append(message)

    return {'messages': filtered_messages[:50]}


app.run()
