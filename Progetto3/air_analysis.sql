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
SELECT distinct r."Source airport ID", r."Source airport" 
FROM air.routes r
full join air.airports a
on r."Source airport ID" = a."Airport ID"::text
where a."Airport ID" is null
order by 1
;

-- Esempio di airport ID presente in routes e non in airports
select * from airports a
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
SELECT distinct r."Source airport ID", r."Source airport" 
FROM air.routes r
full join air.airports a
on r."Source airport ID" = a."Airport ID"::text
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

---------- Inserimento riga supplementare nella tabella airport per gestire i valori 'N'
INSERT INTO air.airports
("Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz database time zone", "Type", "Source")
VALUES(-1, 'Unknown', '', '', '', '', 0, 0, 0, '', '', '', '', '');

-- Andiamo a creare una nuova tabella routes in cui le compagnie aeree e gli aeroporti con id 'N' assumono valore -1,
-- valore che sulle tabelle airlines e airports va ad indicare le compagnie e gli aeroporti non identificati

CREATE TABLE air.routes_corretta AS
	select
		"airline",
		CASE 
	        WHEN "Airline ID" = 'N' THEN -1 
	        ELSE "Airline ID"::INT
	    END AS "Airline ID",
		"Source airport",
		CASE 
        	WHEN "Source airport ID" = 'N' THEN -1 
        	ELSE "Source airport ID"::INT
    	END AS "Source airport ID",
		"Destination airport",
		CASE 
        	WHEN "Destination airport ID" = 'N' THEN -1 
        	ELSE "Destination airport ID"::INT
    	END AS "Destination airport ID",
		"codeshare",
		"stops",
		"equipment"
	from
		air.routes;

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
--476

-- Elenco rotte con Source/Destination airport senza corrispondenza nella tabella aiports
SELECT r."Source airport ID", r."Source airport", r."Destination airport ID", r."Destination airport"
FROM air.routes_corretta r
LEFT JOIN air.airports a1
  ON r."Source airport ID" = a1."Airport ID"
LEFT JOIN air.airports a2
  ON r."Destination airport ID" = a2."Airport ID"
WHERE a1."Airport ID" IS NULL OR a2."Airport ID" IS NULL
;

