CREATE SCHEMA IF NOT EXISTS content;

DROP TABLE IF EXISTS content.film_work CASCADE;

DROP TABLE IF EXISTS content.genre CASCADE;

DROP TABLE IF EXISTS content.person CASCADE;

DROP TABLE IF EXISTS content.genre_film_work;

DROP TABLE IF EXISTS content.person_film_work;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE INDEX ON content.film_work (title, creation_date, rating);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);
CREATE UNIQUE INDEX name_idx ON content.genre (name);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
	genre_id uuid NOT NULL REFERENCES content.genre (id) ON DELETE CASCADE,
	film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
    created timestamp with time zone
);
CREATE UNIQUE INDEX film_work_genre ON content.genre_film_work (film_work_id, genre_id);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
	person_id uuid NOT NULL REFERENCES content.person (id) ON DELETE CASCADE,
	film_work_id uuid NOT NULL REFERENCES content.film_work (id) ON DELETE CASCADE,
	role TEXT NOT NULL,
    created timestamp with time zone
);
CREATE UNIQUE INDEX film_work_person_role ON content.person_film_work (film_work_id, person_id, role);