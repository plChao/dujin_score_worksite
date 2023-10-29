SELECT *
INTO OUTFILE '/var/lib/mysql-files/actual_exam_situation.csv'
FIELDS TERMINATED BY ','
-- OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '\\'
LINES TERMINATED BY '\n'
FROM actual_exam_situation;