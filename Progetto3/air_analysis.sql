SELECT "Airline ID", "Name", "Alias", "IATA", "ICAO", "Callsign", "Country", "Active"
FROM air.airlines;
 
SELECT "Name", "IATA code", "ICAO code"
FROM air.airplanes;
 
SELECT "Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone", "Type", "Source"
FROM air.airports;

SELECT "airline", "Airline ID", "Source airport", "Source airport ID", "Destination airport", "Destination airport ID", "codeshare", "stops", "equipment"
FROM air.routes;

--------- Analisi relazione routes-airlines

SELECT r.*, a.*
FROM air.routes r
full join air.airlines a
on r."Airline ID" = a."Airline ID"::text;
 
SELECT count(*)
FROM air.routes r;
--67663

-- Vediamo come l'inner join perda delle informazioni riguardo le rotte
SELECT count(*)
FROM air.routes r
inner join air.airlines a
on r."Airline ID" = a."Airline ID"::text;
--67184
 
SELECT count(*)
FROM air.routes r
full join air.airlines a
on r."Airline ID" = a."Airline ID"::text;
--73278
 
SELECT count(*)
FROM air.routes r
full join air.airlines a
on r."Airline ID" = a."Airline ID"::text
where r."Airline ID" is null;
--routes -> 5615
--airlines -> 479


-- Notiamo che si sono rotte di compagnie aeree non identificate
select count(*) from routes r
where r."Airline ID" = 'N'
--479
 
SELECT a."Airline ID"
FROM air.routes r
full join air.airlines a
on r."Airline ID" = a."Airline ID"::text
where r."Airline ID" is null
order by 1
;
 
 
SELECT a.*
FROM air.routes r
full join air.airlines a
on r."Airline ID" = a."Airline ID"::text
where r."Airline ID" is null
order by 1
;
 
 
SELECT r.*
FROM air.routes r
full join air.airlines a
on r."Airline ID" = a."Airline ID"::text
where a."Airline ID" is null
order by 1
;
 
SELECT distinct r."Airline ID"
FROM air.routes r
full join air.airlines a
on r."Airline ID" = a."Airline ID"::text
where a."Airline ID" is null
order by 1
;

------------------------- Analisi relazione routes-airports

SELECT r.*, a.*
FROM air.routes r
full join air.airports a
on r."Source airport ID" = a."Airport ID"::text;
 
SELECT count(*)
FROM air.routes r;
--67663

-- Vediamo come l'inner join perda delle informazioni riguardo le rotte su aeroporti di partenza
SELECT count(*)
FROM air.routes r
inner join air.airports a
on r."Source airport ID" = a."Airport ID"::text;
--67180

SELECT count(*)
FROM air.routes r
full join air.airports a
on r."Source airport ID" = a."Airport ID"::text
where a."Airport ID" is null;
-- 483

-- Elenco rotte con aeroporti di partenza non presenti o non aventi corrispondenza nella tabella airplanes
SELECT distinct r."Source airport ID"
FROM air.routes r
full join air.airports a
on r."Source airport ID" = a."Airport ID"::text
where a."Airport ID" is null
order by 1
;

-- Esempio di airport ID presente in routes e non in airports
select * from air.airports a
where "Airport ID" = '2611'

------- Stesso discorso da fare su aeroporti di destinazione

-- Vediamo come l'inner join perda delle informazioni riguardo le rotte su aeroporti di destinazione
SELECT count(*)
FROM air.routes r
inner join air.airports a
on r."Destination airport ID" = a."Airport ID"::text;
--67175

SELECT count(*)
FROM air.routes r
full join air.airports a
on r."Destination airport ID" = a."Airport ID"::text
where a."Airport ID" is null;
-- 488

-- Elenco rotte con aeroporti di destinazione non presenti o non aventi corrispondenza nella tabella airplanes
SELECT distinct r."Destination airport ID" 
FROM air.routes r
full join air.airports a
on r."Destination airport ID" = a."Airport ID"::text
where a."Airport ID" is null
order by 1
;

