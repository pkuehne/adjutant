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

SAMPLE_DATA = """
INSERT INTO bases VALUES (null, "Retributor", "32mm", "Round", 32, 0, 1, "Plastic", "", "Games Workshop", "", "Element Games", 0.0, CURRENT_DATE,  NULL, NULL, 0, "not varnished", "AOS-Ret1-1", 0, 0, 0);
INSERT INTO bases VALUES (null, "Retributor", "32mm", "Round", 32, 0, 1, "Plastic", "", "Games Workshop", "", "Element Games", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "AOS-Ret1-2", 0, 0, 0);
INSERT INTO bases VALUES (null, "Retributor", "32mm", "Round", 32, 0, 1, "Plastic", "", "Games Workshop", "", "Element Games", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "AOS-Ret1-3", 0, 0, 0);
INSERT INTO bases VALUES (null, "Retributor", "32mm", "Round", 32, 0, 1, "Plastic", "", "Games Workshop", "", "Element Games", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "AOS-Ret1-4", 0, 0, 0);
INSERT INTO bases VALUES (null, "Retributor-Primer", "32mm", "Round", 32, 0, 1, "Plastic", "", "Games Workshop", "", "Element Games", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "AOS-Ret1-P", 0, 0, 0);
INSERT INTO bases VALUES (null, "Prussian Jaeger", "28mm", "Rectangle", 40, 20, 2, "Plastic", "Alan Perry", "Perry Miniatures", "", "Perry Miniatures", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "PRU-Sil1-1", 0, 0, 0);
INSERT INTO bases VALUES (null, "Prussian Jaeger", "28mm", "Rectangle", 40, 20, 2, "Plastic", "Alan Perry", "Perry Miniatures", "", "Perry Miniatures", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "PRU-Sil1-1", 0, 0, 0);
INSERT INTO bases VALUES (null, "Prussian Infantry", "28mm", "Square", 40, 40, 4, "Plastic", "Alan Perry", "Perry Miniatures", "", "Perry Miniatures", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "PRU-Sil1-1", 0, 0, 0);
INSERT INTO bases VALUES (null, "Prussian Infantry", "28mm", "Square", 40, 40, 4, "Plastic", "Alan Perry", "Perry Miniatures", "", "Perry Miniatures", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "PRU-Sil1-1", 0, 0, 0);
INSERT INTO bases VALUES (null, "Prussian Infantry", "28mm", "Square", 40, 40, 4, "Plastic", "Alan Perry", "Perry Miniatures", "", "Perry Miniatures", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "PRU-Sil1-1", 0, 0, 0);
INSERT INTO bases VALUES (null, "Prussian Infantry", "28mm", "Square", 40, 40, 4, "Plastic", "Alan Perry", "Perry Miniatures", "", "Perry Miniatures", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "PRU-Sil1-1", 0, 0, 0);
INSERT INTO bases VALUES (null, "Prussian Infantry", "28mm", "Square", 40, 40, 4, "Plastic", "Alan Perry", "Perry Miniatures", "", "Perry Miniatures", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "PRU-Sil1-1", 0, 0, 0);
INSERT INTO bases VALUES (null, "Prussian Command", "28mm", "Square", 40, 40, 3, "Plastic", "Alan Perry", "Perry Miniatures", "", "Perry Miniatures", 0.0, CURRENT_DATE, NULL, NULL, 0, "not varnished", "PRU-Sil1-1", 0, 0, 0);

INSERT INTO tags VALUES (NULL, "sword");
INSERT INTO tags VALUES (NULL, "bow");
INSERT INTO tags VALUES (NULL, "rifle");
INSERT INTO tags VALUES (NULL, "musket");
INSERT INTO tags VALUES (NULL, "pistol");
INSERT INTO tags VALUES (NULL, "assault rifle");
INSERT INTO tags VALUES (NULL, "submachine gun");
INSERT INTO tags VALUES (NULL, "MG");
INSERT INTO tags VALUES (NULL, "bolt rifle");
INSERT INTO tags VALUES (NULL, "repeater");
INSERT INTO tags VALUES (NULL, "claws");
INSERT INTO tags VALUES (NULL, "spike");
INSERT INTO tags VALUES (NULL, "fangs");
INSERT INTO tags VALUES (NULL, "sword");
INSERT INTO tags VALUES (NULL, "spear");
INSERT INTO tags VALUES (NULL, "halberd");
INSERT INTO tags VALUES (NULL, "club");
INSERT INTO tags VALUES (NULL, "warhammer");
INSERT INTO tags VALUES (NULL, "dagger");
INSERT INTO tags VALUES (NULL, "staff");
INSERT INTO tags VALUES (NULL, "wand");
INSERT INTO tags VALUES (NULL, "light armour");
INSERT INTO tags VALUES (NULL, "leather armour");
INSERT INTO tags VALUES (NULL, "plate armour");
INSERT INTO tags VALUES (NULL, "cowl");
INSERT INTO tags VALUES (NULL, "robe");
INSERT INTO tags VALUES (NULL, "shako");
INSERT INTO tags VALUES (NULL, "helmet");
INSERT INTO tags VALUES (NULL, "bedroll");
INSERT INTO tags VALUES (NULL, "forage bag");
INSERT INTO tags VALUES (NULL, "musket pouch");
INSERT INTO tags VALUES (NULL, "lamp");
INSERT INTO tags VALUES (NULL, "torch");
INSERT INTO tags VALUES (NULL, "human");
INSERT INTO tags VALUES (NULL, "dwarf");
INSERT INTO tags VALUES (NULL, "troll");
INSERT INTO tags VALUES (NULL, "orc");
INSERT INTO tags VALUES (NULL, "snakeman");
INSERT INTO tags VALUES (NULL, "elf");
INSERT INTO tags VALUES (NULL, "prussian");
INSERT INTO tags VALUES (NULL, "french");
INSERT INTO tags VALUES (NULL, "british");
INSERT INTO tags VALUES (NULL, "austrian");
INSERT INTO tags VALUES (NULL, "russian");
INSERT INTO tags VALUES (NULL, "japanese");
INSERT INTO tags VALUES (NULL, "german");
INSERT INTO tags VALUES (NULL, "american");
INSERT INTO tags VALUES (NULL, "italian");
INSERT INTO tags VALUES (NULL, "fantasy");
INSERT INTO tags VALUES (NULL, "medieval");
INSERT INTO tags VALUES (NULL, "ww2");
INSERT INTO tags VALUES (NULL, "ww1");
INSERT INTO tags VALUES (NULL, "acw");
INSERT INTO tags VALUES (NULL, "awi");
INSERT INTO tags VALUES (NULL, "7yw");
INSERT INTO tags VALUES (NULL, "mounted");
INSERT INTO tags VALUES (NULL, "pet");
INSERT INTO tags VALUES (NULL, "dramatic");
INSERT INTO tags VALUES (NULL, "injured");

INSERT INTO storage VALUES (NULL, "Cardboard box", "1st shelf", 10, 0, 0, "Slightly damp");
INSERT INTO storage VALUES (NULL, "Warhammer", "Top shelf", 25, 1, 1, "Can fit one more 32mm base");
INSERT INTO storage VALUES (NULL, "Ancients", "Top shelf", 15, 1, 0, "");

INSERT INTO statuses VALUES (NULL, "New");
INSERT INTO statuses VALUES (NULL, "Built");
INSERT INTO statuses VALUES (NULL, "Undercoated");
INSERT INTO statuses VALUES (NULL, "Painted");
INSERT INTO statuses VALUES (NULL, "Varnished");
INSERT INTO statuses VALUES (NULL, "Complete");

INSERT INTO step_operations VALUES (NULL, "Base");
INSERT INTO step_operations VALUES (NULL, "Wash");
INSERT INTO step_operations VALUES (NULL, "Layer");
INSERT INTO step_operations VALUES (NULL, "Highlight");
INSERT INTO step_operations VALUES (NULL, "Glaze");
INSERT INTO step_operations VALUES (NULL, "Varnish");

INSERT INTO paints VALUES (NULL, "Mournfang Brown", "Citadel", "Base", "#640909", "");
INSERT INTO paints VALUES (NULL, "Gorthor Brown ", "Citadel", "Layer", "#654741", "");
INSERT INTO paints VALUES (NULL, "Skrag Brown", "Citadel", "Layer", "#90490F", "");
INSERT INTO paints VALUES (NULL, "Tallarn Sand", "Citadel", "Layer", "#A67610", "");
INSERT INTO paints VALUES (NULL, "Agrax Earthshade", "Citadel", "Shade", "#5A573F", "");

INSERT INTO recipes VALUES (NULL, "Light Leather", "Useful for belts, bags and any other straps");

INSERT INTO recipe_steps VALUES(NULL, NULL, 1, 1, 1);
INSERT INTO recipe_steps VALUES(NULL, NULL, 5, 2, 2);
INSERT INTO recipe_steps VALUES(NULL, NULL, 2, 3, 3);
INSERT INTO recipe_steps VALUES(NULL, NULL, 3, 4, 4);
INSERT INTO recipe_steps VALUES(NULL, NULL, 4, 4, 5);

INSERT INTO colour_schemes VALUES(NULL, "Orks", "Mainly for old-school warhammer orks, but also applies to Oathmark conversions");
INSERT INTO scheme_components VALUES(NULL, NULL, "Leather", 1);
"""