import psycopg2
import psycopg2.extras 
import sys

def login(conn):
    while True:
        print("====================================================")
        print("             * Hotel Management Login *             ")
        print("              Please select your role:              ")
        print("====================================================")
        print("1. Manager")
        print("2. Client")
        print("3. Back to main menu")
        print()
        roleChoice = input("Enter your choice: ")
        print()
        if roleChoice == '1':
            loginManager(conn)
        elif roleChoice == '2':
            loginClient(conn)
        elif roleChoice == '3':
            return
        
def register(conn):
    while True:
        print("====================================================")
        print("          * Hotel Management Registration *         ")
        print("              Please select your role:              ")
        print("====================================================")
        print("1. Manager")
        print("2. Client")
        print("3. Back to main menu")
        print()
        roleChoice = input("Enter your choice: ")
        print()
        if roleChoice == '1':
            registerManager(conn)
        elif roleChoice == '2':
            registerClient(conn)
        elif roleChoice == '3':
            return

def loginManager(conn):
    print("====================================================")
    print("                 * Manager Login *                  ")
    print("====================================================")
    ssn = input("Please enter your SSN: ")
    print()
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Manager WHERE ssn = %s", (ssn,))
        manager = cur.fetchone()
        if manager:
            print(f"Login Successful! Welcome, {manager['name']}!")
            print()
            managerOperations(conn)
        else:
            print("No manager found with this SSN. Please try again.")
            print()
    return

def loginClient(conn):
    print("====================================================")
    print("                 * Client Login *                  ")
    print("====================================================")
    email = input("Please enter your email: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Client WHERE email = %s", (email,))
        client = cur.fetchone()

        if client:
            print(f"Login Successful! Welcome, {client['name']}!")
            print()
            clientOperations(conn, email)
        else:
            print("No client found with this email. Please try again.")
            print()

def registerManager(conn):
    print("====================================================")
    print("              * Manager Registration *              ")
    print("====================================================")
    name = input("Name: ")
    email = input("Email: ")
    ssn = input("SSN: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Manager WHERE ssn = %s", (ssn,))
        manager = cur.fetchone()
        if manager:
            print("Manager with this SSN already exists. Please try again.")
            print()

        else:
            cur.execute("INSERT INTO Manager (name, email, ssn) VALUES (%s, %s, %s)", (name, email, ssn))
            conn.commit()
            print(f"Manager with SSN {ssn} registered successfully!")
            print()
            managerOperations(conn)
    return

