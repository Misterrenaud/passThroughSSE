#!/bin/python
#encoding:utf-8
from datetime import datetime
from threading import Lock
from queue import Queue

class HouseLock(object):
    def __init__(self):
        self._lock = Lock()
        self._queue = Queue()

    def aquire(self, listenner):
        if self._lock.locked():
            self._queue.put(listenner)
        return self._lock.aquire()

    def release(self):
        self._lock.release()

class TheHouse(object):
    _rooms = {}
    lock = HouseLock()
    lock.aquire("TheRoom")

    @staticmethod
    def _get_room(id):
        room = TheHouse._rooms.get(id)
        if room is None:
            room = Room(id)
            TheHouse._rooms[id] = room
        return room

    @staticmethod
    def write_in_room(id, message):
        TheHouse._get_room(room_id)._write(message)
        TheHouse.lock.release()
        # we let through every listener in the queue for The House
        TheHouse.lock.aquire("TheRoom")

    @staticmethod
    def to_json():
        return [room.to_json() for room in TheHouse._rooms.values()]

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
