BEGIN;

DROP TABLE IF EXISTS "artist";
DROP TABLE IF EXISTS "album";
DROP TABLE IF EXISTS "music";

CREATE TABLE "artist" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL
);

CREATE TABLE "album" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "artist_id" integer NOT NULL REFERENCES "artist" ("id"),
    "year" integer NOT NULL,
    "genre" varchar(20) NOT NULL
);

CREATE TABLE "music" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "album_id" integer NOT NULL REFERENCES "album" ("id"),
    "track" integer NOT NULL,
    "length" integer NOT NULL,
    "bitrate" integer NOT NULL,
    "path" varchar(1000) NOT NULL,
    "size" integer NOT NULL
);

COMMIT;
