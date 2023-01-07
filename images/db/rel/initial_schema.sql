CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;


CREATE TABLE public.nationalities (
	id              INT PRIMARY KEY,
	name            VARCHAR(250) UNIQUE,
	geom            GEOMETRY,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.players (
	id              INT PRIMARY KEY,
	name            VARCHAR(250),
	age             INT,
	overall         INT,
	nationality     INT,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);