---------- Doppia join su aeroporti di partenza e destinazione

SELECT count(*)
FROM air.routes r
INNER JOIN air.airports a
  ON r."Source airport ID" = a."Airport ID"::text
INNER JOIN air.airports a2
  ON r."Destination airport ID" = a2."Airport ID"::text;
--66771

SELECT count(*)
FROM air.routes r
LEFT JOIN air.airports a1
  ON r."Source airport ID" = a1."Airport ID"::text
LEFT JOIN air.airports a2
  ON r."Destination airport ID" = a2."Airport ID"::text
WHERE a1."Airport ID" IS NULL OR a2."Airport ID" IS NULL;
-- 892

-- Elenco rotte con aeroporti di destinazione o partenza non presenti o non aventi corrispondenza nella tabella airplanes
SELECT r."Source airport ID", r."Source airport", r."Destination airport ID", r."Destination airport"
FROM air.routes r
LEFT JOIN air.airports a1
  ON r."Source airport ID" = a1."Airport ID"::text
LEFT JOIN air.airports a2
  ON r."Destination airport ID" = a2."Airport ID"::text
WHERE a1."Airport ID" IS NULL OR a2."Airport ID" IS NULL
;

ALTER TABLE air.airlines
ADD CONSTRAINT PK_airlines PRIMARY KEY ("Airline ID");

ALTER TABLE air.airports 
ADD CONSTRAINT PK_airports PRIMARY KEY ("Airport ID");

drop table air.routes_corretta

CREATE TABLE air.routes_corretta (
    "Airline ID" INT,
    "Source airport ID" INT,
    "Destination airport ID" INT,
    "codeshare" TEXT,
    "stops" INT,
    "equipment" TEXT,
    FOREIGN KEY ("Airline ID") REFERENCES air.airlines("Airline ID") ON DELETE CASCADE,
    FOREIGN KEY ("Source airport ID") REFERENCES air.airports("Airport ID") ON DELETE SET NULL,
    FOREIGN KEY ("Destination airport ID") REFERENCES air.airports("Airport ID") ON DELETE SET NULL
);

---Controllo e insert su source airport

SELECT DISTINCT r."Source airport ID", r."Source airport"
FROM air.routes r
LEFT JOIN air.airports a
  ON r."Source airport ID" = a."Airport ID"::text 
WHERE a."Airport ID" IS null and r."Source airport ID" = 'N'
ORDER BY 2;

