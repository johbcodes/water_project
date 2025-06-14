-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: project_db
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('5c20f220f872');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `constituencies`
--

DROP TABLE IF EXISTS `constituencies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `constituencies` (
  `ConstituencyID` int NOT NULL AUTO_INCREMENT,
  `ConstituencyName` varchar(100) NOT NULL,
  `CountyID` int NOT NULL,
  PRIMARY KEY (`ConstituencyID`),
  KEY `CountyID` (`CountyID`),
  CONSTRAINT `constituencies_ibfk_1` FOREIGN KEY (`CountyID`) REFERENCES `counties` (`CountyID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `constituencies`
--

LOCK TABLES `constituencies` WRITE;
/*!40000 ALTER TABLE `constituencies` DISABLE KEYS */;
INSERT INTO `constituencies` VALUES (1,'Changamwe',1),(2,'Jomvu',1),(3,'Kisauni',1),(4,'Nyali',1),(5,'Likoni',1),(6,'Mvita',1);
/*!40000 ALTER TABLE `constituencies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `counties`
--

DROP TABLE IF EXISTS `counties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `counties` (
  `CountyID` int NOT NULL AUTO_INCREMENT,
  `CountyName` varchar(100) NOT NULL,
  PRIMARY KEY (`CountyID`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `counties`
--

LOCK TABLES `counties` WRITE;
/*!40000 ALTER TABLE `counties` DISABLE KEYS */;
INSERT INTO `counties` VALUES (1,'Mombasa'),(2,'Kwale'),(3,'Kilifi'),(4,'Tana River'),(5,'Lamu'),(6,'Taita-Taveta'),(7,'Garissa'),(8,'Wajir'),(9,'Mandera'),(10,'Marsabit'),(11,'Isiolo'),(12,'Meru'),(13,'Tharaka-Nithi'),(14,'Embu'),(15,'Kitui'),(16,'Machakos'),(17,'Makueni'),(18,'Nyandarua'),(19,'Nyeri'),(20,'Kirinyaga'),(21,'Murang\'a'),(22,'Kiambu'),(23,'Turkana'),(24,'West Pokot'),(25,'Samburu'),(26,'Trans Nzoia'),(27,'Uasin Gishu'),(28,'Elgeyo-Marakwet'),(29,'Nandi'),(30,'Baringo'),(31,'Laikipia'),(32,'Nakuru'),(33,'Narok'),(34,'Kajiado'),(35,'Kericho'),(36,'Bomet'),(37,'Kakamega'),(38,'Vihiga'),(39,'Bungoma'),(40,'Busia'),(41,'Siaya'),(42,'Kisumu'),(43,'Homa Bay'),(44,'Migori'),(45,'Kisii'),(46,'Nyamira'),(47,'Nairobi');
/*!40000 ALTER TABLE `counties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funding`
--

DROP TABLE IF EXISTS `funding`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funding` (
  `FundingID` int NOT NULL AUTO_INCREMENT,
  `ProjectID` int DEFAULT NULL,
  `SourceOfFunds` varchar(255) DEFAULT NULL,
  `GoK_KES` decimal(15,2) DEFAULT NULL,
  `AFD_KES` decimal(15,2) DEFAULT NULL,
  `ADB_KES` decimal(15,2) DEFAULT NULL,
  `EU_KES` decimal(15,2) DEFAULT NULL,
  `EIB_KES` decimal(15,2) DEFAULT NULL,
  `KfW_KES` decimal(15,2) DEFAULT NULL,
  `Belgium_KES` decimal(15,2) DEFAULT NULL,
  `Italy_KES` decimal(15,2) DEFAULT NULL,
  `Netherlands_KES` decimal(15,2) DEFAULT NULL,
  `EXIMBank_KES` decimal(15,2) DEFAULT NULL,
  `WB_KES` decimal(15,2) DEFAULT NULL,
  `BADEA_KES` decimal(15,2) DEFAULT NULL,
  `JICA_KES` decimal(15,2) DEFAULT NULL,
  `KOREA_KES` decimal(15,2) DEFAULT NULL,
  `OFID_KES` decimal(15,2) DEFAULT NULL,
  `SAUDIARABIA_KES` decimal(15,2) DEFAULT NULL,
  `DANIDA_KES` decimal(15,2) DEFAULT NULL,
  PRIMARY KEY (`FundingID`),
  KEY `ProjectID` (`ProjectID`),
  CONSTRAINT `funding_ibfk_1` FOREIGN KEY (`ProjectID`) REFERENCES `projects` (`ProjectID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funding`
--

LOCK TABLES `funding` WRITE;
/*!40000 ALTER TABLE `funding` DISABLE KEYS */;
/*!40000 ALTER TABLE `funding` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `ProjectID` int NOT NULL AUTO_INCREMENT,
  `ImplementingAgency` varchar(255) DEFAULT NULL,
  `Program` varchar(255) DEFAULT NULL,
  `ProjectName` varchar(255) DEFAULT NULL,
  `CountyID` int DEFAULT NULL,
  `ConstituencyID` int DEFAULT NULL,
  `WardID` int DEFAULT NULL,
  `GPSCoordinates` varchar(50) DEFAULT NULL,
  `ProjectType` varchar(100) DEFAULT NULL,
  `ProjectLocation` enum('Rural','Urban') DEFAULT NULL,
  `ScopeOfWorks` text,
  `IntakeCapacity_m3` decimal(10,2) DEFAULT NULL,
  `TreatmentCapacity_m3` decimal(10,2) DEFAULT NULL,
  `StorageCapacity_m3` decimal(10,2) DEFAULT NULL,
  `TreatedWaterMains_km` decimal(10,2) DEFAULT NULL,
  `DistributionLines_km` decimal(10,2) DEFAULT NULL,
  `NumberOfWaterKiosks` int DEFAULT NULL,
  `NumberOfConnections` int DEFAULT NULL,
  `WastewaterCapacity_m3` decimal(10,2) DEFAULT NULL,
  `TargetAreas` varchar(255) DEFAULT NULL,
  `TargetBeneficiaries_Households` int DEFAULT NULL,
  `TargetBeneficiaries_Population` int DEFAULT NULL,
  `Contractor` varchar(255) DEFAULT NULL,
  `Consultant` varchar(255) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `PlannedEndDate` date DEFAULT NULL,
  `ActualEndDate` date DEFAULT NULL,
  `ProgressPercentage` decimal(5,2) DEFAULT NULL,
  `TotalContractSum_KES` decimal(15,2) DEFAULT NULL,
  `CumulativeExpenditure_KES` decimal(15,2) DEFAULT NULL,
  `OutstandingCost_KES` decimal(15,2) DEFAULT NULL,
  `ExchequerReleases_KES` decimal(15,2) DEFAULT NULL,
  `SumOfPendingBills_KES` decimal(15,2) DEFAULT NULL,
  `ApprovedBudgetFY2021_22` decimal(15,2) DEFAULT NULL,
  `ApprovedBudgetFY2021_23` decimal(15,2) DEFAULT NULL,
  `ApprovedBudgetFY2022_23` decimal(15,2) DEFAULT NULL,
  `ApprovedBudgetFY2022_24` decimal(15,2) DEFAULT NULL,
  `ApprovedBudgetFY2023_24` decimal(15,2) DEFAULT NULL,
  `ApprovedBudgetFY2023_25` decimal(15,2) DEFAULT NULL,
  `BudgetAllocationFY2024_25` decimal(15,2) DEFAULT NULL,
  `BudgetAllocationFY2024_26` decimal(15,2) DEFAULT NULL,
  `ImpactsOfTheProject` text,
  `KeyChallenges` text,
  `Remarks` text,
  PRIMARY KEY (`ProjectID`),
  KEY `ConstituencyID` (`ConstituencyID`),
  KEY `CountyID` (`CountyID`),
  KEY `WardID` (`WardID`),
  CONSTRAINT `projects_ibfk_1` FOREIGN KEY (`ConstituencyID`) REFERENCES `constituencies` (`ConstituencyID`),
  CONSTRAINT `projects_ibfk_2` FOREIGN KEY (`CountyID`) REFERENCES `counties` (`CountyID`),
  CONSTRAINT `projects_ibfk_3` FOREIGN KEY (`WardID`) REFERENCES `wards` (`WardID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (1,'Water Services Board','Sanitation','Sewerage Water Project	',1,1,1,'-4.050, 39.667','borehole','Rural','ghkjjlklk.',9.00,9.00,78.00,525.00,96.00,455,55,556.00,'5546',54465,55646,'546','5665','2025-02-12','2025-02-19','2025-02-27',78.00,54796563.00,656555.00,5875.00,545.00,587452.00,54525.00,54875.00,8754258.00,8754265.00,87452452.00,58425842.00,564999.00,7455.00,'igkhlj;k\'','guiholjp;k','Good project'),(2,'Mins water','water supply','roads ',1,3,10,'-4.050, 39.667','distribution_network','Urban','yes nice ',52.00,565.00,454.00,455.00,54.00,45,454,85.00,'454',5656,1545,'ndege','casper','2025-02-12','2025-02-19','2025-02-28',52.00,254616.00,56236.00,456365.00,4556.00,655.00,546.00,546565.00,56566.00,54656.00,45465.00,545456.00,45665.00,54545.00,'ygjhjklk ikujnk','jgujhbikjnkl','gvbujk7fu'),(3,'Thwake ','Thwake multipurpose Dam','Thwake Dam Phase 1',1,1,1,'-4.050, 39.667','storage_tank','Urban','To Build a Good dam that hold alot of water and serve many people At once ',34.00,35.00,3000.00,489.00,23.00,45,90,90.00,'56',67,67,'Joseph Kinyau','Watson ondike','2025-02-13','2025-02-25','2025-02-18',89.00,7878980.00,65532352.00,254521.00,532806.00,60000525.00,8693323.00,9865623.00,85210582.00,235869865.00,2358256.00,25859865.00,2855204.00,535596856.00,'To increase the volume of water capacity and supply enough water to the community','Starting the project need a lot of funding ','The project will be a lifetime to the community and all other areas within the county.'),(4,'Athi River water works','Water supply','Water Supply and Sanitation',1,4,17,'-5.050, 49.667','water_treatment','Rural','The project need to be completed before the end of the year and water to treated well for human conservation.',78.00,98.00,87990.00,98.00,567.00,543,234,4657878.00,'788689',576789,3456577,'samuel ','Ndirangu','2025-03-03','2025-03-27','2025-03-26',98.00,6659665.00,556666.00,6622626.00,626396.00,3656852.00,365516.00,5698659.00,656526.00,5636985.00,56356.00,3855.00,5522252.00,85262.00,'To provide clean water and best sanitation','Costly to acquire chemicals for treating water.','The project is almost done and need some small materials to be completed.');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(100) NOT NULL,
  `Password` varchar(512) DEFAULT NULL,
  `Role` enum('Admin','Manager','Viewer') NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','scrypt:32768:8:1$g0pBiFHfZETBWCXW$0de36ac25f2e551d846b6b5b53d02f73cfe9eeb0b7e2e5da5929c5acfbc7b56d3b58e25a4c7a63d275efde69953c029e02f98cb581f3740166cfa2becefdc41c','Admin'),(2,'naurimwei','scrypt:32768:8:1$qlZFugMwarVTU7cQ$c0827c94dbe39b5b8d0ed96453e9cfa432cf524d496ec0855fe1b909be744c527b57994135d7722149ebb7729c7f027e46a142a5dbb18367ceab0edb15d35605','Manager'),(5,'Anderson Kigen','87654321','Viewer'),(6,'Dan','scrypt:32768:8:1$a6uwQ9kAqoiobtGO$c4563a6600b891033a4d4faa0605021615f2f1309c795962a765c0d545b9997e69494cf6161af9467fd746ef84d1be5d6241c400f005304112c67e65a63782e7','Viewer'),(7,'cas','scrypt:32768:8:1$MmozERNJcqKyW6IW$de24310d1cb02f6a38519c7e68a568a159ca22903438c96a5d50bd9d95df5b367b6ddd202dba3713dd77fa0d509549685a2f611fc7da0bdaf6bdf08cb6ebdac6','Viewer');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wards`
--

DROP TABLE IF EXISTS `wards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wards` (
  `WardID` int NOT NULL AUTO_INCREMENT,
  `WardName` varchar(100) NOT NULL,
  `ConstituencyID` int NOT NULL,
  PRIMARY KEY (`WardID`),
  KEY `ConstituencyID` (`ConstituencyID`),
  CONSTRAINT `wards_ibfk_1` FOREIGN KEY (`ConstituencyID`) REFERENCES `constituencies` (`ConstituencyID`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wards`
--

LOCK TABLES `wards` WRITE;
/*!40000 ALTER TABLE `wards` DISABLE KEYS */;
INSERT INTO `wards` VALUES (1,'Port Reitz',1),(2,'Kipevu',1),(3,'Airport',1),(4,'Miritini',1),(5,'Chaani',1),(6,'Jomvu Kuu',2),(7,'Mikindani',2),(8,'Mjambere',2),(9,'Mtongwe',3),(10,'Shika Adabu',3),(11,'Bofu',3),(12,'Likoni',3),(13,'Timbwani',3),(14,'Frere Town',4),(15,'Ziwa La Ng\'ombe',4),(16,'Mkomani',4),(17,'Kongowea',4),(18,'Kadzandani',4),(19,'Mtongwe',5),(20,'Shika Adabu',5),(21,'Bofu',5),(22,'Likoni',5),(23,'Timbwani',5),(24,'Mji Wa Kale',6),(25,'Tudor',6),(26,'Tononoka',6),(27,'Shimanzi',6),(28,'Majengo',6);
/*!40000 ALTER TABLE `wards` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-16 22:25:36
