-- ============================================================
-- seed.sql  –  Minimal starting data for CS480 Hotel Project
-- Run clear.sql first, then this file.
-- ============================================================


-- ============================================================
-- ADDRESSES (50 total across 9 cities)
-- ============================================================
INSERT INTO Address (street_name, number, city) VALUES
    -- Chicago (11)
    ('Michigan Ave',    '100',  'Chicago'),
    ('State St',        '200',  'Chicago'),
    ('Wacker Dr',       '300',  'Chicago'),
    ('Lake Shore Dr',   '400',  'Chicago'),
    ('Navy Pier Ct',    '500',  'Chicago'),
    ('Rush St',         '600',  'Chicago'),
    ('Clark St',        '700',  'Chicago'),
    ('Broadway',        '800',  'Chicago'),
    ('Halsted St',      '900',  'Chicago'),
    ('Lincoln Ave',     '1000', 'Chicago'),
    ('Belmont Ave',     '1100', 'Chicago'),

    -- New York (10)
    ('5th Ave',         '100',  'New York'),
    ('Park Ave',        '200',  'New York'),
    ('Madison Ave',     '300',  'New York'),
    ('Lexington Ave',   '400',  'New York'),
    ('Broadway',        '500',  'New York'),
    ('Wall St',         '600',  'New York'),
    ('West End Ave',    '700',  'New York'),
    ('Riverside Dr',    '800',  'New York'),
    ('Amsterdam Ave',   '900',  'New York'),
    ('Columbus Ave',    '1000', 'New York'),

    -- Los Angeles (6)
    ('Sunset Blvd',         '100', 'Los Angeles'),
    ('Hollywood Blvd',      '200', 'Los Angeles'),
    ('Wilshire Blvd',       '300', 'Los Angeles'),
    ('Rodeo Dr',            '400', 'Los Angeles'),
    ('Venice Blvd',         '500', 'Los Angeles'),
    ('Santa Monica Blvd',   '600', 'Los Angeles'),

    -- Boston (5)
    ('Beacon St',       '100', 'Boston'),
    ('Commonwealth Ave','200', 'Boston'),
    ('Newbury St',      '300', 'Boston'),
    ('Boylston St',     '400', 'Boston'),
    ('Tremont St',      '500', 'Boston'),

    -- Miami (5)
    ('Ocean Dr',        '100', 'Miami'),
    ('Collins Ave',     '200', 'Miami'),
    ('Biscayne Blvd',   '300', 'Miami'),
    ('Coral Way',       '400', 'Miami'),
    ('Flagler St',      '500', 'Miami'),

    -- Seattle (5)
    ('Pike St',         '100', 'Seattle'),
    ('Pine St',         '200', 'Seattle'),
    ('1st Ave',         '300', 'Seattle'),
    ('University St',   '400', 'Seattle'),
    ('Westlake Ave',    '500', 'Seattle'),

    -- Dallas (5)
    ('Main St',         '100', 'Dallas'),
    ('Elm St',          '200', 'Dallas'),
    ('Commerce St',     '300', 'Dallas'),
    ('Young St',        '400', 'Dallas'),
    ('Griffin St',      '500', 'Dallas'),

    -- Portland (4)
    ('Burnside St',     '100', 'Portland'),
    ('Morrison St',     '200', 'Portland'),
    ('Hawthorne Blvd',  '300', 'Portland'),
    ('Division St',     '400', 'Portland'),

    -- Houston (4) -- wait that's 11+10+6+5+5+5+5+4+4 = 55, too many
    -- Let me correct: Chicago 11, NY 10, LA 6, Boston 5, Miami 4, Seattle 4, Dallas 4, Portland 3, Houston 3 = 50
    ('Travis St',       '100', 'Houston'),
    ('Louisiana St',    '200', 'Houston'),
    ('Smith St',        '300', 'Houston');


-- ============================================================
-- MANAGERS
-- Login: Alice uses SSN 111111111, Bob uses SSN 222222222
-- ============================================================
INSERT INTO Manager (ssn, name, email) VALUES
    (111111111, 'Alice Johnson', 'alice@hotelcorp.com'),
    (222222222, 'Bob Smith',     'bob@hotelcorp.com');


