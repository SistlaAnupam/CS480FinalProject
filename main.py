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
    email = input("Please enter your email to login: ")

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Client WHERE email = %s", (email,))
        client = cur.fetchone()

        if client:
            print(f"Login Successful. Welcome, {client['name']}!")
            clientOperations(conn, email)
        else:
            print("No client found with this email. Please try again.")

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
    print("Please enter the requested client details")
    name = input("Name: ")
    email = input("Email: ")

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("SELECT * FROM Client WHERE email = %s", (email,))
        existing_client = cur.fetchone()

        if existing_client:
            print("Client with this email already exists.")
            return
        
        try:
            cur.execute(
                "INSERT INTO Client (email, name) VALUES (%s, %s)", (email, name)
            )

            num_addresses = int(input("How many addresses would you like to add? "))

            if num_addresses < 1:
                print("A client must have at least one address.")
                conn.rollback()
                return
            
            for i in range(num_addresses):
                print(f"Address {i + 1}:")
                street_name = input("Street name: ")
                number = input("Street number: ")
                city = input("City: ")

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

            num_cards = int(input("How many credit crads would you like to add? "))

            if num_cards < 1:
                print("A client must have at least one credit card.")
                conn.rollback()
                return
            
            for i in range(num_cards):
                print(f"Credit Card {i + 1}:")
                card_number = input("Card number: ")

                print("Billing address for this card:")
                billing_street = input("Billing street name: ")
                billing_number = input("Billing street number: ")
                billing_city = input("Billing city: ")

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
            print("Client registered successfully.")
            clientOperations(conn, email)

        except Exception as e:
            conn.rollback()
            print(f"Registeration failed: {e}")

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

"""
2. A client should be able to update their information (except their email), including
name, addresses, and credit cards.
"""

def clientOperations(conn, email):
    while True:
        print("======Client Operations======")
        print("1. Update My Information")
        print("2. Logout")



        print("6. View My Bookings")
        print("7. Submit Review")


        choice = input("Enter your choice: ")

        if choice == '1':
            updateClientInfo(conn, email)
        elif choice == '2':
            print("Logging out...")
            return
        

        elif choice == '6':
            viewBookings(conn,email)
        elif choice == '7':
            submitReview(conn,email)

        else:
            print("Invalid choice. Please try again.")

def updateClientInfo(conn, email):
    while True:
        print("======Update Client Information======")
        print("1. Update Name")
        print("2. Add Address")
        print("3. Remove Address")
        print("4. Add Credit Card")
        print("5. Remove Credit Card")
        print("6. Update Credit Card Billing Address")
        print("7. Back")

        choice = input("Enter your choice: ")

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
    new_name = input("Enter new name: ")

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE Client SET name = %s WHERE email = %s", (new_name, email)
        )
        conn.commit()
        print("Name updated successfully.")

def addClientAddress(conn, email):
    street_name = input("Street name: ")
    number = input("Street number: ")
    city = input("City: ")

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
            print("Address added successfully.")

        except Exception as e:
            conn.rollback()
            print(f"Could not add address: {e}")

def removeClientAddress(conn, email):
    street_name = input("Street name to remove: ")
    number = input("Street number to remove: ")
    city = input("City to remove: ")

    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM ClientAddress
            WHERE client_email = %s
                    AND street_name = %s
                    AND number = %s
                    AND city = %s
        """, (email, street_name, number, city))

        conn.commit()

        if cur.rowcount > 0:
            print("Address removed successfully.")
        else:
            print("No matching address found for this client.")

def addClientCreditCard(conn, email):
    card_number = input("Card number: ")

    print("Billing address for this card: ")
    billing_street = input("Billing street name: ")
    billing_number = input("Billing street number: ")
    billing_city = input("Billing city: ")

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
            print("Credit card added successfully.")

        except Exception as e:
            conn.rollback()
            print(f"Could not add credit card: {e}")

def removeClientCreditCard(conn, email):
    card_number = input("Card number to remove: ")

    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM Creditcard
            WHERE card_number = %s
                AND client_email = %s
        """, (card_number, email))

        conn.commit()

        if cur.rowcount > 0:
            print("Credit card removed successfully.")
        else:
            print("No matching credit card found for this client.")

def updateCreditCardBillingAddress(conn, email):
    card_number = input("Card number to update: ")

    print("New billing address: ")
    billing_street = input("Billing street name: ")
    billing_number = input("Billing street number: ")
    billing_city = input("Billing city: ")

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
                    billing_city = % s
                WHERE card_number = %s
                        AND client_email = %s
            """, (billing_street, billing_number, billing_city, card_number, email))

            conn.commit()

            if cur.rowcount > 0:
                print("Billing address updated successfully.")
            else:
                print("No matching credit card found for this client.")

        except Exception as e:
            conn.rollback()
            print(f"Could not update billing address: {e}")

def viewBookings(conn,email):
    try:
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
                return
            
            for Booking in Bookings:
                print(f"Hotel: {Booking['hotel_name']}, Room: {Booking['room_number']}, ")
                print(f"From: {Booking['start_date']} To: {Booking['end_date']},")
                print(f"Total Cost: {Booking['total_cost']}")
    except Exception as e:
        print(f"Error retrieving bookings: {e}")

def submitReview(conn,email):
    try:
        hotel_id = input("Enter hotel ID: ")
        message = input("Enter your review: ")
        rating = input("Enter rating from 0 to 10: ")

        with conn.cursor() as cur:
            cur.execute("""
                        SELECT 1
                        FROM Booking
                        WHERE client_email = %s AND hotel_id = %s
                        LIMIT 1;
                        """, (email,hotel_id))
            
            if cur.fetchone() is None:
                print("Error: You cannot review a hotel you haven't stayed at.")
                return
            cur.execute("SELECT COALESCE(MAX(review_id), 0) + 1 FROM Review")
            review_id = cur.fetchone()[0]
            
            cur.execute("""
                        INSERT INTO REVIEW (hotel_id, review_id, client_email, message, rating)
                        VALUES (%s,%s,%s,%s,%s)
                        """, (hotel_id,review_id,email,message,rating))
            conn.commit()
            print("Review was submitted successfully.")

    except Exception as e:
        conn.rollback()
        print(f"Error submitting review: {e}")



   

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
