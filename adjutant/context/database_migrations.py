""" Definitions for the database tables """

LATEST_DATABASE_VERSION = 1

VERSION_1 = """
CREATE TABLE settings (
    id TEXT PRIMARY KEY,
    version INTEGER
);

CREATE TABLE bases ( 
    id TEXT PRIMARY KEY,
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
    storages_id TEXT DEFAULT "",
    status_id TEXT DEFAULT "",
    schemes_id TEXT DEFAULT "",

    CONSTRAINT fk_storages_id FOREIGN KEY(storages_id) REFERENCES storages(id),
    CONSTRAINT fk_status_id FOREIGN KEY(status_id) REFERENCES statuses(id),
    CONSTRAINT fk_scheme_id FOREIGN KEY(schemes_id) REFERENCES colour_schemes(id)
);

CREATE TABLE tags (
    id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE bases_tags (
    id TEXT PRIMARY KEY,
    bases_id TEXT,
    tags_id TEXT,

    CONSTRAINT fk_bases_id FOREIGN KEY(bases_id) REFERENCES bases(id) ON DELETE CASCADE,
    CONSTRAINT fk_tags_id FOREIGN KEY(tags_id) REFERENCES tags(id) ON DELETE CASCADE
);

CREATE TABLE searches (
    id TEXT PRIMARY KEY,
    name TEXT,
    encoded TEXT
);

CREATE TABLE storages (
    id TEXT PRIMARY KEY,
    name TEXT DEFAULT "",
    location TEXT DEFAULT "",
    height INTEGER DEFAULT 0,
    magnetized BOOLEAN DEFAULT 0,
    full BOOLEAN DEFAULT 0,
    notes TEXT DEFAULT ""
);

CREATE TABLE statuses (
    id TEXT PRIMARY KEY,
    name TEXT DEFAULT ""
);

CREATE TABLE paints (
    id TEXT PRIMARY KEY,
    name TEXT DEFAULT "",
    manufacturer TEXT DEFAULT "",
    range TEXT DEFAULT "",
    hexvalue TEXT DEFAULT "",
    notes TEXT DEFAULT ""    
);

CREATE TABLE recipes (
    id TEXT PRIMARY KEY,
    name TEXT DEFAULT "",
    notes TEXT DEFAULT ""
);

CREATE TABLE recipe_steps (
    id TEXT PRIMARY KEY,
    recipes_id TEXT DEFAULT "",
    paints_id TEXT DEFAULT "",
    operations_id TEXT DEFAULT "",
    priority INTEGER DEFAULT 0
);

CREATE TABLE step_operations (
    id TEXT PRIMARY KEY,
    name TEXT DEFAULT ""
);

CREATE TABLE colour_schemes (
    id TEXT PRIMARY KEY,
    name TEXT DEFAULT "",
    notes TEXT DEFAULT ""
);

CREATE TABLE scheme_components (
    id TEXT PRIMARY KEY,
    schemes_id TEXT DEFAULT "",
    name TEXT DEFAULT "",
    recipes_id TEXT DEFAULT ""
);
"""
