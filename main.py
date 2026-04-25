import psycopg2
import psycopg2.extras 
import sys

"""
Notes:
1. Do we care about the case of a foreign key error, for example an a manager enters an invalid hotel address, do we want to handle this without an exception?
2. Mix up join order in queries if you have to submit code
"""
def login(conn):
    while True:
        print("Thank you for choosing to login! Please select your role:")
        print("1. Manager")
        print("2. Client")
        print("3. Back to main menu")
        roleChoice = input("Enter your choice: ")
        if roleChoice == '1':
            loginManager(conn)
        elif roleChoice == '2':
            loginClient(conn)
        elif roleChoice == '3':
            main()
        
def register(conn):
    while True:
        print("Thank you for choosing to register with us! Please select your role:")
        print("1. Manager")
        print("2. Client")
        print("3. Back to main menu")
        roleChoice = input("Enter your choice: ")
        if roleChoice == '1':
            registerManager(conn)
        elif roleChoice == '2':
            registerClient(conn)
        elif roleChoice == '3':
            main()

def loginManager(conn):
    ssn = input("Please enter your SSN to login: ")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Manager WHERE ssn = %s", (ssn,))
        manager = cur.fetchone()
        if manager:
            print(f"Login Successful. Welcome, {manager['name']}!")
            managerOperations(conn, ssn)
        else:
            print("No manager found with this SSN. Please try again.")
    return

def loginClient(conn):
    pass

def registerManager(conn):
    print("Please enter the requested details")
    name = input("Name: ")
    email = input("Email: ")
    ssn = input("SSN: ")

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Manager WHERE ssn = %s", (ssn,))
        manager = cur.fetchone()
        if manager:
            print("Manager with this SSN already exists. Please try again.")

        else:
            cur.execute("INSERT INTO Manager (name, email, ssn) VALUES (%s, %s, %s)", (name, email, ssn))
            conn.commit()
            print(f"Manager with SSN {ssn} registered successfully.")
            managerOperations(conn, ssn)
    return

def registerClient(conn):
    pass

"""
2. Managers should be able to insert, remove, and update hotels and rooms.
3. Managers should be able to remove clients from the system.
4. Managers should be able to input a number k, and the system should return the names
and emails of the top-k clients based on the number of bookings.
5. Managers should be able to generate a list of all hotel rooms along with the number
of bookings for each room.
6. Managers should be able to generate a list: for every hotel X show the name of X, the
total number of bookings in X, and the average rating of X.
7. A manager should be able to input two cities C1 and C2, and the system should return
the names and emails of clients who have at least one address in C1 and have booked
a hotel located in C2.
8. Managers should be able to report the names of problematic local hotels. These are
hotels located in Chicago with an average rating less than 2, and that have been
booked by at least two different clients, each of whom has no address in city Chicago.
9. Managers should be able to report a list showing each client’s name along with the
total amount they have spent on bookings.
"""

