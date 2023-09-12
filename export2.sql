--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4
-- Dumped by pg_dump version 15.4

-- Started on 2023-09-12 22:33:16

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 3331 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 216 (class 1259 OID 16420)
-- Name: images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.images (
    part_number text NOT NULL,
    image_path text NOT NULL
);


ALTER TABLE public.images OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16401)
-- Name: product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product (
    part_number text NOT NULL,
    description text
);


ALTER TABLE public.product OWNER TO postgres;

--
-- TOC entry 3325 (class 0 OID 16420)
-- Dependencies: 216
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.images (part_number, image_path) FROM stdin;
TEST	C:\\23.jpg
TEST	C:\\24.jpg
TEST2	C:\\26.jpg
TEST2	C:\\27.jpg
\.


--
-- TOC entry 3324 (class 0 OID 16401)
-- Dependencies: 215
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product (part_number, description) FROM stdin;
TEST	TESTDESCR
TEST2	another description
\.


--
-- TOC entry 3180 (class 2606 OID 16426)
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (part_number, image_path);


--
-- TOC entry 3178 (class 2606 OID 16407)
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (part_number);


--
-- TOC entry 3181 (class 2606 OID 16427)
-- Name: images images_part_number_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_part_number_fkey FOREIGN KEY (part_number) REFERENCES public.product(part_number) ON DELETE CASCADE;


-- Completed on 2023-09-12 22:33:16

--
-- PostgreSQL database dump complete
--

