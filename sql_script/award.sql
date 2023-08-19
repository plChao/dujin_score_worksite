DROP TABLE IF EXISTS `mydb`.`awards` ;

CREATE TABLE IF NOT EXISTS `mydb`.`awards` (
    `award_id` VARCHAR(45) NOT NULL,
    `article_id` VARCHAR(45) NOT NULL,
    `article_name` VARCHAR(200) NOT NULL);

load data local infile '../2023_table/awards.csv'
into table awards
fields terminated by ','
enclosed by '"'
lines terminated by '\n'
ignore 1 lines;
