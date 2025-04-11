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

drop table air.routes;
drop table air.airplanes;

select distinct "Destination airport" from air.air_traffic a
where "Destination Country" = 'Italy'

select "Source City", "Destination City", route_id, "Airline Name" from air.air_traffic at2
where "Source City" = 'Brindisi'

CREATE TABLE air.flights (
    flight_id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL,
    numero_posti INTEGER NOT NULL CHECK (numero_posti > 0),
    data_volo DATE NOT NULL,
    orario_partenza TIME NOT NULL,
    orario_arrivo TIME NOT NULL,
    stato_volo VARCHAR(20) DEFAULT 'scheduled',
    FOREIGN KEY (route_id) REFERENCES air.routes_corretta(route_id) ON DELETE cascade)
   ;

CREATE TABLE air.passengers (
    passenger_id SERIAL PRIMARY KEY,
    flight_id INTEGER NOT NULL,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    data_nascita DATE NOT NULL,
    documento_identita VARCHAR(30) NOT NULL UNIQUE,
    FOREIGN KEY (flight_id) REFERENCES air.flights(flight_id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION air.check_posti_disponibili()
RETURNS TRIGGER AS $$
DECLARE
    posti_occupati INTEGER;
    posti_totali INTEGER;
BEGIN
    SELECT COUNT(*) INTO posti_occupati
    FROM air.passengers
    WHERE flight_id = NEW.flight_id;

    SELECT numero_posti INTO posti_totali
    FROM air.flights
    WHERE flight_id = NEW.flight_id;

    IF posti_occupati >= posti_totali THEN
        RAISE EXCEPTION 'Non ci sono più posti disponibili per il volo ID %', NEW.flight_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_posti_disponibili
BEFORE INSERT ON air.passengers
FOR EACH ROW
EXECUTE FUNCTION air.check_posti_disponibili();

CREATE OR REPLACE FUNCTION air.capitalize_nome_cognome()
RETURNS TRIGGER AS $$
BEGIN
    NEW.nome := INITCAP(NEW.nome);
    NEW.cognome := INITCAP(NEW.cognome);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_capitalize_nome_cognome
BEFORE INSERT OR UPDATE ON air.passengers
FOR EACH ROW
EXECUTE FUNCTION air.capitalize_nome_cognome();

INSERT INTO air.flights (route_id, numero_posti, data_volo, orario_partenza, orario_arrivo, stato_volo) VALUES
(32398, 180, '2025-05-01', '08:30', '11:00', 'scheduled'),
(62662, 150, '2025-05-02', '13:15', '16:00', 'scheduled'),
(3119, 200, '2025-05-03', '07:00', '09:30', 'scheduled'),
(46006, 180, '2025-05-04', '19:45', '22:30', 'scheduled'),
(65094, 160, '2025-05-05', '06:00', '08:45', 'scheduled'),
(41315, 140, '2025-05-06', '15:10', '18:00', 'scheduled'),
(56124, 180, '2025-05-07', '12:30', '15:15', 'scheduled'),
(39353, 170, '2025-05-08', '09:00', '11:50', 'scheduled'),
(13554, 190, '2025-05-09', '10:45', '13:20', 'scheduled'),
(1890, 150, '2025-05-10', '17:00', '19:30', 'scheduled'),
(12014, 160, '2025-05-11', '08:20', '10:50', 'scheduled'),
(51969, 175, '2025-05-12', '11:15', '14:00', 'scheduled'),
(3119, 180, '2025-05-13', '06:45', '09:20', 'scheduled'),
(23457, 165, '2025-05-14', '13:00', '15:40', 'scheduled'),
(9310, 185, '2025-05-15', '07:30', '10:15', 'scheduled'),
(48475, 190, '2025-05-16', '18:50', '21:35', 'scheduled'),
(26354, 200, '2025-05-17', '16:00', '18:45', 'scheduled'),
(42729, 160, '2025-05-18', '09:30', '12:10', 'scheduled'),
(4134, 170, '2025-05-19', '05:15', '08:00', 'scheduled'),
(13081, 2, '2025-05-20', '14:20', '17:10', 'scheduled');

INSERT INTO air.passengers (flight_id, nome, cognome, data_nascita, documento_identita) VALUES
(1, 'Luca', 'Bianchi', '1990-01-15', 'AB123456'),
(1, 'Maria', 'Rossi', '1985-07-22', 'CD789012'),
(1, 'Marco', 'Verdi', '1995-03-11', 'EF345678'),
(2, 'Anna', 'Neri', '1992-10-05', 'GH901234'),
(2, 'Giulia', 'Moretti', '1998-06-19', 'IJ567890'),
(3, 'Stefano', 'Gallo', '1980-04-12', 'KL123789'),
(3, 'Paolo', 'Conti', '1975-09-25', 'MN456123'),
(4, 'Simona', 'Russo', '1988-12-30', 'OP789345'),
(4, 'Davide', 'Ferrari', '1991-02-17', 'QR012678'),
(5, 'Francesca', 'Greco', '1993-11-03', 'ST345901'),
(5, 'Giorgio', 'Marino', '1986-08-08', 'UV678234'),
(6, 'Alessia', 'Barbieri', '1997-05-14', 'WX901567'),
(6, 'Valerio', 'Costa', '1990-03-23', 'YZ234890'),
(7, 'Chiara', 'De Luca', '1989-10-10', 'AA345612'),
(7, 'Luigi', 'Rinaldi', '1978-06-06', 'BB678945'),
(8, 'Roberta', 'Leone', '1994-01-21', 'CC901278'),
(8, 'Andrea', 'Palmieri', '1982-09-09', 'DD234561'),
(9, 'Martina', 'Orlando', '1996-07-07', 'EE567894'),
(9, 'Fabio', 'Vitale', '1987-03-19', 'FF890127'),
(10, 'Silvia', 'Longo', '1991-12-01', 'GG123450'),
(10, 'Enrico', 'Messina', '1983-02-02', 'HH456783'),
(11, 'Sofia', 'Negri', '1999-04-04', 'II789016'),
(11, 'Matteo', 'Parisi', '1984-11-11', 'JJ012349'),
(12, 'Beatrice', 'Fiore', '1990-08-18', 'KK345682'),
(12, 'Lorenzo', 'Amato', '1979-05-20', 'LL678915'),
(13, 'Alessandro', 'Grasso', '1985-10-28', 'MM901248'),
(13, 'Elisa', 'Sartori', '1993-06-15', 'NN234581'),
(14, 'Daniele', 'Fontana', '1986-01-09', 'OO567894'),
(14, 'Camilla', 'Rizzi', '1992-03-13', 'PP890127'),
(15, 'Riccardo', 'Testa', '1988-07-07', 'QQ123450'),
(15, 'Eleonora', 'Martini', '1997-11-17', 'RR456783'),
(16, 'Gabriele', 'Bellini', '1995-09-09', 'SS789016'),
(16, 'Ilaria', 'De Santis', '1990-12-24', 'TT012349'),
(17, 'Emanuele', 'Caputo', '1981-02-02', 'UU345682'),
(17, 'Arianna', 'Pellegrini', '1996-06-06', 'VV678915'),
(18, 'Tommaso', 'Sanna', '1987-10-10', 'WW901248'),
(18, 'Serena', 'D’Angelo', '1994-08-08', 'XX234581'),
(19, 'Federico', 'Valenti', '1989-04-30', 'YY567894'),
(19, 'Veronica', 'Gatti', '1993-02-02', 'ZZ890127'),
(20, 'Michele', 'Colombo', '1983-06-06', 'AAA123450'),
(20, 'Noemi', 'Serra', '1991-01-01', 'BBB456783'),
(1, 'Elena', 'Pagani', '1995-12-12', 'CCC789016'),
(2, 'Samuele', 'Basili', '1998-03-03', 'DDD012349'),
(3, 'Claudia', 'Donati', '1990-07-07', 'EEE345682'),
(4, 'Stefania', 'Locatelli', '1985-09-09', 'FFF678915'),
(5, 'Nicola', 'Manzoni', '1977-11-11', 'GGG901248'),
(6, 'Giada', 'Sartore', '1992-10-10', 'HHH234581'),
(7, 'Massimo', 'Nobili', '1986-04-04', 'III567894'),
(8, 'Patrizia', 'Vitali', '1983-08-08', 'JJJ890127');

