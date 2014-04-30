SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `mydb` ;
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Hashes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Hashes` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Hashes` (
  `User_ID` VARCHAR(100) NOT NULL ,
  `Hash` VARCHAR(45) NULL ,
  `Salt` VARCHAR(45) NULL ,
  PRIMARY KEY (`User_ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Medical_Facility`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Medical_Facility` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Medical_Facility` (
  `Facility_ID` INT NOT NULL ,
  `Facility_Name` VARCHAR(45) NULL ,
  `Facility_Address` VARCHAR(200) NULL ,
  `Facility_Phone` VARCHAR(45) NULL ,
  PRIMARY KEY (`Facility_ID`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Admin`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Admin` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Admin` (
  `Admin_ID` INT NOT NULL ,
  `Admin_UserID` VARCHAR(100) NULL ,
  `Admin_Name` VARCHAR(45) NULL ,
  `Admin_Address` VARCHAR(200) NULL ,
  `Admin_Phone` VARCHAR(45) NULL ,
  `Facility_ID` INT NULL ,
  PRIMARY KEY (`Admin_ID`) ,
  CONSTRAINT `FK_Hashes_Admin_User_ID`
    FOREIGN KEY (`Admin_UserID` )
    REFERENCES `mydb`.`Hashes` (`User_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Admin_Facility_ID`
    FOREIGN KEY (`Facility_ID` )
    REFERENCES `mydb`.`Medical_Facility` (`Facility_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `FK_Hashes_User_ID_idx` ON `mydb`.`Admin` (`Admin_UserID` ASC) ;

CREATE INDEX `FK_Admin_Facility_ID_idx` ON `mydb`.`Admin` (`Facility_ID` ASC) ;


-- -----------------------------------------------------
-- Table `mydb`.`Patient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Patient` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Patient` (
  `SSN` INT NOT NULL ,
  `Patient_UserID` VARCHAR(100) NULL ,
  `Patient_Name` VARCHAR(45) NULL ,
  `Patient_DOB` DATETIME NULL ,
  `Age` INT NULL ,
  `Sex` VARCHAR(45) NULL ,
  `Patient_Address` VARCHAR(200) NULL ,
  `Patient_Phone` VARCHAR(45) NULL ,
  `Emergency_Contact` VARCHAR(45) NULL ,
  `Insurance_Type` VARCHAR(45) NULL ,
  `Medical_Condition` VARCHAR(500) NULL ,
  PRIMARY KEY (`SSN`) ,
  CONSTRAINT `FK_Patient_Hash_User`
    FOREIGN KEY (`Patient_UserID` )
    REFERENCES `mydb`.`Hashes` (`User_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `FK_Patient_Hash_User_idx` ON `mydb`.`Patient` (`Patient_UserID` ASC) ;


-- -----------------------------------------------------
-- Table `mydb`.`Doctor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Doctor` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Doctor` (
  `Doctor_Lic_No` INT NOT NULL ,
  `Doctor_UserID` VARCHAR(100) NULL ,
  `Doctor_Name` VARCHAR(45) NULL ,
  `Doctor_Address` VARCHAR(200) NULL ,
  `Doctor_Phone` VARCHAR(45) NULL ,
  `Admin_ID` INT NULL ,
  `Specialization` VARCHAR(45) NULL ,
  PRIMARY KEY (`Doctor_Lic_No`) ,
  CONSTRAINT `FK_Doctor_Hash_User_ID`
    FOREIGN KEY (`Doctor_UserID` )
    REFERENCES `mydb`.`Hashes` (`User_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Doctor_Admin`
    FOREIGN KEY (`Admin_ID` )
    REFERENCES `mydb`.`Admin` (`Admin_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `FK_Doctor_Hash_User_ID_idx` ON `mydb`.`Doctor` (`Doctor_UserID` ASC) ;

CREATE INDEX `FK_Doctor_Admin_idx` ON `mydb`.`Doctor` (`Admin_ID` ASC) ;


-- -----------------------------------------------------
-- Table `mydb`.`Medical_Record`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Medical_Record` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Medical_Record` (
  `Record_ID` INT NOT NULL AUTO_INCREMENT ,
  `Patient_SSN` INT NULL ,
  `Patient_Record` VARCHAR(500) NULL ,
  `Date_Created` DATETIME NULL ,
  `Last_Updated_Admin_ID` INT NULL ,
  `Last_Updated_Date` DATETIME NULL ,
  `Doctor's Note` VARCHAR(200) NULL ,
  PRIMARY KEY (`Record_ID`) ,
  CONSTRAINT `FK_Record_Patient`
    FOREIGN KEY (`Patient_SSN` )
    REFERENCES `mydb`.`Patient` (`SSN` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Record_Admin`
    FOREIGN KEY (`Last_Updated_Admin_ID` )
    REFERENCES `mydb`.`Admin` (`Admin_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `FK_Record_Patient_idx` ON `mydb`.`Medical_Record` (`Patient_SSN` ASC) ;

CREATE INDEX `FK_Record_Admin_idx` ON `mydb`.`Medical_Record` (`Last_Updated_Admin_ID` ASC) ;


-- -----------------------------------------------------
-- Table `mydb`.`Prescription`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Prescription` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Prescription` (
  `Prescription_ID` INT NOT NULL ,
  `Patient_SSN` INT NULL ,
  `Doctor_Lic_No` INT NULL ,
  `Patient_Name` VARCHAR(45) NULL ,
  `Patient_DOB` DATETIME NULL ,
  `Doctor_Name` VARCHAR(45) NULL ,
  `Drug_Name` VARCHAR(45) NULL ,
  `Dose_Details` VARCHAR(200) NULL ,
  PRIMARY KEY (`Prescription_ID`) ,
  CONSTRAINT `FK_Prescription_Patient`
    FOREIGN KEY (`Patient_SSN` )
    REFERENCES `mydb`.`Patient` (`SSN` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Prescription_Doctor`
    FOREIGN KEY (`Doctor_Lic_No` )
    REFERENCES `mydb`.`Doctor` (`Doctor_Lic_No` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `FK_Prescription_Patient_idx` ON `mydb`.`Prescription` (`Patient_SSN` ASC) ;

CREATE INDEX `FK_Prescription_Doctor_idx` ON `mydb`.`Prescription` (`Doctor_Lic_No` ASC) ;


-- -----------------------------------------------------
-- Table `mydb`.`Ticket`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`Ticket` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`Ticket` (
  `Ticket_ID` INT NOT NULL AUTO_INCREMENT ,
  `Patient_SSN` INT NULL ,
  `Admin_ID` INT NULL ,
  `Record_ID` INT NULL ,
  `Message` VARCHAR(500) NULL ,
  `Status` VARCHAR(45) NULL ,
  `Date` DATETIME NULL ,
  PRIMARY KEY (`Ticket_ID`) ,
  CONSTRAINT `FK_Ticket_Patient`
    FOREIGN KEY (`Patient_SSN` )
    REFERENCES `mydb`.`Patient` (`SSN` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Ticket_Admin`
    FOREIGN KEY (`Admin_ID` )
    REFERENCES `mydb`.`Admin` (`Admin_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_Ticket_Record`
    FOREIGN KEY (`Record_ID` )
    REFERENCES `mydb`.`Medical_Record` (`Record_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `FK_Ticket_Admin_idx` ON `mydb`.`Ticket` (`Admin_ID` ASC) ;

CREATE INDEX `FK_Ticket_Record_idx` ON `mydb`.`Ticket` (`Record_ID` ASC) ;

CREATE INDEX `FK_Ticket_Patient_idx` ON `mydb`.`Ticket` (`Patient_SSN` ASC) ;


-- -----------------------------------------------------
-- Table `mydb`.`XRef_Pat_Doc`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`XRef_Pat_Doc` ;

CREATE  TABLE IF NOT EXISTS `mydb`.`XRef_Pat_Doc` (
  `Patient_SSN` INT NOT NULL ,
  `Doctor_Lic_No` INT NOT NULL ,
  CONSTRAINT `FK_XRef_Patient`
    FOREIGN KEY (`Patient_SSN` )
    REFERENCES `mydb`.`Patient` (`SSN` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_XRef_Doctor`
    FOREIGN KEY (`Doctor_Lic_No` )
    REFERENCES `mydb`.`Doctor` (`Doctor_Lic_No` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `FK_XRef_Patient_idx` ON `mydb`.`XRef_Pat_Doc` (`Patient_SSN` ASC) ;

CREATE INDEX `FK_XRef_Doctor_idx` ON `mydb`.`XRef_Pat_Doc` (`Doctor_Lic_No` ASC) ;

USE `mydb` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
