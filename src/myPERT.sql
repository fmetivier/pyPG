-- MariaDB dump 10.19  Distrib 10.5.18-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: myPERT
-- ------------------------------------------------------
-- Server version	10.5.18-MariaDB-0+deb11u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `correl`
--

DROP TABLE IF EXISTS `correl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `correl` (
  `mid_target` int(11) NOT NULL,
  `mid_depends` int(11) NOT NULL,
  `pid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `correl`
--

LOCK TABLES `correl` WRITE;
/*!40000 ALTER TABLE `correl` DISABLE KEYS */;
INSERT INTO `correl` VALUES (6,2,1),(5,4,1),(6,5,1),(7,6,1),(10,9,1),(11,10,1),(12,1,1),(13,12,1),(9,8,1),(4,1,1),(14,13,1),(8,1,1),(10,2,1);
/*!40000 ALTER TABLE `correl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deliverables`
--

DROP TABLE IF EXISTS `deliverables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deliverables` (
  `did` varchar(10) DEFAULT NULL,
  `dname` varchar(55) DEFAULT NULL,
  `pid` int(11) DEFAULT NULL,
  `wid` int(11) DEFAULT NULL,
  `tid` int(11) DEFAULT NULL,
  `dd` int(11) DEFAULT NULL,
  `mid` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deliverables`
--

LOCK TABLES `deliverables` WRITE;
/*!40000 ALTER TABLE `deliverables` DISABLE KEYS */;
INSERT INTO `deliverables` VALUES ('1.1','Partnership agreement',1,1,1,3,1),('1.2','Project management handbook',1,1,2,6,0),('1.3','Quality Assurance plan',1,1,2,9,3),('1.4','Dissemination plan',1,1,4,6,0),('1.5','Web site',1,1,4,6,2),('1.6','Dataverse',1,1,4,3,0),('1.7','Steering committee meeting',1,1,3,4,0),('1.8','Steering committee meeting',1,1,3,8,0),('1.9','Steering committee meeting',1,1,3,12,0),('1.10','Steering committee meeting',1,1,3,16,0),('1.11','Steering committee meeting',1,1,3,20,0),('1.12','Steering committee meeting',1,1,3,24,0),('1.13','Steering committee meeting',1,1,3,28,0),('1.14','Steering committee meeting',1,1,3,32,0),('1.15','Ethics committee meeting',1,1,5,6,0),('1.16','Ethics committee meeting',1,1,5,12,0),('1.17','Ethics committee meeting',1,1,5,18,0),('1.18','Ethics committee meeting',1,1,5,24,0),('1.19','Ethics committee meeting',1,1,5,30,0),('2.3','Training session of academic staff and vacatories in hy',1,2,3,18,0),('2.2','New or updated Module in hydrology',1,2,4,33,8),('2.1','Lab room in water chemistry and biology',1,2,1,12,0),('2.4','Training session of academic staff and vacatories in wa',1,2,3,27,6),('2.5','Training session of academic staff and vacatories in mi',1,2,3,27,6),('2.6','New or updated Module in water chemistry',1,2,4,33,8),('2.7','New or update Module in microbiology',1,2,4,33,8),('2.8','Online course material',1,2,3,27,0),('3.1','Computer room',1,3,1,12,0),('3.2','Training for academic staff and vacatories',1,3,3,21,0),('3.3','Module creation',1,3,4,27,0),('3.4','Online course material',1,3,3,21,0),('3.1','Training for academic staff and vacatories',1,4,3,30,0),('3.2','Module delivered',1,4,4,33,0);
/*!40000 ALTER TABLE `deliverables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `milestones`
--

DROP TABLE IF EXISTS `milestones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `milestones` (
  `mid` int(11) NOT NULL AUTO_INCREMENT,
  `mname` varchar(255) NOT NULL,
  `t` int(11) NOT NULL,
  `min_t` int(11) DEFAULT NULL,
  `max_t` int(11) DEFAULT NULL,
  `wid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `tid` int(11) NOT NULL,
  PRIMARY KEY (`mid`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `milestones`
--

LOCK TABLES `milestones` WRITE;
/*!40000 ALTER TABLE `milestones` DISABLE KEYS */;
INSERT INTO `milestones` VALUES (1,'Agreement',3,1,6,1,1,1),(2,'web and dataverse',6,3,9,1,1,4),(3,'Quality Assurance',9,4,14,1,1,2),(4,'Laboratory material Delivered',12,8,14,2,1,1),(5,'Laboratory ready',18,16,20,2,1,1),(6,'Trainings in WASH/IWRM delivered',27,20,28,2,1,3),(7,'Modules delivered',33,30,36,2,1,4),(8,'Computers Delivered',6,3,9,3,1,1),(9,'Computer room ready',12,9,15,3,1,1),(10,'Trainings in DATA/GIS delivered',21,15,21,3,1,3),(11,'Modules delivered',27,24,32,3,1,4),(12,'Camp stewardship organized',24,22,26,4,1,2),(13,'Onsite training delivered',30,28,32,4,1,3),(14,'First Camp organized',33,31,35,4,1,4);
/*!40000 ALTER TABLE `milestones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `projects` (
  `pid` int(11) NOT NULL AUTO_INCREMENT,
  `pname` varchar(255) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'SHEWAM','SHEWAM=SAFE-M en anglais avec UCLouvain, temps en mois');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tasks` (
  `tid` int(11) NOT NULL,
  `tname` varchar(255) DEFAULT NULL,
  `wid` int(11) NOT NULL,
  `pid` int(11) NOT NULL,
  `sdate` int(11) NOT NULL,
  `edate` int(11) NOT NULL,
  PRIMARY KEY (`tid`,`wid`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` VALUES (1,'Write Agreements',1,1,1,3),(1,'Equip lab rooms',2,1,3,18),(1,'Equip computer rooms',3,1,3,12),(1,'Organize syllabus of field camp',4,1,18,24),(2,'Coordinate',1,1,1,36),(2,'organize practical teaching units',2,1,9,24),(2,'organize teaching units',3,1,7,18),(2,'Stewardship: of field camp',4,1,18,24),(3,'Manage',1,1,1,36),(3,'Form: train faculties and vacatories',2,1,12,27),(3,'Form: organize training sessions',3,1,18,21),(3,'Form faculties and vacatories',4,1,24,30),(4,'Disseminate',1,1,1,36),(4,'Follow: Organize followup sessions and adapt modules and training',2,1,27,33),(4,'Follow: organize follow up sessions',3,1,21,27),(4,'Follow realization of first editions',4,1,30,33),(5,'Beware',1,1,1,36);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wps`
--

DROP TABLE IF EXISTS `wps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wps` (
  `wpid` int(11) NOT NULL,
  `wpname` varchar(255) NOT NULL,
  `pid` int(11) NOT NULL,
  `wpstart` int(11) DEFAULT NULL,
  `wpend` int(11) DEFAULT NULL,
  PRIMARY KEY (`wpid`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wps`
--

LOCK TABLES `wps` WRITE;
/*!40000 ALTER TABLE `wps` DISABLE KEYS */;
INSERT INTO `wps` VALUES (1,'Management',1,1,36),(2,'Hands on learning in WASH/IWRM',1,1,33),(3,'Building the toolbox',1,1,27),(4,'Field camp in the Ankavia Basin',1,18,33);
/*!40000 ALTER TABLE `wps` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-05 18:33:44
