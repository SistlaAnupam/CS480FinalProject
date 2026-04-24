import psycopg2
import psycopg2.extras 

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
    print("Made it here with ssn: ", ssn)
    return

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
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return

if __name__ == "__main__":
    main()