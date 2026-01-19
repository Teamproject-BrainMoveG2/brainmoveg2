CREATE DATABASE  IF NOT EXISTS `Brainmove` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `Brainmove`;
-- MySQL dump 10.13  Distrib 5.7.44, for Win64 (x86_64)
--
-- Host: localhost    Database: Brainmove
-- ------------------------------------------------------
-- Server version	11.8.3-MariaDB-0+deb13u1 from Debian

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `moeilijkheid`
--

DROP TABLE IF EXISTS `moeilijkheid`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `moeilijkheid` (
  `moeilijkheid_id` int(11) NOT NULL AUTO_INCREMENT,
  `naam` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`moeilijkheid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moeilijkheid`
--

LOCK TABLES `moeilijkheid` WRITE;
/*!40000 ALTER TABLE `moeilijkheid` DISABLE KEYS */;
/*!40000 ALTER TABLE `moeilijkheid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `potje`
--

DROP TABLE IF EXISTS `potje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `potje` (
  `potje_id` int(11) NOT NULL AUTO_INCREMENT,
  `kleur` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`potje_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `potje`
--

LOCK TABLES `potje` WRITE;
/*!40000 ALTER TABLE `potje` DISABLE KEYS */;
/*!40000 ALTER TABLE `potje` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spelmodus`
--

DROP TABLE IF EXISTS `spelmodus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spelmodus` (
  `spelmodus_id` int(11) NOT NULL AUTO_INCREMENT,
  `naam` varchar(45) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  `icon` varchar(45) DEFAULT NULL,
  `image` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`spelmodus_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spelmodus`
--

LOCK TABLES `spelmodus` WRITE;
/*!40000 ALTER TABLE `spelmodus` DISABLE KEYS */;
INSERT INTO `spelmodus` VALUES (1,'Speed Reflex','Raak de juiste kleur aan binnen het tijdslimiet','clock','brain_between_cones'),(2,'Memory Game','Onthoudt het juiste patroon van de kleuren','brain','brain_between_cones'),(3,'Calm Colors','Raak zo snel mogelijk de kleuren aan, er is geen tijdslimiet','target','brain_between_cones');
/*!40000 ALTER TABLE `spelmodus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spelmodus_handleiding_stappen`
--

DROP TABLE IF EXISTS `spelmodus_handleiding_stappen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spelmodus_handleiding_stappen` (
  `spelmodus_handleiding_stappen_id` int(11) NOT NULL,
  `spelmodus_id` int(11) DEFAULT NULL,
  `text` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`spelmodus_handleiding_stappen_id`),
  KEY `fk_spelmodus_handleiding_stappen_spelmodus_idx` (`spelmodus_id`),
  CONSTRAINT `fk_spelmodus_handleiding_stappen_spelmodus` FOREIGN KEY (`spelmodus_id`) REFERENCES `spelmodus` (`spelmodus_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spelmodus_handleiding_stappen`
--

LOCK TABLES `spelmodus_handleiding_stappen` WRITE;
/*!40000 ALTER TABLE `spelmodus_handleiding_stappen` DISABLE KEYS */;
INSERT INTO `spelmodus_handleiding_stappen` VALUES (1,1,'Een kleur verschijnt op je scherm'),(2,1,'Tik zo snel mogelijk het bijbehorende potje aan'),(3,1,'De tijd wordt steeds korter - hoe lang houd je vol?');
/*!40000 ALTER TABLE `spelmodus_handleiding_stappen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spelronde`
--

DROP TABLE IF EXISTS `spelronde`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spelronde` (
  `spelronde_id` int(11) NOT NULL AUTO_INCREMENT,
  `spelsessie_id` int(11) DEFAULT NULL,
  `ronde_nummer` int(11) DEFAULT NULL,
  `reactietijd_ms` int(11) DEFAULT NULL,
  `potje_id` int(11) DEFAULT NULL,
  `uitkomst` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`spelronde_id`),
  KEY `spelsessie_id_idx` (`spelsessie_id`),
  KEY `potje_id_idx` (`potje_id`),
  CONSTRAINT `potje_id` FOREIGN KEY (`potje_id`) REFERENCES `potje` (`potje_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `spelsessie_id` FOREIGN KEY (`spelsessie_id`) REFERENCES `spelsessie` (`spelsessie_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spelronde`
--

LOCK TABLES `spelronde` WRITE;
/*!40000 ALTER TABLE `spelronde` DISABLE KEYS */;
/*!40000 ALTER TABLE `spelronde` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spelsessie`
--

DROP TABLE IF EXISTS `spelsessie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spelsessie` (
  `spelsessie_id` int(11) NOT NULL AUTO_INCREMENT,
  `gebruikersnaam` varchar(45) DEFAULT NULL,
  `spelmodus_id` int(11) DEFAULT NULL,
  `moeilijkheid_id` int(11) DEFAULT NULL,
  `gestart_op` datetime DEFAULT NULL,
  `geëindigd_op` datetime DEFAULT NULL,
  PRIMARY KEY (`spelsessie_id`),
  KEY `spelmodus_id_idx` (`spelmodus_id`),
  KEY `moeilijkheid_id_idx` (`moeilijkheid_id`),
  CONSTRAINT `moeilijkheid_id` FOREIGN KEY (`moeilijkheid_id`) REFERENCES `moeilijkheid` (`moeilijkheid_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `spelmodus_id` FOREIGN KEY (`spelmodus_id`) REFERENCES `spelmodus` (`spelmodus_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spelsessie`
--

LOCK TABLES `spelsessie` WRITE;
/*!40000 ALTER TABLE `spelsessie` DISABLE KEYS */;
/*!40000 ALTER TABLE `spelsessie` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-19  9:43:23
