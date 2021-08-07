DROP TABLE IF EXISTS bases;
CREATE TABLE IF NOT EXISTS bases ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT DEFAULT "",
    scale TEXT DEFAULT "",
    base TEXT DEFAULT "Round",
    width INTEGER DEFAULT 20,
    depth INTEGER DEFAULT 0,
    figures INTEGER DEFAULT 1,
    material TEXT DEFAULT "Plastic",
    sculptor TEXT DEFAULT "",
    manufacturer TEXT DEFAULT "",
    retailer TEXT DEFAULT "",
    price FLOAT DEFAULT 0.0,
    date_added DATE DEFAULT CURRENT_DATE,
    date_acquired DATE DEFAULT 0,
    completed BOOLEAN DEFAULT 0,
    damaged BOOLEAN DEFAULT 0,
    notes TEXT DEFAULT "",
    custom_id TEXT DEFAULT "",
    storage INTEGER DEFAULT NULL
);

DROP TABLE IF EXISTS tags;
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY,
    name TEXT
);

DROP TABLE IF EXISTS bases_tags;
CREATE TABLE IF NOT EXISTS bases_tags (
    id INTEGER PRIMARY KEY,
    bases_id INTEGER,
    tags_id INTEGER,

    CONSTRAINT fk_bases_id FOREIGN KEY(bases_id) REFERENCES bases(id) ON DELETE CASCADE,
    CONSTRAINT fk_tags_id FOREIGN KEY(tags_id) REFERENCES tags(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS searches;
CREATE TABLE IF NOT EXISTS searches (
    id INTEGER PRIMARY KEY,
    name TEXT,
    encoded TEXT
);

DROP TABLE IF EXISTS storage;
CREATE TABLE IF NOT EXISTS storage (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT "",
    location TEXT DEFAULT "",
    height INTEGER DEFAULT 0,
    magnetized BOOLEAN DEFAULT 0,
    full BOOLEAN DEFAULT 0,
    notes TEXT DEFAULT ""
);

DROP TABLE IF EXISTS settings;
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY,
    version INTEGER
);
INSERT into settings(version) VALUES(1);