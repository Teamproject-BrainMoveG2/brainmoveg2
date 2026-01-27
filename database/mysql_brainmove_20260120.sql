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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moeilijkheid`
--

LOCK TABLES `moeilijkheid` WRITE;
/*!40000 ALTER TABLE `moeilijkheid` DISABLE KEYS */;
INSERT INTO `moeilijkheid` VALUES (1,'Relaxed'),(2,'Challenging'),(3,'Intense');
/*!40000 ALTER TABLE `moeilijkheid` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `niveaus`
--

DROP TABLE IF EXISTS `niveaus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `niveaus` (
  `niveau_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`niveau_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveaus`
--

LOCK TABLES `niveaus` WRITE;
/*!40000 ALTER TABLE `niveaus` DISABLE KEYS */;
INSERT INTO `niveaus` VALUES (1,'Beginner'),(2,'Amateur'),(3,'Intermediate'),(4,'Pro'),(5,'Champion');
/*!40000 ALTER TABLE `niveaus` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `potje`
--

LOCK TABLES `potje` WRITE;
/*!40000 ALTER TABLE `potje` DISABLE KEYS */;
INSERT INTO `potje` VALUES (1,'red'),(2,'blue'),(3,'green'),(4,'yellow');
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
  `image` varchar(45) DEFAULT NULL,
  `icon` varchar(45) DEFAULT NULL,
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
  `handleiding_id` int(11) NOT NULL AUTO_INCREMENT,
  `spelmodus_id` int(11) NOT NULL,
  `description` varchar(250) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  PRIMARY KEY (`handleiding_id`),
  KEY `fk_spelmodus_handleiding_stappen_spelmodus_idx` (`spelmodus_id`),
  CONSTRAINT `fk_spelmodus_handleiding_stappen_spelmodus` FOREIGN KEY (`spelmodus_id`) REFERENCES `spelmodus` (`spelmodus_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spelmodus_handleiding_stappen`
--

LOCK TABLES `spelmodus_handleiding_stappen` WRITE;
/*!40000 ALTER TABLE `spelmodus_handleiding_stappen` DISABLE KEYS */;
INSERT INTO `spelmodus_handleiding_stappen` VALUES (1,1,'Een kleur verschijnt op je scherm',1),(2,1,'Tik zo snel mogelijk het bijbehorende potje aan',2),(3,1,'De tijd wordt steeds korter - hoe lang houd je vol?',3),(4,2,'tutorial 1',1),(5,2,'tutorial 2',2),(6,2,'tutorial 3',3);
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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spelronde`
--

LOCK TABLES `spelronde` WRITE;
/*!40000 ALTER TABLE `spelronde` DISABLE KEYS */;
INSERT INTO `spelronde` VALUES (6,7,1,2065,1,'goed'),(7,7,2,1250,1,'goed'),(8,7,3,863,1,'goed'),(9,7,4,710,1,'goed'),(10,7,5,1566,1,'goed'),(11,8,1,2443,1,'goed'),(12,8,2,2560,1,'goed'),(13,8,3,946,1,'goed'),(14,8,4,1958,1,'goed'),(15,8,5,868,1,'goed'),(16,9,1,2454,1,'fout'),(17,9,2,1171,1,'fout'),(18,9,3,1015,1,'goed'),(19,9,4,1214,1,'fout'),(20,9,5,852,1,'goed'),(21,10,1,2543,1,'goed'),(22,10,2,1455,1,'goed'),(23,10,3,1116,1,'goed'),(24,10,4,2175,1,'fout'),(25,10,5,1040,1,'fout'),(26,11,1,68,3,'fout'),(27,11,2,1130,3,'fout'),(28,11,3,181,1,'fout'),(29,11,4,74,3,'fout'),(30,11,5,1160,1,'goed'),(31,17,1,2145,1,'goed'),(32,17,2,1095,1,'goed'),(33,17,3,661,1,'goed'),(34,17,4,1418,1,'goed'),(35,17,5,939,1,'goed');
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
  `username` varchar(45) DEFAULT NULL,
  `spelmodus_id` int(11) DEFAULT NULL,
  `moeilijkheid_id` int(11) DEFAULT NULL,
  `gestart_op` datetime DEFAULT NULL,
  `geëindigd_op` datetime DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  PRIMARY KEY (`spelsessie_id`),
  KEY `spelmodus_id_idx` (`spelmodus_id`),
  KEY `moeilijkheid_id_idx` (`moeilijkheid_id`),
  CONSTRAINT `moeilijkheid_id` FOREIGN KEY (`moeilijkheid_id`) REFERENCES `moeilijkheid` (`moeilijkheid_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `spelmodus_id` FOREIGN KEY (`spelmodus_id`) REFERENCES `spelmodus` (`spelmodus_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spelsessie`
--

LOCK TABLES `spelsessie` WRITE;
/*!40000 ALTER TABLE `spelsessie` DISABLE KEYS */;
INSERT INTO `spelsessie` VALUES (7,'maarten',1,1,'2026-01-19 13:07:11','2026-01-19 13:07:22',1144),(8,'maarten2',1,1,'2026-01-19 13:07:40','2026-01-19 13:07:53',947),(9,'vince',1,1,'2026-01-19 13:09:30','2026-01-19 13:09:41',876),(10,'vince2',1,1,'2026-01-19 13:15:53','2026-01-19 13:16:06',816),(11,'vinceNew',1,1,'2026-01-19 14:20:09','2026-01-19 14:20:15',1917),(12,'vinceNew',1,1,'2026-01-19 14:40:36','2026-01-19 14:40:56',551),(13,'vinceNew',1,1,'2026-01-19 14:42:38','2026-01-19 14:42:56',484),(14,'vinceNew',1,1,'2026-01-19 14:44:51','2026-01-19 14:45:00',1063),(15,'vinceNew',1,1,'2026-01-19 14:48:03',NULL,NULL),(16,'vinceNew',1,1,'2026-01-19 14:48:07','2026-01-19 14:48:19',1031),(17,'vinceNew',1,1,'2026-01-19 14:49:02','2026-01-19 14:49:12',1167);
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

-- Dump completed on 2026-01-20  9:24:40
