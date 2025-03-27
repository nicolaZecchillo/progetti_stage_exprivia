select count(*) from school.voti v 
--100

select count(*) from school.studenti s 
full join school.voti v
on s."Nome_Studente" = v."Nome_Studente";
--100

select count(*) from school.orario o 
full join school.studenti s 
on o."ID_Classe" = s."Classe";
--842

select count(*) from school.orario o 
full join school.aule a 
on o."Nome_Aula" = a."Nome_Aula";
--500

select count(*) from school.orario o  
--500

-- 842 - 500 = 342 (righe aggiuntive)

select count(*) from school.orario o 
full join school.studenti s 
on o."ID_Classe" = s."Classe"
where o."ID_Classe" is null;
--0

select count(*) from school.orario o 
full join school.studenti s 
on o."ID_Classe" = s."Classe"
where s."Classe" is null;
--0

select distinct(o."ID_Classe"), count(*) from school.orario o 
full join school.studenti s 
on o."ID_Classe" = s."Classe"
group by o."ID_Classe"
--1A = 158
--2B = 368
--3C = 316

select count(*) from school.orario o 
where o."ID_Classe" = '1A';
-- 158

select count(*) from school.orario o 
where o."ID_Classe" = '2B';
--184 (esattamente il doppio della join, perchè 2 studenti frequentano la classe 2B)

select count(*) from school.orario o 
where o."ID_Classe" = '3C';
--158 (esattamente il doppio della join, perchè 2 studenti frequentano la classe 3C)

-- 184 + 158 = 342 (corrispondente al numero di righe aggiuntive della full join)

create table school.studenti_normalizzata as 
select * from school.studenti s;

ALTER TABLE school.studenti_normalizzata
ADD COLUMN "ID_Studente" SERIAL PRIMARY KEY;

ALTER TABLE school.aule
ADD CONSTRAINT PK_aule PRIMARY KEY ("Nome_Aula");

CREATE TABLE school.orario_normalizzata (
    "ID_Orario" SERIAL PRIMARY KEY,
    "ID_Studente" INT,
    "Classe" TEXT,
    "Ora" INT,
    "Materia" TEXT,
    "Insegnante" TEXT,
    "Data" TEXT,
    "Nome_Aula" TEXT,
    FOREIGN KEY ("ID_Studente") REFERENCES school.studenti_normalizzata("ID_Studente") ON DELETE CASCADE,
    FOREIGN KEY ("Nome_Aula") REFERENCES school.aule("Nome_Aula") ON DELETE SET NULL
);

INSERT INTO school.orario_normalizzata ("ID_Studente", "Classe", "Ora", "Materia", "Insegnante", "Data", "Nome_Aula")
SELECT 
    s."ID_Studente",
    o."ID_Classe",
    o."Ora",
    o."Materia",
    o."Insegnante",
    o."Data",
    o."Nome_Aula"
FROM school.orario o
LEFT JOIN school.studenti_normalizzata s ON o."ID_Classe" = s."Classe"

create table school.voti_normalizzata (
	"ID_Voto" SERIAL PRIMARY KEY,
	"ID_Studente" INT,
    "Materia" TEXT,
    "Voto" TEXT,
    "Data_Voto" TEXT,
    FOREIGN KEY ("ID_Studente") REFERENCES school.studenti_normalizzata("ID_Studente") ON DELETE cascade
    );

INSERT INTO school.voti_normalizzata ("ID_Studente", "Materia", "Voto", "Data_Voto")
SELECT 
    s."ID_Studente",
    v."Materia",
    v."Voto",
    v."Data_Voto"
FROM school.voti v
LEFT JOIN school.studenti_normalizzata s ON v."Nome_Studente" = s."Nome_Studente";

