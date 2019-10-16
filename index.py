#!/bin/python
#encoding:utf-8
from flask import Flask, request, Response, jsonify
from werkzeug.contrib.fixers import ProxyFix
import uuid
from kernel import TheHouse

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

def get_uuid():
    return str(uuid.uuid4())

def messages_stream(room_id):
    listenner_uuid = get_uuid()
    while True:
        TheHouse.lock.aquire(listenner_uuid)
        message = TheHouse.read_from_room(room_id)
        TheHouse.lock.release()
        yield "data:{}\n\n".format(messages)

@app.route("/listen/<room_id>")
def listner(room_id):
    return Response(messages_stream(room_id), mimetype="text/event-stream")

@app.route("/write/<room_id>", methods=["POST"])
def write(room_id):
    TheHouse.write_in_room(room_id, request.data)
    return jsonify({"success":True})

@app.route("/ping")
def ping():
    return Response("pong")

@app.route("/thehouse")
def show_thehouse():
    return jsonify({
        "TheHouse": TheHouse.to_json()
    })
