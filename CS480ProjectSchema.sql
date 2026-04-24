CREATE TABLE Manager (
    ssn INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100)
);

CREATE TABLE Client (
    email VARCHAR(100) PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE Address (
    street_name VARCHAR(100),
    number VARCHAR(10),
    city VARCHAR(50),
    PRIMARY KEY (street_name, number, city)
);

CREATE TABLE ClientAddress (
    client_email VARCHAR(100),
    street_name VARCHAR(100),
    number VARCHAR(10),
    city VARCHAR(50),
    PRIMARY KEY (client_email, street_name, number, city),
    FOREIGN KEY (client_email) REFERENCES Client(email),
    FOREIGN KEY (street_name, number, city) REFERENCES Address(street_name, number, city)
);

CREATE TABLE Hotel (
    hotel_id INT PRIMARY KEY,
    name VARCHAR(50),
    street_name VARCHAR(100),
    number VARCHAR(10),
    city VARCHAR(50),
    FOREIGN KEY (street_name, number, city) REFERENCES Address(street_name, number, city),
    UNIQUE (street_name, number, city) 
);

CREATE TABLE Room (
    hotel_id INT,
    room_number INT,
    windows INT,
    renovation_year INT,
    access_type VARCHAR(10),
    PRIMARY KEY (hotel_id, room_number),
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id),
    CHECK (access_type IN ('elevator', 'stairs'))
);

CREATE TABLE CreditCard (
    card_number VARCHAR(20) PRIMARY KEY,
    client_email VARCHAR(100) NOT NULL,
    billing_street_name VARCHAR(100) NOT NULL,
    billing_number VARCHAR(10) NOT NULL,
    billing_city VARCHAR(50) NOT NULL,
    FOREIGN KEY (client_email) REFERENCES Client(email),
    FOREIGN KEY (billing_street_name, billing_number, billing_city) REFERENCES Address(street_name, number, city)
);

CREATE TABLE Booking (
    booking_id INT PRIMARY KEY,
    client_email VARCHAR(100) NOT NULL,
    hotel_id INT NOT NULL,
    room_number INT NOT NULL,
    start_date DATE,
    end_date DATE,
    price_per_day NUMERIC(10,2),
    FOREIGN KEY (client_email) REFERENCES Client(email),
    FOREIGN KEY (hotel_id, room_number) REFERENCES Room(hotel_id, room_number),
    CHECK (start_date <= end_date)
);

CREATE TABLE Review (
    hotel_id INT NOT NULL,
    review_id INT,
    client_email VARCHAR(100) NOT NULL,
    message TEXT,
    rating INT,
    PRIMARY KEY (hotel_id, review_id),
    FOREIGN KEY (hotel_id) REFERENCES Hotel(hotel_id),
    FOREIGN KEY (client_email) REFERENCES Client(email),
    CHECK (rating BETWEEN 0 AND 10)
);