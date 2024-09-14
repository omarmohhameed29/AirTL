-- Drop the table if it exists
DROP TABLE IF EXISTS matches;

-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS matches (
    away_team VARCHAR(100),
    home_team VARCHAR(100),
    round VARCHAR(5),
    cancelled BOOLEAN,
    finished BOOLEAN,
    match_date DATE,
    country VARCHAR(100),
    name VARCHAR(100),
    selected_season VARCHAR(20),
    type VARCHAR(50),
    home_score INT,
    away_score INT
);
