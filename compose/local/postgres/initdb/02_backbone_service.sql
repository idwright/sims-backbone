--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.taxonomy_identifiers DROP CONSTRAINT fk_taxa;
ALTER TABLE ONLY public.attrs DROP CONSTRAINT fk_study_loc;
ALTER TABLE ONLY public.original_samples DROP CONSTRAINT fk_species;
ALTER TABLE ONLY public.sampling_event_attrs DROP CONSTRAINT fk_sampling_event_attr;
ALTER TABLE ONLY public.sampling_event_attrs DROP CONSTRAINT fk_sampling_event;
ALTER TABLE ONLY public.sampling_events DROP CONSTRAINT fk_proxy_location;
ALTER TABLE ONLY public.partner_species_identifiers DROP CONSTRAINT fk_partner_sp_study;
ALTER TABLE ONLY public.taxonomy_identifiers DROP CONSTRAINT fk_partner_sp;
ALTER TABLE ONLY public.original_samples DROP CONSTRAINT fk_os_study;
ALTER TABLE ONLY public.original_samples DROP CONSTRAINT fk_os_se;
ALTER TABLE ONLY public.original_sample_attrs DROP CONSTRAINT fk_original_sample;
ALTER TABLE ONLY public.location_attrs DROP CONSTRAINT fk_location_attr;
ALTER TABLE ONLY public.location_attrs DROP CONSTRAINT fk_location;
ALTER TABLE ONLY public.sampling_events DROP CONSTRAINT fk_location;
ALTER TABLE ONLY public.individual_attrs DROP CONSTRAINT fk_individual_attr;
ALTER TABLE ONLY public.individual_attrs DROP CONSTRAINT fk_individual;
ALTER TABLE ONLY public.sampling_events DROP CONSTRAINT fk_individual;
ALTER TABLE ONLY public.event_set_notes DROP CONSTRAINT fk_esn_es;
ALTER TABLE ONLY public.event_set_members DROP CONSTRAINT fk_esm_se;
ALTER TABLE ONLY public.event_set_members DROP CONSTRAINT fk_esm_es;
ALTER TABLE ONLY public.derivative_samples DROP CONSTRAINT fk_ds_os;
ALTER TABLE ONLY public.derivative_sample_attrs DROP CONSTRAINT fk_derivative_sample;
ALTER TABLE ONLY public.locations DROP CONSTRAINT fk_country;
ALTER TABLE ONLY public.assay_datum_attrs DROP CONSTRAINT fk_assay_datum;
ALTER TABLE ONLY public.assay_data DROP CONSTRAINT fk_ad_ds;
ALTER TABLE ONLY public.derivative_samples DROP CONSTRAINT derivative_samples_derivative_samples_fk;
DROP INDEX public.studies_study_code_idx;
DROP INDEX public.partner_species_identifiers_partner_species_idx;
DROP INDEX public.original_sample_attrs_original_sample_id_idx;
DROP INDEX public.location_attrs_location_id_idx;
DROP INDEX public.individual_attrs_individual_id_idx;
DROP INDEX public.idx_study_name;
DROP INDEX public.idx_study_id;
DROP INDEX public.idx_se_doc;
DROP INDEX public.idx_partner_species;
DROP INDEX public.idx_ident_value;
DROP INDEX public.idx_ident_type;
DROP INDEX public.fki_sampling_event_id;
DROP INDEX public.fki_sampling_event_attr_id;
DROP INDEX public.fki_proxy_location;
DROP INDEX public.fki_location_id;
DROP INDEX public.fki_location_attr_id;
DROP INDEX public.fki_location;
DROP INDEX public.fki_individual_id;
DROP INDEX public.fki_individual_attr_id;
DROP INDEX public.fki_individual;
DROP INDEX public.fki_fk_esn_es;
DROP INDEX public.fki_fk_esm_se;
DROP INDEX public.fki_fk_esm_es;
DROP INDEX public.event_set_members_sampling_event_id_idx;
DROP INDEX public.attrs_attr_type_idx;
DROP INDEX public.attrs_attr_source_idx;
ALTER TABLE ONLY public.studies DROP CONSTRAINT uniq_study_code;
ALTER TABLE ONLY public.event_sets DROP CONSTRAINT uniq_event_sets;
ALTER TABLE ONLY public.event_set_members DROP CONSTRAINT uniq_event_set_members;
ALTER TABLE ONLY public.taxonomies DROP CONSTRAINT taxonomy_id;
ALTER TABLE ONLY public.studies DROP CONSTRAINT studies_id;
ALTER TABLE ONLY public.sampling_events DROP CONSTRAINT sampling_event_id;
ALTER TABLE ONLY public.event_set_notes DROP CONSTRAINT pk_esn;
ALTER TABLE ONLY public.event_sets DROP CONSTRAINT pk_es;
ALTER TABLE ONLY public.partner_species_identifiers DROP CONSTRAINT partner_species_identifiers_id;
ALTER TABLE ONLY public.original_samples DROP CONSTRAINT original_sample_id;
ALTER TABLE ONLY public.locations DROP CONSTRAINT location_id;
ALTER TABLE ONLY public.individuals DROP CONSTRAINT individual_id;
ALTER TABLE ONLY public.derivative_samples DROP CONSTRAINT derivative_sample_id;
ALTER TABLE ONLY public.countries DROP CONSTRAINT countries_id;
ALTER TABLE ONLY public.attrs DROP CONSTRAINT attr_id;
ALTER TABLE ONLY public.assay_data DROP CONSTRAINT assay_datum_id;
ALTER TABLE public.event_sets ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.archive ALTER COLUMN id DROP DEFAULT;
DROP VIEW public.v_sampling_events;
DROP TABLE public.taxonomy_identifiers;
DROP TABLE public.taxonomies;
DROP TABLE public.studies;
DROP TABLE public.sampling_events;
DROP TABLE public.sampling_event_attrs;
DROP TABLE public.partner_species_identifiers;
DROP TABLE public.original_samples;
DROP TABLE public.original_sample_attrs;
DROP TABLE public.locations;
DROP TABLE public.location_attrs;
DROP TABLE public.individuals;
DROP TABLE public.individual_attrs;
DROP SEQUENCE public.event_sets_id_seq;
DROP TABLE public.event_sets;
DROP TABLE public.event_set_notes;
DROP TABLE public.event_set_members;
DROP TABLE public.derived_sample_attrs;
DROP TABLE public.derivative_samples;
DROP TABLE public.derivative_sample_attrs;
DROP TABLE public.countries;
DROP TABLE public.attrs;
DROP TABLE public.assay_datum_attrs;
DROP TABLE public.assay_data;
DROP SEQUENCE public.archive_id_seq;
DROP TABLE public.archive;
DROP EXTENSION postgis;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: archive; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.archive (
    id integer NOT NULL,
    submitter character varying(64),
    action_id character varying(64),
    entity_id character varying(64),
    input_value text,
    output_value json,
    result_code integer,
    action_date timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: archive_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.archive_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: archive_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.archive_id_seq OWNED BY public.archive.id;


--
-- Name: assay_data; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assay_data (
    id uuid NOT NULL,
    derivative_sample_id uuid,
    ebi_run_acc character varying
);


--
-- Name: assay_datum_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.assay_datum_attrs (
    assay_datum_id uuid,
    attr_id uuid
);


--
-- Name: attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.attrs (
    id uuid NOT NULL,
    study_id uuid,
    attr_type character varying(256),
    attr_value character varying(256),
    attr_source character varying(256)
);


--
-- Name: countries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.countries (
    english character varying,
    french character varying,
    alpha2 character(2),
    alpha3 character(3) NOT NULL,
    numeric_code integer
);


--
-- Name: derivative_sample_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.derivative_sample_attrs (
    derivative_sample_id uuid,
    attr_id uuid
);


--
-- Name: derivative_samples; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.derivative_samples (
    id uuid NOT NULL,
    original_sample_id uuid,
    dna_prep character varying,
    parent_derivative_sample_id uuid
);


--
-- Name: derived_sample_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.derived_sample_attrs (
    derived_sample_id uuid,
    attr_id uuid
);


--
-- Name: event_set_members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_set_members (
    event_set_id integer,
    sampling_event_id uuid
);


--
-- Name: event_set_notes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_set_notes (
    event_set_id integer NOT NULL,
    note_name character varying(128) NOT NULL,
    note_text text
);


--
-- Name: event_sets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event_sets (
    id integer NOT NULL,
    event_set_name character varying(128) NOT NULL
);


--
-- Name: event_sets_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.event_sets_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: event_sets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.event_sets_id_seq OWNED BY public.event_sets.id;


--
-- Name: individual_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.individual_attrs (
    individual_id uuid,
    attr_id uuid
);


--
-- Name: individuals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.individuals (
    id uuid NOT NULL
);


--
-- Name: location_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.location_attrs (
    location_id uuid,
    attr_id uuid
);


--
-- Name: locations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.locations (
    id uuid NOT NULL,
    location public.geometry(Point),
    country character(3),
    accuracy character varying,
    curated_name character varying,
    curation_method character varying,
    notes character varying
);


--
-- Name: original_sample_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.original_sample_attrs (
    original_sample_id uuid,
    attr_id uuid
);


--
-- Name: original_samples; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.original_samples (
    id uuid NOT NULL,
    study_id uuid,
    sampling_event_id uuid,
    partner_species_id uuid,
    days_in_culture integer
);


--
-- Name: partner_species_identifiers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.partner_species_identifiers (
    id uuid NOT NULL,
    study_id uuid,
    partner_species character varying(128)
);


--
-- Name: sampling_event_attrs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sampling_event_attrs (
    sampling_event_id uuid,
    attr_id uuid
);


--
-- Name: sampling_events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sampling_events (
    id uuid NOT NULL,
    doc date,
    doc_accuracy character varying,
    location_id uuid,
    individual_id uuid,
    proxy_location_id uuid
);


--
-- Name: studies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.studies (
    id uuid NOT NULL,
    study_name character varying(64),
    study_code character varying(4)
);


--
-- Name: taxonomies; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.taxonomies (
    id bigint NOT NULL,
    rank character varying(32),
    name character varying(128)
);


--
-- Name: taxonomy_identifiers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.taxonomy_identifiers (
    taxonomy_id bigint,
    partner_species_id uuid
);


--
-- Name: v_sampling_events; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.v_sampling_events AS
 SELECT sampling_events.id,
    sampling_events.doc,
    sampling_events.doc_accuracy,
    sampling_events.location_id,
    sampling_events.individual_id,
    public.st_x(loc.location) AS latitude,
    public.st_y(loc.location) AS longitude,
    loc.accuracy,
    loc.curated_name,
    loc.curation_method,
    loc.country,
    loc.notes,
    la.attr_value AS partner_name,
    sampling_events.proxy_location_id,
    public.st_x(proxy_loc.location) AS proxy_latitude,
    public.st_y(proxy_loc.location) AS proxy_longitude,
    proxy_loc.accuracy AS proxy_accuracy,
    proxy_loc.curated_name AS proxy_curated_name,
    proxy_loc.curation_method AS proxy_curation_method,
    proxy_loc.country AS proxy_country,
    proxy_loc.notes AS proxy_notes,
    pla.attr_value AS proxy_partner_name
   FROM ((((((public.sampling_events
     LEFT JOIN public.locations loc ON ((loc.id = sampling_events.location_id)))
     LEFT JOIN public.location_attrs li ON ((li.location_id = sampling_events.location_id)))
     LEFT JOIN public.attrs la ON (((li.attr_id = la.id) AND ((la.attr_type)::text = 'partner_name'::text))))
     LEFT JOIN public.locations proxy_loc ON ((proxy_loc.id = sampling_events.proxy_location_id)))
     LEFT JOIN public.location_attrs pli ON ((pli.location_id = sampling_events.proxy_location_id)))
     LEFT JOIN public.attrs pla ON (((pli.attr_id = pla.id) AND ((pla.attr_type)::text = 'partner_name'::text))));


--
-- Name: archive id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.archive ALTER COLUMN id SET DEFAULT nextval('public.archive_id_seq'::regclass);


--
-- Name: event_sets id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_sets ALTER COLUMN id SET DEFAULT nextval('public.event_sets_id_seq'::regclass);


--
-- Name: assay_data assay_datum_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assay_data
    ADD CONSTRAINT assay_datum_id PRIMARY KEY (id);


--
-- Name: attrs attr_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attrs
    ADD CONSTRAINT attr_id PRIMARY KEY (id);


--
-- Name: countries countries_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_id PRIMARY KEY (alpha3);


--
-- Name: derivative_samples derivative_sample_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_samples
    ADD CONSTRAINT derivative_sample_id PRIMARY KEY (id);


--
-- Name: individuals individual_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.individuals
    ADD CONSTRAINT individual_id PRIMARY KEY (id);


--
-- Name: locations location_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT location_id PRIMARY KEY (id);


--
-- Name: original_samples original_sample_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_samples
    ADD CONSTRAINT original_sample_id PRIMARY KEY (id);


--
-- Name: partner_species_identifiers partner_species_identifiers_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partner_species_identifiers
    ADD CONSTRAINT partner_species_identifiers_id PRIMARY KEY (id);


--
-- Name: event_sets pk_es; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_sets
    ADD CONSTRAINT pk_es PRIMARY KEY (id);


--
-- Name: event_set_notes pk_esn; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_notes
    ADD CONSTRAINT pk_esn PRIMARY KEY (event_set_id, note_name);


--
-- Name: sampling_events sampling_event_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_events
    ADD CONSTRAINT sampling_event_id PRIMARY KEY (id);


--
-- Name: studies studies_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.studies
    ADD CONSTRAINT studies_id PRIMARY KEY (id);


--
-- Name: taxonomies taxonomy_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.taxonomies
    ADD CONSTRAINT taxonomy_id PRIMARY KEY (id);


--
-- Name: event_set_members uniq_event_set_members; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_members
    ADD CONSTRAINT uniq_event_set_members UNIQUE (event_set_id, sampling_event_id);


--
-- Name: event_sets uniq_event_sets; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_sets
    ADD CONSTRAINT uniq_event_sets UNIQUE (event_set_name);


--
-- Name: studies uniq_study_code; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.studies
    ADD CONSTRAINT uniq_study_code UNIQUE (study_code);


--
-- Name: attrs_attr_source_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX attrs_attr_source_idx ON public.attrs USING btree (attr_source);


--
-- Name: attrs_attr_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX attrs_attr_type_idx ON public.attrs USING btree (attr_type, attr_value);


--
-- Name: event_set_members_sampling_event_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_set_members_sampling_event_id_idx ON public.event_set_members USING btree (sampling_event_id);


--
-- Name: fki_fk_esm_es; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_fk_esm_es ON public.event_set_members USING btree (event_set_id);


--
-- Name: fki_fk_esm_se; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_fk_esm_se ON public.event_set_members USING btree (sampling_event_id);


--
-- Name: fki_fk_esn_es; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_fk_esn_es ON public.event_set_notes USING btree (event_set_id);


--
-- Name: fki_individual; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_individual ON public.sampling_events USING btree (individual_id);


--
-- Name: fki_individual_attr_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_individual_attr_id ON public.individual_attrs USING btree (attr_id);


--
-- Name: fki_individual_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_individual_id ON public.individual_attrs USING btree (individual_id);


--
-- Name: fki_location; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_location ON public.sampling_events USING btree (location_id);


--
-- Name: fki_location_attr_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_location_attr_id ON public.location_attrs USING btree (attr_id);


--
-- Name: fki_location_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_location_id ON public.location_attrs USING btree (location_id);


--
-- Name: fki_proxy_location; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_proxy_location ON public.sampling_events USING btree (proxy_location_id);


--
-- Name: fki_sampling_event_attr_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_sampling_event_attr_id ON public.sampling_event_attrs USING btree (attr_id);


--
-- Name: fki_sampling_event_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX fki_sampling_event_id ON public.sampling_event_attrs USING btree (sampling_event_id);


--
-- Name: idx_ident_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ident_type ON public.attrs USING btree (attr_type);


--
-- Name: idx_ident_value; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ident_value ON public.attrs USING btree (attr_value);


--
-- Name: idx_partner_species; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_partner_species ON public.partner_species_identifiers USING btree (partner_species);


--
-- Name: idx_se_doc; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_se_doc ON public.sampling_events USING btree (doc);


--
-- Name: idx_study_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_study_id ON public.studies USING btree (id);


--
-- Name: idx_study_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_study_name ON public.studies USING btree (study_name);


--
-- Name: individual_attrs_individual_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX individual_attrs_individual_id_idx ON public.individual_attrs USING btree (individual_id);


--
-- Name: location_attrs_location_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX location_attrs_location_id_idx ON public.location_attrs USING btree (location_id);


--
-- Name: original_sample_attrs_original_sample_id_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX original_sample_attrs_original_sample_id_idx ON public.original_sample_attrs USING btree (original_sample_id);


--
-- Name: partner_species_identifiers_partner_species_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX partner_species_identifiers_partner_species_idx ON public.partner_species_identifiers USING btree (partner_species);


--
-- Name: studies_study_code_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX studies_study_code_idx ON public.studies USING btree (study_code);


--
-- Name: derivative_samples derivative_samples_derivative_samples_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_samples
    ADD CONSTRAINT derivative_samples_derivative_samples_fk FOREIGN KEY (parent_derivative_sample_id) REFERENCES public.derivative_samples(id);


--
-- Name: assay_data fk_ad_ds; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assay_data
    ADD CONSTRAINT fk_ad_ds FOREIGN KEY (derivative_sample_id) REFERENCES public.derivative_samples(id);


--
-- Name: assay_datum_attrs fk_assay_datum; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.assay_datum_attrs
    ADD CONSTRAINT fk_assay_datum FOREIGN KEY (assay_datum_id) REFERENCES public.assay_data(id);


--
-- Name: locations fk_country; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.locations
    ADD CONSTRAINT fk_country FOREIGN KEY (country) REFERENCES public.countries(alpha3);


--
-- Name: derivative_sample_attrs fk_derivative_sample; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_sample_attrs
    ADD CONSTRAINT fk_derivative_sample FOREIGN KEY (derivative_sample_id) REFERENCES public.derivative_samples(id);


--
-- Name: derivative_samples fk_ds_os; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.derivative_samples
    ADD CONSTRAINT fk_ds_os FOREIGN KEY (original_sample_id) REFERENCES public.original_samples(id);


--
-- Name: event_set_members fk_esm_es; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_members
    ADD CONSTRAINT fk_esm_es FOREIGN KEY (event_set_id) REFERENCES public.event_sets(id);


--
-- Name: event_set_members fk_esm_se; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_members
    ADD CONSTRAINT fk_esm_se FOREIGN KEY (sampling_event_id) REFERENCES public.sampling_events(id);


--
-- Name: event_set_notes fk_esn_es; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event_set_notes
    ADD CONSTRAINT fk_esn_es FOREIGN KEY (event_set_id) REFERENCES public.event_sets(id);


--
-- Name: sampling_events fk_individual; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_events
    ADD CONSTRAINT fk_individual FOREIGN KEY (individual_id) REFERENCES public.individuals(id);


--
-- Name: individual_attrs fk_individual; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.individual_attrs
    ADD CONSTRAINT fk_individual FOREIGN KEY (individual_id) REFERENCES public.individuals(id);


--
-- Name: individual_attrs fk_individual_attr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.individual_attrs
    ADD CONSTRAINT fk_individual_attr FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- Name: sampling_events fk_location; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_events
    ADD CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES public.locations(id);


--
-- Name: location_attrs fk_location; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.location_attrs
    ADD CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES public.locations(id);


--
-- Name: location_attrs fk_location_attr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.location_attrs
    ADD CONSTRAINT fk_location_attr FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- Name: original_sample_attrs fk_original_sample; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_sample_attrs
    ADD CONSTRAINT fk_original_sample FOREIGN KEY (original_sample_id) REFERENCES public.original_samples(id);


--
-- Name: original_samples fk_os_se; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_samples
    ADD CONSTRAINT fk_os_se FOREIGN KEY (sampling_event_id) REFERENCES public.sampling_events(id);


--
-- Name: original_samples fk_os_study; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_samples
    ADD CONSTRAINT fk_os_study FOREIGN KEY (study_id) REFERENCES public.studies(id);


--
-- Name: taxonomy_identifiers fk_partner_sp; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.taxonomy_identifiers
    ADD CONSTRAINT fk_partner_sp FOREIGN KEY (partner_species_id) REFERENCES public.partner_species_identifiers(id);


--
-- Name: partner_species_identifiers fk_partner_sp_study; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.partner_species_identifiers
    ADD CONSTRAINT fk_partner_sp_study FOREIGN KEY (study_id) REFERENCES public.studies(id);


--
-- Name: sampling_events fk_proxy_location; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_events
    ADD CONSTRAINT fk_proxy_location FOREIGN KEY (proxy_location_id) REFERENCES public.locations(id);


--
-- Name: sampling_event_attrs fk_sampling_event; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_event_attrs
    ADD CONSTRAINT fk_sampling_event FOREIGN KEY (sampling_event_id) REFERENCES public.sampling_events(id);


--
-- Name: sampling_event_attrs fk_sampling_event_attr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sampling_event_attrs
    ADD CONSTRAINT fk_sampling_event_attr FOREIGN KEY (attr_id) REFERENCES public.attrs(id);


--
-- Name: original_samples fk_species; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.original_samples
    ADD CONSTRAINT fk_species FOREIGN KEY (partner_species_id) REFERENCES public.partner_species_identifiers(id);


--
-- Name: attrs fk_study_loc; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attrs
    ADD CONSTRAINT fk_study_loc FOREIGN KEY (study_id) REFERENCES public.studies(id);


--
-- Name: taxonomy_identifiers fk_taxa; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.taxonomy_identifiers
    ADD CONSTRAINT fk_taxa FOREIGN KEY (taxonomy_id) REFERENCES public.taxonomies(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: -
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

