"""
There really isn't much in this file, the only thing here is classes that are defined and are used in other files
with desired outputs being printed out by raising it.
"""

class TimeslotAlreadyBookedError(Exception):
    pass

class RoomNotFoundError(Exception):
    pass

class RoomAlreadyExistsError(Exception):
    pass