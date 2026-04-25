-- ============================================================
-- seed.sql  –  Sample data for CS480 Hotel Management Project
-- Run after executing the schema script.
-- ============================================================

-- ============================================================
-- ADDRESSES
-- Must come first — Hotels, ClientAddresses, and CreditCards
-- all reference this table.
-- ============================================================
INSERT INTO Address (street_name, number, city) VALUES
    ('Main St',      '123', 'Chicago'),
    ('Lake Shore Dr','456', 'Chicago'),
    ('Maple Ave',    '789', 'Chicago'),
    ('Broadway',     '321', 'New York'),
    ('Sunset Blvd',  '654', 'Los Angeles'),
    ('Beacon St',    '987', 'Boston'),
    ('Ocean Dr',     '111', 'Miami'),
    ('Elm St',       '222', 'New York'),
    ('Cedar Ln',     '333', 'Boston');

-- ============================================================
-- MANAGERS
-- ============================================================
INSERT INTO Manager (ssn, name, email) VALUES
    (100000001, 'Alice Johnson', 'alice@hotelcorp.com'),
    (100000002, 'Bob Smith',     'bob@hotelcorp.com');

-- ============================================================
-- CLIENTS
-- Note: john and sarah have Chicago addresses.
--       jane and mike do NOT — used to test the "problematic
--       local hotel" query (manager operation 8).
-- ============================================================
INSERT INTO Client (email, name) VALUES
    ('john@example.com',  'John Doe'),
    ('jane@example.com',  'Jane Smith'),
    ('mike@example.com',  'Mike Brown'),
    ('sarah@example.com', 'Sarah Davis');

-- ============================================================
-- CLIENT ADDRESSES
-- ============================================================
INSERT INTO ClientAddress (client_email, street_name, number, city) VALUES
    ('john@example.com',  'Maple Ave',  '789', 'Chicago'),   -- John: Chicago
    ('sarah@example.com', 'Main St',    '123', 'Chicago'),   -- Sarah: Chicago
    ('jane@example.com',  'Beacon St',  '987', 'Boston'),    -- Jane: Boston only
    ('mike@example.com',  'Ocean Dr',   '111', 'Miami'),     -- Mike: Miami only
    ('john@example.com',  'Broadway',   '321', 'New York');  -- John also has NY

-- ============================================================
-- HOTELS
-- Hotel 1 is the "problematic" Chicago hotel (will get low
-- ratings from non-Chicago clients to satisfy manager query 8).
-- ============================================================
INSERT INTO Hotel (hotel_id, name, street_name, number, city) VALUES
    (1, 'Grand Central Chicago', 'Main St',       '123', 'Chicago'),
    (2, 'Lake View Inn',         'Lake Shore Dr', '456', 'Chicago'),
    (3, 'NYC Plaza',             'Broadway',      '321', 'New York'),
    (4, 'LA Suites',             'Sunset Blvd',   '654', 'Los Angeles');

-- ============================================================
-- ROOMS
-- ============================================================
INSERT INTO Room (hotel_id, room_number, windows, renovation_year, access_type) VALUES
    -- Grand Central Chicago
    (1, 101, 2, 2018, 'elevator'),
    (1, 102, 1, 2015, 'stairs'),
    (1, 103, 3, 2021, 'elevator'),
    -- Lake View Inn
    (2, 201, 2, 2020, 'elevator'),
    (2, 202, 4, 2022, 'elevator'),
    -- NYC Plaza
    (3, 301, 1, 2019, 'elevator'),
    (3, 302, 2, 2017, 'stairs'),
    -- LA Suites
    (4, 401, 3, 2023, 'elevator'),
    (4, 402, 2, 2020, 'stairs');

-- ============================================================
-- CREDIT CARDS
-- Billing addresses must already exist in Address table.
-- ============================================================
INSERT INTO CreditCard (card_number, client_email, billing_street_name, billing_number, billing_city) VALUES
    ('4111111111111111', 'john@example.com',  'Maple Ave',  '789', 'Chicago'),
    ('4222222222222222', 'jane@example.com',  'Beacon St',  '987', 'Boston'),
    ('4333333333333333', 'mike@example.com',  'Ocean Dr',   '111', 'Miami'),
    ('4444444444444444', 'sarah@example.com', 'Main St',    '123', 'Chicago'),
    ('4555555555555555', 'john@example.com',  'Broadway',   '321', 'New York');  -- John's second card

-- ============================================================
-- BOOKINGS
-- Dates must not overlap for the same room.
-- ============================================================
INSERT INTO Booking (booking_id, client_email, hotel_id, room_number, start_date, end_date, price_per_day) VALUES
    -- Hotel 1 (Grand Central Chicago)
    (1, 'jane@example.com',  1, 101, '2026-01-10', '2026-01-15', 120.00),
    (2, 'mike@example.com',  1, 101, '2026-02-01', '2026-02-05', 120.00),
    (3, 'john@example.com',  1, 102, '2026-01-20', '2026-01-22', 95.00),
    -- Hotel 2 (Lake View Inn)
    (4, 'sarah@example.com', 2, 201, '2026-03-01', '2026-03-07', 150.00),
    (5, 'john@example.com',  2, 202, '2026-03-10', '2026-03-12', 175.00),
    -- Hotel 3 (NYC Plaza)
    (6, 'jane@example.com',  3, 301, '2026-04-05', '2026-04-10', 200.00),
    (7, 'mike@example.com',  3, 302, '2026-04-01', '2026-04-03', 185.00),
    -- Hotel 4 (LA Suites)
    (8, 'sarah@example.com', 4, 401, '2026-05-01', '2026-05-04', 210.00);

-- ============================================================
-- REVIEWS
-- A client can only review a hotel they have booked.
-- Hotel 1 gets low ratings (avg < 2) from jane and mike —
-- neither has a Chicago address, satisfying manager query 8.
-- ============================================================
INSERT INTO Review (hotel_id, review_id, client_email, message, rating) VALUES
    -- Hotel 1: low ratings (problematic hotel)
    (1, 1, 'jane@example.com', 'Very disappointing stay, would not return.',  1),
    (1, 2, 'mike@example.com', 'Room was outdated and service was poor.',     1),
    (1, 3, 'john@example.com', 'Decent location but needs improvement.',      5),
    -- Hotel 2: good ratings
    (2, 1, 'sarah@example.com','Beautiful lake views, great service!',        9),
    (2, 2, 'john@example.com', 'Loved the amenities, will definitely return.',8),
    -- Hotel 3
    (3, 1, 'jane@example.com', 'Perfect location in the city.',               7),
    -- Hotel 4
    (4, 1, 'sarah@example.com','Modern rooms, excellent staff.',              10);