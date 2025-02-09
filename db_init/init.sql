CREATE TABLE buyers (
    id SERIAL PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    postcode VARCHAR(20)
);

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    postcode VARCHAR(20) NOT NULL
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    event_id INT UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    number VARCHAR(50) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    event_id INT REFERENCES events(event_id) ON DELETE CASCADE,
    cancellation_reason TEXT,
    generated_at TIMESTAMPTZ NOT NULL,
    promoter VARCHAR(255) NOT NULL,
    price_amount DECIMAL(10,2) NOT NULL,
    price_currency VARCHAR(10) NOT NULL,
    buyer_id INT REFERENCES buyers(id) ON DELETE SET NULL
);

CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    ticket_id INT REFERENCES tickets(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    doors TIME NOT NULL,
    location_id INT REFERENCES locations(id) ON DELETE CASCADE
);