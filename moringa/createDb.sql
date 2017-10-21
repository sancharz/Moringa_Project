CREATE USER moringa WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  NOCREATEDB
  NOCREATEROLE
  NOREPLICATION;

CREATE DATABASE "moringa-db"
    WITH 
    OWNER = moringa
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

CREATE TABLE public."Users"
(
    "LastName" character varying(60) COLLATE pg_catalog."default",
    "FirstName" character varying(60) COLLATE pg_catalog."default",
    "Role" character varying(10) COLLATE pg_catalog."default",
    "Email" character varying(100) COLLATE pg_catalog."default",
    salt character varying(256) COLLATE pg_catalog."default",
    "Password" character varying(256) COLLATE pg_catalog."default",
    "userId" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "userIdKey" PRIMARY KEY ("userId")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Users"
    OWNER to moringa;

CREATE TABLE public."Students"
(
    "userId" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "Program" character varying(6) COLLATE pg_catalog."default",
    "Cohort" character varying(10) COLLATE pg_catalog."default",
    "Location" character varying(60) COLLATE pg_catalog."default",
    CONSTRAINT "Students_pkey" PRIMARY KEY ("userId"),
    CONSTRAINT "userIdFKey" FOREIGN KEY ("userId")
        REFERENCES public."Users" ("userId") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."Students"
    OWNER to moringa;

CREATE TABLE public."LocalAdmin"
(
    "userId" character varying(100) COLLATE pg_catalog."default" NOT NULL,
    "Location" character varying(50) COLLATE pg_catalog."default",
    "Program" character varying(6) COLLATE pg_catalog."default",
    CONSTRAINT "LocalAdmin_pkey" PRIMARY KEY ("userId"),
    CONSTRAINT "UserIdFKey" FOREIGN KEY ("userId")
        REFERENCES public."Users" ("userId") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."LocalAdmin"
    OWNER to moringa;

CREATE TABLE public."GlobalAdmin"
(
    "userId" character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT "UserIdFKey" FOREIGN KEY ("userId")
        REFERENCES public."Users" ("userId") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public."GlobalAdmin"
    OWNER to moringa;

-- Index: fki_UserIdFKey

-- DROP INDEX public."fki_UserIdFKey";

CREATE INDEX "fki_UserIdFKey"
    ON public."GlobalAdmin" USING btree
    ("userId" COLLATE pg_catalog."default")
    TABLESPACE pg_default;
