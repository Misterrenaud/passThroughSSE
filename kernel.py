#!/bin/python
#encoding:utf-8
from datetime import datetime
from threading import Lock
from queue import Queue

class HouseLock(object):
    def __init__(self):
        self._master_lock = Lock()
        self._queue = Queue()

    def acquire(self, listenner):
        if not self._master_lock.locked():
            self._master_lock.acquire()
            return
        listenner_lock = Lock()
        listenner_lock.acquire()
        self._queue.put(listenner_lock)
        return listenner_lock.acquire()

    def release(self):
        if self._queue.empty():
            return self._master_lock.release()
        next_lock = self._queue.get()
        return next_lock.release()

class TheHouse(object):
    _rooms = {}
    lock = HouseLock()
    lock.acquire("TheRoom")

    @staticmethod
    def _get_room(id):
        room = TheHouse._rooms.get(id)
        if room is None:
            room = Room(id)
            TheHouse._rooms[id] = room
        return room

    @staticmethod
    def write_in_room(room_id, message):
        TheHouse._get_room(room_id)._write(message)
        TheHouse.lock.release()
        # we let through every listener in the queue for The House
        TheHouse.lock.acquire("TheRoom")

    @staticmethod
    def read_from_room(room_id):
        room = TheHouse._rooms.get(room_id)
        if room is None:
            return 0, None
        return room.last_update, room.last_message

    @staticmethod
    def to_json():
        return [room.to_json() for room in TheHouse._rooms.values()]

class Room(object):
    def __init__(self, id):
        self.id = id
        self.last_update = 0
        self.last_message = None

    def _update(self):
        self.last_update = get_ts()

    def _write(self, message):
        self.last_message = message
        self._update()

    def to_json(self):
        return vars(self)

def get_ts():
    return int(datetime.now().timestamp() * 1000)
