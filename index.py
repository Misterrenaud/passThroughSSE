#!/bin/python
#encoding:utf-8
from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.contrib.fixers import ProxyFix
import uuid
from kernel import TheHouse, get_ts

app = Flask(__name__)
cors = CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app)

def get_uuid():
    return str(uuid.uuid4())

def messages_stream(room_id):
    listenner_uuid = get_uuid()
    last_date = get_ts()
    while True:
        TheHouse.lock.acquire(listenner_uuid)
        date, message = TheHouse.read_from_room(room_id)
        TheHouse.lock.release()
        if last_date < date:
            last_date = date
            yield "data:{}\n\n".format(message)

@app.route("/listen/<room_id>")
@cross_origin()
def listner(room_id):
    return Response(messages_stream(room_id), mimetype="text/event-stream")

@app.route("/write/<room_id>", methods=["POST"])
@cross_origin()
def write(room_id):
    TheHouse.write_in_room(room_id, request.data.decode("utf8"))
    return jsonify({"success":True})

@app.route("/ping")
@cross_origin()
def ping():
    return Response("pong")

@app.route("/thehouse")
@cross_origin()
def show_thehouse():
    return jsonify({
        "TheHouse": TheHouse.to_json()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, ssl_context='adhoc')