INSERT INTO air.airports values
(-1, 'Unknown', '', '', '', '', 0, 0, 0, '', '', '', '', ''),
(14112, 'Aeroporto de Oiapoque', 'Oiapoque', 'Brazil', 'AOQ', 'SBOI', 3.855, -51.796, 63, -3.0, 'S', 'America/Belem', 'small_airport', 'OurAirports'),
(14115, 'Chefornak Airport', 'Chefornak', 'United States', 'CBS', '', 60.5828, -164.286, 40, -9.0, 'A', 'America/Anchorage', 'small_airport', 'OurAirports'),
(14116, 'Chatham Seaplane Base', 'Chatham', 'United States', 'CKX', '', 57.515, -134.945, 0, -9.0, 'A', 'America/Anchorage', 'seaplane_base', 'OurAirports'),
(14120, 'Ed Daein Airport', 'Ed Daein', 'Sudan', 'EDA', 'none', 11.4067, 26.1183, 1581, 3.0, 'N', 'Africa/Khartoum', 'small_airport', 'OurAirports'),
(14126, 'Ikerasak Heliport', 'Ikerasak', 'Greenland', 'IKE', 'BGIA', 70.4981, -51.3031, 0, 0, '', '', '', 'OurAirports'),
(14127, 'Illorsuit Heliport', 'Illorsuit', 'Greenland', 'IOT', 'BGLL', 71.23972, -53.55556, 0, 0, '', '', '', 'OurAirports'),
(14128, 'Innaarsuit Heliport', 'Innaarsuit', 'Greenland', 'IUI', 'BGIN', 73.2025, -56.0111, 0, 0, '', '', '', 'OurAirports'),
(14130, 'Jajao Airport', 'Isabel', 'Solomon Islands', 'JJA', 'AGJO', -9.5850, 159.5000, 0, 0, '', '', '', 'OurAirports'),
(14138, 'Waterfall Seaplane Base', 'Waterfall', 'United States', 'KWF', 'none', 55.29639, -133.24333, 0, 0, '', '', '', 'OurAirports'),
(14139, 'Katiu Airport', 'Katiu', 'French Polynesia', 'KXU', 'NTKT', -16.3394, -144.4030, 0, 0, '', '', '', 'OurAirports'),
(14144, 'EuroAirport Basel Mulhouse Freiburg', 'Saint-Louis', 'Saint-Louis', 'MLH', 'LFSB', 47.5896, 7.5299, 0, 0, '', '', '', 'OurAirports'),
(14150, 'Naukati Bay Seaplane Base', 'Naukati Bay', 'United States', 'NKI', 'none', 55.84972, -133.22778, 0, 0, '', '', '', 'OurAirports'),
(14152, 'Ustupu-Ogobsucum Airport', 'Ustupo', 'Panama', 'OGM', '', 9.1383, -77.9339, 0, 0, '', '', '', 'OurAirports'),
(14155, 'Orange Walk Airport', 'Orange Walk Town', 'Belize', 'ORZ', 'MZTH', 18.0667, -88.5583, 0, 0, '', '', '', 'OurAirports'),
(14161, 'Aratika-Nord Airport', 'Aratika', 'French Polynesia', 'RKA', 'NTKK', 15.48557, -145.46492, 0, 0, 'none', 'none', 'none', 'OurAirports'),
(14162, 'Simanggang Airport', 'Sri Aman', 'Malaysia', 'SGG', 'WBGY', 1.217, 111.450, 0, 0, '', '', '', 'OurAirports'),
(14163, 'Matthew Spain Airport', 'San Ignacio', 'Belize', 'SQS', '', 17.1859, -89.0099, 0, 0, '', '', '', 'OurAirports'),
(14171, 'Ugashik Bay Airport', 'Ugashik', 'United States', 'UGB', '', 57.42528, -157.74000, 0, 0, '', '', '', 'OurAirports'),
(14176, 'Biloela Airport', 'Biloela', 'Australia', 'ZBL', 'YBLE', -24.3958, 150.5000, 0, 0, '', '', '', 'OurAirports'),
(14178, 'Balsas Airport	', 'Balsas', 'Brazil', 'BSS', 'SNBS', 50.25972, -60.67389, 0, 0, '', '', '', 'OurAirports'),
(14179, 'Monte Alegre Airport', 'Monte Alegre', 'Brazil', 'MTE', 'SNMA', -1.99667, -54.07139, 0, 0, '', '', '', 'OurAirports');

----Problematica riscontrata

select * from air.routes r 
where r."Source airport ID" = '6428'

select * from air.airports a
where a."IATA" = 'JGS'

UPDATE air.routes
SET "Source airport ID" = '6964'
WHERE "Source airport ID" = '6428';

UPDATE air.routes
SET "Destination airport ID" = '6964'
WHERE "Destination airport ID" = '6428';

----Verifica soluzione

create table air.tmp as (
select r."Airline", 
	   r."Airline ID", 
	   r."Source airport", 
	   a."Airport ID" as "Source airport ID", 
	   r."Destination airport", 
	   a2."Airport ID" as "Destination airport ID",
	   r."Codeshare",
	   r."Stops",
	   r."Equipment"
from air.routes r
left join air.airports a
	on r."Source airport" = a."IATA"
left join air.airports a2
	on r."Destination airport" = a2."IATA"
order by 1,3,5)


