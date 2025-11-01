"""
Defines the RoomBookingSystem which manages the overall classroom booking logic. Manages the preexisting room
objects and helps store them and create new ones too. Handles the booking part by helping with filtering and searching
Also loads and sends all data to the csv file.

"""
import csv
from room import Room
from exceptions import RoomNotFoundError, RoomAlreadyExistsError


class RoomBookingSystem:
    #Creates and empty dict of rooms
    def __init__(self):
        self.rooms = {}
    # Creates a new room in the system taking the parameters room_no, building and capacity (I didn't include
    # opening and closing hours since I'd have to fix the room.py, maybe add two parameters in the __init__ part
    # being open and close and then edit the book() accordingly by adding in another if statement. first then
    # I'd have to force 2 more columns in the csv file as well ) and utilises the error in case of it already
    # existing.
    def create_room(self, room_no, building, capacity):
        if room_no in self.rooms:
            raise RoomAlreadyExistsError(f"Room '{room_no}' already exists.")
        
        self.rooms[room_no] = Room(room_no, building, capacity)
        print(f"Room '{room_no}' created successfully.")

    #Books one or more hours for a room and returns error if there's no room with the given id
    def book_room(self, room_no, hours):
        room = self.rooms.get(room_no)
        if not room:
            raise RoomNotFoundError(f"No room found with ID '{room_no}'.")

        if isinstance(hours, int):
            hours = [hours]

        booked_success = []
        already_booked = []

        for hour in hours:
            if room.availability(hour):
                room.book(hour)
                booked_success.append(hour)
            else:
                already_booked.append(hour)

        if booked_success:
            print(f"Successfully booked Room {room_no} for hour(s): {', '.join(map(str, booked_success))}.")
        if already_booked:
            print(f"Room {room_no} was already booked for hour(s): {', '.join(map(str, already_booked))}.")

    #filters rooms according to filters and returns a list of rooms which match the criteria
    def find_rooms(self, building=None, min_capacity=None, free_at_hour=None):
        results = []
        for room in self.rooms.values():
            if building and room.building.lower() != building.lower():
                continue
            if min_capacity and room.capacity < min_capacity:
                continue
            if free_at_hour is not None and not room.is_available(free_at_hour):
                continue
            results.append(room)
        return results

    #This is where the __str__ part's used in room.py
    def view_room(self, room_no):
        room = self.rooms.get(room_no)
        if not room:
            raise RoomNotFoundError(f"No room found with ID '{room_no}'.")
        print(room)

    #Loads rooms and booked hours from the csv file.
    def load_from_csv(self, filename):
        try:
            with open(filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    room = Room.from_csv_row(row)
                    self.rooms[room.room_no] = room
            print(f"Loaded {len(self.rooms)} rooms from '{filename}'.")
        except FileNotFoundError:
            print(f"No existing data file found ('{filename}'). Starting fresh.")

    #Saves all data into a csv file.
    def save_to_csv(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["room_no", "building", "capacity", "booked_hours"])
            for room in self.rooms.values():
                writer.writerow(room.to_csv_row())
        print(f"Data saved successfully to '{filename}'.")