def managerOperations(conn, ssn):
    while True:
        print("======Manager Operations======")
        print("1. Insert/Remove/Update Hotels or Rooms")
        print("2. Remove Client")
        print("3. Top-k Clients")
        print("4. Number of Bookings for Each Room")
        print("5. Hotel Booking and Rating Summary")
        print("6. Clients with Addresses in C1 and Bookings in C2")
        print("7. Problematic Local Hotels")
        print("8. Total Amount Spent by Each Client")
        print("9. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            managerUpdateHotelRoom(conn)
        elif choice == '2':
            managerRemoveClient(conn)
        elif choice == '3':
            managerTopKClients(conn)
        elif choice == '4':
            managerNumBookingsEachRoom(conn)
        elif choice == '5':
            managerHotelBookingRatingSummary(conn)
        elif choice == '6':
            managerClientsC1BookingsC2(conn)
        elif choice == '7':
            managerProblematicLocalHotels(conn)
        elif choice == '8':
            managerTotalAmountSpent(conn)
        elif choice == '9':
            print("Logging out...")
            main()
        
def managerRemoveClient(conn):
    print("Please enter the client details as requested below")
    email = input("Email: ")

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Client WHERE email = %s", (email,))
        client = cur.fetchone()
        if client:
            cur.execute("DELETE FROM Booking WHERE client_email = %s", (email,))
            cur.execute("DELETE FROM Review WHERE client_email = %s", (email,))
            cur.execute("DELETE FROM ClientAddress WHERE client_email = %s", (email,))
            cur.execute("DELETE FROM CreditCard WHERE client_email = %s", (email,))
            cur.execute("DELETE FROM Client WHERE email = %s", (email,))
            conn.commit()
            print(f"Client with email {email} removed successfully.")
        else:
            print("No client found with this email.")

def managerTopKClients(conn):
    k = input("Please enter the value of k: ")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT name, email, COUNT(booking_id) AS count
        FROM Client
        JOIN Booking ON Client.email = Booking.client_email
        GROUP BY name, email
        ORDER BY count DESC
        LIMIT %s;
        """
        cur.execute(query, (k,))
        clients = cur.fetchall()
        print(f"Top {k} clients based on number of bookings:")
        for client in clients:
            print(f"Name: {client['name']}, Email: {client['email']}, Number of Bookings: {client['count']}")

def managerNumBookingsEachRoom(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT Room.hotel_id, Room.room_number, COUNT(booking_id) AS count
        FROM Room
        JOIN Booking ON Room.hotel_id = Booking.hotel_id AND Room.room_number = Booking.room_number
        GROUP BY Room.hotel_id, Room.room_number
        ORDER BY Room.hotel_id, Room.room_number ASC;
        """
        cur.execute(query)
        rooms = cur.fetchall()
        print("Number of bookings for each room:")
        for room in rooms:
            print(f"Hotel ID: {room['hotel_id']}, Room Number: {room['room_number']}, Number of Bookings: {room['count']}")

def managerHotelBookingRatingSummary(conn):
    # lets try an approach without left joins
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT Hotel.hotel_id, Hotel.name, COUNT(booking_id) AS total_bookings, AVG(rating) AS average_rating
        FROM Hotel
        JOIN Booking ON Hotel.hotel_id = Booking.hotel_id
        JOIN Review ON Hotel.hotel_id = Review.hotel_id
        GROUP BY Hotel.hotel_id, Hotel.name
        ORDER BY Hotel.hotel_id ASC;
        """
        cur.execute(query)
        hotels = cur.fetchall()
        print("Hotel booking and rating summary:")
        for hotel in hotels:
            print(f"Hotel ID: {hotel['hotel_id']}, Name: {hotel['name']}, Total Bookings: {hotel['total_bookings']}, Average Rating: {hotel['average_rating']}")

def managerClientsC1BookingsC2(conn):
    c1 = input("Please enter city C1: ")
    c2 = input("Please enter city C2: ")
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT DISTINCT Client.name, Client.email
        FROM Client
        JOIN ClientAddress ON Client.email = ClientAddress.client_email
        JOIN Booking ON Client.email = Booking.client_email
        JOIN Hotel ON Booking.hotel_id = Hotel.hotel_id
        WHERE ClientAddress.city = %s AND Hotel.city = %s;
        """
        cur.execute(query, (c1, c2))
        clients = cur.fetchall()
        print(f"Clients with addresses in {c1} and bookings in {c2}:")
        for client in clients:
            print(f"Name: {client['name']}, Email: {client['email']}")

def managerProblematicLocalHotels(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT Hotel.name
        FROM Hotel
        JOIN Review ON Hotel.hotel_id = Review.hotel_id
        WHERE Hotel.city = 'Chicago'
        AND Hotel.hotel_id IN (
            SELECT Booking.hotel_id
            FROM Booking
            JOIN Client ON Booking.client_email = Client.email
            WHERE NOT EXISTS (
                SELECT 1 FROM ClientAddress
                WHERE ClientAddress.client_email = Client.email
                AND ClientAddress.city = 'Chicago'
            )
            GROUP BY Booking.hotel_id
            HAVING COUNT(DISTINCT Booking.client_email) >= 2
        )
        GROUP BY Hotel.hotel_id, Hotel.name
        HAVING AVG(Review.rating) < 2;
        """
        cur.execute(query)
        hotels = cur.fetchall()
        print("Problematic local hotels:")
        for hotel in hotels:
            print(f"Name: {hotel['name']}")

def managerTotalAmountSpent(conn):
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT Client.name, SUM((Booking.end_date - Booking.start_date) * Booking.price_per_day) AS total_spent
        FROM Client
        JOIN Booking ON Client.email = Booking.client_email
        GROUP BY Client.name
        ORDER By Client.name ASC;
        """
        cur.execute(query)
        clients = cur.fetchall()
        print("Total amount spent by each client:")
        for client in clients:
            print(f"Name: {client['name']}, Total Amount Spent: {client['total_spent']}")
   


def managerUpdateHotelRoom(conn):
    while True:
        print("======Hotel/Room Management======")
        print("1. Insert Hotel")
        print("2. Remove Hotel")
        print("3. Update Hotel")
        print("4. Insert Room")
        print("5. Remove Room")
        print("6. Update Room")
        print("7. Back to Manager Operations")
        print("8. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            insertHotel(conn)
        elif choice == '2':
            removeHotel(conn)
        elif choice == '3':
            updateHotel(conn)
        elif choice == '4':
            insertRoom(conn)
        elif choice == '5':
            removeRoom(conn)
        elif choice == '6':
            updateRoom(conn)
        elif choice == '7':
            managerOperations(conn)
        elif choice == '8':
            print("Logging out...")
            main()

def insertHotel(conn):
    print("Please enter the hotel details as requested below")
    id = input("ID: ")
    name = input("Name: ")
    streetName = input("Street name: ")
    streetNumber = input("Street number: ")
    city = input("City: ")

    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Hotel WHERE hotel_id = %s", (id,))
        hotel = cur.fetchone()
        if hotel:
            print("Hotel with this ID already exists. Please enter a different hotel.")
        else:
            cur.execute("INSERT INTO Hotel (hotel_id, name, street_name, number, city) VALUES (%s, %s, %s, %s, %s)", (id, name, streetName, streetNumber, city))
            conn.commit()
            print(f"Hotel with ID {id} inserted successfully.")

def updateHotel(conn):
    print("Please enter the hotel details as requested below")
    id = input("ID: ")
    name = input("Name: ")
    streetName = input("Street name: ")
    streetNumber = input("Street number: ")
    city = input("City: ")

    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Hotel WHERE hotel_id = %s", (id,))
        hotel = cur.fetchone()
        if hotel:
            cur.execute("UPDATE Hotel SET name = %s, street_name = %s, number = %s, city = %s WHERE hotel_id = %s", (name, streetName, streetNumber, city, id))
            conn.commit()
            print(f"Hotel with ID {id} updated successfully.")
        else:
            print("No hotel found with this ID. Please try again.")
    
def removeHotel(conn):
    print("Please enter the hotel details as requested below")
    id = input("ID: ")

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Hotel WHERE hotel_id = %s", (id,))
        hotel = cur.fetchone()
        if hotel:
            cur.execute("DELETE FROM Booking WHERE hotel_id = %s", (id,))
            cur.execute("DELETE FROM Room WHERE hotel_id = %s", (id,))
            cur.execute("DELETE FROM Review WHERE hotel_id = %s", (id,))
            cur.execute("DELETE FROM Hotel WHERE hotel_id = %s", (id,))
            conn.commit()
            print(f"Hotel with ID {id} removed successfully.")
        else:
            print("No hotel found with this ID.")

def insertRoom(conn):
    print("Please enter the room details as requested below")
    hotel_id = input("Hotel ID: ")
    room_number = input("Room number: ")
    windows = input("Windows: ")
    renovation_year = input("Renovation year: ")
    access_type = input("Access type: ")

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
        room = cur.fetchone()
        if room:
            print("Room with this ID already exists. Please enter a different room ID.")
        else:
            cur.execute("INSERT INTO Room (hotel_id, room_number, windows, renovation_year, access_type) VALUES (%s, %s, %s, %s, %s)", (hotel_id, room_number, windows, renovation_year, access_type))
            conn.commit()
            print(f"Room with ID {room_number} inserted successfully.")

def updateRoom(conn):
    print("Please enter the room details as requested below")
    hotel_id = input("Hotel ID: ")
    room_number = input("Room number: ")
    windows = input("Windows: ")
    renovation_year = input("Renovation year: ")
    access_type = input("Access type: ")

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
        room = cur.fetchone()
        if room:
            cur.execute("UPDATE Room SET windows = %s, renovation_year = %s, access_type = %s WHERE hotel_id = %s AND room_number = %s", (windows, renovation_year, access_type, hotel_id, room_number))
            conn.commit()
            print(f"Room with ID {room_number} updated successfully.")
        else:
            print("No room found with this ID. Please try again.")

def removeRoom(conn):
    print("Please enter the room details as requested below")
    hotel_id = input("Hotel ID: ")
    room_number = input("Room number: ")

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
        room = cur.fetchone()
        if room:
            cur.execute("DELETE FROM Booking WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
            cur.execute("DELETE FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
            conn.commit()
            print(f"Room with ID {room_number} removed successfully.")
        else:
            print("No room found with this ID.")

def main():
    conn = psycopg2.connect(
        host="localhost",
        database="hotel_management",
        user="anupamsai",
        port="5432"
    )
    
    try:
        while True:
            print("======Jarvis - Your Hotel Management Assistant======")
            print("1. Login")
            print("2. Register")
            print("3. Exit")

            choice = input("Enter your choice: ")
            if choice == '1':
                login(conn)
            elif choice == '2':
                register(conn)
            elif choice == '3':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return

if __name__ == "__main__":
    main()