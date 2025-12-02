--
-- PostgreSQL database dump
--

\restrict Z4B06flLk7buJFoso2qSQwwMXRa8LZhGyaGsJDTus7ZfMgMiVsKeO0t7wRLbVDP

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: banks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.banks (
    bank_id integer NOT NULL,
    bank_name character varying(255) NOT NULL,
    app_name character varying(255)
);


ALTER TABLE public.banks OWNER TO postgres;

--
-- Name: banks_bank_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.banks_bank_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.banks_bank_id_seq OWNER TO postgres;

--
-- Name: banks_bank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.banks_bank_id_seq OWNED BY public.banks.bank_id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    review_id character varying(50) NOT NULL,
    bank_id integer,
    review_text text NOT NULL,
    rating integer,
    review_date date,
    sentiment_label character varying(50),
    sentiment_score numeric(5,4),
    theme character varying(255),
    source character varying(50) DEFAULT 'Google Play Store'::character varying
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- Name: banks bank_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.banks ALTER COLUMN bank_id SET DEFAULT nextval('public.banks_bank_id_seq'::regclass);


--
-- Name: banks banks_bank_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.banks
    ADD CONSTRAINT banks_bank_name_key UNIQUE (bank_name);


--
-- Name: banks banks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.banks
    ADD CONSTRAINT banks_pkey PRIMARY KEY (bank_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: reviews reviews_bank_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_bank_id_fkey FOREIGN KEY (bank_id) REFERENCES public.banks(bank_id);


--
-- PostgreSQL database dump complete
--

\unrestrict Z4B06flLk7buJFoso2qSQwwMXRa8LZhGyaGsJDTus7ZfMgMiVsKeO0t7wRLbVDP

--
-- PostgreSQL database dump
--

\restrict oapzOrS6mngLdPSSWmnmjZbgf0q6PBJiMrbep6GQtNiZGxIUgTUsbi8halisE7U

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: banks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.banks (bank_id, bank_name, app_name) FROM stdin;
1	Commercial Bank of Ethiopia	CBE Birr
2	Bank of Abyssinia	BOA Mobile Banking
3	Dashen Bank	DASHEN BANK MOBILE BANKING
\.


--
-- Name: banks_bank_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.banks_bank_id_seq', 3, true);


--
-- PostgreSQL database dump complete
--

\unrestrict oapzOrS6mngLdPSSWmnmjZbgf0q6PBJiMrbep6GQtNiZGxIUgTUsbi8halisE7U

