"""
The executable file, it handles all user interaction on the CLI and takes away everything in between from
the booking_system file's class RoomBookingSystem. Oh also the errors which were mandatory are attached.
"""
from booking_system import RoomBookingSystem
from exceptions import RoomNotFoundError, RoomAlreadyExistsError, TimeslotAlreadyBookedError

filename = "bookings_final_state.csv"

def main():

    #Loads any preexising data in filename and starts the system
    system = RoomBookingSystem()
    system.load_from_csv(filename)

    print("\nWelcome to the Classroom Booking System!\n")

    while True:
        #The main UI
        print("\n--- MENU ---")
        print("1. Create a New Room")
        print("2. Find Rooms")
        print("3. Book a Room")
        print("4. View a Room's Schedule")
        print("5. Exit")

        choice = input("\nEnter your choice: ").strip()
        
        #I think the stuff under this is pretty self explanatory.
        try:
            if choice == "1":
                print("\n--- Create a New Room ---")
                room_no = input("Enter Room ID: ").strip()
                building = input("Enter Building Name: ").strip()
                capacity = int(input("Enter Capacity: "))
                system.create_room(room_no, building, capacity)

            elif choice == "2":
                print("\n--- Find Rooms ---")
                building = input("Filter by Building (Hit Enter to skip): ").strip() or None
                cap_input = input("Minimum Capacity (Hit Enter to skip): ").strip()
                min_capacity = int(cap_input) if cap_input else None
                hour_input = input("Free at Hour (0-23, Hit Enter to skip): ").strip()
                free_at_hour = int(hour_input) if hour_input else None

                results = system.find_rooms(building, min_capacity, free_at_hour)
                if results:
                    print(f"\nFound {len(results)} room(s):\n")
                    for r in results:
                        print(r)
                        print("-" * 30)
                else:
                    print("\nNo rooms matched your filters.")

            elif choice == "3":
                print("\n--- Book a Room ---")
                room_no = input("Enter Room ID: ").strip()
                hours_input = input("Enter Hour to Book (0-23): ").strip()
                hour = [int(h.strip()) for h in hours_input.split(",") if h.strip()] #This was for taking multiple inputs say segregated by commas, so I could type in say 8, 9, 10 and it'd register it.
                system.book_room(room_no, hour)

            elif choice == "4":
                print("\n--- View Room Details ---")
                room_no = input("Enter Room ID: ").strip()
                system.view_room(room_no)

            elif choice == "5":
                print("\nSaving and exiting...")
                system.save_to_csv(filename)
                break

            else:
                print("Invalid choice. Try again.")

        except (ValueError, RoomNotFoundError, RoomAlreadyExistsError, TimeslotAlreadyBookedError) as e:
            print(f"\nError: {e}")
        except Exception as e:
            print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
