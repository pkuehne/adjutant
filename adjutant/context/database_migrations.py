""" Definitions for the database tables """

LATEST_DATABASE_VERSION = 1

VERSION_1 = """
CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    version INTEGER
);

CREATE TABLE bases ( 
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
    pack_code TEXT DEFAULT "",
    retailer TEXT DEFAULT "",
    price FLOAT DEFAULT 0.0,
    date_added DATE DEFAULT CURRENT_DATE,
    date_acquired DATE DEFAULT 0,
    date_completed DATE DEFAULT 0,
    damaged BOOLEAN DEFAULT 0,
    notes TEXT DEFAULT "",
    custom_id TEXT DEFAULT "",
    storage_id INTEGER DEFAULT 0,
    status_id INTEGER DEFAULT 0,
    schemes_id INTEGER DEFAULT 0,

    CONSTRAINT fk_storage_id FOREIGN KEY(storage_id) REFERENCES storage(id),
    CONSTRAINT fk_status_id FOREIGN KEY(status_id) REFERENCES statuses(id),
    CONSTRAINT fk_scheme_id FOREIGN KEY(schemes_id) REFERENCES colour_schemes(id)
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE bases_tags (
    id INTEGER PRIMARY KEY,
    bases_id INTEGER,
    tags_id INTEGER,

    CONSTRAINT fk_bases_id FOREIGN KEY(bases_id) REFERENCES bases(id) ON DELETE CASCADE,
    CONSTRAINT fk_tags_id FOREIGN KEY(tags_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE searches (
    id INTEGER PRIMARY KEY,
    name TEXT,
    encoded TEXT
);

CREATE TABLE storage (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT "",
    location TEXT DEFAULT "",
    height INTEGER DEFAULT 0,
    magnetized BOOLEAN DEFAULT 0,
    full BOOLEAN DEFAULT 0,
    notes TEXT DEFAULT ""
);

CREATE TABLE statuses (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT ""
);

CREATE TABLE paints (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT "",
    manufacturer TEXT DEFAULT "",
    range TEXT DEFAULT "",
    hexvalue TEXT DEFAULT "",
    notes TEXT DEFAULT ""    
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT "",
    notes TEXT DEFAULT ""
);

CREATE TABLE recipe_steps (
    id INTEGER PRIMARY KEY,
    recipes_id INTEGER DEFAULT 0,
    paints_id INTEGER DEFAULT 0,
    operations_id INTEGER DEFAULT 0,
    priority INTEGER DEFAULT 0
);

CREATE TABLE step_operations (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT ""
);

CREATE TABLE colour_schemes (
    id INTEGER PRIMARY KEY,
    name TEXT DEFAULT "",
    notes TEXT DEFAULT ""
);

CREATE TABLE scheme_components (
    id INTEGER PRIMARY KEY,
    schemes_id INTEGER DEFAULT 0,
    name TEXT DEFAULT "",
    recipes_id INTEGER DEFAULT 0
);
"""
