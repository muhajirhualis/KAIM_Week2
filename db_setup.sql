CREATE DATABASE bank_reviews
-- \c bank_reviews; -- Connect to the new database

-- A. Banks Table (Reference/Dimension Table)
CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) UNIQUE NOT NULL,
    app_name VARCHAR(255)
);

-- B. Reviews Table (Fact/Main Data Table)
-- We use a combination of processed data and data loaded from the CSV
CREATE TABLE reviews (
    review_id VARCHAR(50) PRIMARY KEY, -- Using VARCHAR to store the external unique ID
    bank_id INTEGER REFERENCES banks (bank_id), -- FOREIGN KEY linking to the Banks table
    review_text TEXT NOT NULL,
    rating INTEGER,
    review_date DATE, -- Assuming you have a date column (if scraped)
    sentiment_label VARCHAR(50), -- e.g., 'Positive', 'Negative'
    sentiment_score NUMERIC(5, 4), -- Polarity/Compound score (e.g., -1.0000 to 1.0000)
    theme VARCHAR(255), -- e.g., 'core-functionality', 'performance'
    source VARCHAR(50) DEFAULT 'Google Play Store' -- Optional: Source identification
);


-- 3. Insert Initial Bank Data
INSERT INTO banks (bank_name, app_name) VALUES
    ('Commercial Bank of Ethiopia', 'CBE Birr'),
    ('Bank of Abyssinia', 'BOA Mobile Banking'),
    ('Dashen Bank', 'DASHEN BANK MOBILE BANKING');

-- Verification query (Optional)
SELECT * FROM banks;


-- Verification Query 1: Count reviews per bank
SELECT 
    b.bank_name, 
    COUNT(r.review_id) AS total_reviews
FROM 
    banks b
JOIN 
    reviews r ON b.bank_id = r.bank_id
GROUP BY 
    b.bank_name
ORDER BY 
    total_reviews DESC;

-- Verification Query 2: Average rating and sentiment score per bank
SELECT 
    b.bank_name,
    CAST(AVG(r.rating) AS NUMERIC(3, 2)) AS average_rating,
    CAST(AVG(r.sentiment_score) AS NUMERIC(5, 4)) AS average_sentiment
FROM 
    banks b
JOIN 
    reviews r ON b.bank_id = r.bank_id
GROUP BY 
    b.bank_name
ORDER BY 
    average_rating DESC;


-- Verification Query 3: Count reviews per bank

SELECT 
    b.bank_name, 
    COUNT(r.review_id) AS total_reviews
FROM 
    banks b
JOIN 
    reviews r ON b.bank_id = r.bank_id
GROUP BY 
    b.bank_name
ORDER BY 
    total_reviews DESC;