def registerClient(conn):
    print("====================================================")
    print("               * Client Registration *              ")
    print("====================================================")
    name = input("Name: ")
    email = input("Email: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Client WHERE email = %s", (email,))
        existing_client = cur.fetchone()

        if existing_client:
            print("Client with this email already exists.")
            print()
            return
        
        try:
            cur.execute(
                "INSERT INTO Client (email, name) VALUES (%s, %s)", (email, name)
            )
            print("---------------------------------------------")
            num_addresses = int(input("How many addresses would you like to add? "))

            if num_addresses < 1:
                print("A client must have at least one address.")
                print()
                conn.rollback()
                return
            
            for i in range(num_addresses):
                print(f"Address {i + 1}:")
                street_name = input("   Street name: ")
                number = input("   Street number: ")
                city = input("   City: ")
                print()

                cur.execute("""
                    INSERT INTO Address (street_name, number, city)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (street_name, number, city) DO NOTHING
                """, (street_name, number, city))

                cur.execute("""
                    INSERT INTO ClientAddress (client_email, street_name, number, city)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                """, (email, street_name, number, city))

            print("---------------------------------------------")
            num_cards = int(input("How many credit cards would you like to add? "))

            if num_cards < 1:
                print("A client must have at least one credit card.")
                print()
                conn.rollback()
                return
            
            for i in range(num_cards):
                print(f"Credit Card {i + 1}:")
                card_number = input("   Card number: ")

                print("   Billing address for this card:")
                billing_street = input("   Billing street name: ")
                billing_number = input("   Billing street number: ")
                billing_city = input("   Billing city: ")
                print()

                cur.execute("""
                    INSERT INTO Address (street_name, number, city)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (street_name, number, city) DO NOTHING
                """, (billing_street, billing_number, billing_city))

                cur.execute("""
                    INSERT INTO CreditCard (
                            card_number,
                            client_email,
                            billing_street_name,
                            billing_number,
                            billing_city
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (card_number, email, billing_street, billing_number, billing_city))

            conn.commit()
            print("Client registered successfully!")
            print()
            clientOperations(conn, email)

        except Exception as e:
            conn.rollback()
            print(f"Registration failed: {e}")
            print()

def managerOperations(conn):
    while True:
        print("====================================================")
        print("               * Manager Operations *               ")
        print("====================================================")
        print("1. Insert/Remove/Update Hotels or Rooms")
        print("2. Remove Client")
        print("3. Top-k Clients")
        print("4. Number of Bookings for Each Room")
        print("5. Hotel Booking and Rating Summary")
        print("6. Clients with Addresses in C1 and Bookings in C2")
        print("7. Problematic Local Hotels")
        print("8. Total Amount Spent by Each Client")
        print("9. Logout")
        print()
        choice = input("Enter your choice: ")
        print()
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
            print()
            return
        else:
            print("Invalid choice. Please try again.")
            print()
        
def managerRemoveClient(conn):
    print("====================================================")
    print("                 * Remove Client *                  ")
    print("====================================================")
    print("Please enter the client details as requested below")
    email = input("Email: ")
    print()

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

            print(f"Client with email {email} removed successfully!")
            print()
        else:
            print("No client found with this email.")
            print()

def managerTopKClients(conn):
    print("====================================================")
    print("                 * Top-k Clients *                  ")
    print("====================================================")
    k = input("Please enter the value of k: ")
    print()
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
        print()
        for client in clients:
            print(f"Name: {client['name']}, Email: {client['email']}, Number of Bookings: {client['count']}")
        print()

def managerNumBookingsEachRoom(conn):
    print("====================================================")
    print("        * Number Of Bookings For Each Room *        ")
    print("====================================================")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT Room.hotel_id, Room.room_number, COUNT(Booking.booking_id) AS count
        FROM Room
        LEFT JOIN Booking ON Room.hotel_id = Booking.hotel_id AND Room.room_number = Booking.room_number
        GROUP BY Room.hotel_id, Room.room_number
        ORDER BY Room.hotel_id, Room.room_number ASC;
        """
        cur.execute(query)
        rooms = cur.fetchall()
        for room in rooms:
            print(f"Hotel ID: {room['hotel_id']}, Room Number: {room['room_number']}, Number of Bookings: {room['count']}")
        print()

def managerHotelBookingRatingSummary(conn):
    print("====================================================")
    print("         * Hotel Booking & Rating Summary *         ")
    print("====================================================")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        WITH numberOfBookings AS (
            SELECT hotel_id, COUNT(*) AS bookings
            FROM Booking
            GROUP BY hotel_id
        ),
        avgRatings AS (
            SELECT hotel_id, AVG(rating) AS avg
            FROM Review
            GROUP BY hotel_id
        )
        SELECT 
            Hotel.hotel_id,
            Hotel.name,
            COALESCE(numberOfBookings.bookings, 0) AS bookings,
            avgRatings.avg
        FROM Hotel
        LEFT JOIN numberOfBookings ON Hotel.hotel_id = numberOfBookings.hotel_id
        LEFT JOIN avgRatings ON Hotel.hotel_id = avgRatings.hotel_id
        ORDER BY Hotel.hotel_id ASC;
        """
        cur.execute(query)
        hotels = cur.fetchall()
        for hotel in hotels:
            print(f"Hotel ID: {hotel['hotel_id']}, Name: {hotel['name']}, Total Bookings: {hotel['bookings']}, Average Rating: {hotel['avg']}")
        print()

def managerClientsC1BookingsC2(conn):
    print("====================================================")
    print("  * Clients with Adresses in C1 & Bookings in C2 *  ")
    print("====================================================")
    c1 = input("Please enter city C1: ")
    c2 = input("Please enter city C2: ")
    print()
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT DISTINCT Client.name, Client.email
        FROM Client
        JOIN Booking ON Client.email = Booking.client_email
        JOIN ClientAddress ON Client.email = ClientAddress.client_email
        JOIN Hotel ON Booking.hotel_id = Hotel.hotel_id
        WHERE ClientAddress.city = %s AND Hotel.city = %s;
        """
        cur.execute(query, (c1, c2))
        clients = cur.fetchall()
        print(f"Clients with addresses in {c1} and bookings in {c2}:")
        print("-------------------------------------------------------------")
        for client in clients:
            print(f"Name: {client['name']}, Email: {client['email']}")
        print()

def managerProblematicLocalHotels(conn):
    print("====================================================")
    print("            * Problematic Local Hotels *            ")
    print("====================================================")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        WITH allClients AS (
            SELECT Client.email
            FROM Client
        ),
        chicagoClients AS (
            SELECT ClientAddress.client_email AS email
            FROM ClientAddress
            WHERE ClientAddress.city = 'Chicago'
        ),
        nonChicagoClients AS (
            SELECT email FROM allClients
            EXCEPT
            SELECT email FROM chicagoClients
        ),
        bookedByNonChicago AS (
            SELECT Booking.hotel_id, COUNT(DISTINCT Booking.client_email) AS nonChicagoBookers
            FROM Booking
            JOIN nonChicagoClients ON Booking.client_email = nonChicagoClients.email
            GROUP BY Booking.hotel_id
            HAVING COUNT(DISTINCT Booking.client_email) >= 2
        ),
        chicagoHotels AS (
            SELECT Hotel.hotel_id, Hotel.name
            FROM Hotel
            WHERE Hotel.city = 'Chicago'
        ),
        lowRatedChicagoHotels AS (
            SELECT chicagoHotels.hotel_id, chicagoHotels.name
            FROM chicagoHotels
            JOIN Review ON chicagoHotels.hotel_id = Review.hotel_id
            GROUP BY chicagoHotels.hotel_id, chicagoHotels.name
            HAVING AVG(Review.rating) < 2
        )
        SELECT lowRatedChicagoHotels.name
        FROM lowRatedChicagoHotels
        JOIN bookedByNonChicago ON lowRatedChicagoHotels.hotel_id = bookedByNonChicago.hotel_id;
        """

        cur.execute(query)
        hotels = cur.fetchall()
        for hotel in hotels:
            print(f"Name: {hotel['name']}")
        print()

def managerTotalAmountSpent(conn):
    print("====================================================")
    print("        * Total Amount Spent by Each Client *       ")
    print("====================================================")
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT Client.name, SUM((Booking.end_date - Booking.start_date) * Booking.price_per_day) AS total
        FROM Client
        JOIN Booking ON Client.email = Booking.client_email
        GROUP BY Client.name
        ORDER By Client.name ASC;
        """
        cur.execute(query)
        clients = cur.fetchall()
        for client in clients:
            print(f"Name: {client['name']}, Total Amount Spent: {client['total']}")
        print()
   
def managerUpdateHotelRoom(conn):
    while True:
        print("====================================================")
        print("              * Hotel/Room Management *             ")
        print("====================================================")
        print("1. Insert Hotel")
        print("2. Remove Hotel")
        print("3. Update Hotel")
        print("4. Insert Room")
        print("5. Remove Room")
        print("6. Update Room")
        print("7. Back to Manager Operations")
        print("8. Logout")
        print()
        choice = input("Enter your choice: ")
        print()

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
            print()
            return

def insertHotel(conn):
    print("====================================================")
    print("                  * Insert Hotel *                  ")
    print("====================================================")
    id = input("ID: ")
    name = input("Name: ")
    streetName = input("Street name: ")
    streetNumber = input("Street number: ")
    city = input("City: ")
    print()
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Hotel WHERE hotel_id = %s", (id,))
        hotel = cur.fetchone()
        if hotel:
            print("Hotel with this ID already exists. Please enter a different hotel.")
            print()
            return

        cur.execute("SELECT 1 FROM Address WHERE street_name = %s AND number =%s AND city = %s", (streetName, streetNumber, city))

        if not cur.fetchone():
            cur.execute("INSERT INTO Address (street_name, number, city) Values (%s, %s, %s)", (streetName, streetNumber, city))

        cur.execute("INSERT INTO Hotel (hotel_id, name, street_name, number, city) VALUES (%s, %s, %s, %s, %s)", (id, name, streetName, streetNumber, city))
        conn.commit()
        print(f"Hotel with ID {id} inserted successfully!")
        print()

def updateHotel(conn):
    print("====================================================")
    print("                  * Update Hotel *                  ")
    print("====================================================")
    print("Please enter updated hotel details below:")
    id = input("ID: ")
    name = input("Name: ")
    streetName = input("Street name: ")
    streetNumber = input("Street number: ")
    city = input("City: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Hotel WHERE hotel_id = %s", (id,))
        hotel = cur.fetchone()
        if not hotel:
            print("No hotel found with this ID. Please try again.")
            print()
            return

        cur.execute("SELECT 1 FROM Address WHERE street_name = %s AND number = %s AND city = %s", (streetName, streetNumber, city))

        if not cur.fetchone():
            cur.execute("INSERT INTO Address (street_name, number, city) VALUES (%s, %s, %s)", (streetName, streetNumber, city))

        cur.execute("UPDATE Hotel SET name = %s, street_name = %s, number = %s, city = %s WHERE hotel_id = %s", (name, streetName, streetNumber, city, id))
        conn.commit()
        print(f"Hotel with ID {id} updated successfully!")
        print()
    
def removeHotel(conn):
    print("====================================================")
    print("                  * Remove Hotel *                  ")
    print("====================================================")
    id = input("ID: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Hotel WHERE hotel_id = %s", (id,))
        hotel = cur.fetchone()
        if hotel:
            cur.execute("DELETE FROM Booking WHERE hotel_id = %s", (id,))
            cur.execute("DELETE FROM Room WHERE hotel_id = %s", (id,))
            cur.execute("DELETE FROM Review WHERE hotel_id = %s", (id,))
            cur.execute("DELETE FROM Hotel WHERE hotel_id = %s", (id,))
            conn.commit()
            print(f"Hotel with ID {id} removed successfully!")
            print()
        else:
            print("No hotel with this ID found.")
            print()

def insertRoom(conn):
    print("====================================================")
    print("                  * Insert Room *                   ")
    print("====================================================")
    hotel_id = input("Hotel ID: ")
    room_number = input("Room number: ")
    windows = input("Windows: ")
    renovation_year = input("Renovation year: ")
    access_type = input("Access type: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
        room = cur.fetchone()
        if room:
            print("Room with this ID already exists. Please enter a different room ID.")
            print()
        else:
            cur.execute("INSERT INTO Room (hotel_id, room_number, windows, renovation_year, access_type) VALUES (%s, %s, %s, %s, %s)", (hotel_id, room_number, windows, renovation_year, access_type))
            conn.commit()
            print(f"Room with ID {room_number} inserted successfully!")
            print()

def updateRoom(conn):
    print("====================================================")
    print("                  * Update Room *                   ")
    print("====================================================")
    print("Please enter updated room details below:")
    hotel_id = input("Hotel ID: ")
    room_number = input("Room number: ")
    windows = input("Windows: ")
    renovation_year = input("Renovation year: ")
    access_type = input("Access type: ")
    print()
    
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
        room = cur.fetchone()
        if room:
            cur.execute("UPDATE Room SET windows = %s, renovation_year = %s, access_type = %s WHERE hotel_id = %s AND room_number = %s", (windows, renovation_year, access_type, hotel_id, room_number))
            conn.commit()
            print(f"Room with ID {room_number} updated successfully!")
            print()
        else:
            print("No room found with this ID. Please try again.")
            print()

def removeRoom(conn):
    print("====================================================")
    print("                  * Remove Room *                   ")
    print("====================================================")
    hotel_id = input("Hotel ID: ")
    room_number = input("Room number: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
        room = cur.fetchone()
        if room:
            cur.execute("DELETE FROM Booking WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
            cur.execute("DELETE FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
            conn.commit()
            print(f"Room with ID {room_number} removed successfully!")
            print()
        else:
            print("No room found with this ID.")
            print()

def clientOperations(conn, email):
    while True:
        print("====================================================")
        print("                * Client Operations *               ")
        print("====================================================")
        print("1. Update My Information")
        print("2. Search Available Rooms")
        print("3. Book a Specific Room")
        print("4. Auto-Book a Room at a Hotel")
        print("5. View My Bookings")
        print("6. Submit Review")
        print("7. Logout")
        print()
        choice = input("Enter your choice: ")
        print()

        if choice == '1':
            updateClientInfo(conn, email)
        elif choice == '2':
            searchAvailableRooms(conn)
        elif choice == '3':
            bookRoom(conn, email)
        elif choice == '4':
            autoBookRoom(conn, email)
        elif choice == '5':
            viewBookings(conn,email)
        elif choice == '6':
            submitReview(conn,email)
        elif choice == '7':
            print("Logging out...")
            print()
            return
        else:
            print("Invalid choice. Please try again.")
            print()

###
### Helper functions for input validation ###
###
def _get_date(prompt):
    from datetime import datetime
    while True:
        val = input(prompt).strip()
        try:
            datetime.strptime(val, "%Y-%m-%d")
            return val
        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD format.")

def _get_positive_int(prompt):
    while True:
        val = input(prompt).strip()
        if val.isdigit() and int(val) > 0:
            return int(val)
        print("Please enter a positive integer.")

def _get_positive_decimal(prompt):
    while True:
        val = input(prompt).strip()
        try:
            f = float(val)
            if f > 0:
                return f
            print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")
### End of helper functions ###

def searchAvailableRooms(conn):
    print("====================================================")
    print("             * Search Available Rooms *             ")
    print("====================================================")
    print("Please enter the date range for your search:")
    start_date = _get_date("Enter start date (YYYY-MM-DD): ")
    end_date = _get_date("Enter end date (YYYY-MM-DD): ")
    print()
    if start_date > end_date:
        print("Start date must be before or equal to end date.")
        print()
        return

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        query = """
        SELECT Hotel.name AS hotel_name, Room.hotel_id, Room.room_number
        FROM Room
        JOIN Hotel ON Room.hotel_id = Hotel.hotel_id
        WHERE NOT EXISTS (
            SELECT 1 FROM Booking
            WHERE Booking.hotel_id = Room.hotel_id
              AND Booking.room_number = Room.room_number
              AND Booking.start_date <= %s
              AND Booking.end_date >= %s
        )
        ORDER BY Hotel.name, Room.room_number;
        """
        cur.execute(query, (end_date, start_date))
        rooms = cur.fetchall()
        if rooms:
            print(f"Available rooms from {start_date} to {end_date}:")
            print("-------------------------------------------------------")
            for room in rooms:
                print(f"Hotel: {room['hotel_name']} (ID: {room['hotel_id']}), Room: {room['room_number']}")
            print()
        else:
            print("No available rooms for that date range.")
            print()

def bookRoom(conn, email):
    print("====================================================")
    print("              * Book a Specific Room *              ")
    print("====================================================")
    hotel_id = _get_positive_int("Hotel ID: ")
    room_number = _get_positive_int("Room number: ")
    start_date = _get_date("Start date (YYYY-MM-DD): ")
    end_date = _get_date("End date (YYYY-MM-DD): ")
    print()

    if start_date > end_date:
        print("Start date must be before or equal to end date.")
        print()
        return
    price_per_day = _get_positive_decimal("Price per day: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT 1 FROM Room WHERE hotel_id = %s AND room_number = %s", (hotel_id, room_number))
        if not cur.fetchone():
            print("No room found with that hotel ID and room number.")
            print()
            return

        cur.execute("""
            SELECT 1 FROM Booking
            WHERE hotel_id = %s AND room_number = %s
              AND start_date <= %s AND end_date >= %s
        """, (hotel_id, room_number, end_date, start_date))
        if cur.fetchone():
            print("That room is not available for the selected dates.")
            print()
            return

        cur.execute("SELECT COALESCE(MAX(booking_id), 0) + 1 FROM Booking")
        booking_id = cur.fetchone()[0]

        try:
            cur.execute("""
                INSERT INTO Booking (booking_id, client_email, hotel_id, room_number, start_date, end_date, price_per_day)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (booking_id, email, hotel_id, room_number, start_date, end_date, price_per_day))
            conn.commit()
            print(f"Room {room_number} at hotel {hotel_id} booked successfully (Booking ID: {booking_id})!")
            print()
        except Exception as e:
            conn.rollback()
            print(f"Booking failed: {e}")
            print()

def autoBookRoom(conn, email):
    print("====================================================")
    print("           * Auto-Book a Room at a Hotel *          ")
    print("====================================================")
    hotel_id = _get_positive_int("Hotel ID: ")
    start_date = _get_date("Start date (YYYY-MM-DD): ")
    end_date = _get_date("End date (YYYY-MM-DD): ")
    print()

    if start_date > end_date:
        print("Start date must be before or equal to end date.")
        print()
        return
    price_per_day = _get_positive_decimal("Price per day: ")
    print()

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT 1 FROM Hotel WHERE hotel_id = %s", (hotel_id,))
        if not cur.fetchone():
            print("No hotel found with that ID.")
            print()
            return

        cur.execute("""
            SELECT Room.room_number FROM Room
            WHERE Room.hotel_id = %s
              AND NOT EXISTS (
                SELECT 1 FROM Booking
                WHERE Booking.hotel_id = Room.hotel_id
                  AND Booking.room_number = Room.room_number
                  AND Booking.start_date <= %s
                  AND Booking.end_date >= %s
              )
            LIMIT 1
        """, (hotel_id, end_date, start_date))

        available = cur.fetchone()

        if available:
            room_number = available['room_number']
            cur.execute("SELECT COALESCE(MAX(booking_id), 0) + 1 FROM Booking")
            booking_id = cur.fetchone()[0]
            try:
                cur.execute("""
                    INSERT INTO Booking (booking_id, client_email, hotel_id, room_number, start_date, end_date, price_per_day)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (booking_id, email, hotel_id, room_number, start_date, end_date, price_per_day))
                conn.commit()
                print(f"Booked room {room_number} at hotel {hotel_id} from {start_date} to {end_date} (Booking ID: {booking_id})!")
                print()
            except Exception as e:
                conn.rollback()
                print(f"Booking failed: {e}")
                print()
        else:
            print(f"No available rooms at hotel {hotel_id} for that date range.")
            print()
            cur.execute("""
                SELECT DISTINCT Hotel.hotel_id, Hotel.name FROM Hotel
                JOIN Room ON Hotel.hotel_id = Room.hotel_id
                WHERE Hotel.hotel_id != %s
                  AND NOT EXISTS (
                    SELECT 1 FROM Booking
                    WHERE Booking.hotel_id = Room.hotel_id
                      AND Booking.room_number = Room.room_number
                      AND Booking.start_date <= %s
                      AND Booking.end_date >= %s
                  )
                ORDER BY Hotel.name;
            """, (hotel_id, end_date, start_date))
            alternatives = cur.fetchall()
            if alternatives:
                print("Alternative hotels with availability:")
                print("-------------------------------------")
                for h in alternatives:
                    print(f"  Hotel ID: {h['hotel_id']}, Name: {h['name']}")
                print()
            else:
                print("No alternative hotels are available for that date range.")
                print()

def updateClientInfo(conn, email):
    while True:
        print("====================================================")
        print("           * Update Client Information *            ")
        print("====================================================")
        print("1. Update Name")
        print("2. Add Address")
        print("3. Remove Address")
        print("4. Add Credit Card")
        print("5. Remove Credit Card")
        print("6. Update Credit Card Billing Address")
        print("7. Back")
        print()
        choice = input("Enter your choice: ")
        print()

        if choice == '1':
            updateClientName(conn, email)
        elif choice == '2':
            addClientAddress(conn, email)
        elif choice == '3':
            removeClientAddress(conn, email)
        elif choice == '4':
            addClientCreditCard(conn, email)
        elif choice == '5':
            removeClientCreditCard(conn, email)
        elif choice == '6':
            updateCreditCardBillingAddress(conn, email)
        elif choice == '7':
            return
        else:
            print("Invalid choice. Please try again.")

def updateClientName(conn, email):
    print("====================================================")
    print("                   * Update Name *                  ")
    print("====================================================")
    new_name = input("Enter new name: ")
    print()

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE Client SET name = %s WHERE email = %s", (new_name, email)
        )
        conn.commit()
        print("Name updated successfully!")
        print()

def addClientAddress(conn, email):
    print("====================================================")
    print("                   * Add Address *                  ")
    print("====================================================")
    street_name = input("Street name: ")
    number = input("Street number: ")
    city = input("City: ")
    print()

    with conn.cursor() as cur:
        try:
            cur.execute(""" 
                INSERT INTO Address (street_name, number, city)
                VALUES (%s, %s, %s)
                ON CONFLICT (street_name, number, city) DO NOTHING
            """, (street_name, number, city))

            cur.execute(""" 
                INSERT INTO ClientAddress (client_email, street_name, number, city)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (email, street_name, number, city))

            conn.commit()
            print("Address added successfully!")
            print()

        except Exception as e:
            conn.rollback()
            print(f"Could not add address: {e}")
            print()

def removeClientAddress(conn, email):
    print("====================================================")
    print("                 * Remove Address *                 ")
    print("====================================================")
    street_name = input("Street name: ")
    number = input("Street number: ")
    city = input("City: ")
    print()

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM ClientAddress WHERE client_email = %s", (email,))

        if cur.fetchone()[0] <= 1:
            print("You must have at least one address on file.")
            print()
            return
        
        cur.execute("""
            DELETE FROM ClientAddress
            WHERE client_email = %s
                    AND street_name = %s
                    AND number = %s
                    AND city = %s
        """, (email, street_name, number, city))

        conn.commit()

        if cur.rowcount > 0:
            print("Address removed successfully!")
            print()
        else:
            print("No matching address found for this client.")
            print()

def addClientCreditCard(conn, email):
    print("====================================================")
    print("                * Add Credit Card *                 ")
    print("====================================================")
    card_number = input("Card number: ")

    billing_street = input("Billing street name: ")
    billing_number = input("Billing street number: ")
    billing_city = input("Billing city: ")
    print()

    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO Address (street_name, number, city)
                VALUES (%s, %s, %s)
                ON CONFLICT (street_name, number, city) DO NOTHING
            """, (billing_street, billing_number, billing_city))

            cur.execute("""
                INSERT INTO CreditCard (
                        card_number,
                        client_email,
                        billing_street_name,
                        billing_number,
                        billing_city
                )
                VALUES (%s, %s, %s, %s, %s)
            """, (card_number, email, billing_street, billing_number, billing_city))

            conn.commit()
            print("Credit card added successfully!")
            print()

        except Exception as e:
            conn.rollback()
            print(f"Could not add credit card: {e}")
            print()

def removeClientCreditCard(conn, email):
    print("====================================================")
    print("               * Remove Credit Card *               ")
    print("====================================================")
    card_number = input("Card number to remove: ")
    print()

    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM CreditCard WHERE client_email = %s", (email,))

        if cur.fetchone()[0] <= 1:
            print("You must have at least one credit card on file.")
            print()
            return
        
        cur.execute("""
            DELETE FROM CreditCard
            WHERE card_number = %s
                AND client_email = %s
        """, (card_number, email))

        conn.commit()

        if cur.rowcount > 0:
            print("Credit card removed successfully!")
            print()
        else:
            print("No matching credit card found for this client.")
            print()

def updateCreditCardBillingAddress(conn, email):
    print("====================================================")
    print("       * Update Credit Card Billing Address *       ")
    print("====================================================")
    card_number = input("Card number to update: ")
    print()
    print("Please enter the new billing address details below: ")
    billing_street = input("Billing street name: ")
    billing_number = input("Billing street number: ")
    billing_city = input("Billing city: ")
    print()

    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO Address (street_name, number, city)
                VALUES (%s, %s, %s)
                ON CONFLICT (street_name, number, city) DO NOTHING
            """, (billing_street, billing_number, billing_city))

            cur.execute("""
                UPDATE CreditCard
                SET billing_street_name = %s,
                    billing_number = %s,
                    billing_city = %s
                WHERE card_number = %s
                        AND client_email = %s
            """, (billing_street, billing_number, billing_city, card_number, email))

            conn.commit()

            if cur.rowcount > 0:
                print("Billing address updated successfully!")
                print()
            else:
                print("No matching credit card found for this client.")
                print()

        except Exception as e:
            conn.rollback()
            print(f"Could not update billing address: {e}")
            print()

def viewBookings(conn,email):
    try:
        print("====================================================")
        print("                * View My Bookings *                ")
        print("====================================================")
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                        SELECT Hotel.name AS hotel_name, Room.room_number, Booking.start_date, Booking.end_date,
                            (Booking.price_per_day * (Booking.end_date - Booking.start_date)) AS total_cost
                        FROM Booking 
                        JOIN Room
                            ON Booking.hotel_id = Room.hotel_id 
                            AND Booking.room_number = Room.room_number
                        JOIN Hotel 
                            ON Room.hotel_id = Hotel.hotel_id
                        WHERE Booking.client_email = %s

                        """, (email,))
            
            Bookings = cur.fetchall()

            if not Bookings:
                print("No bookings found.")
                print()
                return
            
            for Booking in Bookings:
                print(f"Hotel: {Booking['hotel_name']}, Room: {Booking['room_number']} ")
                print(f"From: {Booking['start_date']} To: {Booking['end_date']}")
                print(f"Total Cost: {Booking['total_cost']}")
                print()
    except Exception as e:
        print(f"Error retrieving bookings: {e}")
        print()

def submitReview(conn,email):
    try:
        print("====================================================")
        print("                  * Submit review *                 ")
        print("====================================================")
        hotel_id = input("Enter hotel ID: ")
        message = input("Enter your review: ")
        rating = input("Enter rating from 0 to 10: ")
        print()

        with conn.cursor() as cur:
            cur.execute("""
                        SELECT 1
                        FROM Booking
                        WHERE client_email = %s AND hotel_id = %s
                        LIMIT 1;
                        """, (email,hotel_id))
            
            if cur.fetchone() is None:
                print("Error: You cannot review a hotel you haven't stayed at.")
                print()
                return
            cur.execute("SELECT COALESCE(MAX(review_id), 0) + 1 FROM Review WHERE hotel_id = %s", (hotel_id,))
            review_id = cur.fetchone()[0]
            
            cur.execute("""
                        INSERT INTO REVIEW (hotel_id, review_id, client_email, message, rating)
                        VALUES (%s,%s,%s,%s,%s)
                        """, (hotel_id,review_id,email,message,rating))
            conn.commit()
            print("Review was submitted successfully!")
            print()

    except Exception as e:
        conn.rollback()
        print(f"Error submitting review: {e}")
        print()

def main():
    # conn = psycopg2.connect(
    #     host="localhost",
    #     database="hotel_management",
    #     user="anupamsai",
    #     port="5432"
    # )
    
    conn = psycopg2.connect(
        host="localhost",
        database="CS480Project",
        user="postgres",
        password="Ashu5223",
        port="5432"
    )

    try:
        while True:
            print("====================================================")
            print("     * Jarvis Your Hotel Management Assistant *     ")
            print("====================================================")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            print()
            choice = input("Enter your choice: ")
            print()
            if choice == '1':
                login(conn)
            elif choice == '2':
                register(conn)
            elif choice == '3':
                print("Exiting...")
                print()
                sys.exit()
            else:
                print("Invalid choice. Please try again.")
                print()
    except Exception as e:
        print(f"An error occurred: {e}")
        print()
    return

if __name__ == "__main__":
    main()