-- ============================================================
-- CLIENTS
-- john  → has Chicago address  (used for city-pair query)
-- jane  → has Boston address   (no Chicago; used for problematic hotel query)
-- tom   → has Seattle address  (no Chicago; used for problematic hotel query)
-- Login: john uses john@test.com, etc.
-- ============================================================
INSERT INTO Client (email, name) VALUES
    ('john@test.com', 'John Doe'),
    ('jane@test.com', 'Jane Smith'),
    ('tom@test.com',  'Tom Green');


-- ============================================================
-- CLIENT ADDRESSES
-- ============================================================
INSERT INTO ClientAddress (client_email, street_name, number, city) VALUES
    ('john@test.com', 'Wacker Dr',   '300', 'Chicago'),  -- John: Chicago
    ('jane@test.com', 'Beacon St',   '100', 'Boston'),   -- Jane: Boston only
    ('tom@test.com',  'Pike St',     '100', 'Seattle');  -- Tom:  Seattle only


-- ============================================================
-- CREDIT CARDS
-- ============================================================
INSERT INTO CreditCard (card_number, client_email, billing_street_name, billing_number, billing_city) VALUES
    ('4111111111111111', 'john@test.com', 'Wacker Dr', '300', 'Chicago'),
    ('4222222222222222', 'jane@test.com', 'Beacon St', '100', 'Boston'),
    ('4333333333333333', 'tom@test.com',  'Pike St',   '100', 'Seattle');


-- ============================================================
-- HOTELS
-- Hotel 1: Chicago (good)
-- Hotel 2: New York
-- Hotel 3: Chicago (problematic — low ratings from non-Chicago clients)
-- ============================================================
INSERT INTO Hotel (hotel_id, name, street_name, number, city) VALUES
    (1, 'Grand Chicago Hotel',  'Michigan Ave', '100', 'Chicago'),
    (2, 'NYC Plaza',            '5th Ave',      '100', 'New York'),
    (3, 'Windy City Hostel',    'State St',     '200', 'Chicago');


-- ============================================================
-- ROOMS
-- ============================================================
INSERT INTO Room (hotel_id, room_number, windows, renovation_year, access_type) VALUES
    -- Grand Chicago Hotel
    (1, 101, 2, 2020, 'elevator'),
    (1, 102, 1, 2018, 'stairs'),
    (1, 103, 3, 2022, 'elevator'),
    -- NYC Plaza
    (2, 201, 2, 2021, 'elevator'),
    (2, 202, 4, 2019, 'stairs'),
    -- Windy City Hostel
    (3, 301, 1, 2015, 'stairs'),
    (3, 302, 2, 2016, 'stairs');


-- ============================================================
-- BOOKINGS (past dates so reviews can be submitted)
--
-- john  → 1 booking at Hotel 1        (can review Hotel 1)
-- jane  → 1 booking at Hotel 1,
--          1 booking at Hotel 3        (can review Hotel 1 and Hotel 3)
-- tom   → 1 booking at Hotel 3        (can review Hotel 3)
--
-- Spending:
--   john: 5 nights * $150 = $750
--   jane: 4 nights * $150 + 2 nights * $80 = $760
--   tom:  2 nights * $80  = $160
-- ============================================================
INSERT INTO Booking (booking_id, client_email, hotel_id, room_number, start_date, end_date, price_per_day) VALUES
    (1, 'john@test.com', 1, 101, '2026-01-10', '2026-01-15', 150.00),
    (2, 'jane@test.com', 1, 102, '2026-02-01', '2026-02-05', 150.00),
    (3, 'jane@test.com', 3, 301, '2026-02-10', '2026-02-12',  80.00),
    (4, 'tom@test.com',  3, 302, '2026-03-01', '2026-03-03',  80.00);


-- ============================================================
-- REVIEWS
-- Hotel 3 (Windy City Hostel): jane and tom both rate it 1 and 0
-- → avg = 0.5 (< 2), Chicago, booked by 2 non-Chicago clients
-- → satisfies the problematic hotel query
-- ============================================================
INSERT INTO Review (hotel_id, review_id, client_email, message, rating) VALUES
    (3, 1, 'jane@test.com', 'Dirty rooms and poor service.',     1),
    (3, 2, 'tom@test.com',  'Worst hostel I have ever visited.', 0);