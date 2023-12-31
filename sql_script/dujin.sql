-- MySQL Script generated by MySQL Workbench
-- Thu Jul  6 00:26:14 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`tan_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`tan_info` ;

CREATE TABLE IF NOT EXISTS `mydb`.`tan_info` (
  `area` VARCHAR(45) NOT NULL,
  `group` VARCHAR(45) NULL,
  `tan_id` VARCHAR(45) NOT NULL,
  `tan_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`tan_id`),
  UNIQUE INDEX `tan_id_UNIQUE` (`tan_id` ASC) VISIBLE,
  UNIQUE INDEX `tan_name_UNIQUE` (`tan_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`all_examinee_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`all_examinee_info` ;

CREATE TABLE IF NOT EXISTS `mydb`.`all_examinee_info` (
  `name` VARCHAR(45) NOT NULL,
  `gender` VARCHAR(45) NOT NULL,
  `personal_phone_number` VARCHAR(45) NULL,
  `contact_person` VARCHAR(45) NULL,
  `contact_person_num` VARCHAR(45) NULL,
  `email` VARCHAR(100) NULL,
  `tan_id` VARCHAR(45) NOT NULL,
  `exam_id` VARCHAR(45) NOT NULL,
  `tan_name` VARCHAR(45) NOT NULL,
  `job` VARCHAR(45) NOT NULL,
  `exam_date` VARCHAR(45) NOT NULL,
  `exam_group` INT NOT NULL,
  `signed` VARCHAR(45) NULL,
  `finished` VARCHAR(45) NULL,
  UNIQUE INDEX `exam_id_UNIQUE` (`exam_id` ASC) VISIBLE,
  PRIMARY KEY (`exam_id`),
  INDEX `tan_id_fk_idx` (`tan_id` ASC) VISIBLE,
  CONSTRAINT `tan_id_fk`
    FOREIGN KEY (`tan_id`)
    REFERENCES `mydb`.`tan_info` (`tan_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`article_info`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`article_info` ;

CREATE TABLE IF NOT EXISTS `mydb`.`article_info` (
  `article_id` VARCHAR(45) NOT NULL,
  `article_name` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`article_id`),
  UNIQUE INDEX `article_name_UNIQUE` (`article_name` ASC) VISIBLE,
  UNIQUE INDEX `article_id_UNIQUE` (`article_id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`actual_exam_situation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`actual_exam_situation` ;

CREATE TABLE IF NOT EXISTS `mydb`.`actual_exam_situation` (
  `article_id` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `correctness_minus` VARCHAR(45) NULL,
  `fluency_minus` VARCHAR(45) NULL,
  `final_score` INT NULL,
  `final_examinar` VARCHAR(45) NULL,
  `score_id` INT NOT NULL AUTO_INCREMENT,
  `exam_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`score_id`),
  UNIQUE INDEX `score_id_UNIQUE` (`score_id` ASC) VISIBLE,
  INDEX `exam_id_fk_idx` (`exam_id` ASC) VISIBLE,
  INDEX `article_id_fk_idx` (`article_id` ASC) VISIBLE,
  CONSTRAINT `exam_id_fk`
    FOREIGN KEY (`exam_id`)
    REFERENCES `mydb`.`all_examinee_info` (`exam_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `article_id_fk`
    FOREIGN KEY (`article_id`)
    REFERENCES `mydb`.`article_info` (`article_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`exams`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`exams` ;

CREATE TABLE IF NOT EXISTS `mydb`.`exams` (
  `exam_group_id` INT NOT NULL AUTO_INCREMENT,
  `exam_id` VARCHAR(45) NOT NULL,
  `exam_date` VARCHAR(45) NOT NULL,
  `exam_group` INT NOT NULL,
  PRIMARY KEY (`exam_group_id`),
  INDEX `exam_id_fk_idx` (`exam_id` ASC) VISIBLE,
  CONSTRAINT `exams_exam_id_fk`
    FOREIGN KEY (`exam_id`)
    REFERENCES `mydb`.`all_examinee_info` (`exam_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
