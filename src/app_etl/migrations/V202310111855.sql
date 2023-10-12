CREATE TABLE IF NOT EXISTS malaria.annualconfirmedcases (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	etl_id int4 NOT NULL,
	region varchar(50) NULL,
	regioncode varchar(10) NULL,
	country varchar(10) NULL,
	"year" int4 NULL,
	cases_confirmed int4 NULL,
	CONSTRAINT annualconfirmedcases_pkey PRIMARY KEY (id),
    CONSTRAINT fk_etl FOREIGN KEY (etl_id) REFERENCES etl.etl(id)
);