INSERT INTO air.routes_corretta
	select
		CASE 
	        WHEN "Airline ID" = 'N' THEN -1 
	        ELSE "Airline ID"::INT
	    END AS "Airline ID",
		CASE 
        	WHEN "Source airport ID" IS NULL THEN -1 
        	ELSE "Source airport ID"::INT
    	END AS "Source airport ID",
		CASE 
        	WHEN "Destination airport ID" IS NULL THEN -1 
        	ELSE "Destination airport ID"::INT
    	END AS "Destination airport ID",
		"Codeshare",
		"Stops",
		"Equipment"
	from
		air.tmp;	
	
drop table air.tmp;	
	
ALTER TABLE air.routes_corretta 
ADD COLUMN "route_id" SERIAL;

ALTER TABLE air.routes_corretta
ADD CONSTRAINT PK_routes PRIMARY KEY ("route_id");
	
-- In questo caso la full join opera anche sulle compagnie aeree non identificate
	
SELECT count(*)
FROM air.routes_corretta r
full join air.airlines a
on r."Airline ID" = a."Airline ID"
where a."Airline ID" is null;
--0

 SELECT count(*)
FROM air.routes_corretta r;
--67663
 
SELECT count(*)
FROM air.routes_corretta r
inner join air.airlines a
on r."Airline ID" = a."Airline ID";
--67663

SELECT count(*)
FROM air.routes_corretta r
LEFT JOIN air.airports a1
  ON r."Source airport ID" = a1."Airport ID"
LEFT JOIN air.airports a2
  ON r."Destination airport ID" = a2."Airport ID"
WHERE a1."Airport ID" IS NULL OR a2."Airport ID" IS NULL;
--0

create view air.air_traffic as 
select 
r."route_id", 
r."Source airport ID", 
a1."Name" as "Source airport", 
a1."City" as "Source City", 
a1."Country" as "Source Country", 
a1."IATA" as "Src airport IATA", 
a1."ICAO" as "Src airport ICAO", 
a1."Latitude" as "Src airport Latitude", 
a1."Longitude" as "Src airport Longitude", 
a1."Altitude" as "Src airport Altitude", 
a1."Timezone" as "Src airport Timezone", 
a1."DST" as "Src airport DST", 
a1."Tz database time zone" as "Src airport Tz database time zone", 
a1."Type" as "Src airport Type", 
a1."Source" as "Src airport Source",
r."Destination airport ID", 
a2."Name" as "Destination airport", 
a2."City" as "Destination City", 
a2."Country" as "Destination Country", 
a2."IATA" as "Dest airport IATA", 
a2."ICAO" as "Dest airport ICAO", 
a2."Latitude" as "Dest airport Latitude", 
a2."Longitude" as "Dest airport Longitude", 
a2."Altitude" as "Dest airport Altitude", 
a2."Timezone" as "Dest airport Timezone", 
a2."DST" as "Dest airport DST", 
a2."Tz database time zone" as "Dest airport Tz database time zone", 
a2."Type" as "Dest airport Type", 
a2."Source" as "Dest airport Source",
a."Airline ID",
a."Name" as "Airline Name",
a."Alias" as "Airline Alias",
a."IATA" as "Airline IATA",
a."ICAO" as "Airline ICAO",
a."Callsign" as "Airline Callsign",
a."Country" as "Airline Country",
a."Active" as "Active Airline",
r."codeshare", r."stops", r."equipment"
FROM air.routes_corretta r
inner join air.airlines a
on r."Airline ID" = a."Airline ID"
inner JOIN air.airports a1
  ON r."Source airport ID" = a1."Airport ID"
inner JOIN air.airports a2
  ON r."Destination airport ID" = a2."Airport ID";
 
select count(*) from air.air_traffic 

select distinct "Destination airport" from air.air_traffic a
where "Destination Country" = 'Italy'