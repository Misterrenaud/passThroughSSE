#!/bin/python
#encoding:utf-8
from flask import Flask, request
from werkzeug.contrib.fixers import ProxyFix
import uuid

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

def get_uuid():
    return str(uuid.uuid4())

def messages_stream(id):
    listenner_uuid = get_uuid()
    while True:
        yield "data:{}\n\n".format(messages)"

@route("/listen/<room_id>")
def listner(room_id):
    return Response(messages_stream(room_id), mimetype="text/event-stream")

@route("/write/<room_id>")
def write(room_id):
    message = request.data



if __name__ == "__main__":
    app.run()
