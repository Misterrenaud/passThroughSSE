#!/bin/python
#encoding:utf-8
from flask import Flask, request, Response, jsonify
from werkzeug.contrib.fixers import ProxyFix
import uuid
from datetime import datetime
from threading import Lock
from queue import Queue

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

def get_uuid():
    return str(uuid.uuid4())

def messages_stream(id):
    listenner_uuid = get_uuid()
    while True:
        # get message from room
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

class QLock(object):
    def __init__(self):
        self.__lock = Lock()

    def __enter__(self):
        return self.__lock.aquire()

    def __exit__(self, type, value, traceback):
        #Exception handling here
        self.__lock.release()

class TheHouse(object):
    __rooms = {}
    lock = QLock()

    @staticmethod
    def _get_room(id):
        room = TheHouse.__rooms.get(id)
        if room is None:
            room = Room(id)
            TheHouse.__rooms[id] = room
        return room

    @staticmethod
    def write_in_room(id, message):
        TheHouse._get_room(room_id)._write(message)

    @staticmethod
    def to_json():
        return [room.to_json() for room in TheHouse.__rooms]

class Room(object):
    def __init__(self, id):
        self.id = id
        self.last_update = 0
        self.last_message = None

    def _update(self):
        self.last_update = int(datetime.now().timestamp() * 1000)

    def _write(self, message):
        self.last_message = message
        self._update()

    def to_json():
        return self.__dict__
