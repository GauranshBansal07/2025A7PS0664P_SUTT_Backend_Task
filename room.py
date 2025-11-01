"""
Defines the Room Class

It defines the parameter that each booking holds, room_no, building, capacity and booked hours.

This file provides the methods to check for room availability, booked hours and convert room data to CSV and
get data from CSV.

"""
from exceptions import TimeslotAlreadyBookedError

class Room:
    #Defines the parameters taken into consideration
    def __init__(self, room_no, building, capacity, booked_hours = None):
        self.room_no = room_no
        self.building = building
        self.capacity = capacity
        self.booked_hours = booked_hours if booked_hours is not None else []

    #Returns false if room's not available, if it's returns true
    def availability(self, hour):
        return hour not in self.booked_hours
    
    #Books room for given hour provided it's a valid time, if not then it returns the errors.
    def book(self, hour):
        if hour < 0 or hour>23:
            raise ValueError("Enter an hour in between 0 and 23.")
        if not self.availability(hour):
            raise TimeslotAlreadyBookedError(f"Hour {hour} is already booked for room {self.room_no}.")
        self.booked_hours.append(hour)

    #Returns a text description of the room, it's called whenever you're printing room, __str__ has higher precendance than __repr__ so this'll be called.
    def __str__(self):
        hours = sorted(self.booked_hours)
        hours_display = str(hours) if hours else "[]"
        return (f"ID: {self.room_no}\n"
                f"Building: {self.building}\n"
                f"Capacity: {self.capacity}\n"
                f"Booked Hours: {hours_display}")
    
    #CSV Handling Part
    
    #Converts the room object into something suitable for writing to a csv file.
    def to_csv_row(self):
        hours_list = sorted(self.booked_hours)
        hours_str = ";".join(str(hour) for hour in hours_list)

        return [
            self.room_no,
            self.building,
            str(self.capacity),
            hours_str
        ]

    #Does the opposite of the above function and converts stuff from the csv to room object. It's static because we're
    #getting stuff from the csv file, we don't have anything pertaining to the info we need in room object yet.
    @staticmethod
    def from_csv_row(row):
        booked_hours_str = row.get("booked_hours", "")
        if booked_hours_str:
            booked_hours = [int(hour) for hour in booked_hours_str.split(";") if hour]
        else:
            booked_hours = []

        return Room(
            room_no=row["room_no"],
            building=row["building"],
            capacity=int(row["capacity"]),
            booked_hours=booked_hours
        )


