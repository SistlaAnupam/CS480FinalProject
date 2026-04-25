import psycopg2
import psycopg2.extras 
import sys

"""
Notes:
1. Do we care about the case of a foreign key error, for example an a manager enters an invalid hotel address, do we want to handle this without an exception?
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

def managerOperations(conn, ssn):
    while True:
        print("======Manager Operations======")
        print("1. Insert/Remove/Update Hotels or Rooms")
        print("2. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            managerUpdateHotelRoom(conn, ssn)
        
        elif choice == '2':
            print("Logging out...")
            main()

def managerUpdateHotelRoom(conn, ssn):
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
            cur.execute("DELETE FROM Hotel WHERE hotel_id = %s", (id,))
            conn.commit()
            print(f"Hotel with ID {id} removed successfully.")
        else:
            print("No hotel found with this ID.")

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