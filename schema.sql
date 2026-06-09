-- Table to store mission statement and project info
CREATE TABLE IF NOT EXISTS site_content (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_name TEXT NOT NULL,
    content_body TEXT NOT NULL
);

-- Table structure for incident analysis (Sub-Task B)
CREATE TABLE IF NOT EXISTS crash_data (
    accident_no TEXT PRIMARY KEY,
    severity TEXT,
    total_persons INTEGER,
    serious_injury INTEGER,
    other_injury INTEGER,
    bicyclist INTEGER,
    pedestrian INTEGER,
    driver INTEGER
);

-- personas
CREATE TABLE personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    filter_query TEXT NOT NULL
);