-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: bajaj
-- ------------------------------------------------------
-- Server version	5.5.44-0ubuntu0.14.04.1

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Admins'),(2,'AreaSalesManagers'),(3,'AreaServiceManagers'),(4,'AreaSparesManagers'),(5,'AuthorisedServiceCenters'),(6,'BrandManagers'),(7,'CircleHeads'),(42,'CountryDistributors'),(8,'CTSAdmins'),(9,'CxoAdmins'),(11,'DealerAdmins'),(12,'Dealers'),(10,'DependentAuthorisedServiceCenters'),(14,'DisitrbutorSalesReps'),(13,'Distributors'),(15,'DistributorStaffs'),(27,'EscalationAuthority'),(16,'FscAdmins'),(17,'FscSuperAdmins'),(20,'LogisticPartners'),(18,'LoyaltyAdmins'),(19,'LoyaltySuperAdmins'),(43,'MainCountryDealers'),(44,'nationalsalesmanager'),(21,'NationalSparesManagers'),(22,'ReadOnly'),(23,'RedemptionEscalation'),(25,'RedemptionPartners'),(24,'RegionalManagers'),(26,'SdAdmins'),(28,'SdManagers'),(29,'SdOwners'),(30,'SdReadOnly'),(31,'SdSuperAdmins'),(32,'ServiceAdvisors'),(33,'SuperAdmins'),(34,'Supervisors'),(35,'Transporters'),(36,'Users'),(37,'VisualizationAdmins'),(38,'VisualizationStaffs'),(39,'VisualizationUsers'),(40,'WelcomeKitEscalation'),(41,'ZonalServiceManagers');
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=943 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (919,1,7),(920,1,8),(917,1,322),(918,1,323),(921,1,340),(922,1,341),(924,2,494),(923,2,1670),(1,4,484),(2,4,485),(3,4,486),(7,4,493),(8,4,494),(9,4,495),(4,4,499),(5,4,500),(6,4,501),(11,4,503),(13,4,506),(12,4,509),(10,4,512),(896,13,7),(897,13,8),(898,13,9),(910,13,322),(907,13,323),(900,13,487),(906,13,488),(908,13,489),(899,13,490),(911,13,491),(901,13,492),(902,13,493),(903,13,494),(904,13,495),(909,13,503),(892,13,1666),(893,13,1667),(894,13,1668),(895,13,1670),(905,13,2384),(771,15,7),(772,15,8),(773,15,9),(768,15,322),(769,15,323),(770,15,324),(774,15,490),(775,15,491),(776,15,492),(777,15,493),(778,15,494),(14,21,484),(15,21,485),(16,21,486),(20,21,493),(21,21,494),(22,21,495),(17,21,499),(18,21,500),(19,21,501),(24,21,503),(26,21,506),(25,21,509),(23,21,512),(939,44,7),(940,44,8),(937,44,322),(938,44,323),(941,44,340),(942,44,341);
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2734 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add client',8,'add_client'),(23,'Can change client',8,'change_client'),(24,'Can delete client',8,'delete_client'),(25,'Can add grant',9,'add_grant'),(26,'Can change grant',9,'change_grant'),(27,'Can delete grant',9,'delete_grant'),(28,'Can add access token',10,'add_accesstoken'),(29,'Can change access token',10,'change_accesstoken'),(30,'Can delete access token',10,'delete_accesstoken'),(31,'Can add refresh token',11,'add_refreshtoken'),(32,'Can change refresh token',11,'change_refreshtoken'),(33,'Can delete refresh token',11,'delete_refreshtoken'),(79,'Can add brand product category',27,'add_brandproductcategory'),(80,'Can change brand product category',27,'change_brandproductcategory'),(81,'Can delete brand product category',27,'delete_brandproductcategory'),(82,'Can add user profile',28,'add_userprofile'),(83,'Can change user profile',28,'change_userprofile'),(84,'Can delete user profile',28,'delete_userprofile'),(85,'Can add zonal service manager',29,'add_zonalservicemanager'),(86,'Can change zonal service manager',29,'change_zonalservicemanager'),(87,'Can delete zonal service manager',29,'delete_zonalservicemanager'),(88,'Can add area service manager',30,'add_areaservicemanager'),(89,'Can change area service manager',30,'change_areaservicemanager'),(90,'Can delete area service manager',30,'delete_areaservicemanager'),(91,'Can add dealer',31,'add_dealer'),(92,'Can change dealer',31,'change_dealer'),(93,'Can delete dealer',31,'delete_dealer'),(94,'Can add authorized service center',32,'add_authorizedservicecenter'),(95,'Can change authorized service center',32,'change_authorizedservicecenter'),(96,'Can delete authorized service center',32,'delete_authorizedservicecenter'),(97,'Can add service advisor',33,'add_serviceadvisor'),(98,'Can change service advisor',33,'change_serviceadvisor'),(99,'Can delete service advisor',33,'delete_serviceadvisor'),(100,'Can add brand department',34,'add_branddepartment'),(101,'Can change brand department',34,'change_branddepartment'),(102,'Can delete brand department',34,'delete_branddepartment'),(103,'Can add department sub categories',35,'add_departmentsubcategories'),(104,'Can change department sub categories',35,'change_departmentsubcategories'),(105,'Can delete department sub categories',35,'delete_departmentsubcategories'),(106,'Can add service desk user',36,'add_servicedeskuser'),(107,'Can change service desk user',36,'change_servicedeskuser'),(108,'Can delete service desk user',36,'delete_servicedeskuser'),(109,'Can add feedback',37,'add_feedback'),(110,'Can change feedback',37,'change_feedback'),(111,'Can delete feedback',37,'delete_feedback'),(112,'Can add activity',38,'add_activity'),(113,'Can change activity',38,'change_activity'),(114,'Can delete activity',38,'delete_activity'),(115,'Can add comment',39,'add_comment'),(116,'Can change comment',39,'change_comment'),(117,'Can delete comment',39,'delete_comment'),(118,'Can add feedback event',40,'add_feedbackevent'),(119,'Can change feedback event',40,'change_feedbackevent'),(120,'Can delete feedback event',40,'delete_feedbackevent'),(121,'Can add product type',41,'add_producttype'),(122,'Can change product type',41,'change_producttype'),(123,'Can delete product type',41,'delete_producttype'),(124,'Can add product data',42,'add_productdata'),(125,'Can change product data',42,'change_productdata'),(126,'Can delete product data',42,'delete_productdata'),(127,'Can add coupon data',43,'add_coupondata'),(128,'Can change coupon data',43,'change_coupondata'),(129,'Can delete coupon data',43,'delete_coupondata'),(130,'Can add service advisor coupon relationship',44,'add_serviceadvisorcouponrelationship'),(131,'Can change service advisor coupon relationship',44,'change_serviceadvisorcouponrelationship'),(132,'Can delete service advisor coupon relationship',44,'delete_serviceadvisorcouponrelationship'),(133,'Can add ucn recovery',45,'add_ucnrecovery'),(134,'Can change ucn recovery',45,'change_ucnrecovery'),(135,'Can delete ucn recovery',45,'delete_ucnrecovery'),(136,'Can add old fsc data',46,'add_oldfscdata'),(137,'Can change old fsc data',46,'change_oldfscdata'),(138,'Can delete old fsc data',46,'delete_oldfscdata'),(139,'Can add cdms data',47,'add_cdmsdata'),(140,'Can change cdms data',47,'change_cdmsdata'),(141,'Can delete cdms data',47,'delete_cdmsdata'),(142,'Can add otp token',48,'add_otptoken'),(143,'Can change otp token',48,'change_otptoken'),(144,'Can delete otp token',48,'delete_otptoken'),(145,'Can add message template',49,'add_messagetemplate'),(146,'Can change message template',49,'change_messagetemplate'),(147,'Can delete message template',49,'delete_messagetemplate'),(148,'Can add email template',50,'add_emailtemplate'),(149,'Can change email template',50,'change_emailtemplate'),(150,'Can delete email template',50,'delete_emailtemplate'),(151,'Can add asc temp registration',51,'add_asctempregistration'),(152,'Can change asc temp registration',51,'change_asctempregistration'),(153,'Can delete asc temp registration',51,'delete_asctempregistration'),(154,'Can add sa temp registration',52,'add_satempregistration'),(155,'Can change sa temp registration',52,'change_satempregistration'),(156,'Can delete sa temp registration',52,'delete_satempregistration'),(157,'Can add customer temp registration',53,'add_customertempregistration'),(158,'Can change customer temp registration',53,'change_customertempregistration'),(159,'Can delete customer temp registration',53,'delete_customertempregistration'),(160,'Can add customer update failure',54,'add_customerupdatefailure'),(161,'Can change customer update failure',54,'change_customerupdatefailure'),(162,'Can delete customer update failure',54,'delete_customerupdatefailure'),(163,'Can add customer update history',55,'add_customerupdatehistory'),(164,'Can change customer update history',55,'change_customerupdatehistory'),(165,'Can delete customer update history',55,'delete_customerupdatehistory'),(166,'Can add user preference',56,'add_userpreference'),(167,'Can change user preference',56,'change_userpreference'),(168,'Can delete user preference',56,'delete_userpreference'),(169,'Can add sms log',57,'add_smslog'),(170,'Can change sms log',57,'change_smslog'),(171,'Can delete sms log',57,'delete_smslog'),(172,'Can add email log',58,'add_emaillog'),(173,'Can change email log',58,'change_emaillog'),(174,'Can delete email log',58,'delete_emaillog'),(175,'Can add data feed log',59,'add_datafeedlog'),(176,'Can change data feed log',59,'change_datafeedlog'),(177,'Can delete data feed log',59,'delete_datafeedlog'),(178,'Can add feed failure log',60,'add_feedfailurelog'),(179,'Can change feed failure log',60,'change_feedfailurelog'),(180,'Can delete feed failure log',60,'delete_feedfailurelog'),(181,'Can add vin sync feed log',61,'add_vinsyncfeedlog'),(182,'Can change vin sync feed log',61,'change_vinsyncfeedlog'),(183,'Can delete vin sync feed log',61,'delete_vinsyncfeedlog'),(184,'Can add audit log',62,'add_auditlog'),(185,'Can change audit log',62,'change_auditlog'),(186,'Can delete audit log',62,'delete_auditlog'),(187,'Can add sla',63,'add_sla'),(188,'Can change sla',63,'change_sla'),(189,'Can delete sla',63,'delete_sla'),(190,'Can add service type',64,'add_servicetype'),(191,'Can change service type',64,'change_servicetype'),(192,'Can delete service type',64,'delete_servicetype'),(193,'Can add service',65,'add_service'),(194,'Can change service',65,'change_service'),(195,'Can delete service',65,'delete_service'),(196,'Can add constant',66,'add_constant'),(197,'Can change constant',66,'change_constant'),(198,'Can delete constant',66,'delete_constant'),(199,'Can add date dimension',67,'add_datedimension'),(200,'Can change date dimension',67,'change_datedimension'),(201,'Can delete date dimension',67,'delete_datedimension'),(202,'Can add coupon fact',68,'add_couponfact'),(203,'Can change coupon fact',68,'change_couponfact'),(204,'Can delete coupon fact',68,'delete_couponfact'),(205,'Can add transporter',69,'add_transporter'),(206,'Can change transporter',69,'change_transporter'),(207,'Can delete transporter',69,'delete_transporter'),(208,'Can add supervisor',70,'add_supervisor'),(209,'Can change supervisor',70,'change_supervisor'),(210,'Can delete supervisor',70,'delete_supervisor'),(211,'Can add container indent',71,'add_containerindent'),(212,'Can change container indent',71,'change_containerindent'),(213,'Can delete container indent',71,'delete_containerindent'),(214,'Can add container lr',72,'add_containerlr'),(215,'Can change container lr',72,'change_containerlr'),(216,'Can delete container lr',72,'delete_containerlr'),(217,'Can add container tracker',73,'add_containertracker'),(218,'Can change container tracker',73,'change_containertracker'),(219,'Can delete container tracker',73,'delete_containertracker'),(220,'Can add territory',74,'add_territory'),(221,'Can change territory',74,'change_territory'),(222,'Can delete territory',74,'delete_territory'),(223,'Can add state',75,'add_state'),(224,'Can change state',75,'change_state'),(225,'Can delete state',75,'delete_state'),(226,'Can add city',76,'add_city'),(227,'Can change city',76,'change_city'),(228,'Can delete city',76,'delete_city'),(229,'Can add national spares manager',77,'add_nationalsparesmanager'),(230,'Can change national spares manager',77,'change_nationalsparesmanager'),(231,'Can delete national spares manager',77,'delete_nationalsparesmanager'),(232,'Can add area spares manager',78,'add_areasparesmanager'),(233,'Can change area spares manager',78,'change_areasparesmanager'),(234,'Can delete area spares manager',78,'delete_areasparesmanager'),(235,'Can add distributor',79,'add_distributor'),(236,'Can change distributor',79,'change_distributor'),(237,'Can delete distributor',79,'delete_distributor'),(238,'Can add distributor staff',80,'add_distributorstaff'),(239,'Can change distributor staff',80,'change_distributorstaff'),(240,'Can delete distributor staff',80,'delete_distributorstaff'),(241,'Can add distributor sales rep',81,'add_distributorsalesrep'),(242,'Can change distributor sales rep',81,'change_distributorsalesrep'),(243,'Can delete distributor sales rep',81,'delete_distributorsalesrep'),(244,'Can add retailer',82,'add_retailer'),(245,'Can change retailer',82,'change_retailer'),(246,'Can delete retailer',82,'delete_retailer'),(247,'Can add dsr wrok allocation',83,'add_dsrwrokallocation'),(248,'Can change dsr wrok allocation',83,'change_dsrwrokallocation'),(249,'Can delete dsr wrok allocation',83,'delete_dsrwrokallocation'),(250,'Can add member',84,'add_member'),(251,'Can change member',84,'change_member'),(252,'Can delete member',84,'delete_member'),(253,'Can add spare part master data',85,'add_sparepartmasterdata'),(254,'Can change spare part master data',85,'change_sparepartmasterdata'),(255,'Can delete spare part master data',85,'delete_sparepartmasterdata'),(256,'Can add spare part upc',86,'add_sparepartupc'),(257,'Can change spare part upc',86,'change_sparepartupc'),(258,'Can delete spare part upc',86,'delete_sparepartupc'),(259,'Can add spare part point',87,'add_sparepartpoint'),(260,'Can change spare part point',87,'change_sparepartpoint'),(261,'Can delete spare part point',87,'delete_sparepartpoint'),(262,'Can add accumulation request',88,'add_accumulationrequest'),(263,'Can change accumulation request',88,'change_accumulationrequest'),(264,'Can delete accumulation request',88,'delete_accumulationrequest'),(265,'Can add partner',89,'add_partner'),(266,'Can change partner',89,'change_partner'),(267,'Can delete partner',89,'delete_partner'),(268,'Can add product catalog',90,'add_productcatalog'),(269,'Can change product catalog',90,'change_productcatalog'),(270,'Can delete product catalog',90,'delete_productcatalog'),(271,'Can add redemption request',91,'add_redemptionrequest'),(272,'Can change redemption request',91,'change_redemptionrequest'),(273,'Can delete redemption request',91,'delete_redemptionrequest'),(274,'Can add welcome kit',92,'add_welcomekit'),(275,'Can change welcome kit',92,'change_welcomekit'),(276,'Can delete welcome kit',92,'delete_welcomekit'),(277,'Can add comment thread',93,'add_commentthread'),(278,'Can change comment thread',93,'change_commentthread'),(279,'Can delete comment thread',93,'delete_commentthread'),(280,'Can add loyalty sla',94,'add_loyaltysla'),(281,'Can change loyalty sla',94,'change_loyaltysla'),(282,'Can delete loyalty sla',94,'delete_loyaltysla'),(283,'Can add discrepant accumulation',95,'add_discrepantaccumulation'),(284,'Can change discrepant accumulation',95,'change_discrepantaccumulation'),(285,'Can delete discrepant accumulation',95,'delete_discrepantaccumulation'),(286,'Can add eco release',96,'add_ecorelease'),(287,'Can change eco release',96,'change_ecorelease'),(288,'Can delete eco release',96,'delete_ecorelease'),(289,'Can add eco implementation',97,'add_ecoimplementation'),(290,'Can change eco implementation',97,'change_ecoimplementation'),(291,'Can delete eco implementation',97,'delete_ecoimplementation'),(292,'Can add brand vertical',98,'add_brandvertical'),(293,'Can change brand vertical',98,'change_brandvertical'),(294,'Can delete brand vertical',98,'delete_brandvertical'),(295,'Can add brand product range',99,'add_brandproductrange'),(296,'Can change brand product range',99,'change_brandproductrange'),(297,'Can delete brand product range',99,'delete_brandproductrange'),(298,'Can add bom header',100,'add_bomheader'),(299,'Can change bom header',100,'change_bomheader'),(300,'Can delete bom header',100,'delete_bomheader'),(301,'Can add bom plate',101,'add_bomplate'),(302,'Can change bom plate',101,'change_bomplate'),(303,'Can delete bom plate',101,'delete_bomplate'),(304,'Can add bom part',102,'add_bompart'),(305,'Can change bom part',102,'change_bompart'),(306,'Can delete bom part',102,'delete_bompart'),(307,'Can add bom plate part',103,'add_bomplatepart'),(308,'Can change bom plate part',103,'change_bomplatepart'),(309,'Can delete bom plate part',103,'delete_bomplatepart'),(310,'Can add bom visualization',104,'add_bomvisualization'),(311,'Can change bom visualization',104,'change_bomvisualization'),(312,'Can delete bom visualization',104,'delete_bomvisualization'),(313,'Can add service circular',105,'add_servicecircular'),(314,'Can change service circular',105,'change_servicecircular'),(315,'Can delete service circular',105,'delete_servicecircular'),(316,'Can add manufacturing data',106,'add_manufacturingdata'),(317,'Can change manufacturing data',106,'change_manufacturingdata'),(318,'Can delete manufacturing data',106,'delete_manufacturingdata'),(319,'Can add brand product category',107,'add_brandproductcategory'),(320,'Can change brand product category',107,'change_brandproductcategory'),(321,'Can delete brand product category',107,'delete_brandproductcategory'),(322,'Can add user profile',108,'add_userprofile'),(323,'Can change user profile',108,'change_userprofile'),(324,'Can delete user profile',108,'delete_userprofile'),(325,'Can add zonal service manager',109,'add_zonalservicemanager'),(326,'Can change zonal service manager',109,'change_zonalservicemanager'),(327,'Can delete zonal service manager',109,'delete_zonalservicemanager'),(328,'Can add circle head',110,'add_circlehead'),(329,'Can change circle head',110,'change_circlehead'),(330,'Can delete circle head',110,'delete_circlehead'),(331,'Can add regional manager',111,'add_regionalmanager'),(332,'Can change regional manager',111,'change_regionalmanager'),(333,'Can delete regional manager',111,'delete_regionalmanager'),(334,'Can add territory',112,'add_territory'),(335,'Can change territory',112,'change_territory'),(336,'Can delete territory',112,'delete_territory'),(337,'Can add state',113,'add_state'),(338,'Can change state',113,'change_state'),(339,'Can delete state',113,'delete_state'),(340,'Can add area sales manager',114,'add_areasalesmanager'),(341,'Can change area sales manager',114,'change_areasalesmanager'),(342,'Can delete area sales manager',114,'delete_areasalesmanager'),(343,'Can add area service manager',115,'add_areaservicemanager'),(344,'Can change area service manager',115,'change_areaservicemanager'),(345,'Can delete area service manager',115,'delete_areaservicemanager'),(346,'Can add dealer',116,'add_dealer'),(347,'Can change dealer',116,'change_dealer'),(348,'Can delete dealer',116,'delete_dealer'),(349,'Can add authorized service center',117,'add_authorizedservicecenter'),(350,'Can change authorized service center',117,'change_authorizedservicecenter'),(351,'Can delete authorized service center',117,'delete_authorizedservicecenter'),(352,'Can add service advisor',118,'add_serviceadvisor'),(353,'Can change service advisor',118,'change_serviceadvisor'),(354,'Can delete service advisor',118,'delete_serviceadvisor'),(355,'Can add service desk user',119,'add_servicedeskuser'),(356,'Can change service desk user',119,'change_servicedeskuser'),(357,'Can delete service desk user',119,'delete_servicedeskuser'),(358,'Can add brand department',120,'add_branddepartment'),(359,'Can change brand department',120,'change_branddepartment'),(360,'Can delete brand department',120,'delete_branddepartment'),(361,'Can add department sub categories',121,'add_departmentsubcategories'),(362,'Can change department sub categories',121,'change_departmentsubcategories'),(363,'Can delete department sub categories',121,'delete_departmentsubcategories'),(364,'Can add feedback',122,'add_feedback'),(365,'Can change feedback',122,'change_feedback'),(366,'Can delete feedback',122,'delete_feedback'),(367,'Can add activity',123,'add_activity'),(368,'Can change activity',123,'change_activity'),(369,'Can delete activity',123,'delete_activity'),(370,'Can add comment',124,'add_comment'),(371,'Can change comment',124,'change_comment'),(372,'Can delete comment',124,'delete_comment'),(373,'Can add feedback event',125,'add_feedbackevent'),(374,'Can change feedback event',125,'change_feedbackevent'),(375,'Can delete feedback event',125,'delete_feedbackevent'),(376,'Can add product type',126,'add_producttype'),(377,'Can change product type',126,'change_producttype'),(378,'Can delete product type',126,'delete_producttype'),(379,'Can add product data',127,'add_productdata'),(380,'Can change product data',127,'change_productdata'),(381,'Can delete product data',127,'delete_productdata'),(382,'Can add coupon data',128,'add_coupondata'),(383,'Can change coupon data',128,'change_coupondata'),(384,'Can delete coupon data',128,'delete_coupondata'),(385,'Can add service advisor coupon relationship',129,'add_serviceadvisorcouponrelationship'),(386,'Can change service advisor coupon relationship',129,'change_serviceadvisorcouponrelationship'),(387,'Can delete service advisor coupon relationship',129,'delete_serviceadvisorcouponrelationship'),(388,'Can add ucn recovery',130,'add_ucnrecovery'),(389,'Can change ucn recovery',130,'change_ucnrecovery'),(390,'Can delete ucn recovery',130,'delete_ucnrecovery'),(391,'Can add old fsc data',131,'add_oldfscdata'),(392,'Can change old fsc data',131,'change_oldfscdata'),(393,'Can delete old fsc data',131,'delete_oldfscdata'),(394,'Can add cdms data',132,'add_cdmsdata'),(395,'Can change cdms data',132,'change_cdmsdata'),(396,'Can delete cdms data',132,'delete_cdmsdata'),(397,'Can add otp token',133,'add_otptoken'),(398,'Can change otp token',133,'change_otptoken'),(399,'Can delete otp token',133,'delete_otptoken'),(400,'Can add message template',134,'add_messagetemplate'),(401,'Can change message template',134,'change_messagetemplate'),(402,'Can delete message template',134,'delete_messagetemplate'),(403,'Can add email template',135,'add_emailtemplate'),(404,'Can change email template',135,'change_emailtemplate'),(405,'Can delete email template',135,'delete_emailtemplate'),(406,'Can add asc temp registration',136,'add_asctempregistration'),(407,'Can change asc temp registration',136,'change_asctempregistration'),(408,'Can delete asc temp registration',136,'delete_asctempregistration'),(409,'Can add sa temp registration',137,'add_satempregistration'),(410,'Can change sa temp registration',137,'change_satempregistration'),(411,'Can delete sa temp registration',137,'delete_satempregistration'),(412,'Can add customer temp registration',138,'add_customertempregistration'),(413,'Can change customer temp registration',138,'change_customertempregistration'),(414,'Can delete customer temp registration',138,'delete_customertempregistration'),(415,'Can add customer update failure',139,'add_customerupdatefailure'),(416,'Can change customer update failure',139,'change_customerupdatefailure'),(417,'Can delete customer update failure',139,'delete_customerupdatefailure'),(418,'Can add customer update history',140,'add_customerupdatehistory'),(419,'Can change customer update history',140,'change_customerupdatehistory'),(420,'Can delete customer update history',140,'delete_customerupdatehistory'),(421,'Can add user preference',141,'add_userpreference'),(422,'Can change user preference',141,'change_userpreference'),(423,'Can delete user preference',141,'delete_userpreference'),(424,'Can add sms log',142,'add_smslog'),(425,'Can change sms log',142,'change_smslog'),(426,'Can delete sms log',142,'delete_smslog'),(427,'Can add email log',143,'add_emaillog'),(428,'Can change email log',143,'change_emaillog'),(429,'Can delete email log',143,'delete_emaillog'),(430,'Can add data feed log',144,'add_datafeedlog'),(431,'Can change data feed log',144,'change_datafeedlog'),(432,'Can delete data feed log',144,'delete_datafeedlog'),(433,'Can add feed failure log',145,'add_feedfailurelog'),(434,'Can change feed failure log',145,'change_feedfailurelog'),(435,'Can delete feed failure log',145,'delete_feedfailurelog'),(436,'Can add vin sync feed log',146,'add_vinsyncfeedlog'),(437,'Can change vin sync feed log',146,'change_vinsyncfeedlog'),(438,'Can delete vin sync feed log',146,'delete_vinsyncfeedlog'),(439,'Can add audit log',147,'add_auditlog'),(440,'Can change audit log',147,'change_auditlog'),(441,'Can delete audit log',147,'delete_auditlog'),(442,'Can add sla',148,'add_sla'),(443,'Can change sla',148,'change_sla'),(444,'Can delete sla',148,'delete_sla'),(445,'Can add service type',149,'add_servicetype'),(446,'Can change service type',149,'change_servicetype'),(447,'Can delete service type',149,'delete_servicetype'),(448,'Can add service',150,'add_service'),(449,'Can change service',150,'change_service'),(450,'Can delete service',150,'delete_service'),(451,'Can add constant',151,'add_constant'),(452,'Can change constant',151,'change_constant'),(453,'Can delete constant',151,'delete_constant'),(454,'Can add date dimension',152,'add_datedimension'),(455,'Can change date dimension',152,'change_datedimension'),(456,'Can delete date dimension',152,'delete_datedimension'),(457,'Can add coupon fact',153,'add_couponfact'),(458,'Can change coupon fact',153,'change_couponfact'),(459,'Can delete coupon fact',153,'delete_couponfact'),(460,'Can add transporter',154,'add_transporter'),(461,'Can change transporter',154,'change_transporter'),(462,'Can delete transporter',154,'delete_transporter'),(463,'Can add supervisor',155,'add_supervisor'),(464,'Can change supervisor',155,'change_supervisor'),(465,'Can delete supervisor',155,'delete_supervisor'),(466,'Can add container indent',156,'add_containerindent'),(467,'Can change container indent',156,'change_containerindent'),(468,'Can delete container indent',156,'delete_containerindent'),(469,'Can add container lr',157,'add_containerlr'),(470,'Can change container lr',157,'change_containerlr'),(471,'Can delete container lr',157,'delete_containerlr'),(472,'Can add container tracker',158,'add_containertracker'),(473,'Can change container tracker',158,'change_containertracker'),(474,'Can delete container tracker',158,'delete_containertracker'),(475,'Can add city',159,'add_city'),(476,'Can change city',159,'change_city'),(477,'Can delete city',159,'delete_city'),(478,'Can add national spares manager',160,'add_nationalsparesmanager'),(479,'Can change national spares manager',160,'change_nationalsparesmanager'),(480,'Can delete national spares manager',160,'delete_nationalsparesmanager'),(481,'Can add area spares manager',161,'add_areasparesmanager'),(482,'Can change area spares manager',161,'change_areasparesmanager'),(483,'Can delete area spares manager',161,'delete_areasparesmanager'),(484,'Can add distributor',162,'add_distributor'),(485,'Can change distributor',162,'change_distributor'),(486,'Can delete distributor',162,'delete_distributor'),(487,'Can add distributor staff',163,'add_distributorstaff'),(488,'Can change distributor staff',163,'change_distributorstaff'),(489,'Can delete distributor staff',163,'delete_distributorstaff'),(490,'Can add distributor sales rep',164,'add_distributorsalesrep'),(491,'Can change distributor sales rep',164,'change_distributorsalesrep'),(492,'Can delete distributor sales rep',164,'delete_distributorsalesrep'),(493,'Can add retailer',165,'add_retailer'),(494,'Can change retailer',165,'change_retailer'),(495,'Can delete retailer',165,'delete_retailer'),(496,'Can add dsr wrok allocation',166,'add_dsrwrokallocation'),(497,'Can change dsr wrok allocation',166,'change_dsrwrokallocation'),(498,'Can delete dsr wrok allocation',166,'delete_dsrwrokallocation'),(499,'Can add member',167,'add_member'),(500,'Can change member',167,'change_member'),(501,'Can delete member',167,'delete_member'),(502,'Can add spare part master data',168,'add_sparepartmasterdata'),(503,'Can change spare part master data',168,'change_sparepartmasterdata'),(504,'Can delete spare part master data',168,'delete_sparepartmasterdata'),(505,'Can add spare part upc',169,'add_sparepartupc'),(506,'Can change spare part upc',169,'change_sparepartupc'),(507,'Can delete spare part upc',169,'delete_sparepartupc'),(508,'Can add spare part point',170,'add_sparepartpoint'),(509,'Can change spare part point',170,'change_sparepartpoint'),(510,'Can delete spare part point',170,'delete_sparepartpoint'),(511,'Can add accumulation request',171,'add_accumulationrequest'),(512,'Can change accumulation request',171,'change_accumulationrequest'),(513,'Can delete accumulation request',171,'delete_accumulationrequest'),(514,'Can add partner',172,'add_partner'),(515,'Can change partner',172,'change_partner'),(516,'Can delete partner',172,'delete_partner'),(517,'Can add product catalog',173,'add_productcatalog'),(518,'Can change product catalog',173,'change_productcatalog'),(519,'Can delete product catalog',173,'delete_productcatalog'),(520,'Can add redemption request',174,'add_redemptionrequest'),(521,'Can change redemption request',174,'change_redemptionrequest'),(522,'Can delete redemption request',174,'delete_redemptionrequest'),(523,'Can add welcome kit',175,'add_welcomekit'),(524,'Can change welcome kit',175,'change_welcomekit'),(525,'Can delete welcome kit',175,'delete_welcomekit'),(526,'Can add comment thread',176,'add_commentthread'),(527,'Can change comment thread',176,'change_commentthread'),(528,'Can delete comment thread',176,'delete_commentthread'),(529,'Can add loyalty sla',177,'add_loyaltysla'),(530,'Can change loyalty sla',177,'change_loyaltysla'),(531,'Can delete loyalty sla',177,'delete_loyaltysla'),(532,'Can add email token',178,'add_emailtoken'),(533,'Can change email token',178,'change_emailtoken'),(534,'Can delete email token',178,'delete_emailtoken'),(535,'Can add discrepant accumulation',179,'add_discrepantaccumulation'),(536,'Can change discrepant accumulation',179,'change_discrepantaccumulation'),(537,'Can delete discrepant accumulation',179,'delete_discrepantaccumulation'),(538,'Can add eco release',180,'add_ecorelease'),(539,'Can change eco release',180,'change_ecorelease'),(540,'Can delete eco release',180,'delete_ecorelease'),(541,'Can add eco implementation',181,'add_ecoimplementation'),(542,'Can change eco implementation',181,'change_ecoimplementation'),(543,'Can delete eco implementation',181,'delete_ecoimplementation'),(544,'Can add brand vertical',182,'add_brandvertical'),(545,'Can change brand vertical',182,'change_brandvertical'),(546,'Can delete brand vertical',182,'delete_brandvertical'),(547,'Can add brand product range',183,'add_brandproductrange'),(548,'Can change brand product range',183,'change_brandproductrange'),(549,'Can delete brand product range',183,'delete_brandproductrange'),(550,'Can add bom header',184,'add_bomheader'),(551,'Can change bom header',184,'change_bomheader'),(552,'Can delete bom header',184,'delete_bomheader'),(553,'Can add bom plate',185,'add_bomplate'),(554,'Can change bom plate',185,'change_bomplate'),(555,'Can delete bom plate',185,'delete_bomplate'),(556,'Can add bom part',186,'add_bompart'),(557,'Can change bom part',186,'change_bompart'),(558,'Can delete bom part',186,'delete_bompart'),(559,'Can add bom plate part',187,'add_bomplatepart'),(560,'Can change bom plate part',187,'change_bomplatepart'),(561,'Can delete bom plate part',187,'delete_bomplatepart'),(562,'Can add bom visualization',188,'add_bomvisualization'),(563,'Can change bom visualization',188,'change_bomvisualization'),(564,'Can delete bom visualization',188,'delete_bomvisualization'),(565,'Can add service circular',189,'add_servicecircular'),(566,'Can change service circular',189,'change_servicecircular'),(567,'Can delete service circular',189,'delete_servicecircular'),(568,'Can add manufacturing data',190,'add_manufacturingdata'),(569,'Can change manufacturing data',190,'change_manufacturingdata'),(570,'Can delete manufacturing data',190,'delete_manufacturingdata'),(856,'Can add task state',286,'add_taskmeta'),(857,'Can change task state',286,'change_taskmeta'),(858,'Can delete task state',286,'delete_taskmeta'),(859,'Can add saved group result',287,'add_tasksetmeta'),(860,'Can change saved group result',287,'change_tasksetmeta'),(861,'Can delete saved group result',287,'delete_tasksetmeta'),(862,'Can add interval',288,'add_intervalschedule'),(863,'Can change interval',288,'change_intervalschedule'),(864,'Can delete interval',288,'delete_intervalschedule'),(865,'Can add crontab',289,'add_crontabschedule'),(866,'Can change crontab',289,'change_crontabschedule'),(867,'Can delete crontab',289,'delete_crontabschedule'),(868,'Can add periodic tasks',290,'add_periodictasks'),(869,'Can change periodic tasks',290,'change_periodictasks'),(870,'Can delete periodic tasks',290,'delete_periodictasks'),(871,'Can add periodic task',291,'add_periodictask'),(872,'Can change periodic task',291,'change_periodictask'),(873,'Can delete periodic task',291,'delete_periodictask'),(874,'Can add worker',292,'add_workerstate'),(875,'Can change worker',292,'change_workerstate'),(876,'Can delete worker',292,'delete_workerstate'),(877,'Can add task',293,'add_taskstate'),(878,'Can change task',293,'change_taskstate'),(879,'Can delete task',293,'delete_taskstate'),(880,'Can add TOTP device',294,'add_totpdevice'),(881,'Can change TOTP device',294,'change_totpdevice'),(882,'Can delete TOTP device',294,'delete_totpdevice'),(928,'Can add national sales manager',295,'add_nationalsalesmanager'),(929,'Can change national sales manager',295,'change_nationalsalesmanager'),(930,'Can delete national sales manager',295,'delete_nationalsalesmanager'),(931,'Can add national sales manager',296,'add_nationalsalesmanager'),(932,'Can change national sales manager',296,'change_nationalsalesmanager'),(933,'Can delete national sales manager',296,'delete_nationalsalesmanager'),(1549,'Can add brand product category',297,'add_brandproductcategory'),(1550,'Can change brand product category',297,'change_brandproductcategory'),(1551,'Can delete brand product category',297,'delete_brandproductcategory'),(1552,'Can add user profile',298,'add_userprofile'),(1553,'Can change user profile',298,'change_userprofile'),(1554,'Can delete user profile',298,'delete_userprofile'),(1555,'Can add country',299,'add_country'),(1556,'Can change country',299,'change_country'),(1557,'Can delete country',299,'delete_country'),(1558,'Can add country distributor',300,'add_countrydistributor'),(1559,'Can change country distributor',300,'change_countrydistributor'),(1560,'Can delete country distributor',300,'delete_countrydistributor'),(1561,'Can add main country dealer',301,'add_maincountrydealer'),(1562,'Can change main country dealer',301,'change_maincountrydealer'),(1563,'Can delete main country dealer',301,'delete_maincountrydealer'),(1564,'Can add dealer',302,'add_dealer'),(1565,'Can change dealer',302,'change_dealer'),(1566,'Can delete dealer',302,'delete_dealer'),(1567,'Can add service advisor',303,'add_serviceadvisor'),(1568,'Can change service advisor',303,'change_serviceadvisor'),(1569,'Can delete service advisor',303,'delete_serviceadvisor'),(1570,'Can add product type',304,'add_producttype'),(1571,'Can change product type',304,'change_producttype'),(1572,'Can delete product type',304,'delete_producttype'),(1573,'Can add product data',305,'add_productdata'),(1574,'Can change product data',305,'change_productdata'),(1575,'Can delete product data',305,'delete_productdata'),(1576,'Can add fleet rider',306,'add_fleetrider'),(1577,'Can change fleet rider',306,'change_fleetrider'),(1578,'Can delete fleet rider',306,'delete_fleetrider'),(1579,'Can add coupon data',307,'add_coupondata'),(1580,'Can change coupon data',307,'change_coupondata'),(1581,'Can delete coupon data',307,'delete_coupondata'),(1582,'Can add service advisor coupon relationship',308,'add_serviceadvisorcouponrelationship'),(1583,'Can change service advisor coupon relationship',308,'change_serviceadvisorcouponrelationship'),(1584,'Can delete service advisor coupon relationship',308,'delete_serviceadvisorcouponrelationship'),(1585,'Can add ucn recovery',309,'add_ucnrecovery'),(1586,'Can change ucn recovery',309,'change_ucnrecovery'),(1587,'Can delete ucn recovery',309,'delete_ucnrecovery'),(1588,'Can add otp token',310,'add_otptoken'),(1589,'Can change otp token',310,'change_otptoken'),(1590,'Can delete otp token',310,'delete_otptoken'),(1591,'Can add message template',311,'add_messagetemplate'),(1592,'Can change message template',311,'change_messagetemplate'),(1593,'Can delete message template',311,'delete_messagetemplate'),(1594,'Can add email template',312,'add_emailtemplate'),(1595,'Can change email template',312,'change_emailtemplate'),(1596,'Can delete email template',312,'delete_emailtemplate'),(1597,'Can add sms log',313,'add_smslog'),(1598,'Can change sms log',313,'change_smslog'),(1599,'Can delete sms log',313,'delete_smslog'),(1600,'Can add email log',314,'add_emaillog'),(1601,'Can change email log',314,'change_emaillog'),(1602,'Can delete email log',314,'delete_emaillog'),(1603,'Can add data feed log',315,'add_datafeedlog'),(1604,'Can change data feed log',315,'change_datafeedlog'),(1605,'Can delete data feed log',315,'delete_datafeedlog'),(1606,'Can add feed failure log',316,'add_feedfailurelog'),(1607,'Can change feed failure log',316,'change_feedfailurelog'),(1608,'Can delete feed failure log',316,'delete_feedfailurelog'),(1609,'Can add vin sync feed log',317,'add_vinsyncfeedlog'),(1610,'Can change vin sync feed log',317,'change_vinsyncfeedlog'),(1611,'Can delete vin sync feed log',317,'delete_vinsyncfeedlog'),(1612,'Can add constant',318,'add_constant'),(1613,'Can change constant',318,'change_constant'),(1614,'Can delete constant',318,'delete_constant'),(1615,'Can add customer update history',319,'add_customerupdatehistory'),(1616,'Can change customer update history',319,'change_customerupdatehistory'),(1617,'Can delete customer update history',319,'delete_customerupdatehistory'),(1663,'Can add dsr work allocation',320,'add_dsrworkallocation'),(1664,'Can change dsr work allocation',320,'change_dsrworkallocation'),(1665,'Can delete dsr work allocation',320,'delete_dsrworkallocation'),(1666,'Can add dsr work allocation',321,'add_dsrworkallocation'),(1667,'Can change dsr work allocation',321,'change_dsrworkallocation'),(1668,'Can delete dsr work allocation',321,'delete_dsrworkallocation'),(1669,'Can add order part',322,'add_orderpart'),(1670,'Can change order part',322,'change_orderpart'),(1671,'Can delete order part',322,'delete_orderpart'),(2332,'Can add order part',323,'add_orderpart'),(2333,'Can change order part',323,'change_orderpart'),(2334,'Can delete order part',323,'delete_orderpart'),(2380,'Can add part pricing',324,'add_partpricing'),(2381,'Can change part pricing',324,'change_partpricing'),(2382,'Can delete part pricing',324,'delete_partpricing'),(2383,'Can add part pricing',325,'add_partpricing'),(2384,'Can change part pricing',325,'change_partpricing'),(2385,'Can delete part pricing',325,'delete_partpricing'),(2716,'Can add part models',326,'add_partmodels'),(2717,'Can change part models',326,'change_partmodels'),(2718,'Can delete part models',326,'delete_partmodels'),(2719,'Can add categories',327,'add_categories'),(2720,'Can change categories',327,'change_categories'),(2721,'Can delete categories',327,'delete_categories'),(2722,'Can add sub categories',328,'add_subcategories'),(2723,'Can change sub categories',328,'change_subcategories'),(2724,'Can delete sub categories',328,'delete_subcategories'),(2725,'Can add part models',329,'add_partmodels'),(2726,'Can change part models',329,'change_partmodels'),(2727,'Can delete part models',329,'delete_partmodels'),(2728,'Can add categories',330,'add_categories'),(2729,'Can change categories',330,'change_categories'),(2730,'Can delete categories',330,'delete_categories'),(2731,'Can add sub categories',331,'add_subcategories'),(2732,'Can change sub categories',331,'change_subcategories'),(2733,'Can delete sub categories',331,'delete_subcategories');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(250) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$MNMkMyeZzEhg$FYcl9lGJCcLEFuFAw9VOROiDnGizlQUOp2pRpJoFBr4=','2015-10-02 07:26:22',1,'bajaj','','','',1,1,'2015-08-19 08:17:06'),(46,'pbkdf2_sha256$12000$0SUiIHqx6dUv$0aHcpfrixchnFUVTRlVIWv3PrQOfFOhMQHFOLOYUu/g=','2015-09-25 09:11:54',0,'naveen','naveen','shankar','',0,1,'2015-09-25 09:11:54'),(47,'pbkdf2_sha256$12000$hJ6tU85hL8ii$iVsaQtiJPkC2y+jjcMzZTSVwyPF74zkgQgb4RJBOVFA=','2015-10-02 05:46:13',0,'shashank','','','',1,1,'2015-09-25 09:15:22'),(48,'pbkdf2_sha256$12000$c6Kc4fl8nsEI$3o6UKPJg2HKBal0rsHASK8DH5Pl5Mm5/A+UI/GvLRLk=','2015-09-25 10:10:28',0,'sudhir','','','',0,1,'2015-09-25 10:10:28'),(51,'pbkdf2_sha256$12000$JPYvuNlgpn7r$FH36ZwBhIQ+ulz/qqfwCEVtn9N0lTXZZ0saTFVqdlww=','2015-10-01 05:13:24',0,'ranjan','','','',1,1,'2015-09-28 06:28:18'),(52,'pbkdf2_sha256$12000$2wIn4MPMVcxc$TcvZ32O+Uzp8/bt49H2/nwG8V0FP11zxqaWFULZbe6s=','2015-09-28 07:59:40',0,'aras','','','',1,1,'2015-09-28 07:40:05'),(53,'pbkdf2_sha256$12000$Jkz6F1O6q0mr$LHlmROubaquVs/cIeF5PVUX8a4wuIzONyk4v3bSyWSc=','2015-10-02 05:42:08',0,'jitendar','','','',1,1,'2015-10-01 04:50:58');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (17,1,33),(25,47,13),(26,51,2),(27,52,1),(28,53,44);
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bajaj_orderpart`
--

DROP TABLE IF EXISTS `bajaj_orderpart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bajaj_orderpart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `part_id` int(11) NOT NULL,
  `dsr_id` int(11) DEFAULT NULL,
  `retailer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bajaj_orderpart_8c28136d` (`part_id`),
  KEY `bajaj_orderpart_9f70fd12` (`dsr_id`),
  KEY `bajaj_orderpart_64f72e30` (`retailer_id`),
  CONSTRAINT `dsr_id_refs_id_dcd46864` FOREIGN KEY (`dsr_id`) REFERENCES `gm_distributorsalesrep` (`id`),
  CONSTRAINT `part_id_refs_id_f08e4a6a` FOREIGN KEY (`part_id`) REFERENCES `gm_sparepartmasterdata` (`id`),
  CONSTRAINT `retailer_id_refs_id_85bb25be` FOREIGN KEY (`retailer_id`) REFERENCES `gm_retailer` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bajaj_orderpart`
--

LOCK TABLES `bajaj_orderpart` WRITE;
/*!40000 ALTER TABLE `bajaj_orderpart` DISABLE KEYS */;
/*!40000 ALTER TABLE `bajaj_orderpart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_taskmeta`
--

DROP TABLE IF EXISTS `celery_taskmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_taskmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) NOT NULL,
  `status` varchar(50) NOT NULL,
  `result` longtext,
  `date_done` datetime NOT NULL,
  `traceback` longtext,
  `hidden` tinyint(1) NOT NULL,
  `meta` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `celery_taskmeta_2ff6b945` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_taskmeta`
--

LOCK TABLES `celery_taskmeta` WRITE;
/*!40000 ALTER TABLE `celery_taskmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_taskmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `celery_tasksetmeta`
--

DROP TABLE IF EXISTS `celery_tasksetmeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `celery_tasksetmeta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taskset_id` varchar(255) NOT NULL,
  `result` longtext NOT NULL,
  `date_done` datetime NOT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `taskset_id` (`taskset_id`),
  KEY `celery_tasksetmeta_2ff6b945` (`hidden`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `celery_tasksetmeta`
--

LOCK TABLES `celery_tasksetmeta` WRITE;
/*!40000 ALTER TABLE `celery_tasksetmeta` DISABLE KEYS */;
/*!40000 ALTER TABLE `celery_tasksetmeta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_apppreferences`
--

DROP TABLE IF EXISTS `default_apppreferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_apppreferences` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `brand_id` int(11) NOT NULL,
  `key` varchar(100) NOT NULL,
  `value` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `brand_id` (`brand_id`,`key`),
  KEY `default_apppreferences_5afadb1e` (`brand_id`),
  CONSTRAINT `brand_id_refs_id_3b1b8acc` FOREIGN KEY (`brand_id`) REFERENCES `default_brand` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_apppreferences`
--

LOCK TABLES `default_apppreferences` WRITE;
/*!40000 ALTER TABLE `default_apppreferences` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_apppreferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_auditlog`
--

DROP TABLE IF EXISTS `default_auditlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_auditlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `device` varchar(250) DEFAULT NULL,
  `user_agent` varchar(250) DEFAULT NULL,
  `urls` varchar(250) NOT NULL,
  `access_token` varchar(250) DEFAULT NULL,
  `user_profile_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `default_auditlog_82936d91` (`user_profile_id`),
  CONSTRAINT `user_profile_id_refs_user_id_9552938c` FOREIGN KEY (`user_profile_id`) REFERENCES `default_gladmindsuser` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_auditlog`
--

LOCK TABLES `default_auditlog` WRITE;
/*!40000 ALTER TABLE `default_auditlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_auditlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_brand`
--

DROP TABLE IF EXISTS `default_brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_brand` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(250) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `description` longtext,
  `industry_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `default_brand_c3dc70a9` (`industry_id`),
  CONSTRAINT `industry_id_refs_id_6107e146` FOREIGN KEY (`industry_id`) REFERENCES `default_industry` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_brand`
--

LOCK TABLES `default_brand` WRITE;
/*!40000 ALTER TABLE `default_brand` DISABLE KEYS */;
INSERT INTO `default_brand` VALUES (1,'2015-09-29 18:00:08','2015-09-29 18:00:08','demo','',1,NULL,1),(2,'2015-09-29 18:00:08','2015-09-29 18:00:08','bajaj','',1,NULL,1),(3,'2015-09-29 18:00:08','2015-09-29 18:00:08','bajajib','',1,NULL,1),(4,'2015-09-29 18:00:08','2015-09-29 18:00:08','daimler','',1,NULL,1);
/*!40000 ALTER TABLE `default_brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_brandproductcategory`
--

DROP TABLE IF EXISTS `default_brandproductcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_brandproductcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(250) NOT NULL,
  `description` longtext,
  `brand_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `default_brandproductcategory_5afadb1e` (`brand_id`),
  CONSTRAINT `brand_id_refs_id_95daea81` FOREIGN KEY (`brand_id`) REFERENCES `default_brand` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_brandproductcategory`
--

LOCK TABLES `default_brandproductcategory` WRITE;
/*!40000 ALTER TABLE `default_brandproductcategory` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_brandproductcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_brandservice`
--

DROP TABLE IF EXISTS `default_brandservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_brandservice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `brand_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `comment` longtext,
  PRIMARY KEY (`id`),
  KEY `default_brandservice_5afadb1e` (`brand_id`),
  KEY `default_brandservice_91a0ac17` (`service_id`),
  CONSTRAINT `brand_id_refs_id_0e6c9bb9` FOREIGN KEY (`brand_id`) REFERENCES `default_brand` (`id`),
  CONSTRAINT `service_id_refs_id_36ab5ce1` FOREIGN KEY (`service_id`) REFERENCES `default_service` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_brandservice`
--

LOCK TABLES `default_brandservice` WRITE;
/*!40000 ALTER TABLE `default_brandservice` DISABLE KEYS */;
INSERT INTO `default_brandservice` VALUES (1,'2015-09-29 18:00:09','2015-09-29 18:00:09',1,4,1,NULL),(2,'2015-09-29 18:00:09','2015-09-29 18:00:09',2,1,1,NULL),(3,'2015-09-29 18:00:09','2015-09-29 18:00:09',2,2,1,NULL),(4,'2015-09-29 18:00:09','2015-09-29 18:00:09',2,3,1,NULL),(5,'2015-09-29 18:00:09','2015-09-29 18:00:09',2,4,1,NULL),(6,'2015-09-29 18:00:09','2015-09-29 18:00:09',2,5,1,NULL),(7,'2015-09-29 18:00:09','2015-09-29 18:00:09',3,1,1,NULL),(8,'2015-09-29 18:00:09','2015-09-29 18:00:09',3,2,1,NULL),(9,'2015-09-29 18:00:09','2015-09-29 18:00:09',3,3,1,NULL),(10,'2015-09-29 18:00:10','2015-09-29 18:00:10',3,4,1,NULL),(11,'2015-09-29 18:00:10','2015-09-29 18:00:10',4,4,1,NULL);
/*!40000 ALTER TABLE `default_brandservice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_emaillog`
--

DROP TABLE IF EXISTS `default_emaillog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_emaillog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `subject` varchar(250) DEFAULT NULL,
  `message` longtext,
  `sender` varchar(100) DEFAULT NULL,
  `receiver` longtext NOT NULL,
  `cc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_emaillog`
--

LOCK TABLES `default_emaillog` WRITE;
/*!40000 ALTER TABLE `default_emaillog` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_emaillog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_emailtemplate`
--

DROP TABLE IF EXISTS `default_emailtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_emailtemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `template_key` varchar(255) NOT NULL,
  `sender` varchar(512) NOT NULL,
  `receiver` varchar(512) NOT NULL,
  `subject` varchar(512) NOT NULL,
  `body` varchar(512) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `template_key` (`template_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_emailtemplate`
--

LOCK TABLES `default_emailtemplate` WRITE;
/*!40000 ALTER TABLE `default_emailtemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_emailtemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_gladmindsuser`
--

DROP TABLE IF EXISTS `default_gladmindsuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_gladmindsuser` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `address` longtext,
  `state` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `pincode` varchar(15) DEFAULT NULL,
  `date_of_birth` datetime DEFAULT NULL,
  `is_email_verified` tinyint(1) NOT NULL,
  `is_phone_verified` tinyint(1) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `reset_password` tinyint(1) NOT NULL,
  `reset_date` datetime DEFAULT NULL,
  `gender` varchar(2) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_id_refs_id_6ec1f2b0` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_gladmindsuser`
--

LOCK TABLES `default_gladmindsuser` WRITE;
/*!40000 ALTER TABLE `default_gladmindsuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_gladmindsuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_industry`
--

DROP TABLE IF EXISTS `default_industry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_industry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_industry`
--

LOCK TABLES `default_industry` WRITE;
/*!40000 ALTER TABLE `default_industry` DISABLE KEYS */;
INSERT INTO `default_industry` VALUES (1,'2015-09-29 18:00:08','2015-09-29 18:00:08','automobiles',NULL);
/*!40000 ALTER TABLE `default_industry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_messagetemplate`
--

DROP TABLE IF EXISTS `default_messagetemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_messagetemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `template_key` varchar(255) NOT NULL,
  `template` varchar(512) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `template_key` (`template_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_messagetemplate`
--

LOCK TABLES `default_messagetemplate` WRITE;
/*!40000 ALTER TABLE `default_messagetemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_messagetemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_otptoken`
--

DROP TABLE IF EXISTS `default_otptoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_otptoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `token` varchar(256) NOT NULL,
  `request_date` datetime DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `default_otptoken_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_f0518456` FOREIGN KEY (`user_id`) REFERENCES `default_gladmindsuser` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_otptoken`
--

LOCK TABLES `default_otptoken` WRITE;
/*!40000 ALTER TABLE `default_otptoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_otptoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_service`
--

DROP TABLE IF EXISTS `default_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `service_type_id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `default_service_cca592ae` (`service_type_id`),
  CONSTRAINT `service_type_id_refs_id_68386fcd` FOREIGN KEY (`service_type_id`) REFERENCES `default_servicetype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_service`
--

LOCK TABLES `default_service` WRITE;
/*!40000 ALTER TABLE `default_service` DISABLE KEYS */;
INSERT INTO `default_service` VALUES (1,'2015-09-29 18:00:07','2015-09-29 18:00:07',1,'afterbuy',NULL),(2,'2015-09-29 18:00:07','2015-09-29 18:00:07',2,'free_service_coupon',NULL),(3,'2015-09-29 18:00:08','2015-09-29 18:00:08',3,'loyalty',NULL),(4,'2015-09-29 18:00:08','2015-09-29 18:00:08',4,'service_desk',NULL),(5,'2015-09-29 18:00:08','2015-09-29 18:00:08',5,'sfa',NULL);
/*!40000 ALTER TABLE `default_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_servicetype`
--

DROP TABLE IF EXISTS `default_servicetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_servicetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_servicetype`
--

LOCK TABLES `default_servicetype` WRITE;
/*!40000 ALTER TABLE `default_servicetype` DISABLE KEYS */;
INSERT INTO `default_servicetype` VALUES (1,'2015-09-29 18:00:07','2015-09-29 18:00:07','afterbuy',NULL),(2,'2015-09-29 18:00:07','2015-09-29 18:00:07','free_service_coupon',NULL),(3,'2015-09-29 18:00:07','2015-09-29 18:00:07','loyalty',NULL),(4,'2015-09-29 18:00:07','2015-09-29 18:00:07','service_desk',NULL),(5,'2015-09-29 18:00:07','2015-09-29 18:00:07','sfa',NULL);
/*!40000 ALTER TABLE `default_servicetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `default_smslog`
--

DROP TABLE IF EXISTS `default_smslog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `default_smslog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `action` varchar(250) NOT NULL,
  `message` longtext,
  `sender` varchar(15) NOT NULL,
  `receiver` varchar(15) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `default_smslog`
--

LOCK TABLES `default_smslog` WRITE;
/*!40000 ALTER TABLE `default_smslog` DISABLE KEYS */;
/*!40000 ALTER TABLE `default_smslog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_93d2d1f8` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c0d12874` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=219 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (73,'2015-09-05 16:43:15',1,3,'12','distributorone',1,''),(74,'2015-09-05 16:46:16',1,108,'12','9878654323 distributorone',1,''),(75,'2015-09-05 16:47:46',1,162,'6','distributorone distributor',1,''),(76,'2015-09-05 16:52:51',1,3,'12','distributorone',2,'Changed is_staff.'),(77,'2015-09-05 16:55:16',1,3,'12','distributorone',2,'Changed is_staff.'),(78,'2015-09-05 17:09:47',1,3,'12','distributorone',2,'Changed groups.'),(79,'2015-09-05 17:10:36',1,3,'12','distributorone',2,'Changed is_staff.'),(80,'2015-09-05 17:11:34',1,3,'13','distributortwo',1,''),(81,'2015-09-05 17:12:08',1,3,'13','distributortwo',2,'Changed is_staff and groups.'),(82,'2015-09-05 17:12:37',1,3,'14','distributorthree',1,''),(83,'2015-09-05 17:13:15',1,3,'14','distributorthree',2,'Changed is_staff and groups.'),(84,'2015-09-05 17:24:27',1,108,'13','545435345 distributortwo',1,''),(85,'2015-09-05 17:24:59',1,162,'7','distributortwo distributor',1,''),(86,'2015-09-05 17:26:04',1,108,'14','4234234 distributorthree',1,''),(87,'2015-09-05 17:26:48',1,162,'8','distributorthree distributor',1,''),(100,'2015-09-05 17:40:25',1,2,'15','DistributorStaffs',2,'Changed permissions.'),(108,'2015-09-05 18:16:47',1,3,'1','bajaj',2,'Changed groups.'),(109,'2015-09-05 18:16:59',1,3,'19','retailertwo',2,'Changed is_staff.'),(110,'2015-09-08 16:35:48',1,3,'20','nsm',1,''),(111,'2015-09-08 16:38:00',1,3,'20','nsm',2,'Changed is_staff and groups.'),(112,'2015-09-08 16:42:30',1,108,'20','34433355 nsm',1,''),(113,'2015-09-08 16:43:31',1,112,'1','south',1,''),(114,'2015-09-08 16:43:38',1,296,'1','nsm_name',1,''),(115,'2015-09-08 16:58:39',1,3,'20','nsm',2,'Changed user_permissions.'),(116,'2015-09-08 17:54:33',1,3,'20','nsm',2,'Changed user_permissions.'),(117,'2015-09-08 17:55:13',1,3,'20','nsm',2,'No fields changed.'),(118,'2015-09-08 17:56:54',1,3,'20','nsm',2,'Changed user_permissions.'),(132,'2015-09-16 04:32:48',1,3,'39','supreme',1,''),(133,'2015-09-16 04:33:14',1,3,'39','supreme',2,'Changed is_staff and groups.'),(134,'2015-09-16 04:35:54',1,108,'39','+{91)-898989898 supreme',1,''),(135,'2015-09-16 04:43:27',1,162,'9','supreme supreme dealers',1,''),(152,'2015-09-16 08:09:36',1,2,'13','Distributors',2,'Changed permissions.'),(153,'2015-09-16 11:26:47',1,2,'13','Distributors',2,'Changed permissions.'),(158,'2015-09-21 04:29:31',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(162,'2015-09-21 11:06:12',1,2,'13','Distributors',2,'Changed permissions.'),(163,'2015-09-22 06:19:23',1,2,'13','Distributors',2,'Changed permissions.'),(164,'2015-09-25 09:11:54',1,3,'46','naveen',1,''),(165,'2015-09-25 09:12:23',1,3,'46','naveen',2,'No fields changed.'),(166,'2015-09-25 09:14:23',1,108,'46','988076543 naveen',1,''),(167,'2015-09-25 09:15:22',1,3,'47','ashish',1,''),(168,'2015-09-25 09:15:49',1,3,'47','ashish',2,'Changed is_staff and groups.'),(169,'2015-09-25 09:17:56',1,108,'47','9423840394 ashish',1,''),(170,'2015-09-25 09:20:37',1,162,'10','400001 ashish',1,''),(171,'2015-09-25 09:47:19',47,164,'7','500001',1,''),(172,'2015-09-25 09:52:28',47,3,'46','naveen',2,'Changed first_name and last_name.'),(173,'2015-09-25 10:10:28',47,3,'48','sudhir',1,''),(174,'2015-09-25 10:10:44',47,3,'48','sudhir',2,'No fields changed.'),(175,'2015-09-25 10:12:36',47,108,'48','080 - 41123876 sudhir',1,''),(176,'2015-09-25 10:17:45',47,165,'13','sudhir',1,''),(177,'2015-09-25 12:50:51',47,3,'49','ret',1,''),(178,'2015-09-25 12:51:16',47,108,'49','32423 ret',1,''),(179,'2015-09-25 12:52:39',47,165,'14','dffsd',1,''),(180,'2015-09-25 12:56:30',47,165,'14','dffsd',2,'Changed mobile.'),(181,'2015-09-26 05:50:50',47,164,'9','dsr',1,''),(182,'2015-09-26 09:21:33',47,165,'15','d',1,''),(183,'2015-09-26 09:53:11',47,321,'3','DSRWorkAllocation object',1,''),(184,'2015-09-26 09:53:44',47,321,'4','DSRWorkAllocation object',1,''),(185,'2015-09-26 10:44:06',47,321,'5','DSRWorkAllocation object',1,''),(186,'2015-09-26 14:19:52',47,3,'50','retailer',1,''),(187,'2015-09-26 14:20:01',47,3,'50','retailer',2,'No fields changed.'),(188,'2015-09-26 14:20:53',47,108,'50','080 -343 retailer',1,''),(189,'2015-09-26 14:23:41',47,165,'16','60001 retailer',1,''),(190,'2015-09-26 14:39:15',47,165,'None','600002 retailer',1,''),(191,'2015-09-27 02:26:46',1,2,'13','Distributors',2,'Changed permissions.'),(192,'2015-09-27 23:30:39',1,2,'13','Distributors',2,'No fields changed.'),(193,'2015-09-28 00:08:49',1,2,'13','Distributors',2,'No fields changed.'),(194,'2015-09-28 05:34:54',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(195,'2015-09-28 06:28:18',1,3,'51','ranjan',1,''),(196,'2015-09-28 06:28:37',1,3,'51','ranjan',2,'Changed is_staff and groups.'),(197,'2015-09-28 06:30:52',1,108,'51','080 - 78654323 ranjan',1,''),(198,'2015-09-28 06:32:10',1,114,'2','ranjan',1,''),(199,'2015-09-28 07:40:06',1,3,'52','aras',1,''),(200,'2015-09-28 07:40:54',1,3,'52','aras',2,'Changed is_staff and groups.'),(201,'2015-09-28 07:42:14',1,108,'52','080 - 875345355 aras',1,''),(202,'2015-09-28 07:43:57',1,112,'2','north',1,''),(203,'2015-09-28 07:44:02',1,296,'2','aras',1,''),(204,'2015-09-28 07:59:27',1,2,'1','Admins',2,'Changed permissions.'),(205,'2015-09-28 08:01:27',1,2,'1','Admins',2,'Changed permissions.'),(206,'2015-09-28 08:03:13',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(207,'2015-10-01 04:50:59',1,3,'53','pattabi',1,''),(208,'2015-10-01 04:51:12',1,3,'53','pattabi',2,'Changed is_staff.'),(209,'2015-10-01 04:52:23',1,108,'53','080 -7657777 pattabi',1,''),(210,'2015-10-01 05:00:12',1,296,'3','jitendar',1,''),(211,'2015-10-01 05:05:45',1,2,'44','nationalsalesmanager',1,''),(212,'2015-10-01 05:07:03',1,2,'44','nationalsalesmanager',2,'Changed permissions.'),(213,'2015-10-01 05:08:22',1,3,'53','jitendar',2,'Changed groups.'),(214,'2015-10-01 05:09:18',1,3,'54','shashank',1,''),(215,'2015-10-01 05:10:06',1,3,'54','shashank',2,'Changed first_name, email, is_staff and groups.'),(216,'2015-10-01 05:26:34',1,2,'44','nationalsalesmanager',2,'Changed permissions.'),(217,'2015-10-02 05:33:19',47,322,'21','OrderPart object',2,'Changed fullfill, delivered and no_fullfill_reason.'),(218,'2015-10-02 05:41:49',1,2,'44','nationalsalesmanager',2,'Changed permissions.');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=332 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'client','oauth2','client'),(9,'grant','oauth2','grant'),(10,'access token','oauth2','accesstoken'),(11,'refresh token','oauth2','refreshtoken'),(12,'industry','default','industry'),(13,'service type','default','servicetype'),(14,'service','default','service'),(15,'brand','default','brand'),(16,'brand product category','default','brandproductcategory'),(17,'brand service','default','brandservice'),(18,'gladminds user','default','gladmindsuser'),(19,'otp token','default','otptoken'),(20,'message template','default','messagetemplate'),(21,'email template','default','emailtemplate'),(22,'app preferences','default','apppreferences'),(23,'sms log','default','smslog'),(24,'email log','default','emaillog'),(25,'audit log','default','auditlog'),(26,'constant','default','constant'),(27,'brand product category','core','brandproductcategory'),(28,'user profile','core','userprofile'),(29,'zonal service manager','core','zonalservicemanager'),(30,'area service manager','core','areaservicemanager'),(31,'dealer','core','dealer'),(32,'authorized service center','core','authorizedservicecenter'),(33,'service advisor','core','serviceadvisor'),(34,'brand department','core','branddepartment'),(35,'department sub categories','core','departmentsubcategories'),(36,'service desk user','core','servicedeskuser'),(37,'feedback','core','feedback'),(38,'activity','core','activity'),(39,'comment','core','comment'),(40,'feedback event','core','feedbackevent'),(41,'product type','core','producttype'),(42,'product data','core','productdata'),(43,'coupon data','core','coupondata'),(44,'service advisor coupon relationship','core','serviceadvisorcouponrelationship'),(45,'ucn recovery','core','ucnrecovery'),(46,'old fsc data','core','oldfscdata'),(47,'cdms data','core','cdmsdata'),(48,'otp token','core','otptoken'),(49,'message template','core','messagetemplate'),(50,'email template','core','emailtemplate'),(51,'asc temp registration','core','asctempregistration'),(52,'sa temp registration','core','satempregistration'),(53,'customer temp registration','core','customertempregistration'),(54,'customer update failure','core','customerupdatefailure'),(55,'customer update history','core','customerupdatehistory'),(56,'user preference','core','userpreference'),(57,'sms log','core','smslog'),(58,'email log','core','emaillog'),(59,'data feed log','core','datafeedlog'),(60,'feed failure log','core','feedfailurelog'),(61,'vin sync feed log','core','vinsyncfeedlog'),(62,'audit log','core','auditlog'),(63,'sla','core','sla'),(64,'service type','core','servicetype'),(65,'service','core','service'),(66,'constant','core','constant'),(67,'date dimension','core','datedimension'),(68,'coupon fact','core','couponfact'),(69,'transporter','core','transporter'),(70,'supervisor','core','supervisor'),(71,'container indent','core','containerindent'),(72,'container lr','core','containerlr'),(73,'container tracker','core','containertracker'),(74,'territory','core','territory'),(75,'state','core','state'),(76,'city','core','city'),(77,'national spares manager','core','nationalsparesmanager'),(78,'area spares manager','core','areasparesmanager'),(79,'distributor','core','distributor'),(80,'distributor staff','core','distributorstaff'),(81,'distributor sales rep','core','distributorsalesrep'),(82,'retailer','core','retailer'),(83,'dsr wrok allocation','core','dsrwrokallocation'),(84,'member','core','member'),(85,'spare part master data','core','sparepartmasterdata'),(86,'spare part upc','core','sparepartupc'),(87,'spare part point','core','sparepartpoint'),(88,'accumulation request','core','accumulationrequest'),(89,'partner','core','partner'),(90,'product catalog','core','productcatalog'),(91,'redemption request','core','redemptionrequest'),(92,'welcome kit','core','welcomekit'),(93,'comment thread','core','commentthread'),(94,'loyalty sla','core','loyaltysla'),(95,'discrepant accumulation','core','discrepantaccumulation'),(96,'eco release','core','ecorelease'),(97,'eco implementation','core','ecoimplementation'),(98,'brand vertical','core','brandvertical'),(99,'brand product range','core','brandproductrange'),(100,'bom header','core','bomheader'),(101,'bom plate','core','bomplate'),(102,'bom part','core','bompart'),(103,'bom plate part','core','bomplatepart'),(104,'bom visualization','core','bomvisualization'),(105,'service circular','core','servicecircular'),(106,'manufacturing data','core','manufacturingdata'),(107,'brand product category','bajaj','brandproductcategory'),(108,'user profile','bajaj','userprofile'),(109,'zonal service manager','bajaj','zonalservicemanager'),(110,'circle head','bajaj','circlehead'),(111,'regional manager','bajaj','regionalmanager'),(112,'territory','bajaj','territory'),(113,'state','bajaj','state'),(114,'area sales manager','bajaj','areasalesmanager'),(115,'area service manager','bajaj','areaservicemanager'),(116,'dealer','bajaj','dealer'),(117,'authorized service center','bajaj','authorizedservicecenter'),(118,'service advisor','bajaj','serviceadvisor'),(119,'service desk user','bajaj','servicedeskuser'),(120,'brand department','bajaj','branddepartment'),(121,'department sub categories','bajaj','departmentsubcategories'),(122,'feedback','bajaj','feedback'),(123,'activity','bajaj','activity'),(124,'comment','bajaj','comment'),(125,'feedback event','bajaj','feedbackevent'),(126,'product type','bajaj','producttype'),(127,'product data','bajaj','productdata'),(128,'coupon data','bajaj','coupondata'),(129,'service advisor coupon relationship','bajaj','serviceadvisorcouponrelationship'),(130,'ucn recovery','bajaj','ucnrecovery'),(131,'old fsc data','bajaj','oldfscdata'),(132,'cdms data','bajaj','cdmsdata'),(133,'otp token','bajaj','otptoken'),(134,'message template','bajaj','messagetemplate'),(135,'email template','bajaj','emailtemplate'),(136,'asc temp registration','bajaj','asctempregistration'),(137,'sa temp registration','bajaj','satempregistration'),(138,'customer temp registration','bajaj','customertempregistration'),(139,'customer update failure','bajaj','customerupdatefailure'),(140,'customer update history','bajaj','customerupdatehistory'),(141,'user preference','bajaj','userpreference'),(142,'sms log','bajaj','smslog'),(143,'email log','bajaj','emaillog'),(144,'data feed log','bajaj','datafeedlog'),(145,'feed failure log','bajaj','feedfailurelog'),(146,'vin sync feed log','bajaj','vinsyncfeedlog'),(147,'audit log','bajaj','auditlog'),(148,'sla','bajaj','sla'),(149,'service type','bajaj','servicetype'),(150,'service','bajaj','service'),(151,'constant','bajaj','constant'),(152,'date dimension','bajaj','datedimension'),(153,'coupon fact','bajaj','couponfact'),(154,'transporter','bajaj','transporter'),(155,'supervisor','bajaj','supervisor'),(156,'container indent','bajaj','containerindent'),(157,'container lr','bajaj','containerlr'),(158,'container tracker','bajaj','containertracker'),(159,'city','bajaj','city'),(160,'national spares manager','bajaj','nationalsparesmanager'),(161,'area spares manager','bajaj','areasparesmanager'),(162,'distributor','bajaj','distributor'),(163,'distributor staff','bajaj','distributorstaff'),(164,'distributor sales rep','bajaj','distributorsalesrep'),(165,'retailer','bajaj','retailer'),(166,'dsr wrok allocation','bajaj','dsrwrokallocation'),(167,'member','bajaj','member'),(168,'spare part master data','bajaj','sparepartmasterdata'),(169,'spare part upc','bajaj','sparepartupc'),(170,'spare part point','bajaj','sparepartpoint'),(171,'accumulation request','bajaj','accumulationrequest'),(172,'partner','bajaj','partner'),(173,'product catalog','bajaj','productcatalog'),(174,'redemption request','bajaj','redemptionrequest'),(175,'welcome kit','bajaj','welcomekit'),(176,'comment thread','bajaj','commentthread'),(177,'loyalty sla','bajaj','loyaltysla'),(178,'email token','bajaj','emailtoken'),(179,'discrepant accumulation','bajaj','discrepantaccumulation'),(180,'eco release','bajaj','ecorelease'),(181,'eco implementation','bajaj','ecoimplementation'),(182,'brand vertical','bajaj','brandvertical'),(183,'brand product range','bajaj','brandproductrange'),(184,'bom header','bajaj','bomheader'),(185,'bom plate','bajaj','bomplate'),(186,'bom part','bajaj','bompart'),(187,'bom plate part','bajaj','bomplatepart'),(188,'bom visualization','bajaj','bomvisualization'),(189,'service circular','bajaj','servicecircular'),(190,'manufacturing data','bajaj','manufacturingdata'),(191,'brand product category','demo','brandproductcategory'),(192,'user profile','demo','userprofile'),(193,'zonal service manager','demo','zonalservicemanager'),(194,'area service manager','demo','areaservicemanager'),(195,'dealer','demo','dealer'),(196,'authorized service center','demo','authorizedservicecenter'),(197,'service advisor','demo','serviceadvisor'),(198,'brand department','demo','branddepartment'),(199,'department sub categories','demo','departmentsubcategories'),(200,'service desk user','demo','servicedeskuser'),(201,'feedback','demo','feedback'),(202,'activity','demo','activity'),(203,'comment','demo','comment'),(204,'feedback event','demo','feedbackevent'),(205,'product type','demo','producttype'),(206,'product data','demo','productdata'),(207,'coupon data','demo','coupondata'),(208,'service advisor coupon relationship','demo','serviceadvisorcouponrelationship'),(209,'ucn recovery','demo','ucnrecovery'),(210,'old fsc data','demo','oldfscdata'),(211,'cdms data','demo','cdmsdata'),(212,'otp token','demo','otptoken'),(213,'message template','demo','messagetemplate'),(214,'email template','demo','emailtemplate'),(215,'asc temp registration','demo','asctempregistration'),(216,'sa temp registration','demo','satempregistration'),(217,'customer temp registration','demo','customertempregistration'),(218,'user preference','demo','userpreference'),(219,'sms log','demo','smslog'),(220,'email log','demo','emaillog'),(221,'data feed log','demo','datafeedlog'),(222,'feed failure log','demo','feedfailurelog'),(223,'vin sync feed log','demo','vinsyncfeedlog'),(224,'audit log','demo','auditlog'),(225,'sla','demo','sla'),(226,'service type','demo','servicetype'),(227,'service','demo','service'),(228,'constant','demo','constant'),(229,'national spares manager','demo','nationalsparesmanager'),(230,'area spares manager','demo','areasparesmanager'),(231,'territory','demo','territory'),(232,'state','demo','state'),(233,'city','demo','city'),(234,'distributor','demo','distributor'),(235,'retailer','demo','retailer'),(236,'member','demo','member'),(237,'spare part master data','demo','sparepartmasterdata'),(238,'spare part upc','demo','sparepartupc'),(239,'spare part point','demo','sparepartpoint'),(240,'accumulation request','demo','accumulationrequest'),(241,'partner','demo','partner'),(242,'product catalog','demo','productcatalog'),(243,'redemption request','demo','redemptionrequest'),(244,'welcome kit','demo','welcomekit'),(245,'date dimension','demo','datedimension'),(246,'coupon fact','demo','couponfact'),(247,'loyalty sla','demo','loyaltysla'),(248,'comment thread','demo','commentthread'),(249,'discrepant accumulation','demo','discrepantaccumulation'),(250,'industry','afterbuy','industry'),(251,'brand','afterbuy','brand'),(252,'brand product category','afterbuy','brandproductcategory'),(253,'product type','afterbuy','producttype'),(254,'consumer','afterbuy','consumer'),(255,'user product','afterbuy','userproduct'),(256,'product support','afterbuy','productsupport'),(257,'registration certificate','afterbuy','registrationcertificate'),(258,'product insurance info','afterbuy','productinsuranceinfo'),(259,'product warranty info','afterbuy','productwarrantyinfo'),(260,'pollution certificate','afterbuy','pollutioncertificate'),(261,'license','afterbuy','license'),(262,'invoice','afterbuy','invoice'),(263,'support','afterbuy','support'),(264,'product specification','afterbuy','productspecification'),(265,'product feature','afterbuy','productfeature'),(266,'recommended part','afterbuy','recommendedpart'),(267,'otp token','afterbuy','otptoken'),(268,'user notification','afterbuy','usernotification'),(269,'user mobile info','afterbuy','usermobileinfo'),(270,'user preference','afterbuy','userpreference'),(271,'brand preference','afterbuy','brandpreference'),(272,'interest','afterbuy','interest'),(273,'sell information','afterbuy','sellinformation'),(274,'user product images','afterbuy','userproductimages'),(275,'service type','afterbuy','servicetype'),(276,'service','afterbuy','service'),(277,'message template','afterbuy','messagetemplate'),(278,'email template','afterbuy','emailtemplate'),(279,'sms log','afterbuy','smslog'),(280,'email log','afterbuy','emaillog'),(281,'audit log','afterbuy','auditlog'),(282,'constant','afterbuy','constant'),(283,'email token','afterbuy','emailtoken'),(284,'service center location','afterbuy','servicecenterlocation'),(285,'service history','afterbuy','servicehistory'),(286,'task state','djcelery','taskmeta'),(287,'saved group result','djcelery','tasksetmeta'),(288,'interval','djcelery','intervalschedule'),(289,'crontab','djcelery','crontabschedule'),(290,'periodic tasks','djcelery','periodictasks'),(291,'periodic task','djcelery','periodictask'),(292,'worker','djcelery','workerstate'),(293,'task','djcelery','taskstate'),(294,'TOTP device','otp_totp','totpdevice'),(295,'national sales manager','core','nationalsalesmanager'),(296,'national sales manager','bajaj','nationalsalesmanager'),(297,'brand product category','bajajib','brandproductcategory'),(298,'user profile','bajajib','userprofile'),(299,'country','bajajib','country'),(300,'country distributor','bajajib','countrydistributor'),(301,'main country dealer','bajajib','maincountrydealer'),(302,'dealer','bajajib','dealer'),(303,'service advisor','bajajib','serviceadvisor'),(304,'product type','bajajib','producttype'),(305,'product data','bajajib','productdata'),(306,'fleet rider','bajajib','fleetrider'),(307,'coupon data','bajajib','coupondata'),(308,'service advisor coupon relationship','bajajib','serviceadvisorcouponrelationship'),(309,'ucn recovery','bajajib','ucnrecovery'),(310,'otp token','bajajib','otptoken'),(311,'message template','bajajib','messagetemplate'),(312,'email template','bajajib','emailtemplate'),(313,'sms log','bajajib','smslog'),(314,'email log','bajajib','emaillog'),(315,'data feed log','bajajib','datafeedlog'),(316,'feed failure log','bajajib','feedfailurelog'),(317,'vin sync feed log','bajajib','vinsyncfeedlog'),(318,'constant','bajajib','constant'),(319,'customer update history','bajajib','customerupdatehistory'),(320,'dsr work allocation','core','dsrworkallocation'),(321,'dsr work allocation','bajaj','dsrworkallocation'),(322,'order part','bajaj','orderpart'),(323,'order part','core','orderpart'),(324,'part pricing','core','partpricing'),(325,'part pricing','bajaj','partpricing'),(326,'part models','core','partmodels'),(327,'categories','core','categories'),(328,'sub categories','core','subcategories'),(329,'part models','bajaj','partmodels'),(330,'categories','bajaj','categories'),(331,'sub categories','bajaj','subcategories');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('10jm636qvnic5ztiqhtbpjikogi3js1t','MzI4OTMzYzljMmVmNTIzMWQzNjVlZTQ4NzAyNWU2MDI1NmM0ZTA2OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MTJ9','2015-10-08 10:47:37'),('1pwv2nk7bmdkt3ojyamf9ukmwj5bv5bw','NjQ5ZDRhMmZiY2VlMjM4NTkwMjZkMGMzNTBlNWQ0ZWM0Nzc2Y2YyODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NDd9','2015-10-13 18:09:24'),('3ay4ghbya9vz6o23199uprhyufb02dnk','NTc5ZDczZDhhNTNlNGMxNTNiMmQ4YjNkOGE5YmQxNzQ3MzM5NmIyYTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-10-16 07:26:22'),('55l4t209svy0nvl5oeky1lig4u8r5w1q','MjcyMjdiYmUxMDMzY2JiNDc5YWVmOTFlOWZhYzVjMTlkOGYxYzZkMDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6Mzl9','2015-10-06 06:19:39'),('8tajkyrufsey922xomo82clhcgtukbso','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-10-09 09:11:24'),('9s7nfdc7sfbh0u3h4ylrwik4z7e1629t','NTc5ZDczZDhhNTNlNGMxNTNiMmQ4YjNkOGE5YmQxNzQ3MzM5NmIyYTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-09-23 16:05:19'),('fkfuwx2gjvornozghcrcxugcsfu3ii6y','MzI4OTMzYzljMmVmNTIzMWQzNjVlZTQ4NzAyNWU2MDI1NmM0ZTA2OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MTJ9','2015-09-23 10:18:51'),('hyvgonexntng7gf54nvhl1mg6e4zmwj4','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-09-07 04:10:28'),('j4zpcz1oncks5tn6tjhms5qyld2iv8lh','MmM5YWJlMWI3YjhkYjg0ZmFkNDQxNDdiODNmN2YxYmRkZjk5YTFlODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MTN9','2015-09-21 10:11:43'),('jnrafszm6ivzdixuwv8d6jrvshrrt6th','ODA3MTVjMDA0OTIzMzgzYWMwNjkyMzIzMDZjMGRkOGM2MmY2NjYyMzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MjB9','2015-09-22 17:57:11'),('jqfz53hucctkk7q5rk4arhuqco9ugnu2','NTc5ZDczZDhhNTNlNGMxNTNiMmQ4YjNkOGE5YmQxNzQ3MzM5NmIyYTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-10-12 08:02:49'),('marbfhb5jfx8zp4iofoqey1m8191yv2i','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-10-14 08:50:36'),('mvgshd6soe466ui1xdowndplm2tvxnzy','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-09-22 17:38:09'),('olj6zym5wa1hf6ufdyplksrpg8d31fx2','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-09-26 12:21:10'),('rv5qxo242mwcfh6bmwr602yhn3a76slu','MzI4OTMzYzljMmVmNTIzMWQzNjVlZTQ4NzAyNWU2MDI1NmM0ZTA2OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MTJ9','2015-10-05 04:55:56'),('rz2xtpnaqdyavbs5f5p7faimqcdmxcwf','MzI4OTMzYzljMmVmNTIzMWQzNjVlZTQ4NzAyNWU2MDI1NmM0ZTA2OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MTJ9','2015-09-23 05:26:18'),('syv7g08hpiods22rozweu0zafjvohtwv','NjQ5ZDRhMmZiY2VlMjM4NTkwMjZkMGMzNTBlNWQ0ZWM0Nzc2Y2YyODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NDd9','2015-10-14 06:14:15'),('wadtxox44gk5ka3wicjjnos3skzf0vyo','NTc5ZDczZDhhNTNlNGMxNTNiMmQ4YjNkOGE5YmQxNzQ3MzM5NmIyYTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2015-10-15 05:27:58'),('x7pnl25zcvxnvw9hfcptmbbqmemv684o','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-10-13 06:29:53'),('z5q6ak3p1tz2q91olhlva0dxlop7d8b3','NjQ5ZDRhMmZiY2VlMjM4NTkwMjZkMGMzNTBlNWQ0ZWM0Nzc2Y2YyODp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6NDd9','2015-10-13 18:18:26');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_crontabschedule`
--

DROP TABLE IF EXISTS `djcelery_crontabschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_crontabschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `minute` varchar(64) NOT NULL,
  `hour` varchar(64) NOT NULL,
  `day_of_week` varchar(64) NOT NULL,
  `day_of_month` varchar(64) NOT NULL,
  `month_of_year` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_crontabschedule`
--

LOCK TABLES `djcelery_crontabschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_crontabschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_crontabschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_intervalschedule`
--

DROP TABLE IF EXISTS `djcelery_intervalschedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_intervalschedule` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `every` int(11) NOT NULL,
  `period` varchar(24) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_intervalschedule`
--

LOCK TABLES `djcelery_intervalschedule` WRITE;
/*!40000 ALTER TABLE `djcelery_intervalschedule` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_intervalschedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictask`
--

DROP TABLE IF EXISTS `djcelery_periodictask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `task` varchar(200) NOT NULL,
  `interval_id` int(11) DEFAULT NULL,
  `crontab_id` int(11) DEFAULT NULL,
  `args` longtext NOT NULL,
  `kwargs` longtext NOT NULL,
  `queue` varchar(200) DEFAULT NULL,
  `exchange` varchar(200) DEFAULT NULL,
  `routing_key` varchar(200) DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `enabled` tinyint(1) NOT NULL,
  `last_run_at` datetime DEFAULT NULL,
  `total_run_count` int(10) unsigned NOT NULL,
  `date_changed` datetime NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `djcelery_periodictask_8905f60d` (`interval_id`),
  KEY `djcelery_periodictask_7280124f` (`crontab_id`),
  CONSTRAINT `crontab_id_refs_id_286da0d1` FOREIGN KEY (`crontab_id`) REFERENCES `djcelery_crontabschedule` (`id`),
  CONSTRAINT `interval_id_refs_id_1829f358` FOREIGN KEY (`interval_id`) REFERENCES `djcelery_intervalschedule` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictask`
--

LOCK TABLES `djcelery_periodictask` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictask` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_periodictasks`
--

DROP TABLE IF EXISTS `djcelery_periodictasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_periodictasks` (
  `ident` smallint(6) NOT NULL,
  `last_update` datetime NOT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_periodictasks`
--

LOCK TABLES `djcelery_periodictasks` WRITE;
/*!40000 ALTER TABLE `djcelery_periodictasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_periodictasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_taskstate`
--

DROP TABLE IF EXISTS `djcelery_taskstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_taskstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` varchar(64) NOT NULL,
  `task_id` varchar(36) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `tstamp` datetime NOT NULL,
  `args` longtext,
  `kwargs` longtext,
  `eta` datetime DEFAULT NULL,
  `expires` datetime DEFAULT NULL,
  `result` longtext,
  `traceback` longtext,
  `runtime` double DEFAULT NULL,
  `retries` int(11) NOT NULL,
  `worker_id` int(11) DEFAULT NULL,
  `hidden` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `djcelery_taskstate_5654bf12` (`state`),
  KEY `djcelery_taskstate_4da47e07` (`name`),
  KEY `djcelery_taskstate_abaacd02` (`tstamp`),
  KEY `djcelery_taskstate_cac6a03d` (`worker_id`),
  KEY `djcelery_taskstate_2ff6b945` (`hidden`),
  CONSTRAINT `worker_id_refs_id_6fd8ce95` FOREIGN KEY (`worker_id`) REFERENCES `djcelery_workerstate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_taskstate`
--

LOCK TABLES `djcelery_taskstate` WRITE;
/*!40000 ALTER TABLE `djcelery_taskstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_taskstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `djcelery_workerstate`
--

DROP TABLE IF EXISTS `djcelery_workerstate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `djcelery_workerstate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(255) NOT NULL,
  `last_heartbeat` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `hostname` (`hostname`),
  KEY `djcelery_workerstate_11e400ef` (`last_heartbeat`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `djcelery_workerstate`
--

LOCK TABLES `djcelery_workerstate` WRITE;
/*!40000 ALTER TABLE `djcelery_workerstate` DISABLE KEYS */;
/*!40000 ALTER TABLE `djcelery_workerstate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_accumulationrequest`
--

DROP TABLE IF EXISTS `gm_accumulationrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_accumulationrequest` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `points` int(11) NOT NULL,
  `total_points` int(11) NOT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `is_transferred` tinyint(1) NOT NULL,
  `member_id` int(11) NOT NULL,
  `asm_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `gm_accumulationrequest_b3c09425` (`member_id`),
  KEY `gm_accumulationrequest_dae8f18d` (`asm_id`),
  CONSTRAINT `asm_id_refs_id_eb867905` FOREIGN KEY (`asm_id`) REFERENCES `gm_areasparesmanager` (`id`),
  CONSTRAINT `member_id_refs_id_0ee003a9` FOREIGN KEY (`member_id`) REFERENCES `gm_member` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_accumulationrequest`
--

LOCK TABLES `gm_accumulationrequest` WRITE;
/*!40000 ALTER TABLE `gm_accumulationrequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_accumulationrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_accumulationrequest_upcs`
--

DROP TABLE IF EXISTS `gm_accumulationrequest_upcs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_accumulationrequest_upcs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `accumulationrequest_id` int(11) NOT NULL,
  `sparepartupc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accumulationrequest_id` (`accumulationrequest_id`,`sparepartupc_id`),
  KEY `gm_accumulationrequest_upcs_d2480668` (`accumulationrequest_id`),
  KEY `gm_accumulationrequest_upcs_2c265bc6` (`sparepartupc_id`),
  CONSTRAINT `accumulationrequest_id_refs_transaction_id_c454b804` FOREIGN KEY (`accumulationrequest_id`) REFERENCES `gm_accumulationrequest` (`transaction_id`),
  CONSTRAINT `sparepartupc_id_refs_id_6f71b85b` FOREIGN KEY (`sparepartupc_id`) REFERENCES `gm_sparepartupc` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_accumulationrequest_upcs`
--

LOCK TABLES `gm_accumulationrequest_upcs` WRITE;
/*!40000 ALTER TABLE `gm_accumulationrequest_upcs` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_accumulationrequest_upcs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_activity`
--

DROP TABLE IF EXISTS `gm_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_activity` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `action` longtext,
  `original_value` varchar(512) DEFAULT NULL,
  `new_value` varchar(512) DEFAULT NULL,
  `feedback_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_activity_dd2727aa` (`feedback_id`),
  KEY `gm_activity_6340c63c` (`user_id`),
  CONSTRAINT `feedback_id_refs_id_048477b4` FOREIGN KEY (`feedback_id`) REFERENCES `gm_feedback` (`id`),
  CONSTRAINT `user_id_refs_id_d7cae180` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_activity`
--

LOCK TABLES `gm_activity` WRITE;
/*!40000 ALTER TABLE `gm_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_areasalesmanager`
--

DROP TABLE IF EXISTS `gm_areasalesmanager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_areasalesmanager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `rm_id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `nsm_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `gm_areasalesmanager_59c17353` (`rm_id`),
  CONSTRAINT `rm_id_refs_id_e278611d` FOREIGN KEY (`rm_id`) REFERENCES `gm_regionalmanager` (`id`),
  CONSTRAINT `user_id_refs_user_id_ffe86796` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_areasalesmanager`
--

LOCK TABLES `gm_areasalesmanager` WRITE;
/*!40000 ALTER TABLE `gm_areasalesmanager` DISABLE KEYS */;
INSERT INTO `gm_areasalesmanager` VALUES (2,'2015-09-28 06:32:10','2015-09-28 06:32:10',51,NULL,'ranjan','ranjan@bajajauto.in','+918077777756',NULL);
/*!40000 ALTER TABLE `gm_areasalesmanager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_areasalesmanager_state`
--

DROP TABLE IF EXISTS `gm_areasalesmanager_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_areasalesmanager_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `areasalesmanager_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `areasalesmanager_id` (`areasalesmanager_id`,`state_id`),
  KEY `gm_areasalesmanager_state_65c89126` (`areasalesmanager_id`),
  KEY `gm_areasalesmanager_state_5654bf12` (`state_id`),
  CONSTRAINT `areasalesmanager_id_refs_id_477b7de9` FOREIGN KEY (`areasalesmanager_id`) REFERENCES `gm_areasalesmanager` (`id`),
  CONSTRAINT `state_id_refs_id_d951f239` FOREIGN KEY (`state_id`) REFERENCES `gm_state` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_areasalesmanager_state`
--

LOCK TABLES `gm_areasalesmanager_state` WRITE;
/*!40000 ALTER TABLE `gm_areasalesmanager_state` DISABLE KEYS */;
INSERT INTO `gm_areasalesmanager_state` VALUES (2,2,3);
/*!40000 ALTER TABLE `gm_areasalesmanager_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_areaservicemanager`
--

DROP TABLE IF EXISTS `gm_areaservicemanager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_areaservicemanager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `asm_id` varchar(50) NOT NULL,
  `area` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `zsm_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asm_id` (`asm_id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `gm_areaservicemanager_0bed366b` (`zsm_id`),
  CONSTRAINT `user_id_refs_user_id_bf232f2a` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `zsm_id_refs_id_23d39ec9` FOREIGN KEY (`zsm_id`) REFERENCES `gm_zonalservicemanager` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_areaservicemanager`
--

LOCK TABLES `gm_areaservicemanager` WRITE;
/*!40000 ALTER TABLE `gm_areaservicemanager` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_areaservicemanager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_areasparesmanager`
--

DROP TABLE IF EXISTS `gm_areasparesmanager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_areasparesmanager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `asm_id` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `nsm_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `asm_id` (`asm_id`),
  KEY `gm_areasparesmanager_6340c63c` (`user_id`),
  KEY `gm_areasparesmanager_04089bee` (`nsm_id`),
  CONSTRAINT `nsm_id_refs_id_11a233d9` FOREIGN KEY (`nsm_id`) REFERENCES `gm_nationalsparesmanager` (`id`),
  CONSTRAINT `user_id_refs_user_id_192897bb` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_areasparesmanager`
--

LOCK TABLES `gm_areasparesmanager` WRITE;
/*!40000 ALTER TABLE `gm_areasparesmanager` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_areasparesmanager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_areasparesmanager_state`
--

DROP TABLE IF EXISTS `gm_areasparesmanager_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_areasparesmanager_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `areasparesmanager_id` int(11) NOT NULL,
  `state_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `areasparesmanager_id` (`areasparesmanager_id`,`state_id`),
  KEY `gm_areasparesmanager_state_6bcf4a52` (`areasparesmanager_id`),
  KEY `gm_areasparesmanager_state_5654bf12` (`state_id`),
  CONSTRAINT `areasparesmanager_id_refs_id_ad013840` FOREIGN KEY (`areasparesmanager_id`) REFERENCES `gm_areasparesmanager` (`id`),
  CONSTRAINT `state_id_refs_id_01dc1b50` FOREIGN KEY (`state_id`) REFERENCES `gm_state` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_areasparesmanager_state`
--

LOCK TABLES `gm_areasparesmanager_state` WRITE;
/*!40000 ALTER TABLE `gm_areasparesmanager_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_areasparesmanager_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_asctempregistration`
--

DROP TABLE IF EXISTS `gm_asctempregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_asctempregistration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `pincode` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `dealer_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_asctempregistration`
--

LOCK TABLES `gm_asctempregistration` WRITE;
/*!40000 ALTER TABLE `gm_asctempregistration` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_asctempregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_auditlog`
--

DROP TABLE IF EXISTS `gm_auditlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_auditlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `device` varchar(250) DEFAULT NULL,
  `user_agent` varchar(250) DEFAULT NULL,
  `urls` varchar(250) NOT NULL,
  `access_token` varchar(250) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_auditlog_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_e3905dbc` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_auditlog`
--

LOCK TABLES `gm_auditlog` WRITE;
/*!40000 ALTER TABLE `gm_auditlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_auditlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_authorizedservicecenter`
--

DROP TABLE IF EXISTS `gm_authorizedservicecenter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_authorizedservicecenter` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `asc_id` varchar(25) NOT NULL,
  `asc_owner` varchar(100) DEFAULT NULL,
  `asc_owner_phone` varchar(50) DEFAULT NULL,
  `asc_owner_email` varchar(100) DEFAULT NULL,
  `last_transaction_date` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `dealer_id` int(11) DEFAULT NULL,
  `asm_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `asc_id` (`asc_id`),
  KEY `gm_authorizedservicecenter_f65f7b5d` (`dealer_id`),
  KEY `gm_authorizedservicecenter_dae8f18d` (`asm_id`),
  CONSTRAINT `asm_id_refs_id_dea638d3` FOREIGN KEY (`asm_id`) REFERENCES `gm_areaservicemanager` (`id`),
  CONSTRAINT `dealer_id_refs_user_id_77b70a48` FOREIGN KEY (`dealer_id`) REFERENCES `gm_dealer` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_adb8c76a` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_authorizedservicecenter`
--

LOCK TABLES `gm_authorizedservicecenter` WRITE;
/*!40000 ALTER TABLE `gm_authorizedservicecenter` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_authorizedservicecenter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_bomheader`
--

DROP TABLE IF EXISTS `gm_bomheader`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_bomheader` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `sku_code` varchar(20) DEFAULT NULL,
  `plant` varchar(10) DEFAULT NULL,
  `bom_type` varchar(10) DEFAULT NULL,
  `bom_number` varchar(10) DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  `created_on` date DEFAULT NULL,
  `revision_number` int(11) NOT NULL,
  `eco_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_bomheader`
--

LOCK TABLES `gm_bomheader` WRITE;
/*!40000 ALTER TABLE `gm_bomheader` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_bomheader` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_bompart`
--

DROP TABLE IF EXISTS `gm_bompart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_bompart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `timestamp` datetime NOT NULL,
  `part_number` varchar(20) DEFAULT NULL,
  `revision_number` varchar(10) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_bompart`
--

LOCK TABLES `gm_bompart` WRITE;
/*!40000 ALTER TABLE `gm_bompart` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_bompart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_bomplate`
--

DROP TABLE IF EXISTS `gm_bomplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_bomplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `plate_id` varchar(50) NOT NULL,
  `plate_txt` varchar(200) DEFAULT NULL,
  `plate_image` varchar(255) DEFAULT NULL,
  `plate_image_with_part` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `plate_id` (`plate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_bomplate`
--

LOCK TABLES `gm_bomplate` WRITE;
/*!40000 ALTER TABLE `gm_bomplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_bomplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_bomplatepart`
--

DROP TABLE IF EXISTS `gm_bomplatepart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_bomplatepart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `quantity` varchar(20) DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `valid_to` date DEFAULT NULL,
  `uom` varchar(100) DEFAULT NULL,
  `serial_number` varchar(20) DEFAULT NULL,
  `change_number` varchar(12) DEFAULT NULL,
  `change_number_to` varchar(12) DEFAULT NULL,
  `item` varchar(10) DEFAULT NULL,
  `item_id` varchar(10) DEFAULT NULL,
  `bom_id` int(11) NOT NULL,
  `plate_id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_bomplatepart_1b066e1a` (`bom_id`),
  KEY `gm_bomplatepart_fa6448c6` (`plate_id`),
  KEY `gm_bomplatepart_8c28136d` (`part_id`),
  CONSTRAINT `bom_id_refs_id_df9dddce` FOREIGN KEY (`bom_id`) REFERENCES `gm_bomheader` (`id`),
  CONSTRAINT `part_id_refs_id_e473efb5` FOREIGN KEY (`part_id`) REFERENCES `gm_bompart` (`id`),
  CONSTRAINT `plate_id_refs_id_76e0311d` FOREIGN KEY (`plate_id`) REFERENCES `gm_bomplate` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_bomplatepart`
--

LOCK TABLES `gm_bomplatepart` WRITE;
/*!40000 ALTER TABLE `gm_bomplatepart` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_bomplatepart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_bomvisualization`
--

DROP TABLE IF EXISTS `gm_bomvisualization`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_bomvisualization` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `x_coordinate` int(11) NOT NULL,
  `y_coordinate` int(11) NOT NULL,
  `z_coordinate` int(11) NOT NULL,
  `serial_number` int(11) NOT NULL,
  `part_href` varchar(200) NOT NULL,
  `status` varchar(25) DEFAULT NULL,
  `published_date` datetime DEFAULT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `bom_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_bomvisualization_1b066e1a` (`bom_id`),
  CONSTRAINT `bom_id_refs_id_8819d2ed` FOREIGN KEY (`bom_id`) REFERENCES `gm_bomplatepart` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_bomvisualization`
--

LOCK TABLES `gm_bomvisualization` WRITE;
/*!40000 ALTER TABLE `gm_bomvisualization` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_bomvisualization` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_branddepartment`
--

DROP TABLE IF EXISTS `gm_branddepartment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_branddepartment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_branddepartment`
--

LOCK TABLES `gm_branddepartment` WRITE;
/*!40000 ALTER TABLE `gm_branddepartment` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_branddepartment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_brandproductcategory`
--

DROP TABLE IF EXISTS `gm_brandproductcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_brandproductcategory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(250) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_brandproductcategory`
--

LOCK TABLES `gm_brandproductcategory` WRITE;
/*!40000 ALTER TABLE `gm_brandproductcategory` DISABLE KEYS */;
INSERT INTO `gm_brandproductcategory` VALUES (1,'2014-12-20 08:32:42','2014-12-20 08:32:42','dunlop','tyre manufacturer');
/*!40000 ALTER TABLE `gm_brandproductcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_brandproductrange`
--

DROP TABLE IF EXISTS `gm_brandproductrange`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_brandproductrange` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `sku_code` varchar(50) NOT NULL,
  `description` longtext,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sku_code` (`sku_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_brandproductrange`
--

LOCK TABLES `gm_brandproductrange` WRITE;
/*!40000 ALTER TABLE `gm_brandproductrange` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_brandproductrange` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_brandvertical`
--

DROP TABLE IF EXISTS `gm_brandvertical`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_brandvertical` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_brandvertical`
--

LOCK TABLES `gm_brandvertical` WRITE;
/*!40000 ALTER TABLE `gm_brandvertical` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_brandvertical` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_categories`
--

DROP TABLE IF EXISTS `gm_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `category_name` varchar(255) NOT NULL,
  `short_name` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `style_class` varchar(255) DEFAULT NULL,
  `part_model_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `group_by` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_categories_24dcb168` (`part_model_id`),
  CONSTRAINT `part_model_id_refs_id_eb276dc6` FOREIGN KEY (`part_model_id`) REFERENCES `gm_partmodels` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_categories`
--

LOCK TABLES `gm_categories` WRITE;
/*!40000 ALTER TABLE `gm_categories` DISABLE KEYS */;
INSERT INTO `gm_categories` VALUES (1,'0000-00-00 00:00:00','0000-00-00 00:00:00','COMPACT','BA','compact-landing.png','',1,1,'COMPACT'),(2,'0000-00-00 00:00:00','0000-00-00 00:00:00','COMPACT','BA','compact-4s-img.png','double_line',1,1,'COMPACT'),(3,'0000-00-00 00:00:00','0000-00-00 00:00:00','OPTIMA','BH','optima-diesel.PNG','',1,1,'OPTIMA'),(4,'0000-00-00 00:00:00','0000-00-00 00:00:00','MAXIMA','BB','maxima-diesel.png','',1,1,'MAXIMA'),(5,'0000-00-00 00:00:00','0000-00-00 00:00:00','COMPACT 2S ES','24','compact-landing.png','',2,1,'ES'),(6,'0000-00-00 00:00:00','0000-00-00 00:00:00','COMPACT 2S ES','AG','compact-landing.png','',2,1,'ES'),(7,'0000-00-00 00:00:00','0000-00-00 00:00:00','COMPACT 2S ES','AS','compact-landing.png','',2,1,'ES'),(8,'0000-00-00 00:00:00','0000-00-00 00:00:00','COMPACT 2S NES','24','compact-landing.png','',2,1,'NES'),(9,'0000-00-00 00:00:00','0000-00-00 00:00:00','COMPACT 2S NES','AG','compact-landing.png','',2,1,'NES'),(10,'0000-00-00 00:00:00','0000-00-00 00:00:00','COMPACT 2S NES','AS','compact-landing.png','',2,1,'NES');
/*!40000 ALTER TABLE `gm_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_cdmsdata`
--

DROP TABLE IF EXISTS `gm_cdmsdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_cdmsdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `received_date` datetime DEFAULT NULL,
  `cdms_date` datetime DEFAULT NULL,
  `cdms_doc_number` varchar(25) DEFAULT NULL,
  `remarks` varchar(250) DEFAULT NULL,
  `unique_service_coupon_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_cdmsdata_49ac3df4` (`unique_service_coupon_id`),
  CONSTRAINT `unique_service_coupon_id_refs_id_d9c86c37` FOREIGN KEY (`unique_service_coupon_id`) REFERENCES `gm_coupondata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_cdmsdata`
--

LOCK TABLES `gm_cdmsdata` WRITE;
/*!40000 ALTER TABLE `gm_cdmsdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_cdmsdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_circlehead`
--

DROP TABLE IF EXISTS `gm_circlehead`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_circlehead` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_745745fc` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_circlehead`
--

LOCK TABLES `gm_circlehead` WRITE;
/*!40000 ALTER TABLE `gm_circlehead` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_circlehead` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_city`
--

DROP TABLE IF EXISTS `gm_city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `city` varchar(50) NOT NULL,
  `state_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `city` (`city`),
  KEY `gm_city_5654bf12` (`state_id`),
  CONSTRAINT `state_id_refs_id_579431c3` FOREIGN KEY (`state_id`) REFERENCES `gm_state` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_city`
--

LOCK TABLES `gm_city` WRITE;
/*!40000 ALTER TABLE `gm_city` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_city` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_comment`
--

DROP TABLE IF EXISTS `gm_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `user` varchar(20) NOT NULL,
  `comment` varchar(100) DEFAULT NULL,
  `file_location` varchar(215) DEFAULT NULL,
  `feedback_object_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_comment_cb2fd4f1` (`feedback_object_id`),
  CONSTRAINT `feedback_object_id_refs_id_051fc69b` FOREIGN KEY (`feedback_object_id`) REFERENCES `gm_feedback` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_comment`
--

LOCK TABLES `gm_comment` WRITE;
/*!40000 ALTER TABLE `gm_comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_commentthread`
--

DROP TABLE IF EXISTS `gm_commentthread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_commentthread` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` longtext,
  `is_edited` tinyint(1) NOT NULL,
  `welcome_kit_id` int(11) DEFAULT NULL,
  `redemption_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_commentthread_b2e83d57` (`welcome_kit_id`),
  KEY `gm_commentthread_57d79184` (`redemption_id`),
  KEY `gm_commentthread_6340c63c` (`user_id`),
  CONSTRAINT `redemption_id_refs_transaction_id_a5a677f5` FOREIGN KEY (`redemption_id`) REFERENCES `gm_redemptionrequest` (`transaction_id`),
  CONSTRAINT `user_id_refs_id_d9f0d698` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `welcome_kit_id_refs_transaction_id_83d3936d` FOREIGN KEY (`welcome_kit_id`) REFERENCES `gm_welcomekit` (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_commentthread`
--

LOCK TABLES `gm_commentthread` WRITE;
/*!40000 ALTER TABLE `gm_commentthread` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_commentthread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_constant`
--

DROP TABLE IF EXISTS `gm_constant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_constant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `constant_name` varchar(50) DEFAULT NULL,
  `constant_value` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `constant_name` (`constant_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_constant`
--

LOCK TABLES `gm_constant` WRITE;
/*!40000 ALTER TABLE `gm_constant` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_constant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_containerindent`
--

DROP TABLE IF EXISTS `gm_containerindent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_containerindent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `indent_num` varchar(30) NOT NULL,
  `no_of_containers` int(11) NOT NULL,
  `status` varchar(12) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `indent_num` (`indent_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_containerindent`
--

LOCK TABLES `gm_containerindent` WRITE;
/*!40000 ALTER TABLE `gm_containerindent` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_containerindent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_containerlr`
--

DROP TABLE IF EXISTS `gm_containerlr`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_containerlr` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `consignment_id` varchar(30) DEFAULT NULL,
  `truck_no` varchar(30) DEFAULT NULL,
  `lr_number` varchar(20) DEFAULT NULL,
  `lr_date` date DEFAULT NULL,
  `do_num` varchar(30) DEFAULT NULL,
  `gatein_date` date DEFAULT NULL,
  `gatein_time` time DEFAULT NULL,
  `seal_no` varchar(40) DEFAULT NULL,
  `container_no` varchar(40) DEFAULT NULL,
  `shippingline_id` varchar(50) DEFAULT NULL,
  `ib_dispatch_dt` date DEFAULT NULL,
  `cts_created_date` date DEFAULT NULL,
  `submitted_by` varchar(50) DEFAULT NULL,
  `status` varchar(12) NOT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `partner_name` varchar(50) DEFAULT NULL,
  `zib_indent_num_id` int(11) NOT NULL,
  `transporter_id` int(11) NOT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `gm_containerlr_8d3d8c42` (`zib_indent_num_id`),
  KEY `gm_containerlr_c7d7fc7d` (`transporter_id`),
  CONSTRAINT `transporter_id_refs_id_d55cee48` FOREIGN KEY (`transporter_id`) REFERENCES `gm_transporter` (`id`),
  CONSTRAINT `zib_indent_num_id_refs_id_a980d566` FOREIGN KEY (`zib_indent_num_id`) REFERENCES `gm_containerindent` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_containerlr`
--

LOCK TABLES `gm_containerlr` WRITE;
/*!40000 ALTER TABLE `gm_containerlr` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_containerlr` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_containertracker`
--

DROP TABLE IF EXISTS `gm_containertracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_containertracker` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `zib_indent_num` varchar(30) DEFAULT NULL,
  `consignment_id` varchar(30) DEFAULT NULL,
  `truck_no` varchar(30) DEFAULT NULL,
  `lr_number` varchar(20) DEFAULT NULL,
  `lr_date` date DEFAULT NULL,
  `do_num` varchar(30) DEFAULT NULL,
  `gatein_date` date DEFAULT NULL,
  `gatein_time` time DEFAULT NULL,
  `status` varchar(12) NOT NULL,
  `seal_no` varchar(40) DEFAULT NULL,
  `container_no` varchar(40) DEFAULT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `submitted_by` varchar(50) DEFAULT NULL,
  `shippingline_id` varchar(50) DEFAULT NULL,
  `ib_dispatch_dt` date DEFAULT NULL,
  `cts_created_date` date DEFAULT NULL,
  `no_of_containers` int(11) NOT NULL,
  `transporter_id` int(11) NOT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `gm_containertracker_c7d7fc7d` (`transporter_id`),
  CONSTRAINT `transporter_id_refs_id_3dd97792` FOREIGN KEY (`transporter_id`) REFERENCES `gm_transporter` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_containertracker`
--

LOCK TABLES `gm_containertracker` WRITE;
/*!40000 ALTER TABLE `gm_containertracker` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_containertracker` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_coupondata`
--

DROP TABLE IF EXISTS `gm_coupondata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_coupondata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `unique_service_coupon` varchar(215) NOT NULL,
  `valid_days` int(11) NOT NULL,
  `valid_kms` int(11) NOT NULL,
  `service_type` int(11) NOT NULL,
  `status` smallint(6) NOT NULL,
  `closed_date` datetime DEFAULT NULL,
  `mark_expired_on` datetime DEFAULT NULL,
  `actual_service_date` datetime DEFAULT NULL,
  `actual_kms` varchar(10) DEFAULT NULL,
  `last_reminder_date` datetime DEFAULT NULL,
  `schedule_reminder_date` datetime DEFAULT NULL,
  `extended_date` datetime DEFAULT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `credit_date` datetime DEFAULT NULL,
  `credit_note` varchar(50) DEFAULT NULL,
  `special_case` tinyint(1) NOT NULL,
  `servicing_dealer` varchar(50) DEFAULT NULL,
  `product_id` int(11) NOT NULL,
  `service_advisor_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_service_coupon` (`unique_service_coupon`),
  KEY `gm_coupondata_48fb58bb` (`status`),
  KEY `gm_coupondata_7f1b40ad` (`product_id`),
  KEY `gm_coupondata_3758e01b` (`service_advisor_id`),
  CONSTRAINT `product_id_refs_id_b447d7b8` FOREIGN KEY (`product_id`) REFERENCES `gm_productdata` (`id`),
  CONSTRAINT `service_advisor_id_refs_user_id_f9cb3c7a` FOREIGN KEY (`service_advisor_id`) REFERENCES `gm_serviceadvisor` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_coupondata`
--

LOCK TABLES `gm_coupondata` WRITE;
/*!40000 ALTER TABLE `gm_coupondata` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_coupondata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_couponfact`
--

DROP TABLE IF EXISTS `gm_couponfact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_couponfact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `closed` bigint(20) NOT NULL,
  `inprogress` bigint(20) NOT NULL,
  `expired` bigint(20) NOT NULL,
  `unused` bigint(20) NOT NULL,
  `exceeds` bigint(20) NOT NULL,
  `data_type` varchar(20) NOT NULL,
  `date_id` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `date_id` (`date_id`,`data_type`),
  KEY `gm_couponfact_eeede814` (`date_id`),
  CONSTRAINT `date_id_refs_date_id_662588c8` FOREIGN KEY (`date_id`) REFERENCES `gm_datedimension` (`date_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_couponfact`
--

LOCK TABLES `gm_couponfact` WRITE;
/*!40000 ALTER TABLE `gm_couponfact` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_couponfact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_customertempregistration`
--

DROP TABLE IF EXISTS `gm_customertempregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_customertempregistration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `new_customer_name` varchar(50) DEFAULT NULL,
  `new_number` varchar(15) DEFAULT NULL,
  `dealer_asc_id` varchar(15) DEFAULT NULL,
  `product_purchase_date` datetime DEFAULT NULL,
  `temp_customer_id` varchar(50) NOT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `remarks` varchar(500) DEFAULT NULL,
  `tagged_sap_id` varchar(215) DEFAULT NULL,
  `mobile_number_update_count` int(11) DEFAULT NULL,
  `product_data_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `temp_customer_id` (`temp_customer_id`),
  UNIQUE KEY `tagged_sap_id` (`tagged_sap_id`),
  KEY `gm_customertempregistration_ca191704` (`product_data_id`),
  CONSTRAINT `product_data_id_refs_id_85c16668` FOREIGN KEY (`product_data_id`) REFERENCES `gm_productdata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_customertempregistration`
--

LOCK TABLES `gm_customertempregistration` WRITE;
/*!40000 ALTER TABLE `gm_customertempregistration` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_customertempregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_customerupdatefailure`
--

DROP TABLE IF EXISTS `gm_customerupdatefailure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_customerupdatefailure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `customer_name` varchar(50) NOT NULL,
  `customer_id` varchar(50) NOT NULL,
  `updated_by` varchar(50) NOT NULL,
  `old_number` varchar(15) NOT NULL,
  `new_number` varchar(15) NOT NULL,
  `email_flag` tinyint(1) NOT NULL,
  `product_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_customerupdatefailure_10a0e6a0` (`product_id_id`),
  CONSTRAINT `product_id_id_refs_id_31ee72a1` FOREIGN KEY (`product_id_id`) REFERENCES `gm_productdata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_customerupdatefailure`
--

LOCK TABLES `gm_customerupdatefailure` WRITE;
/*!40000 ALTER TABLE `gm_customerupdatefailure` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_customerupdatefailure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_customerupdatehistory`
--

DROP TABLE IF EXISTS `gm_customerupdatehistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_customerupdatehistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `updated_field` varchar(100) NOT NULL,
  `old_value` varchar(100) NOT NULL,
  `new_value` varchar(100) NOT NULL,
  `email_flag` tinyint(1) NOT NULL,
  `temp_customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_customerupdatehistory_4d5d9333` (`temp_customer_id`),
  CONSTRAINT `temp_customer_id_refs_id_dc27ddee` FOREIGN KEY (`temp_customer_id`) REFERENCES `gm_customertempregistration` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_customerupdatehistory`
--

LOCK TABLES `gm_customerupdatehistory` WRITE;
/*!40000 ALTER TABLE `gm_customerupdatehistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_customerupdatehistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_datafeedlog`
--

DROP TABLE IF EXISTS `gm_datafeedlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_datafeedlog` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `data_feed_id` int(11) NOT NULL AUTO_INCREMENT,
  `feed_type` varchar(50) NOT NULL,
  `total_data_count` int(11) NOT NULL,
  `failed_data_count` int(11) NOT NULL,
  `success_data_count` int(11) NOT NULL,
  `action` varchar(50) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `timestamp` datetime NOT NULL,
  `remarks` varchar(2048) DEFAULT NULL,
  `file_location` varchar(215) DEFAULT NULL,
  PRIMARY KEY (`data_feed_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_datafeedlog`
--

LOCK TABLES `gm_datafeedlog` WRITE;
/*!40000 ALTER TABLE `gm_datafeedlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_datafeedlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_datedimension`
--

DROP TABLE IF EXISTS `gm_datedimension`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_datedimension` (
  `date_id` bigint(20) NOT NULL,
  `date` date NOT NULL,
  `timestamp` datetime NOT NULL,
  `weekend` varchar(10) NOT NULL,
  `day_of_week` varchar(10) NOT NULL,
  `month` varchar(10) NOT NULL,
  `month_day` int(11) NOT NULL,
  `year` int(11) NOT NULL,
  `week_starting_monday` varchar(2) NOT NULL,
  PRIMARY KEY (`date_id`),
  UNIQUE KEY `date` (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_datedimension`
--

LOCK TABLES `gm_datedimension` WRITE;
/*!40000 ALTER TABLE `gm_datedimension` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_datedimension` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_dealer`
--

DROP TABLE IF EXISTS `gm_dealer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_dealer` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `dealer_id` varchar(25) NOT NULL,
  `use_cdms` tinyint(1) NOT NULL,
  `last_transaction_date` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `asm_id` int(11) DEFAULT NULL,
  `sm_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `dealer_id` (`dealer_id`),
  KEY `gm_dealer_dae8f18d` (`asm_id`),
  KEY `gm_dealer_3bdd8813` (`sm_id`),
  CONSTRAINT `asm_id_refs_id_f73bb336` FOREIGN KEY (`asm_id`) REFERENCES `gm_areaservicemanager` (`id`),
  CONSTRAINT `sm_id_refs_id_7196dc3a` FOREIGN KEY (`sm_id`) REFERENCES `gm_areasalesmanager` (`id`),
  CONSTRAINT `user_id_refs_user_id_861bfaa3` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_dealer`
--

LOCK TABLES `gm_dealer` WRITE;
/*!40000 ALTER TABLE `gm_dealer` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_dealer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_departmentsubcategories`
--

DROP TABLE IF EXISTS `gm_departmentsubcategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_departmentsubcategories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_departmentsubcategories_69d14838` (`department_id`),
  CONSTRAINT `department_id_refs_id_a5f1fd1c` FOREIGN KEY (`department_id`) REFERENCES `gm_branddepartment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_departmentsubcategories`
--

LOCK TABLES `gm_departmentsubcategories` WRITE;
/*!40000 ALTER TABLE `gm_departmentsubcategories` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_departmentsubcategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_discrepantaccumulation`
--

DROP TABLE IF EXISTS `gm_discrepantaccumulation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_discrepantaccumulation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `upc_id` int(11) NOT NULL,
  `new_member_id` int(11) NOT NULL,
  `accumulation_request_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_discrepantaccumulation_1037f587` (`upc_id`),
  KEY `gm_discrepantaccumulation_555096b4` (`new_member_id`),
  KEY `gm_discrepantaccumulation_ee7dc337` (`accumulation_request_id`),
  CONSTRAINT `accumulation_request_id_refs_transaction_id_2d21a456` FOREIGN KEY (`accumulation_request_id`) REFERENCES `gm_accumulationrequest` (`transaction_id`),
  CONSTRAINT `new_member_id_refs_id_8954529b` FOREIGN KEY (`new_member_id`) REFERENCES `gm_member` (`id`),
  CONSTRAINT `upc_id_refs_id_ea999ee6` FOREIGN KEY (`upc_id`) REFERENCES `gm_sparepartupc` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_discrepantaccumulation`
--

LOCK TABLES `gm_discrepantaccumulation` WRITE;
/*!40000 ALTER TABLE `gm_discrepantaccumulation` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_discrepantaccumulation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_distributor`
--

DROP TABLE IF EXISTS `gm_distributor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_distributor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `distributor_id` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `asm_id` int(11) DEFAULT NULL,
  `state_id` int(11) DEFAULT NULL,
  `territory` varchar(10) DEFAULT NULL,
  `mobile` varchar(10) DEFAULT NULL,
  `profile` varchar(15) DEFAULT NULL,
  `language` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_distributor_6340c63c` (`user_id`),
  KEY `gm_distributor_dae8f18d` (`asm_id`),
  KEY `gm_distributor_5654bf12` (`state_id`),
  CONSTRAINT `asm_id_refs_id_278c6a92` FOREIGN KEY (`asm_id`) REFERENCES `gm_areasparesmanager` (`id`),
  CONSTRAINT `state_id_refs_id_753fc724` FOREIGN KEY (`state_id`) REFERENCES `gm_state` (`id`),
  CONSTRAINT `user_id_refs_user_id_bb62621f` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_distributor`
--

LOCK TABLES `gm_distributor` WRITE;
/*!40000 ALTER TABLE `gm_distributor` DISABLE KEYS */;
INSERT INTO `gm_distributor` VALUES (10,'2015-09-25 09:20:36','2015-09-25 09:20:36','400001','shashank','ashish@bajajauto.in','+9102043232765','Pune',0,47,NULL,NULL,'west','9746344566','Distributor','marathi');
/*!40000 ALTER TABLE `gm_distributor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_distributorsalesrep`
--

DROP TABLE IF EXISTS `gm_distributorsalesrep`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_distributorsalesrep` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `distributor_sales_code` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `distributor_id` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_distributorsalesrep_6340c63c` (`user_id`),
  KEY `gm_distributorsalesrep_818f5865` (`distributor_id`),
  CONSTRAINT `distributor_id_refs_id_1410ee34` FOREIGN KEY (`distributor_id`) REFERENCES `gm_distributor` (`id`),
  CONSTRAINT `user_id_refs_user_id_1e769373` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_distributorsalesrep`
--

LOCK TABLES `gm_distributorsalesrep` WRITE;
/*!40000 ALTER TABLE `gm_distributorsalesrep` DISABLE KEYS */;
INSERT INTO `gm_distributorsalesrep` VALUES (7,'2015-09-25 09:47:19','2015-09-25 09:47:19','500001',1,46,10,'naveen@gladminds.co');
/*!40000 ALTER TABLE `gm_distributorsalesrep` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_distributorstaff`
--

DROP TABLE IF EXISTS `gm_distributorstaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_distributorstaff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `distributor_staff_code` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `distributor_id` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_distributorstaff_6340c63c` (`user_id`),
  KEY `gm_distributorstaff_818f5865` (`distributor_id`),
  CONSTRAINT `distributor_id_refs_id_841530ad` FOREIGN KEY (`distributor_id`) REFERENCES `gm_distributor` (`id`),
  CONSTRAINT `user_id_refs_user_id_2c82df01` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_distributorstaff`
--

LOCK TABLES `gm_distributorstaff` WRITE;
/*!40000 ALTER TABLE `gm_distributorstaff` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_distributorstaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_dsrworkallocation`
--

DROP TABLE IF EXISTS `gm_dsrworkallocation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_dsrworkallocation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `status` varchar(12) NOT NULL,
  `distributor_id` int(11) DEFAULT NULL,
  `retailer_id` int(11) DEFAULT NULL,
  `dsr_id` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_dsrworkallocation_818f5865` (`distributor_id`),
  KEY `gm_dsrworkallocation_64f72e30` (`retailer_id`),
  CONSTRAINT `distributor_id_refs_id_87f3180d` FOREIGN KEY (`distributor_id`) REFERENCES `gm_distributor` (`id`),
  CONSTRAINT `retailer_id_refs_id_270a146f` FOREIGN KEY (`retailer_id`) REFERENCES `gm_retailer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_dsrworkallocation`
--

LOCK TABLES `gm_dsrworkallocation` WRITE;
/*!40000 ALTER TABLE `gm_dsrworkallocation` DISABLE KEYS */;
INSERT INTO `gm_dsrworkallocation` VALUES (5,'2015-09-26 10:44:05','2015-09-26 10:44:05','Open',10,13,7,'2015-09-26 00:00:00');
/*!40000 ALTER TABLE `gm_dsrworkallocation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_ecoimplementation`
--

DROP TABLE IF EXISTS `gm_ecoimplementation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_ecoimplementation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `change_no` varchar(20) DEFAULT NULL,
  `change_date` date DEFAULT NULL,
  `change_time` time DEFAULT NULL,
  `plant` varchar(20) DEFAULT NULL,
  `action` varchar(20) DEFAULT NULL,
  `parent_part` varchar(20) DEFAULT NULL,
  `added_part` varchar(20) DEFAULT NULL,
  `added_part_qty` double DEFAULT NULL,
  `deleted_part` varchar(20) DEFAULT NULL,
  `deleted_part_qty` double DEFAULT NULL,
  `chassis_number` varchar(20) DEFAULT NULL,
  `engine_number` varchar(20) DEFAULT NULL,
  `eco_number` varchar(20) DEFAULT NULL,
  `reason_code` varchar(20) DEFAULT NULL,
  `remarks` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_ecoimplementation`
--

LOCK TABLES `gm_ecoimplementation` WRITE;
/*!40000 ALTER TABLE `gm_ecoimplementation` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_ecoimplementation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_ecorelease`
--

DROP TABLE IF EXISTS `gm_ecorelease`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_ecorelease` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `eco_number` varchar(20) DEFAULT NULL,
  `eco_release_date` date DEFAULT NULL,
  `eco_description` varchar(40) DEFAULT NULL,
  `action` varchar(20) DEFAULT NULL,
  `parent_part` varchar(20) DEFAULT NULL,
  `add_part` varchar(20) DEFAULT NULL,
  `add_part_qty` double DEFAULT NULL,
  `add_part_rev` varchar(20) DEFAULT NULL,
  `add_part_loc_code` varchar(90) DEFAULT NULL,
  `del_part` varchar(20) DEFAULT NULL,
  `del_part_qty` double DEFAULT NULL,
  `del_part_rev` double DEFAULT NULL,
  `del_part_loc_code` varchar(90) DEFAULT NULL,
  `models_applicable` varchar(90) DEFAULT NULL,
  `serviceability` varchar(20) DEFAULT NULL,
  `interchangebility` varchar(20) DEFAULT NULL,
  `reason_for_change` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_ecorelease`
--

LOCK TABLES `gm_ecorelease` WRITE;
/*!40000 ALTER TABLE `gm_ecorelease` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_ecorelease` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_emaillog`
--

DROP TABLE IF EXISTS `gm_emaillog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_emaillog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `subject` varchar(250) DEFAULT NULL,
  `message` longtext,
  `sender` varchar(100) DEFAULT NULL,
  `receiver` longtext NOT NULL,
  `cc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_emaillog`
--

LOCK TABLES `gm_emaillog` WRITE;
/*!40000 ALTER TABLE `gm_emaillog` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_emaillog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_emailtemplate`
--

DROP TABLE IF EXISTS `gm_emailtemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_emailtemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `template_key` varchar(255) NOT NULL,
  `sender` varchar(512) NOT NULL,
  `receiver` varchar(512) NOT NULL,
  `subject` varchar(512) NOT NULL,
  `body` varchar(512) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `template_key` (`template_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_emailtemplate`
--

LOCK TABLES `gm_emailtemplate` WRITE;
/*!40000 ALTER TABLE `gm_emailtemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_emailtemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_emailtoken`
--

DROP TABLE IF EXISTS `gm_emailtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_emailtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `activation_key` varchar(40) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_emailtoken_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_c8668983` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_emailtoken`
--

LOCK TABLES `gm_emailtoken` WRITE;
/*!40000 ALTER TABLE `gm_emailtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_emailtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_feedback`
--

DROP TABLE IF EXISTS `gm_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `summary` varchar(512) DEFAULT NULL,
  `description` varchar(512) DEFAULT NULL,
  `status` varchar(12) NOT NULL,
  `type` varchar(20) NOT NULL,
  `closed_date` datetime DEFAULT NULL,
  `resolved_date` datetime DEFAULT NULL,
  `pending_from` datetime DEFAULT NULL,
  `due_date` datetime DEFAULT NULL,
  `wait_time` double DEFAULT NULL,
  `remarks` varchar(512) DEFAULT NULL,
  `ratings` varchar(20) NOT NULL,
  `root_cause` varchar(20) NOT NULL,
  `resolution` varchar(512) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `assign_to_reporter` tinyint(1) NOT NULL,
  `assignee_created_date` datetime DEFAULT NULL,
  `reminder_date` datetime DEFAULT NULL,
  `reminder_flag` tinyint(1) NOT NULL,
  `resolution_flag` tinyint(1) NOT NULL,
  `file_location` varchar(215) DEFAULT NULL,
  `fcr` tinyint(1) NOT NULL,
  `priority` varchar(12) NOT NULL,
  `reporter_id` int(11) DEFAULT NULL,
  `assignee_id` int(11) DEFAULT NULL,
  `previous_assignee_id` int(11) DEFAULT NULL,
  `sub_department_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_feedback_146d8f29` (`reporter_id`),
  KEY `gm_feedback_98516953` (`assignee_id`),
  KEY `gm_feedback_4b4c122e` (`previous_assignee_id`),
  KEY `gm_feedback_d81e6292` (`sub_department_id`),
  CONSTRAINT `assignee_id_refs_id_8d45642a` FOREIGN KEY (`assignee_id`) REFERENCES `gm_servicedeskuser` (`id`),
  CONSTRAINT `previous_assignee_id_refs_id_8d45642a` FOREIGN KEY (`previous_assignee_id`) REFERENCES `gm_servicedeskuser` (`id`),
  CONSTRAINT `reporter_id_refs_id_8d45642a` FOREIGN KEY (`reporter_id`) REFERENCES `gm_servicedeskuser` (`id`),
  CONSTRAINT `sub_department_id_refs_id_1907f111` FOREIGN KEY (`sub_department_id`) REFERENCES `gm_departmentsubcategories` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_feedback`
--

LOCK TABLES `gm_feedback` WRITE;
/*!40000 ALTER TABLE `gm_feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_feedbackevent`
--

DROP TABLE IF EXISTS `gm_feedbackevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_feedbackevent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `feedback_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `activity_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_feedbackevent_dd2727aa` (`feedback_id`),
  KEY `gm_feedbackevent_6340c63c` (`user_id`),
  KEY `gm_feedbackevent_8005e431` (`activity_id`),
  CONSTRAINT `activity_id_refs_id_c6df9c1b` FOREIGN KEY (`activity_id`) REFERENCES `gm_activity` (`id`),
  CONSTRAINT `feedback_id_refs_id_5d08b44b` FOREIGN KEY (`feedback_id`) REFERENCES `gm_feedback` (`id`),
  CONSTRAINT `user_id_refs_id_22fcd502` FOREIGN KEY (`user_id`) REFERENCES `gm_servicedeskuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_feedbackevent`
--

LOCK TABLES `gm_feedbackevent` WRITE;
/*!40000 ALTER TABLE `gm_feedbackevent` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_feedbackevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_feedfailurelog`
--

DROP TABLE IF EXISTS `gm_feedfailurelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_feedfailurelog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `feed_type` varchar(50) NOT NULL,
  `reason` varchar(2048) DEFAULT NULL,
  `email_flag` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_feedfailurelog`
--

LOCK TABLES `gm_feedfailurelog` WRITE;
/*!40000 ALTER TABLE `gm_feedfailurelog` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_feedfailurelog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_loyaltysla`
--

DROP TABLE IF EXISTS `gm_loyaltysla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_loyaltysla` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(12) NOT NULL,
  `action` varchar(12) NOT NULL,
  `reminder_time` int(10) unsigned NOT NULL,
  `reminder_unit` varchar(12) NOT NULL,
  `resolution_time` int(10) unsigned NOT NULL,
  `resolution_unit` varchar(12) NOT NULL,
  `member_resolution_time` int(10) unsigned NOT NULL,
  `member_resolution_unit` varchar(12) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `status` (`status`,`action`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_loyaltysla`
--

LOCK TABLES `gm_loyaltysla` WRITE;
/*!40000 ALTER TABLE `gm_loyaltysla` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_loyaltysla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_manufacturingdata`
--

DROP TABLE IF EXISTS `gm_manufacturingdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_manufacturingdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` varchar(100) DEFAULT NULL,
  `material_number` varchar(100) DEFAULT NULL,
  `plant` varchar(100) DEFAULT NULL,
  `engine` varchar(100) DEFAULT NULL,
  `vehicle_off_line_date` date DEFAULT NULL,
  `is_discrepant` tinyint(1) NOT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_manufacturingdata`
--

LOCK TABLES `gm_manufacturingdata` WRITE;
/*!40000 ALTER TABLE `gm_manufacturingdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_manufacturingdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_member`
--

DROP TABLE IF EXISTS `gm_member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_member` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `mechanic_id` varchar(50) NOT NULL,
  `permanent_id` varchar(50) DEFAULT NULL,
  `total_points` int(11) DEFAULT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `address_line_1` varchar(40) DEFAULT NULL,
  `address_line_2` varchar(40) DEFAULT NULL,
  `address_line_3` varchar(40) DEFAULT NULL,
  `address_line_4` varchar(40) DEFAULT NULL,
  `address_line_5` varchar(40) DEFAULT NULL,
  `address_line_6` varchar(40) DEFAULT NULL,
  `form_number` int(11) DEFAULT NULL,
  `registered_date` datetime DEFAULT NULL,
  `shop_number` varchar(50) DEFAULT NULL,
  `shop_name` varchar(50) DEFAULT NULL,
  `shop_address` varchar(50) DEFAULT NULL,
  `locality` varchar(50) DEFAULT NULL,
  `tehsil` varchar(50) DEFAULT NULL,
  `district` varchar(50) DEFAULT NULL,
  `pincode` varchar(50) DEFAULT NULL,
  `shop_wall_length` int(11) DEFAULT NULL,
  `shop_wall_width` int(11) DEFAULT NULL,
  `serviced_4S` int(11) DEFAULT NULL,
  `serviced_2S` int(11) DEFAULT NULL,
  `serviced_CNG_LPG` int(11) DEFAULT NULL,
  `serviced_diesel` int(11) DEFAULT NULL,
  `spare_per_month` int(11) DEFAULT NULL,
  `genuine_parts_used` int(11) DEFAULT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `last_transaction_date` datetime DEFAULT NULL,
  `total_accumulation_req` int(11) DEFAULT NULL,
  `total_redemption_req` int(11) DEFAULT NULL,
  `total_accumulation_points` int(11) DEFAULT NULL,
  `total_redemption_points` int(11) DEFAULT NULL,
  `form_status` varchar(15) NOT NULL,
  `sent_sms` tinyint(1) NOT NULL,
  `download_detail` tinyint(1) NOT NULL,
  `registered_by_distributor_id` int(11) DEFAULT NULL,
  `preferred_retailer_id` int(11) DEFAULT NULL,
  `state_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mechanic_id` (`mechanic_id`),
  UNIQUE KEY `permanent_id` (`permanent_id`),
  UNIQUE KEY `phone_number` (`phone_number`),
  KEY `gm_member_e79769ca` (`registered_by_distributor_id`),
  KEY `gm_member_97a4e27e` (`preferred_retailer_id`),
  KEY `gm_member_5654bf12` (`state_id`),
  CONSTRAINT `preferred_retailer_id_refs_id_531cb0fb` FOREIGN KEY (`preferred_retailer_id`) REFERENCES `gm_retailer` (`id`),
  CONSTRAINT `registered_by_distributor_id_refs_id_7926f143` FOREIGN KEY (`registered_by_distributor_id`) REFERENCES `gm_distributor` (`id`),
  CONSTRAINT `state_id_refs_id_44480de4` FOREIGN KEY (`state_id`) REFERENCES `gm_state` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_member`
--

LOCK TABLES `gm_member` WRITE;
/*!40000 ALTER TABLE `gm_member` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_messagetemplate`
--

DROP TABLE IF EXISTS `gm_messagetemplate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_messagetemplate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `template_key` varchar(255) NOT NULL,
  `template` varchar(512) NOT NULL,
  `description` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `template_key` (`template_key`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_messagetemplate`
--

LOCK TABLES `gm_messagetemplate` WRITE;
/*!40000 ALTER TABLE `gm_messagetemplate` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_messagetemplate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_nationalsalesmanager`
--

DROP TABLE IF EXISTS `gm_nationalsalesmanager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_nationalsalesmanager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_nationalsalesmanager_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_4fb5e7a8` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_nationalsalesmanager`
--

LOCK TABLES `gm_nationalsalesmanager` WRITE;
/*!40000 ALTER TABLE `gm_nationalsalesmanager` DISABLE KEYS */;
INSERT INTO `gm_nationalsalesmanager` VALUES (2,'2015-09-28 07:44:02','2015-09-28 07:44:02','aras','araskumar.a@gladminds.co','+911080765676',52),(3,'2015-10-01 05:00:11','2015-10-01 05:00:11','jitendar','jitendar@bajajauto.in','+919180837773',53);
/*!40000 ALTER TABLE `gm_nationalsalesmanager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_nationalsalesmanager_territory`
--

DROP TABLE IF EXISTS `gm_nationalsalesmanager_territory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_nationalsalesmanager_territory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nationalsalesmanager_id` int(11) NOT NULL,
  `territory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nationalsalesmanager_id` (`nationalsalesmanager_id`,`territory_id`),
  KEY `gm_nationalsalesmanager_territory_766c6dc9` (`nationalsalesmanager_id`),
  KEY `gm_nationalsalesmanager_territory_03c62a40` (`territory_id`),
  CONSTRAINT `nationalsalesmanager_id_refs_id_b4851855` FOREIGN KEY (`nationalsalesmanager_id`) REFERENCES `gm_nationalsalesmanager` (`id`),
  CONSTRAINT `territory_id_refs_id_6d25787d` FOREIGN KEY (`territory_id`) REFERENCES `gm_territory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_nationalsalesmanager_territory`
--

LOCK TABLES `gm_nationalsalesmanager_territory` WRITE;
/*!40000 ALTER TABLE `gm_nationalsalesmanager_territory` DISABLE KEYS */;
INSERT INTO `gm_nationalsalesmanager_territory` VALUES (2,2,2),(3,3,2);
/*!40000 ALTER TABLE `gm_nationalsalesmanager_territory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_nationalsparesmanager`
--

DROP TABLE IF EXISTS `gm_nationalsparesmanager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_nationalsparesmanager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `nsm_id` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nsm_id` (`nsm_id`),
  KEY `gm_nationalsparesmanager_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_2dfd4962` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_nationalsparesmanager`
--

LOCK TABLES `gm_nationalsparesmanager` WRITE;
/*!40000 ALTER TABLE `gm_nationalsparesmanager` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_nationalsparesmanager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_nationalsparesmanager_territory`
--

DROP TABLE IF EXISTS `gm_nationalsparesmanager_territory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_nationalsparesmanager_territory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nationalsparesmanager_id` int(11) NOT NULL,
  `territory_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nationalsparesmanager_id` (`nationalsparesmanager_id`,`territory_id`),
  KEY `gm_nationalsparesmanager_territory_c515c81e` (`nationalsparesmanager_id`),
  KEY `gm_nationalsparesmanager_territory_03c62a40` (`territory_id`),
  CONSTRAINT `nationalsparesmanager_id_refs_id_c0ac5986` FOREIGN KEY (`nationalsparesmanager_id`) REFERENCES `gm_nationalsparesmanager` (`id`),
  CONSTRAINT `territory_id_refs_id_4bd80bf0` FOREIGN KEY (`territory_id`) REFERENCES `gm_territory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_nationalsparesmanager_territory`
--

LOCK TABLES `gm_nationalsparesmanager_territory` WRITE;
/*!40000 ALTER TABLE `gm_nationalsparesmanager_territory` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_nationalsparesmanager_territory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_oldfscdata`
--

DROP TABLE IF EXISTS `gm_oldfscdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_oldfscdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `unique_service_coupon` varchar(215) DEFAULT NULL,
  `valid_days` int(11) DEFAULT NULL,
  `valid_kms` int(11) DEFAULT NULL,
  `service_type` int(11) DEFAULT NULL,
  `status` smallint(6) NOT NULL,
  `closed_date` datetime DEFAULT NULL,
  `mark_expired_on` datetime DEFAULT NULL,
  `actual_service_date` datetime DEFAULT NULL,
  `actual_kms` varchar(10) DEFAULT NULL,
  `last_reminder_date` datetime DEFAULT NULL,
  `schedule_reminder_date` datetime DEFAULT NULL,
  `extended_date` datetime DEFAULT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `credit_date` datetime DEFAULT NULL,
  `credit_note` varchar(50) DEFAULT NULL,
  `special_case` tinyint(1) NOT NULL,
  `missing_field` varchar(50) DEFAULT NULL,
  `missing_value` varchar(50) DEFAULT NULL,
  `servicing_dealer` varchar(50) DEFAULT NULL,
  `product_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_oldfscdata_48fb58bb` (`status`),
  KEY `gm_oldfscdata_7f1b40ad` (`product_id`),
  CONSTRAINT `product_id_refs_id_3c8e32a8` FOREIGN KEY (`product_id`) REFERENCES `gm_productdata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_oldfscdata`
--

LOCK TABLES `gm_oldfscdata` WRITE;
/*!40000 ALTER TABLE `gm_oldfscdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_oldfscdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_orderpart`
--

DROP TABLE IF EXISTS `gm_orderpart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_orderpart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `part_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(5,2) NOT NULL,
  `total_price` decimal(8,2) NOT NULL,
  `fullfill` tinyint(1) DEFAULT NULL,
  `delivered` int(11) DEFAULT NULL,
  `no_fullfill_reason` varchar(300) DEFAULT NULL,
  `dsr_id` int(11) DEFAULT NULL,
  `retailer_id` int(11) NOT NULL,
  `order_id` varchar(40) DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `accept` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_orderpart_8c28136d` (`part_id`),
  KEY `gm_orderpart_9f70fd12` (`dsr_id`),
  KEY `gm_orderpart_64f72e30` (`retailer_id`),
  CONSTRAINT `dsr_id_refs_id_a1b19d5a` FOREIGN KEY (`dsr_id`) REFERENCES `gm_distributorsalesrep` (`id`),
  CONSTRAINT `part_id_refs_id_07d47df1` FOREIGN KEY (`part_id`) REFERENCES `gm_partpricing` (`id`),
  CONSTRAINT `retailer_id_refs_id_473cb4b6` FOREIGN KEY (`retailer_id`) REFERENCES `gm_retailer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_orderpart`
--

LOCK TABLES `gm_orderpart` WRITE;
/*!40000 ALTER TABLE `gm_orderpart` DISABLE KEYS */;
INSERT INTO `gm_orderpart` VALUES (1,'2015-09-25 19:37:08','2015-09-25 19:37:08',2,25,150.00,3750.00,NULL,NULL,NULL,7,13,'1320150926','2015-09-26',0),(2,'2015-09-25 19:37:08','2015-09-25 19:37:08',4,15,150.00,2250.00,NULL,NULL,NULL,7,13,'1320150926','2015-09-26',0),(3,'2015-09-25 19:37:08','2015-09-25 19:37:08',6,10,150.00,1500.00,NULL,NULL,NULL,7,13,'1320150926','2015-09-26',0),(4,'2015-09-25 19:37:08','2015-09-25 19:37:08',7,15,150.00,2250.00,NULL,NULL,NULL,7,13,'1320150926','2015-09-26',0),(5,'2015-09-25 19:37:08','2015-09-25 19:37:08',10,45,150.00,6750.00,NULL,NULL,NULL,7,13,'1320150926','2015-09-26',1),(6,'2015-09-25 19:37:08','2015-09-25 19:37:08',11,78,150.00,11700.00,NULL,NULL,NULL,7,13,'1320150926','2015-09-26',0),(7,'2015-09-25 19:37:08','2015-09-25 19:37:08',12,70,150.00,10500.00,NULL,NULL,NULL,7,13,'1320150926','2015-09-26',1),(8,'2015-09-28 09:26:50','2015-09-28 09:26:50',5,56,350.00,19600.00,NULL,NULL,NULL,NULL,13,'60000128092015','2015-09-28',0),(9,'2015-09-28 09:26:50','2015-09-28 09:26:50',2,12,450.00,5400.00,NULL,NULL,NULL,NULL,13,'60000128092015','2015-09-28',0),(10,'2015-09-28 09:29:57','2015-09-28 09:29:57',6,56,250.00,14000.00,NULL,NULL,NULL,7,13,'60000128092015','2015-09-28',0),(11,'2015-09-28 09:29:57','2015-09-28 09:29:57',5,53,350.00,18550.00,NULL,NULL,NULL,7,13,'60000128092015','2015-09-28',1),(12,'2015-09-30 04:32:27','2015-09-30 04:32:27',10,23,150.78,3467.94,NULL,NULL,NULL,7,13,'60000130092015','2015-09-30',0),(13,'2015-09-30 04:32:27','2015-09-30 04:32:27',5,26,350.00,9100.00,NULL,NULL,NULL,7,13,'60000130092015','2015-09-30',1),(14,'2015-09-30 04:33:25','2015-09-30 04:33:25',10,23,150.78,3467.94,NULL,NULL,NULL,7,13,'60000130092015','2015-09-30',0),(15,'2015-09-30 04:33:25','2015-09-30 04:33:25',5,26,350.00,9100.00,NULL,NULL,NULL,7,13,'60000130092015','2015-09-30',0),(16,'2015-10-01 12:40:13','2015-10-01 12:40:13',5,25,19.50,487.50,NULL,NULL,NULL,7,13,'60000101102015','2015-10-01',1),(17,'2015-10-01 12:40:53','2015-10-01 12:40:53',5,26,19.50,507.00,NULL,NULL,NULL,7,13,'60000101102015','2015-10-01',0),(18,'2015-10-01 12:40:53','2015-10-01 12:40:53',7,56,602.00,33712.00,NULL,NULL,NULL,7,13,'60000101102015','2015-10-01',0),(19,'2015-10-01 12:42:01','2015-10-01 12:42:01',4,100,670.00,67000.00,NULL,NULL,NULL,7,13,'60000101102015','2015-10-01',1),(20,'2015-10-01 12:42:01','2015-10-01 12:42:01',5,400,19.50,7800.00,NULL,NULL,NULL,7,13,'60000101102015','2015-10-01',0),(21,'2015-10-01 12:42:01','2015-10-02 05:33:19',11,20,713.00,14260.00,0,2,'no stock',7,13,'60000101102015','2015-10-01',0),(22,'2015-10-02 05:16:47','2015-10-02 05:16:47',2,52,541.00,28132.00,NULL,NULL,NULL,7,13,'60000102102015','2015-10-02',1),(23,'2015-10-02 05:16:47','2015-10-02 05:16:47',4,25,670.00,16750.00,NULL,NULL,NULL,7,13,'60000102102015','2015-10-02',0),(24,'2015-10-02 05:16:47','2015-10-02 05:16:47',5,36,19.50,702.00,NULL,NULL,NULL,7,13,'60000102102015','2015-10-02',0),(25,'2015-10-02 05:16:47','2015-10-02 05:16:47',6,44,257.00,11308.00,NULL,NULL,NULL,7,13,'60000102102015','2015-10-02',0),(26,'2015-10-02 05:16:48','2015-10-02 05:16:48',7,10,602.00,6020.00,NULL,NULL,NULL,7,13,'60000102102015','2015-10-02',0),(27,'2015-10-02 05:51:50','2015-10-02 05:51:50',2,23,541.00,12443.00,NULL,NULL,NULL,7,13,'60000102102015','2015-10-02',0),(28,'2015-10-02 05:51:50','2015-10-02 05:51:50',4,41,670.00,27470.00,NULL,NULL,NULL,7,13,'60000102102015','2015-10-02',0);
/*!40000 ALTER TABLE `gm_orderpart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_otptoken`
--

DROP TABLE IF EXISTS `gm_otptoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_otptoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `token` varchar(256) NOT NULL,
  `request_date` datetime DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_otptoken_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_76c1a8ba` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_otptoken`
--

LOCK TABLES `gm_otptoken` WRITE;
/*!40000 ALTER TABLE `gm_otptoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_otptoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_partmodels`
--

DROP TABLE IF EXISTS `gm_partmodels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_partmodels` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `model_name` varchar(255) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_partmodels`
--

LOCK TABLES `gm_partmodels` WRITE;
/*!40000 ALTER TABLE `gm_partmodels` DISABLE KEYS */;
INSERT INTO `gm_partmodels` VALUES (1,'0000-00-00 00:00:00','0000-00-00 00:00:00','RE - Diesel','diesel.png',1),(2,'0000-00-00 00:00:00','0000-00-00 00:00:00','RE - 2S','2s.png',1),(3,'0000-00-00 00:00:00','0000-00-00 00:00:00','RE - 4S','4s.png',1);
/*!40000 ALTER TABLE `gm_partmodels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_partner`
--

DROP TABLE IF EXISTS `gm_partner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_partner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `partner_id` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `partner_type` varchar(12) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `partner_id` (`partner_id`),
  KEY `gm_partner_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_e6d750a8` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_partner`
--

LOCK TABLES `gm_partner` WRITE;
/*!40000 ALTER TABLE `gm_partner` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_partner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_partpricing`
--

DROP TABLE IF EXISTS `gm_partpricing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_partpricing` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `bajaj_id` int(11) DEFAULT NULL,
  `part_number` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `part_model` varchar(255) DEFAULT NULL,
  `valid_from` date DEFAULT NULL,
  `subcategory_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `mrp` varchar(8) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_partpricing_790ef9fb` (`subcategory_id`),
  KEY `gm_partpricing_6f33f001` (`category_id`),
  CONSTRAINT `category_id_refs_id_3faf5da8` FOREIGN KEY (`category_id`) REFERENCES `gm_categories` (`id`),
  CONSTRAINT `subcategory_id_refs_id_9832c09c` FOREIGN KEY (`subcategory_id`) REFERENCES `gm_subcategories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_partpricing`
--

LOCK TABLES `gm_partpricing` WRITE;
/*!40000 ALTER TABLE `gm_partpricing` DISABLE KEYS */;
INSERT INTO `gm_partpricing` VALUES (2,'0000-00-00 00:00:00','0000-00-00 00:00:00',1,'24121642','ASSEMBLY AIR FILTER-SAI TYPE','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-02-18',17,1,'541',1),(4,'0000-00-00 00:00:00','0000-00-00 00:00:00',2,'24121659','ASSEMBLY AIR FILTER-SAI TYPE','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-01-01',17,1,'670',1),(5,'0000-00-00 00:00:00','0000-00-00 00:00:00',3,'24141120','FILTER ASSY. - 2T OIL FOR RE2S CNG/LPG','ASSEMBLY 3WRE 2SUG LPG EL START-NO COLOR','2005-07-01',18,1,'19.5',1),(6,'0000-00-00 00:00:00','0000-00-00 00:00:00',4,'AA121056','ELEMENT AIR FILTER','3W RE/AR WITH 4 STROKE PETROL ENGINE+ANT','2004-10-01',21,1,'257',1),(7,'0000-00-00 00:00:00','0000-00-00 00:00:00',5,'AA121126','ASSEMBLY AIR FILTER','ASSEMBLY 3WRE 2SUG CNG EL START-NO COLOR','2010-07-31',27,1,'602',1),(8,'0000-00-00 00:00:00','0000-00-00 00:00:00',6,'AA121150','ELEMENT AIR FILTER','ASSEMNLY 3W 4S','0000-00-00',25,1,'297',1),(9,'0000-00-00 00:00:00','0000-00-00 00:00:00',7,'AA121151','ASSEMBLY AIR FILTER','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2012-11-17',23,1,'695',1),(10,'0000-00-00 00:00:00','0000-00-00 00:00:00',8,'AF121393','FILTER AIR CARBURETTOR','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2007-09-01',30,1,'13.5',1),(11,'0000-00-00 00:00:00','0000-00-00 00:00:00',9,'AF121505','ASSEMBLY AIR FILTER','RE COMPACT PETROL','2013-07-06',21,1,'713',1),(12,'0000-00-00 00:00:00','0000-00-00 00:00:00',10,'AL121060','FILTER AIR ASSEMBLY','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2006-03-01',22,1,'597',1);
/*!40000 ALTER TABLE `gm_partpricing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_productcatalog`
--

DROP TABLE IF EXISTS `gm_productcatalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_productcatalog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `product_id` varchar(50) NOT NULL,
  `points` int(11) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  `variation` varchar(50) DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `sub_category` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `partner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`),
  KEY `gm_productcatalog_42b53b76` (`partner_id`),
  CONSTRAINT `partner_id_refs_id_5f7e45f6` FOREIGN KEY (`partner_id`) REFERENCES `gm_partner` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_productcatalog`
--

LOCK TABLES `gm_productcatalog` WRITE;
/*!40000 ALTER TABLE `gm_productcatalog` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_productcatalog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_productdata`
--

DROP TABLE IF EXISTS `gm_productdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_productdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `product_id` varchar(215) NOT NULL,
  `customer_id` varchar(215) DEFAULT NULL,
  `customer_phone_number` varchar(15) DEFAULT NULL,
  `customer_name` varchar(215) DEFAULT NULL,
  `customer_city` varchar(100) DEFAULT NULL,
  `customer_state` varchar(100) DEFAULT NULL,
  `customer_pincode` varchar(15) DEFAULT NULL,
  `purchase_date` datetime DEFAULT NULL,
  `invoice_date` datetime DEFAULT NULL,
  `engine` varchar(255) DEFAULT NULL,
  `veh_reg_no` varchar(15) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `sku_code` varchar(20) DEFAULT NULL,
  `product_type_id` int(11) DEFAULT NULL,
  `dealer_id_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_id` (`product_id`),
  UNIQUE KEY `customer_id` (`customer_id`),
  UNIQUE KEY `engine` (`engine`),
  KEY `gm_productdata_31f67551` (`product_type_id`),
  KEY `gm_productdata_e2b16961` (`dealer_id_id`),
  CONSTRAINT `dealer_id_id_refs_user_id_21ad52d3` FOREIGN KEY (`dealer_id_id`) REFERENCES `gm_dealer` (`user_id`),
  CONSTRAINT `product_type_id_refs_id_25086b41` FOREIGN KEY (`product_type_id`) REFERENCES `gm_producttype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_productdata`
--

LOCK TABLES `gm_productdata` WRITE;
/*!40000 ALTER TABLE `gm_productdata` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_productdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_producttype`
--

DROP TABLE IF EXISTS `gm_producttype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_producttype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `product_type` varchar(255) NOT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `overview` varchar(512) DEFAULT NULL,
  `brand_product_category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_type` (`product_type`),
  KEY `gm_producttype_408264f7` (`brand_product_category_id`),
  CONSTRAINT `brand_product_category_id_refs_id_0bed8165` FOREIGN KEY (`brand_product_category_id`) REFERENCES `gm_brandproductcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_producttype`
--

LOCK TABLES `gm_producttype` WRITE;
/*!40000 ALTER TABLE `gm_producttype` DISABLE KEYS */;
INSERT INTO `gm_producttype` VALUES (1,'2014-12-20 08:32:42','2014-12-20 08:32:42','tyre',NULL,1,NULL,1);
/*!40000 ALTER TABLE `gm_producttype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_redemptionrequest`
--

DROP TABLE IF EXISTS `gm_redemptionrequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_redemptionrequest` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `delivery_address` varchar(50) DEFAULT NULL,
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `expected_delivery_date` datetime DEFAULT NULL,
  `status` varchar(12) NOT NULL,
  `packed_by` varchar(50) DEFAULT NULL,
  `tracking_id` varchar(50) DEFAULT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `refunded_points` tinyint(1) NOT NULL,
  `due_date` datetime DEFAULT NULL,
  `resolution_flag` tinyint(1) NOT NULL,
  `approved_date` datetime DEFAULT NULL,
  `shipped_date` datetime DEFAULT NULL,
  `delivery_date` datetime DEFAULT NULL,
  `pod_number` varchar(50) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `points` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `member_id` int(11) NOT NULL,
  `partner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `gm_redemptionrequest_7f1b40ad` (`product_id`),
  KEY `gm_redemptionrequest_b3c09425` (`member_id`),
  KEY `gm_redemptionrequest_42b53b76` (`partner_id`),
  CONSTRAINT `member_id_refs_id_2df21631` FOREIGN KEY (`member_id`) REFERENCES `gm_member` (`id`),
  CONSTRAINT `partner_id_refs_id_ddca6ab4` FOREIGN KEY (`partner_id`) REFERENCES `gm_partner` (`id`),
  CONSTRAINT `product_id_refs_id_53bddfe4` FOREIGN KEY (`product_id`) REFERENCES `gm_productcatalog` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_redemptionrequest`
--

LOCK TABLES `gm_redemptionrequest` WRITE;
/*!40000 ALTER TABLE `gm_redemptionrequest` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_redemptionrequest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_regionalmanager`
--

DROP TABLE IF EXISTS `gm_regionalmanager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_regionalmanager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `region` varchar(100) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `circle_head_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `gm_regionalmanager_85edf0b3` (`circle_head_id`),
  CONSTRAINT `circle_head_id_refs_id_e1123413` FOREIGN KEY (`circle_head_id`) REFERENCES `gm_circlehead` (`id`),
  CONSTRAINT `user_id_refs_user_id_98e4870b` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_regionalmanager`
--

LOCK TABLES `gm_regionalmanager` WRITE;
/*!40000 ALTER TABLE `gm_regionalmanager` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_regionalmanager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_retailer`
--

DROP TABLE IF EXISTS `gm_retailer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_retailer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `retailer_name` varchar(50) NOT NULL,
  `retailer_town` varchar(50) DEFAULT NULL,
  `approved` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `billing_code` varchar(15) DEFAULT NULL,
  `distributor_id` int(11) DEFAULT NULL,
  `territory` varchar(15) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `profile` varchar(15) DEFAULT NULL,
  `language` varchar(10) DEFAULT NULL,
  `rejected_reason` varchar(300) DEFAULT NULL,
  `latitude` decimal(10,6) DEFAULT NULL,
  `longitude` decimal(11,6) DEFAULT NULL,
  `retailer_code` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_retailer`
--

LOCK TABLES `gm_retailer` WRITE;
/*!40000 ALTER TABLE `gm_retailer` DISABLE KEYS */;
INSERT INTO `gm_retailer` VALUES (13,'2015-09-25 10:17:45','2015-09-25 10:17:45','sudhir','bangalore',2,1,48,'RETSUDHIR',10,'south','sudhir@gladminds.co','9765098721','Retailer','kannada',NULL,NULL,NULL,'600001');
/*!40000 ALTER TABLE `gm_retailer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_satempregistration`
--

DROP TABLE IF EXISTS `gm_satempregistration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_satempregistration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_satempregistration`
--

LOCK TABLES `gm_satempregistration` WRITE;
/*!40000 ALTER TABLE `gm_satempregistration` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_satempregistration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_service`
--

DROP TABLE IF EXISTS `gm_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` longtext,
  `training_material_url` varchar(255) DEFAULT NULL,
  `service_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_service_cca592ae` (`service_type_id`),
  CONSTRAINT `service_type_id_refs_id_9f4bd137` FOREIGN KEY (`service_type_id`) REFERENCES `gm_servicetype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_service`
--

LOCK TABLES `gm_service` WRITE;
/*!40000 ALTER TABLE `gm_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_serviceadvisor`
--

DROP TABLE IF EXISTS `gm_serviceadvisor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_serviceadvisor` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `service_advisor_id` varchar(15) NOT NULL,
  `status` varchar(10) NOT NULL,
  `user_id` int(11) NOT NULL,
  `dealer_id` int(11) DEFAULT NULL,
  `asc_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `service_advisor_id` (`service_advisor_id`),
  KEY `gm_serviceadvisor_f65f7b5d` (`dealer_id`),
  KEY `gm_serviceadvisor_446dd36d` (`asc_id`),
  CONSTRAINT `asc_id_refs_user_id_7d52fad5` FOREIGN KEY (`asc_id`) REFERENCES `gm_authorizedservicecenter` (`user_id`),
  CONSTRAINT `dealer_id_refs_user_id_b6a97602` FOREIGN KEY (`dealer_id`) REFERENCES `gm_dealer` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_265434d4` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_serviceadvisor`
--

LOCK TABLES `gm_serviceadvisor` WRITE;
/*!40000 ALTER TABLE `gm_serviceadvisor` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_serviceadvisor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_serviceadvisorcouponrelationship`
--

DROP TABLE IF EXISTS `gm_serviceadvisorcouponrelationship`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_serviceadvisorcouponrelationship` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `unique_service_coupon_id` int(11) NOT NULL,
  `service_advisor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_serviceadvisorcouponrelationship_49ac3df4` (`unique_service_coupon_id`),
  KEY `gm_serviceadvisorcouponrelationship_3758e01b` (`service_advisor_id`),
  CONSTRAINT `service_advisor_id_refs_user_id_9adc7af5` FOREIGN KEY (`service_advisor_id`) REFERENCES `gm_serviceadvisor` (`user_id`),
  CONSTRAINT `unique_service_coupon_id_refs_id_96498d33` FOREIGN KEY (`unique_service_coupon_id`) REFERENCES `gm_coupondata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_serviceadvisorcouponrelationship`
--

LOCK TABLES `gm_serviceadvisorcouponrelationship` WRITE;
/*!40000 ALTER TABLE `gm_serviceadvisorcouponrelationship` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_serviceadvisorcouponrelationship` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_servicecircular`
--

DROP TABLE IF EXISTS `gm_servicecircular`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_servicecircular` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_type` varchar(100) DEFAULT NULL,
  `type_of_circular` varchar(50) DEFAULT NULL,
  `change_no` varchar(50) DEFAULT NULL,
  `new_circular` varchar(50) DEFAULT NULL,
  `buletin_no` varchar(50) DEFAULT NULL,
  `circular_date` datetime DEFAULT NULL,
  `from_circular` varchar(50) DEFAULT NULL,
  `to_circular` varchar(50) DEFAULT NULL,
  `cc_circular` varchar(50) DEFAULT NULL,
  `circular_subject` varchar(50) DEFAULT NULL,
  `part_added` varchar(50) DEFAULT NULL,
  `circular_title` varchar(50) DEFAULT NULL,
  `part_deleted` varchar(50) DEFAULT NULL,
  `part_changed` varchar(50) DEFAULT NULL,
  `model_name` varchar(50) DEFAULT NULL,
  `sku_description` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_servicecircular`
--

LOCK TABLES `gm_servicecircular` WRITE;
/*!40000 ALTER TABLE `gm_servicecircular` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_servicecircular` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_servicecircular_model_sku_code`
--

DROP TABLE IF EXISTS `gm_servicecircular_model_sku_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_servicecircular_model_sku_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `servicecircular_id` int(11) NOT NULL,
  `brandproductrange_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `servicecircular_id` (`servicecircular_id`,`brandproductrange_id`),
  KEY `gm_servicecircular_model_sku_code_c3b87cf4` (`servicecircular_id`),
  KEY `gm_servicecircular_model_sku_code_73dba179` (`brandproductrange_id`),
  CONSTRAINT `brandproductrange_id_refs_id_e4279033` FOREIGN KEY (`brandproductrange_id`) REFERENCES `gm_brandproductrange` (`id`),
  CONSTRAINT `servicecircular_id_refs_id_44e83a32` FOREIGN KEY (`servicecircular_id`) REFERENCES `gm_servicecircular` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_servicecircular_model_sku_code`
--

LOCK TABLES `gm_servicecircular_model_sku_code` WRITE;
/*!40000 ALTER TABLE `gm_servicecircular_model_sku_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_servicecircular_model_sku_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_servicedeskuser`
--

DROP TABLE IF EXISTS `gm_servicedeskuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_servicedeskuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `user_profile_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_servicedeskuser_82936d91` (`user_profile_id`),
  CONSTRAINT `user_profile_id_refs_user_id_efdb6067` FOREIGN KEY (`user_profile_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_servicedeskuser`
--

LOCK TABLES `gm_servicedeskuser` WRITE;
/*!40000 ALTER TABLE `gm_servicedeskuser` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_servicedeskuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_servicetype`
--

DROP TABLE IF EXISTS `gm_servicetype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_servicetype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_servicetype`
--

LOCK TABLES `gm_servicetype` WRITE;
/*!40000 ALTER TABLE `gm_servicetype` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_servicetype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_sla`
--

DROP TABLE IF EXISTS `gm_sla`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_sla` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `response_time` int(10) unsigned NOT NULL,
  `response_unit` varchar(12) NOT NULL,
  `reminder_time` int(10) unsigned NOT NULL,
  `reminder_unit` varchar(12) NOT NULL,
  `resolution_time` int(10) unsigned NOT NULL,
  `resolution_unit` varchar(12) NOT NULL,
  `priority` varchar(12) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `priority` (`priority`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_sla`
--

LOCK TABLES `gm_sla` WRITE;
/*!40000 ALTER TABLE `gm_sla` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_sla` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_smslog`
--

DROP TABLE IF EXISTS `gm_smslog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_smslog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `action` varchar(250) NOT NULL,
  `message` longtext,
  `sender` varchar(15) NOT NULL,
  `receiver` varchar(15) NOT NULL,
  `status` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_smslog`
--

LOCK TABLES `gm_smslog` WRITE;
/*!40000 ALTER TABLE `gm_smslog` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_smslog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_sparepartmasterdata`
--

DROP TABLE IF EXISTS `gm_sparepartmasterdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_sparepartmasterdata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `part_number` varchar(100) NOT NULL,
  `part_model` varchar(50) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `segment_type` varchar(50) DEFAULT NULL,
  `supplier` varchar(50) DEFAULT NULL,
  `product_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `part_number` (`part_number`),
  KEY `gm_sparepartmasterdata_31f67551` (`product_type_id`),
  CONSTRAINT `product_type_id_refs_id_165e142c` FOREIGN KEY (`product_type_id`) REFERENCES `gm_producttype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_sparepartmasterdata`
--

LOCK TABLES `gm_sparepartmasterdata` WRITE;
/*!40000 ALTER TABLE `gm_sparepartmasterdata` DISABLE KEYS */;
INSERT INTO `gm_sparepartmasterdata` VALUES (1,'2014-12-20 08:32:42','2014-12-20 08:32:42','24171136','2S','HUB FRONT WHEEL','3W','','',NULL),(2,'2014-12-20 08:32:42','2014-12-20 08:32:42','24171063','2S','SHOCK ABS RR 4S PETR','3W','','',NULL),(3,'2014-12-20 08:32:43','2014-12-20 08:32:43','24171137','2S','SHOCK ABSORBER FR','3W','','',NULL),(4,'2014-12-20 08:32:43','2014-12-20 08:32:43','24171094','2S','SHOCK ABSORBER RR RE','3W','','',NULL),(5,'2014-12-20 08:32:43','2014-12-20 08:32:43','AP171003','2S','SHOCK ABSORBER FRONT','3W','','',NULL);
/*!40000 ALTER TABLE `gm_sparepartmasterdata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_sparepartpoint`
--

DROP TABLE IF EXISTS `gm_sparepartpoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_sparepartpoint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `points` int(11) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `MRP` double DEFAULT NULL,
  `valid_from` datetime DEFAULT NULL,
  `valid_till` datetime DEFAULT NULL,
  `territory` varchar(50) DEFAULT NULL,
  `part_number_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_sparepartpoint_b1e99e52` (`part_number_id`),
  CONSTRAINT `part_number_id_refs_id_69f218e8` FOREIGN KEY (`part_number_id`) REFERENCES `gm_sparepartmasterdata` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_sparepartpoint`
--

LOCK TABLES `gm_sparepartpoint` WRITE;
/*!40000 ALTER TABLE `gm_sparepartpoint` DISABLE KEYS */;
INSERT INTO `gm_sparepartpoint` VALUES (1,'2014-12-20 08:32:50','2014-12-20 08:32:50',18,750,NULL,'2014-12-21 18:30:00','2015-12-21 18:30:00','South',1),(2,'2014-12-20 08:32:50','2014-12-20 08:32:50',11,750,NULL,'2014-12-21 18:30:00','2015-12-21 18:30:00','South',2),(3,'2014-12-20 08:32:50','2014-12-20 08:32:50',11,1750,NULL,'2014-12-21 18:30:00','2015-12-21 18:30:00','South',3),(4,'2014-12-20 08:32:50','2014-12-20 08:32:50',11,75,NULL,'2014-12-21 18:30:00','2015-12-21 18:30:00','South',4),(5,'2014-12-20 08:32:50','2014-12-20 08:32:50',7,75,NULL,'2014-12-21 18:30:00','2015-12-21 18:30:00','South',5);
/*!40000 ALTER TABLE `gm_sparepartpoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_sparepartupc`
--

DROP TABLE IF EXISTS `gm_sparepartupc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_sparepartupc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `unique_part_code` varchar(50) NOT NULL,
  `is_used` tinyint(1) NOT NULL,
  `part_number_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_part_code` (`unique_part_code`),
  KEY `gm_sparepartupc_b1e99e52` (`part_number_id`),
  CONSTRAINT `part_number_id_refs_id_e1ba91e8` FOREIGN KEY (`part_number_id`) REFERENCES `gm_sparepartmasterdata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_sparepartupc`
--

LOCK TABLES `gm_sparepartupc` WRITE;
/*!40000 ALTER TABLE `gm_sparepartupc` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_sparepartupc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_state`
--

DROP TABLE IF EXISTS `gm_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `state_name` varchar(30) NOT NULL,
  `state_code` varchar(10) NOT NULL,
  `territory_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `state_name` (`state_name`),
  UNIQUE KEY `state_code` (`state_code`),
  KEY `gm_state_03c62a40` (`territory_id`),
  CONSTRAINT `territory_id_refs_id_c31287c3` FOREIGN KEY (`territory_id`) REFERENCES `gm_territory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_state`
--

LOCK TABLES `gm_state` WRITE;
/*!40000 ALTER TABLE `gm_state` DISABLE KEYS */;
INSERT INTO `gm_state` VALUES (1,'2015-08-19 08:17:04','2015-08-19 08:17:04','Andhra Pradesh','AP',NULL),(2,'2015-08-19 08:17:04','2015-08-19 08:17:04','Arunachal Pradesh','ARP',NULL),(3,'2015-08-19 08:17:04','2015-08-19 08:17:04','Assam','AS',NULL),(4,'2015-08-19 08:17:04','2015-08-19 08:17:04','Bhutan','BT',NULL),(5,'2015-08-19 08:17:04','2015-08-19 08:17:04','Bihar','BH',NULL),(6,'2015-08-19 08:17:04','2015-08-19 08:17:04','Chandigarh','CD',NULL),(7,'2015-08-19 08:17:04','2015-08-19 08:17:04','Chattisgarh','CH',NULL),(8,'2015-08-19 08:17:04','2015-08-19 08:17:04','Dadra, Nagarhaveli','DH',NULL),(9,'2015-08-19 08:17:04','2015-08-19 08:17:04','Delhi','DEL',NULL),(10,'2015-08-19 08:17:05','2015-08-19 08:17:05','Goa, Daman & Diu','GDD',NULL),(11,'2015-08-19 08:17:05','2015-08-19 08:17:05','Gujarat','GJ',NULL),(12,'2015-08-19 08:17:05','2015-08-19 08:17:05','Haryana','HR',NULL),(13,'2015-08-19 08:17:05','2015-08-19 08:17:05','Himachal Pradesh','HP',NULL),(14,'2015-08-19 08:17:05','2015-08-19 08:17:05','Jammu & Kashmir','JK',NULL),(15,'2015-08-19 08:17:05','2015-08-19 08:17:05','Jharkhand','JH',NULL),(16,'2015-08-19 08:17:05','2015-08-19 08:17:05','Karnataka','KAR',NULL),(17,'2015-08-19 08:17:05','2015-08-19 08:17:05','Kerala','KER',NULL),(18,'2015-08-19 08:17:05','2015-08-19 08:17:05','Lakshwadeep','LAK',NULL),(19,'2015-08-19 08:17:05','2015-08-19 08:17:05','Madhya Pradesh','MP',NULL),(20,'2015-08-19 08:17:05','2015-08-19 08:17:05','Maharashtra','MAH',NULL),(21,'2015-08-19 08:17:05','2015-08-19 08:17:05','Manipur','MN',NULL),(22,'2015-08-19 08:17:05','2015-08-19 08:17:05','Meghalaya','MG',NULL),(23,'2015-08-19 08:17:05','2015-08-19 08:17:05','Mizoram','MZ',NULL),(24,'2015-08-19 08:17:05','2015-08-19 08:17:05','Nagaland','NG',NULL),(25,'2015-08-19 08:17:05','2015-08-19 08:17:05','Nepal','NP',NULL),(26,'2015-08-19 08:17:05','2015-08-19 08:17:05','Orissa','OR',NULL),(27,'2015-08-19 08:17:05','2015-08-19 08:17:05','Pondicherry','PY',NULL),(28,'2015-08-19 08:17:05','2015-08-19 08:17:05','Punjab','PB',NULL),(29,'2015-08-19 08:17:05','2015-08-19 08:17:05','Rajasthan','RJ',NULL),(30,'2015-08-19 08:17:05','2015-08-19 08:17:05','Sikkim','SK',NULL),(31,'2015-08-19 08:17:06','2015-08-19 08:17:06','Tamil Nadu','TN',NULL),(32,'2015-08-19 08:17:06','2015-08-19 08:17:06','Tripura','TR',NULL),(33,'2015-08-19 08:17:06','2015-08-19 08:17:06','Uttar Pradesh','UP',NULL),(34,'2015-08-19 08:17:06','2015-08-19 08:17:06','Uttaranchal','UT',NULL),(35,'2015-08-19 08:17:06','2015-08-19 08:17:06','West Bengal','WB',NULL),(36,'2015-08-19 08:17:06','2015-08-19 08:17:06','Uttar Pradesh East','UPE',NULL),(37,'2015-08-19 08:17:06','2015-08-19 08:17:06','Uttar Pradesh West','UPW',NULL);
/*!40000 ALTER TABLE `gm_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_subcategories`
--

DROP TABLE IF EXISTS `gm_subcategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_subcategories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `subcategory_name` varchar(255) NOT NULL,
  `category_id` int(11) NOT NULL,
  `part_model_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_subcategories_6f33f001` (`category_id`),
  KEY `gm_subcategories_24dcb168` (`part_model_id`),
  CONSTRAINT `category_id_refs_id_32b98c46` FOREIGN KEY (`category_id`) REFERENCES `gm_categories` (`id`),
  CONSTRAINT `part_model_id_refs_id_cf522c71` FOREIGN KEY (`part_model_id`) REFERENCES `gm_partmodels` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_subcategories`
--

LOCK TABLES `gm_subcategories` WRITE;
/*!40000 ALTER TABLE `gm_subcategories` DISABLE KEYS */;
INSERT INTO `gm_subcategories` VALUES (16,'0000-00-00 00:00:00','0000-00-00 00:00:00','Engine , Cylinder Crankcase',1,1,1,'BA/1.PNG'),(17,'0000-00-00 00:00:00','0000-00-00 00:00:00','Cam shaft Assembly',1,1,1,'BA/2.PNG'),(18,'0000-00-00 00:00:00','0000-00-00 00:00:00','Piston & Connecting Rod Assly',1,1,1,'BA/3.PNG'),(19,'0000-00-00 00:00:00','0000-00-00 00:00:00','Crankshaft Assembly',1,1,1,'BA/4.PNG'),(20,'0000-00-00 00:00:00','0000-00-00 00:00:00','Weight Balancer',1,1,1,'BA/5.PNG'),(21,'0000-00-00 00:00:00','0000-00-00 00:00:00','Governor',1,1,1,'BA/6.PNG'),(22,'0000-00-00 00:00:00','0000-00-00 00:00:00','Speed Control Levers',1,1,1,'BA/7.PNG'),(23,'0000-00-00 00:00:00','0000-00-00 00:00:00','Cover Crankcase',1,1,1,'BA/8.PNG'),(24,'0000-00-00 00:00:00','0000-00-00 00:00:00','Oil Pump',1,1,1,'BA/9.PNG'),(25,'0000-00-00 00:00:00','0000-00-00 00:00:00','Clutch',1,1,1,'BA/10.PNG'),(26,'0000-00-00 00:00:00','0000-00-00 00:00:00','Clutch Shaft Assembly',1,1,1,'BA/11.PNG'),(27,'0000-00-00 00:00:00','0000-00-00 00:00:00','Main Housing',1,1,1,'BA/12.PNG'),(28,'0000-00-00 00:00:00','0000-00-00 00:00:00','Gear Box Cover',1,1,1,'BA/13.PNG'),(29,'0000-00-00 00:00:00','0000-00-00 00:00:00','Gear Shifter Assembly',1,1,1,'BA/14.PNG'),(30,'0000-00-00 00:00:00','0000-00-00 00:00:00','Gear Transmission',1,1,1,'BA/15.PNG');
/*!40000 ALTER TABLE `gm_subcategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_supervisor`
--

DROP TABLE IF EXISTS `gm_supervisor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_supervisor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `supervisor_id` varchar(15) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `transporter_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `supervisor_id` (`supervisor_id`),
  KEY `gm_supervisor_6340c63c` (`user_id`),
  KEY `gm_supervisor_c7d7fc7d` (`transporter_id`),
  CONSTRAINT `transporter_id_refs_id_75ea9d80` FOREIGN KEY (`transporter_id`) REFERENCES `gm_transporter` (`id`),
  CONSTRAINT `user_id_refs_user_id_905df947` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_supervisor`
--

LOCK TABLES `gm_supervisor` WRITE;
/*!40000 ALTER TABLE `gm_supervisor` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_supervisor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_territory`
--

DROP TABLE IF EXISTS `gm_territory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_territory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `territory` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `territory` (`territory`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_territory`
--

LOCK TABLES `gm_territory` WRITE;
/*!40000 ALTER TABLE `gm_territory` DISABLE KEYS */;
INSERT INTO `gm_territory` VALUES (1,'2015-09-08 16:43:31','2015-09-08 16:43:31','south'),(2,'2015-09-28 07:43:57','2015-09-28 07:43:57','north');
/*!40000 ALTER TABLE `gm_territory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_transporter`
--

DROP TABLE IF EXISTS `gm_transporter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_transporter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `transporter_id` varchar(15) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `transporter_id` (`transporter_id`),
  KEY `gm_transporter_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_693c0f49` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_transporter`
--

LOCK TABLES `gm_transporter` WRITE;
/*!40000 ALTER TABLE `gm_transporter` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_transporter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_ucnrecovery`
--

DROP TABLE IF EXISTS `gm_ucnrecovery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_ucnrecovery` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `reason` longtext NOT NULL,
  `customer_id` varchar(215) DEFAULT NULL,
  `file_location` varchar(215) DEFAULT NULL,
  `unique_service_coupon` varchar(215) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_ucnrecovery_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_de17070b` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_ucnrecovery`
--

LOCK TABLES `gm_ucnrecovery` WRITE;
/*!40000 ALTER TABLE `gm_ucnrecovery` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_ucnrecovery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_userpreference`
--

DROP TABLE IF EXISTS `gm_userpreference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_userpreference` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `key` varchar(100) NOT NULL,
  `value` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`key`),
  KEY `gm_userpreference_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_1fc3b13d` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_userpreference`
--

LOCK TABLES `gm_userpreference` WRITE;
/*!40000 ALTER TABLE `gm_userpreference` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_userpreference` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_userprofile`
--

DROP TABLE IF EXISTS `gm_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_userprofile` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `address` longtext,
  `state` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `pincode` varchar(15) DEFAULT NULL,
  `date_of_birth` datetime DEFAULT NULL,
  `is_email_verified` tinyint(1) NOT NULL,
  `is_phone_verified` tinyint(1) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `image_url` varchar(200) DEFAULT NULL,
  `reset_password` tinyint(1) NOT NULL,
  `reset_date` datetime DEFAULT NULL,
  `gender` varchar(2) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `user_id_refs_id_3e6c398e` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_userprofile`
--

LOCK TABLES `gm_userprofile` WRITE;
/*!40000 ALTER TABLE `gm_userprofile` DISABLE KEYS */;
INSERT INTO `gm_userprofile` VALUES ('2015-09-25 09:14:23','2015-09-25 09:14:23','988076543','','7, Raja Rajeshwaree Nagar, Bangalore','karnataka','India','560071',NULL,0,0,'','',0,NULL,'M',46),('2015-09-25 09:17:56','2015-09-25 09:17:56','9423840394','','5, Langford street, Pune','maharastra','India','400029',NULL,0,0,'','',0,NULL,'M',47),('2015-09-25 10:12:36','2015-09-25 10:12:36','080 - 41123876','','#987, St. Paul\'s Avenue, Wilson Garden, HSR Layout, Bangalore','karnataka','India','560090',NULL,0,0,'','',0,NULL,'M',48),('2015-09-28 06:30:52','2015-09-28 06:30:52','080 - 78654323','','#787, pinnacle street,\r\nBangalore','karnataka','India','560068',NULL,0,0,'','',0,NULL,NULL,51),('2015-09-28 07:42:14','2015-09-28 07:42:14','080 - 875345355','','#232, Richmond street, Johnson Market','karnataka','India','560068',NULL,0,0,'','',0,NULL,'M',52),('2015-10-01 04:52:23','2015-10-01 04:52:23','080 -7657777','','#654, J.C. Road,\r\nBangalore','karnataka','India','560068',NULL,0,0,'','',0,NULL,'M',53);
/*!40000 ALTER TABLE `gm_userprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_vinsyncfeedlog`
--

DROP TABLE IF EXISTS `gm_vinsyncfeedlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_vinsyncfeedlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `product_id` varchar(215) DEFAULT NULL,
  `dealer_asc_id` varchar(15) DEFAULT NULL,
  `status_code` varchar(15) DEFAULT NULL,
  `email_flag` tinyint(1) NOT NULL,
  `ucn_count` int(11) DEFAULT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_vinsyncfeedlog`
--

LOCK TABLES `gm_vinsyncfeedlog` WRITE;
/*!40000 ALTER TABLE `gm_vinsyncfeedlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_vinsyncfeedlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_welcomekit`
--

DROP TABLE IF EXISTS `gm_welcomekit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_welcomekit` (
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `delivery_address` varchar(50) DEFAULT NULL,
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `expected_delivery_date` datetime DEFAULT NULL,
  `due_date` datetime DEFAULT NULL,
  `status` varchar(12) NOT NULL,
  `packed_by` varchar(50) DEFAULT NULL,
  `tracking_id` varchar(50) DEFAULT NULL,
  `resolution_flag` tinyint(1) NOT NULL,
  `shipped_date` datetime DEFAULT NULL,
  `delivery_date` datetime DEFAULT NULL,
  `pod_number` varchar(50) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `member_id` int(11) NOT NULL,
  `partner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `gm_welcomekit_b3c09425` (`member_id`),
  KEY `gm_welcomekit_42b53b76` (`partner_id`),
  CONSTRAINT `member_id_refs_id_e5808864` FOREIGN KEY (`member_id`) REFERENCES `gm_member` (`id`),
  CONSTRAINT `partner_id_refs_id_f635793b` FOREIGN KEY (`partner_id`) REFERENCES `gm_partner` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_welcomekit`
--

LOCK TABLES `gm_welcomekit` WRITE;
/*!40000 ALTER TABLE `gm_welcomekit` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_welcomekit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_zonalservicemanager`
--

DROP TABLE IF EXISTS `gm_zonalservicemanager`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_zonalservicemanager` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `zsm_id` varchar(50) DEFAULT NULL,
  `regional_office` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `zsm_id` (`zsm_id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_cffbc396` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_zonalservicemanager`
--

LOCK TABLES `gm_zonalservicemanager` WRITE;
/*!40000 ALTER TABLE `gm_zonalservicemanager` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_zonalservicemanager` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_accesstoken`
--

DROP TABLE IF EXISTS `oauth2_accesstoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_accesstoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `client_id` int(11) NOT NULL,
  `expires` datetime NOT NULL,
  `scope` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `oauth2_accesstoken_6340c63c` (`user_id`),
  KEY `oauth2_accesstoken_e0a0c5a7` (`token`),
  KEY `oauth2_accesstoken_4fea5d6a` (`client_id`),
  CONSTRAINT `client_id_refs_id_dffc817d` FOREIGN KEY (`client_id`) REFERENCES `oauth2_client` (`id`),
  CONSTRAINT `user_id_refs_id_71306ac9` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_accesstoken`
--

LOCK TABLES `oauth2_accesstoken` WRITE;
/*!40000 ALTER TABLE `oauth2_accesstoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_accesstoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_client`
--

DROP TABLE IF EXISTS `oauth2_client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_client` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `url` varchar(200) NOT NULL,
  `redirect_uri` varchar(200) NOT NULL,
  `client_id` varchar(255) NOT NULL,
  `client_secret` varchar(255) NOT NULL,
  `client_type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `oauth2_client_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_b463b928` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_client`
--

LOCK TABLES `oauth2_client` WRITE;
/*!40000 ALTER TABLE `oauth2_client` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_grant`
--

DROP TABLE IF EXISTS `oauth2_grant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_grant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `code` varchar(255) NOT NULL,
  `expires` datetime NOT NULL,
  `redirect_uri` varchar(255) NOT NULL,
  `scope` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `oauth2_grant_6340c63c` (`user_id`),
  KEY `oauth2_grant_4fea5d6a` (`client_id`),
  CONSTRAINT `client_id_refs_id_098c2f19` FOREIGN KEY (`client_id`) REFERENCES `oauth2_client` (`id`),
  CONSTRAINT `user_id_refs_id_8a95efb3` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_grant`
--

LOCK TABLES `oauth2_grant` WRITE;
/*!40000 ALTER TABLE `oauth2_grant` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_grant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth2_refreshtoken`
--

DROP TABLE IF EXISTS `oauth2_refreshtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `oauth2_refreshtoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `access_token_id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `expired` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `access_token_id` (`access_token_id`),
  KEY `oauth2_refreshtoken_6340c63c` (`user_id`),
  KEY `oauth2_refreshtoken_4fea5d6a` (`client_id`),
  CONSTRAINT `access_token_id_refs_id_b5577697` FOREIGN KEY (`access_token_id`) REFERENCES `oauth2_accesstoken` (`id`),
  CONSTRAINT `client_id_refs_id_3730d4ce` FOREIGN KEY (`client_id`) REFERENCES `oauth2_client` (`id`),
  CONSTRAINT `user_id_refs_id_e0af9726` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_refreshtoken`
--

LOCK TABLES `oauth2_refreshtoken` WRITE;
/*!40000 ALTER TABLE `oauth2_refreshtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_refreshtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rr_part_details`
--

DROP TABLE IF EXISTS `rr_part_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rr_part_details` (
  `det_id` int(11) NOT NULL DEFAULT '0',
  `baj_id` int(11) NOT NULL,
  `part_no` varchar(255) NOT NULL,
  `desc` longtext NOT NULL,
  `model` longtext NOT NULL,
  `valid_from` date NOT NULL,
  `models` varchar(255) NOT NULL,
  `cat_id` int(11) NOT NULL,
  `mrp` longtext NOT NULL,
  `active` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`det_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rr_part_details`
--

LOCK TABLES `rr_part_details` WRITE;
/*!40000 ALTER TABLE `rr_part_details` DISABLE KEYS */;
INSERT INTO `rr_part_details` VALUES (1,1,'24121642','ASSEMBLY AIR FILTER-SAI TYPE','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-02-18','24',1,'541',1),(60,60,'1100342','BEARING - BALL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AA,AF,AG,AM,AS,BA,BG,RA,BH',6,'108.5',1),(61,61,'3100338','BEARING WITH STEEL CAGE :- CRANKSHAFT','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AP,AS',6,'124',1),(62,62,'5101018','BEARING - NEEDLE ROLLER','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AS',6,'159',1),(63,63,'6101009','BEARING BALL','ASSEMBLY 3W RE','2002-04-01','22,24,AG,AS',6,'82',1),(64,64,'15101011','BEARING BALL','ASSEMBLY 3W RE','2002-04-01','22,24,AA,BB',6,'105',1),(66,66,'24100308','BEARING - BALL FOR MAINSHAFT','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AS,',6,'108',1),(67,67,'24130105','BEARING - BALL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AA,AB,AC,AF,AG,AM,AN,AP,AS,AT,BA,BG,BH,RA',6,'137',1),(68,68,'24181046','RACE UPPER BEARING','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2009-03-14','24,AA,AF,AG,AL,AM,AN,AP,AS,AT,AU,AZ,BA,RC',6,'76',1),(69,69,'30151065','BEARING BALL','ASSEMBLY 3W RE','2002-04-01','AL,BA,BB,BG',6,'68',1),(70,70,'39100120','BEARING BALL','ASSEMBLY 3W RE','2002-04-01','24,AG,AS',6,'79',1),(71,71,'39121420','BEARING BALL 20X42X1','ASSEMBLY 3W RE','2002-04-01','22,24,AA,BB,BG',6,'83',1),(72,72,'39132420','BEARING - BALL :- 25 X 62 X 17','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2002-04-01','AA,AB,AC,AF,AM,AN,AT,BA,BG,BH,RC',6,'209',1),(74,74,'39143620','BEARING - NEEDLE ROLLER','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB,BG,BH',6,'40',1),(75,75,'39148720','BEARING - BALL :- 30 X 55 X 9','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BB,BH,BA',6,'160',1),(103,103,'KPBB6007','BEARING BALL C3','RE COMPACT PETROL 4S','2003-06-16','AA,AF,AM,AN,BA,BB,BG,BH',6,'148',1),(104,104,'22151106','DRUM BRAKE C.I.4S PE','3WFE 2S A/R AD EXPIC','2004-09-01','22,24,AA,AB,AC,AF,AG,AK,AM,AP',7,'731',1),(105,105,'AL151093','DRUM BRAKE FR GC1000','3W RE DSL PICKUP VAN.OPTIONAL COLOUR','2002-04-01','AL,AN,AT,AU',7,'1373.5',1),(106,106,'AL151151','DRUM BRAKE RR C.I. G','RE DIESEL GC DAC COLR OPTIONAL','2003-06-16','AL,AN,AT,AU,BB',7,'815',1),(107,107,'AP151019','DRUM BRAKE WITH STUD','ASSEMBLY 3W RE 600 DSL WITH DOOR-NO COLO','2009-03-14','24,AP,BG,BH,RC',7,'1136',1),(108,108,'24151171','SHOE BRAKE','3W -2S VEHICLE','2004-01-09','',7,'204',1),(109,109,'24171094','SHOCKABSORBER ASSEMBLY - REAR','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2004-06-01','24,AA,AF,AG,AM',8,'559',1),(110,110,'24171137','SHOCKABSORBER ASSY COMP FR','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2008-04-01','24,AA,AF,AG,AS,BA',8,'566',1),(111,111,'AB171044','SHOCKABSORBER ASSEMBLY COMPLETE - FRONT','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2004-04-02','24,AA,AC,AF,AG',8,'570',1),(135,135,'AE131013','GASKET -FOR DIFFERENTIAL COVER:THK 0.8MM','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AS,AA',9,'46.15',1),(136,136,'AG121009','GASKET -FOR OIL PUMP FOR 3WH RE-2S LPG','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','0000-00-00','AL,AN,AT,AU',8,'635',1),(138,138,'AL131051','GASKET -GEAR BOX COVER','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BB,BG,BH',9,'23.75',1),(139,139,'AL131131','GASKET GEAR SHIFTER','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BB',9,'2.9',1),(140,140,'AN101012','GASKET - HEAD','3W4S RE A/R AD EXP WITH CAT ','2006-06-01','AA,AF,AM,AN,AT,AU,AZ',9,'79',1),(141,141,'AN101129','GASKET CENTRAL','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM,AZ',9,'68.1',1),(142,142,'AN101135','GASKET CYLINDER','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM,AZ',9,'17.5',1),(143,143,'AN101149','GASKET HEAD','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM',9,'89',1),(144,144,'AN101186','GASKET, CLUTCH COVER','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM',9,'66.1',1),(145,145,'AN101312','GASKET DIFFERENTIAL COVER','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM,AZ,RA',9,'52.7',1),(147,147,'AP101005','GASKET CYL BLOCK','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2006-05-01','24,AG,AP,AS',9,'4.8',1),(178,178,'AA101053','GEAR - SPEED :- 4','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2002-04-01','AF',10,'301',1),(179,179,'AA101057','GEAR - IDLER','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AT',10,'711',1),(180,180,'AA101122','GEAR - STARTER','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AB,AC,AF,AK',10,'429',1),(181,181,'AA101286','GEAR ASSEMBLY - SECTOR','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AF,AM,AZ',10,'466',1),(182,182,'AA101424','GEAR - OIL PUMP DRIVE','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AB,AC,AF,AK,AM,AN,AT',10,'51',1),(183,183,'AA101555','GEAR -REVERSE CONTROL','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AB,AC,AF,AM,AK',10,'408',1),(184,184,'AA101588','GEAR MULTIPLE','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2010-04-30','AA,RC',10,'359',1),(185,185,'AA101646','GEAR MULTIPLE II & III (205CC)','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2010-02-01','AA,AF,AM',10,'189.5',0),(189,189,'AA191082','GEAR CABLE ASSY COMP WHITE','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2012-07-21','AA,AF,AM,RC',10,'196',1),(190,190,'AA191083','GEAR CABLE ASSY COMP BLACK','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2012-07-21','AA,AF,AM,RC',10,'197',1),(200,200,'AP101158','GEAR MULTIPLE','ASSEMBLY 3WRE2S UGIN-NO COLOR','2002-04-01','AT',10,'482',1),(212,212,'24100808','PLATE THRUST','3W 2-ST RE A/R LPG/PERU COLR OPTIONAL','2003-06-02','24,AG,AS',11,'39',1),(213,213,'24101601','CLUTCH HOUSING','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2010-11-13','24',11,'462',1),(214,214,'24101611','PLATE CLUTCH','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2010-11-13','24',11,'21.5',1),(215,215,'24101676','CLUTCH LEVER EXTERNAL ASSEMBLY.','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2008-04-01','24,AG,AS',11,'70',1),(216,216,'24101734','CLUTCH ASSY. COMPLETE','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2010-01-01','24,AG,AS',11,'1615',0),(217,217,'24101781','CLUTCH ASSY. COMPLETE','RE COMPACT PETROL','2012-06-28','24,AG,AS',11,'1080',1),(218,218,'52240643','CLUTCH COVER SUB ASSEMBLY','RE COMPACT PETROL','2012-06-28','AS,AG,24',11,'595',1),(219,219,'AA101210','PLATE FRICTION','3W4SRE AUTORIKSHA WITH ANTIDIVE SUSPENSI','2002-04-01','AA,AB,AC,AF',11,'39.5',1),(220,220,'AA101469','CLUTCH COMPLETE','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AB,AC,AF',11,'2001',1),(221,221,'AA101470','PLATE ASSEMBLY - CLUTCH','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2002-04-01','AA,AB,AC,AF',11,'995',1),(238,238,'BG551406','CLUTCH ASSEMBLY COMP','ASSLY RE 900 WITH DOOR HI-DECK','2009-03-14','AL,BG',11,'2174',1),(239,239,'BG551411','PLATE CLUTCH','ASSEMBLY 3W RE 600 DSL WITH DOOR-NO COLO','2009-03-14','BG,BH',11,'1230.5',1),(240,240,'AE121001','VALVE ASSEMBLY - REED','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG',12,'103',1),(241,241,'AF141030','VALVE -CNG CYLINDER:-VANAZ  MAKE(V-0156)','ASSEMBLY 3WRE 2SUG CNG EL START-NO COLOR','2002-04-01','24,AF,AK,AS,AZ,RC',12,'1091.5',1),(242,242,'AN101418','VALVE INTAKE','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM,AZ,RA',12,'189',0),(243,243,'AN101431','VALVE EXHAUST','RE COMPACT PETROL 4S','2013-02-13','RA,AZ,AM,AF,AA',12,'182',0),(244,244,'BA102014','VALVE (INLET)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB,BG,BH',12,'174',1),(245,245,'BA102017','VALVE (EXHAUST)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2004-10-01','AL,BA,BB,BG',12,'172',1),(285,284,'BA102208','CRANKSHAFT WITH GEAR ASSEMBLY','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB,BH',15,'3590',1),(286,288,'22101198','CYL BL PIST ASSY FE2','3W2S PICK UP WITHOUT TRAY AND FRAME WITH','2002-04-01','22',16,'2060',1),(366,359,'24191138','CABLE COMP ACCELERATOR','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-05-01','24,AG',24,'167',1),(367,360,'24191139','CABLE COMPLETE REV GEAR CONTROL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2009-12-01','24,AG,AS',24,'185',1),(384,377,'AA191029','CABLE CLUTCH RE 4S','3W RE','0000-00-00','AA,AF',24,'141',1),(385,378,'AA191031','CABLE CLUTCH 4S PETR','3W RE/AR WITH 4 STROKE PETROL ENGINE+ANT','2002-04-01','AA,AF',24,'151',1),(386,379,'AA191064','CABLE CLUTCH RE 4S','3W RE/AR WITH 4 STROKE PETROL ENGINE+ANT','2006-01-02','AA,AF,AM',24,'144',1),(390,383,'AA191077','CABLE CLUTCH','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2010-07-31','AA',24,'148',1),(392,385,'AA191085','CABLE CLUTCH COMPLETE RE205','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2011-08-22','AA,AF,AN',24,'272',1),(393,386,'AA191091','CABLE ACCELERATOR COMPLETE','RE COMPACT PETROL 4S','2013-12-26','AM,AF,AA',24,'128',1),(394,387,'AA191092','CABLE CLUTCH COMPLETE','RE COMPACT PETROL 4S','2013-12-26','AA,AF,AM,AZ',24,'270',1),(395,388,'AA191093','CABLE GEAR BLACK COMPLETE','RE COMPACT PETROL 4S','2013-12-26','AA,AF,AM,AZ',24,'193',1),(396,389,'AA191094','CABLE GEAR WHITE COMPLETE','RE COMPACT PETROL 4S','2013-12-26','AA,AF,AM,AZ',24,'193',1),(398,391,'AA201248','CABLE ASSEMBLY','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2010-11-01','AA',24,'1313',1),(399,392,'AA201252','CABLE BATTERY RE205 FL','RE COMPACT PETROL 4S','2012-06-11','AA,AF,AM',24,'1474',1),(400,393,'AA251001','CABLE COMPLETE - FAREMETER','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AF,AA,AG',24,'108',1),(401,394,'AF191005','CABLE ASSEMBLY ACCELERATOR','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2011-08-22','AA,AF,AM,AZ',24,'122',1),(404,397,'AL151141','CABLE - RH :- HAND BRAKE','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2003-06-16','AL,AN,AT',24,'183',1),(405,398,'AL191007','CABLE COMPLETE REVERSE LOCK','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2003-06-16','AL,BB,BG,BH',24,'124',1),(406,399,'AL191011','CABLE CLUTCH GC 1000','BAJAJ DIESEL PASSENGER AR NO COLOUR','2004-10-01','BB',24,'176',1),(407,400,'AL191012','CABLE DECOMPRES GC10','3W RE DSL PICKUP VAN.OPTIONAL COLOUR','2002-04-01','AL,BB',24,'130',1),(408,401,'AL191019','CABLE COMPLETE - SPEEDOMETER','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2003-09-01','AF,AL,BB',24,'162',1),(409,402,'AL191033','CABLE DECOMPRESSION FIX END','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2005-10-01','AL,BB',24,'127',1),(411,404,'AL191036','CABLE COMPLETE ENGINE STOP : FIX END INN','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2008-04-01','AL,BB',24,'136',1),(419,412,'AN191037','CABLE REVERSE FIXED END','ASSEMBLY GCMAX CNG BSIII LOWDEC-NO COLOR','2011-08-07','AN',24,'169',1),(430,423,'BA191058','CABLE DECOMPRESSION','3W REAR ENGINE AUTO RIKSHA WITH DIESEL E','2005-10-10','BA',24,'55',1),(431,424,'BA191059','CABLE ENGINE STOP','3W REAR ENGINE AUTO RIKSHA WITH DIESEL E','2008-04-01','BA',24,'93',1),(432,425,'BB191007','CABLE ASSY. DECOMPRESSION','ASSLY RE 900 WITH DOOR HI-DECK','2010-08-01','AL',24,'122',1),(433,426,'BB191031','CABLE CLUTCH','RE MAXIMA DIESEL','2013-01-05','BB',24,'313',1),(434,427,'BG131802','CABLE ASSY HAND BRAKE FRONT','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2009-03-14','24,AG,AF,AM,AS,AZ,BA,BG,BH,RA,RC',24,'175',1),(435,428,'BG161201','CABLE ACCELERATOR','ASSEMBLY 3W RE 600 DSL WITH DOOR-NO COLO','2009-03-14','BG,BH,RC',24,'174',1),(436,429,'24111124','STATOR ASSY(MAGNETO HI POWER COMON CHAS)','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-02-18','24',25,'850',1),(437,430,'24111137','STARTER MOTOR','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2010-01-01','24,AG',25,'2972.5',1),(438,431,'24111151','STATOR ASSEMBLY','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2010-11-13','24',25,'924.5',1),(442,435,'24111150','MAGNETO ASSEMBLY','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2010-01-04','24',26,'2189',1),(454,447,'24201421','REVERSE SWITCH & CABLE ASSY.','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-01-04','24,AA,RC',28,'88.5',1),(455,448,'AA111031','SWITCH - REVERSE (NORMALLY OPEN)','3W4S RE A/R AD EXP WITH CAT SRILANKA','2002-04-01','AA,AF,AL,AM,AN,AT,AU',28,'90.5',1),(457,450,'AB201075','SWITCH - REAR BRAKE','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','23,AL,BA,BB,BG',28,'40.5',1),(458,451,'AB201077','SWITCH - HAZARD WARING','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2007-11-01','24,AA,AF,AG,AL,AM,AN,BA,BB,BG, BH',28,'144',1),(459,452,'AF201053','SWITCH (ON-OFF-ON)','ASSEMBLY 3WRE 2SUG LPG EL START-NO COLOR','2002-04-01','24,AF,AG,AM',28,'124.5',1),(461,454,'AF201094','SWITCH - BRAKE (SEALED DESIGN)','ASSEMBLY 3WRE2 UG ELECT START-NO COLOR','2010-01-01','24,AG',25,'2972.5',1),(464,457,'AL201060','SWITCH - CONTROL :- LH','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2005-07-01','24,AA,AF,AG,AL,AM,AN,AP,AS,AT',28,'104',1),(465,458,'AL201061','SWITCH - CONTROL :- RH','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2005-07-01','24,AA,AF,AG,AL,AM,AP,AS,AT,AU,AZ',28,'164',1),(466,459,'AN201008','BATTERY CUTOFF SWITCH WITH CABLE ASEMBLY','ASSEMBLY GCCNG H DEC W/O DOR,WI-NO COLOR','2007-08-01','AN',28,'852.5',1),(467,460,'AP111023','SWITCH NEUTRAL INTEGRATED CABLE','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2008-04-01','24,AA,AF,AL,AM,AN',28,'51',1),(471,464,'AZ401400','SWITCH G O P CNG VERTICAL FL','RE COMPACT CNG 4S-NO COLOR','2013-08-16','AZ,AF',28,'119',1),(473,466,'BH401400','SWITCH -REVERSE(1 POLE COUP N)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2008-04-01','AL,BA,BB',28,'54.5',1),(474,467,'RA401400','SWITCH G O P LPG VERTICAL FL','RE COMPACT LPG 4S - MF','2013-08-16','AM,RA',28,'119',1),(475,468,'24201472','ASSEMBLY TAIL LIGHT LH REFL','RE COMPACT PETROL','2012-06-11','24,AA,AF,AG,AM,AS,BA,BB',29,'441',1),(476,469,'24201473','ASSEMBLY TAIL LIGHT RH REFL','RE COMPACT PETROL','2012-06-12','BB,BA,AS,AM,AG,AF,AA,24',29,'440',1),(533,526,'BB201071','WIRE HARNESS COMBINED','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2013-07-06','AL,BB',32,'4775',1),(534,527,'22231142','BEADING - RUBBER WITH KEY','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','22,24,AB,AC,AH,AM,AN,BA,BG,RA',33,'509',1),(535,528,'24231661','BEADING PERIPHERAL FL','RE COMPACT PETROL','2013-04-17','BA,AS,AG,24',33,'819',1),(541,534,'AA231239','BEADING ONE PIECE W/S GLASS','RE COMPACT PETROL 4S','2013-08-04','AA,AF,AM,AZ,BB,BH,RA',33,'492',1),(542,535,'AL241065','BEADING -REAR GLASS:- DRIVER CABIN:RE-GC','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2003-12-01','AL,AN,BG,RC',33,'276',1),(545,538,'AL241199','BEADING SWIVELLING GLASS FRONT LH','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2008-01-01','AL,AN,BG,RC',33,'68',1),(546,539,'AL241200','BEADING SWIVELING GLASS REAR','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2007-02-01','AL,AN,BG,RC',33,'53',1),(547,540,'AL241204','BEADING FLOOR BOARD','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2007-11-01','AL,AN,BG,RC',33,'95',1),(548,541,'AL241212','BEADING SWIVELING GLASS RH FRONT','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2007-02-01','AL,AN,BG,RC',33,'67',1),(549,542,'AP161072','BEADING HEADLAMP HOUSING','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2009-02-01','24,AA,AC',33,'58',1),(550,543,'22230635','WIPER ASSEMBLY','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','22,24,AA,AB,AC,AF',34,'116',1),(551,544,'24201408','WIPER MOTOR(PIGTAIL & COUPLER)','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2008-04-01','22,AA,AF,AG,AM,AP',34,'846',1),(552,545,'AL201022','WIPER MOTOR- MAKE LUCAS TVS','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2004-02-02','AL,AN,AT,AU,BB',34,'1867',1),(553,546,'AL241023','WIPER ARM BLADE ASSEMBLY','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2003-06-16','24,AA,AC,AF,AG,AL,AM,AN,AP',34,'151',1),(554,547,'AP201057','WIPER MOTOR (WITH CAPACITOR)','ASSEMBLY 3WRE2S UG ELECT START-NO COLOR','2007-09-01','24,AA,AF,AG,AM,AN,AP,AS,AT',34,'1891.5',1),(618,611,'24161003','BOLT - HEXAGON','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2004-11-01','22,24,AA,AB,AC,AF,AG,AK',38,'20.5',1),(619,612,'39080204','BOLT - SQUARE','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB,BH',38,'5.4',1),(620,613,'39137704','BOLT - HEXAGON WITH COLLAR','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','22,23,24,AA,AB,AC,AF,AG,AK,AL',38,'12',1),(621,614,'39143104','BOLT - `D\' :- M8','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB,BG,BH',38,'5.8',1),(654,647,'52240573','BRACKET WITH ADJUSTER','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2008-04-01','AS,AG,24',39,'35',1),(655,648,'AA101194','BRACKET - FRONT MOUNTING','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AF,AM,AN',39,'61',1),(656,649,'AA101337','BRACKET FOR CLUTCH CABLE','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AF,AM,AT,AU,AZ',39,'13',1),(657,650,'AA101628','BRACKET FOR OIL COOL PIPE MTG.','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2010-04-30','RC,RA,AZ,AM,AF,AA',39,'14',1),(661,654,'AA161106','BRACKET FOR FLASHER','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2004-10-01','22,24,AA,AB,AG,AL,AM',39,'9.5',0),(662,655,'AA161225','BRACKET CONTROL MOUNTING FL','RE COMPACT PETROL 4S','2013-09-07','RA,BH,AZ,AA,AF,AM',39,'98',1),(663,656,'AA201090','BRACKET - MOUNTING :- TAIL LIGHT','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2004-10-01','22,24,AA,AB,AF,AG,AK,AL,AM,AN',39,'6.4',1),(667,660,'AL161253','BRACKET ISOLATOR','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2006-12-01','AL,BB',39,'62',1),(668,661,'AL161344','BRACKET ASSEMBLY: BRAKE PEDAL MOUNTING.','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2008-04-01','AA,AL,AN,AT,AU,BB,BH',39,'108',1),(669,662,'AL241188','BRACKET GLASS SWIVELLING','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2006-12-01','AL,AN,BG',39,'3.4',1),(670,663,'AN101055','BRACKET-ENGINE & AIR FILTER MOUNTING','ASSEMBLY GCCNG H DEC W/O DOR,WI-NO COLOR','2006-06-01','AN',39,'398',0),(671,664,'AN101305','BRACKET REVERSE CABLE','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM,AZ,RA',39,'107',1),(672,665,'AN101334','BRACKET SUPPORT-OIL TUBE','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM,AZ,RA',39,'13',1),(673,666,'AN101423','BRACKET FOR OILCOOLER FL','RE COMPACT PETROL 4S','2013-10-10','AA,AF,AM,AZ,RA',39,'9.8',1),(674,667,'AN121206','BRACKET OIL COOLER MTG.','RE COMPACT PETROL 4S','2012-04-15','RA,AZ,AM,AF,AA',39,'55',1),(679,672,'BA102265','BRACKET DECOMPRESSION','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB,BG,BH',39,'28',0),(680,673,'BA102301','BRACKET COMPLETE ROCKER ARM','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2008-04-01','BH,BG,BB,BA',39,'99',1),(681,674,'BA161134','BRACKET ASSEMBLY - TMC MOUNTING','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2004-11-01','22,24,AA,AB,AC,AF,AG,AK,AM,AN',39,'230',1),(682,675,'BG113806','BRACKET FOR THREE WAY CONNECTION','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2009-03-14','24,BG,BH',39,'15',0),(683,676,'BG551402','BRACKET CLUTCH CABLE','ASSLY RE 900 WITH DOOR HI-DECK','2009-03-14','AL,BG,BH',39,'65',1),(684,677,'BG561401','BRACKET GEAR & REV CABLE','ASSLY RE 900 WITH DOOR HI-DECK','2009-03-01','AL,BG,BH',39,'130',1),(685,678,'AL101011','TUBE - OIL :- 3 (COOLER TO FILTER)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2003-06-16','AL,BB',40,'78',1),(686,679,'BA102146','TUBE (BREATHER)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB,BG',40,'41',1),(687,680,'AL121063','TUBE AIR-1 (FILTER~MANIFOLD)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2006-12-01','AL,BB',40,'126',1),(690,683,'AA101291','TUBE ASSEMBLY - STARTING :- HAND START','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2004-10-01','AA,AF,AM',40,'382',0),(691,684,'BA102235','TUBE ASSEMBLY (1 OIL)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BB,BA,BG,BH',40,'39',1);
/*!40000 ALTER TABLE `rr_part_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rr_part_pricing`
--

DROP TABLE IF EXISTS `rr_part_pricing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rr_part_pricing` (
  `sno` int(11) NOT NULL AUTO_INCREMENT,
  `ITEM_CD` varchar(255) NOT NULL,
  `ITEM_DESC` varchar(255) NOT NULL,
  `NEW_MRP` varchar(255) NOT NULL,
  `SET_QTY` int(11) NOT NULL,
  `MARGIN_CD` varchar(255) NOT NULL,
  `cat` varchar(255) NOT NULL,
  `active` int(11) NOT NULL DEFAULT '1',
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=4992 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rr_part_pricing`
--

LOCK TABLES `rr_part_pricing` WRITE;
/*!40000 ALTER TABLE `rr_part_pricing` DISABLE KEYS */;
INSERT INTO `rr_part_pricing` VALUES (1,'1100315','PLATE   SPRING LOWER','2.20',5,'A','3W',1),(2,'1100316','PLATE   SPRING  UPPE','2.20',5,'A','3W',1),(3,'1100341','CIRCLIP OIL SEAL LOC','12.60',5,'A','3W',1),(4,'1100342','BEARING  BALL','109.00',1,'A','3W',1),(5,'1100610','KEY WOODRUFF MAGNETO','3.90',5,'A','3W',1),(6,'1100611','KEY WOODRUFF CLUTCH','4.50',5,'A','3W',1),(7,'1100612','WASHER   FAN DISC','2.90',10,'A','3W',1),(8,'1100613','NUT WITH COLLAR','12.00',1,'A','3W',1),(9,'1100614','RING  LOCK FOR NUT','2.80',10,'A','3W',1),(10,'1100711','RING  SHOULDER 1 TO ','19.50',1,'A','3W',1),(11,'1100712','SHOULDER RING','16.00',1,'A','3W',1),(12,'1100713','RING   SHOULDER    N','21.00',1,'A','3W',1),(13,'1100714','RING   SHOULDER    N','18.00',1,'A','3W',1),(14,'1100804','SPRING CLUTCH','1.94',50,'A','3W',1),(15,'1100817','RING  LOCK','6.80',5,'A','3W',1),(16,'1100818','WASHER  BRASS','9.20',5,'A','3W',1),(17,'1100823','BUSH SINTERED','45.00',1,'A','3W',1),(18,'1100828','SPACER','5.20',5,'A','3W',1),(19,'1100905','RING  O','1.10',20,'A','3W',1),(20,'1101008','ROLLER','0.34',25,'A','3W',1),(21,'1101205','SPRING  RETURN','26.00',1,'A','3W',1),(22,'1110609','WASHER PLAIN','0.20',50,'A','3W',1),(23,'1160509','BOLT HEX HEAD','0.95',20,'A','3W',1),(24,'1160717','CLIP LOCK','2.00',5,'A','3W',1),(25,'1180123','BALL STEEL','0.90',10,'A','3W',1),(26,'1190205','WASHER   SPRING','0.54',25,'A','3W',1),(27,'1200213','WASHER  CUP','2.40',10,'A','3W',1),(28,'3100335','BEARING NEEDLE','40.00',1,'A','3W',1),(29,'3100338','BEARING +STEEL CAGE','129.00',1,'A','3W',1),(30,'3100619','BEARING ROLLER SMALL','23.50',1,'A','3W',1),(31,'3100620','BEARING ROLLER SMALL','23.50',1,'A','3W',1),(32,'3100621','BEARING ROLLER SMALL','23.50',1,'A','3W',1),(33,'3100622','BEARING SMALL END','23.50',1,'A','3W',1),(34,'3100802','BOX CLUTCH','82.00',1,'A','3W',1),(35,'3150207','RING O','0.95',10,'A','3W',1),(36,'3170109','PIN','2.30',5,'A','3W',1),(37,'3170121','PIN HUB 10 MM','31.00',1,'A','3W',1),(38,'3170127','CIRCLIP','6.40',5,'A','3W',1),(39,'3180116','RING O','1.10',10,'A','3W',1),(40,'3190204','WASHER PLAIN','0.52',50,'A','3W',1),(41,'3190206','WASHER   PLAIN','0.40',25,'A','3W',1),(42,'5101018','BEARING NEEDLE','160.00',1,'A','3W',1),(43,'5101051','BREATHER ASSEMBLY','11.00',1,'A','3W',1),(44,'5101071','KIT PLATE CLUSTER GE','54.00',1,'A','3W',1),(45,'5101072','PLATE THRUST','16.00',1,'A','3W',1),(46,'5101083','ADJUSTER WITH NUT','5.80',5,'A','3W',1),(47,'5151012','ADJUSTER WITH NUT','8.00',5,'A','3W',1),(48,'5190301','DRIVE COMP SPEEDOMET','59.00',1,'A','3W',1),(49,'5190302','GEAR ASSY  NYLON','12.50',1,'A','3W',1),(50,'5191005','SUPPORT','33.00',1,'A','3W',1),(51,'5191046','SCREW TERMINAL ASSY','3.70',5,'A','3W',1),(52,'6100702','STEM SUPER / CHETAK ','51.00',1,'A','3W',1),(53,'6101007','GEAR STARTER','112.00',1,'A','3W',1),(54,'6101009','BEARING  BALL','83.00',1,'A','3W',1),(55,'6101056','CROSS','172.00',1,'A','3W',1),(56,'6101112','SPRING','2.10',5,'A','3W',1),(57,'6101169','CYL BL.PISTON ASSY S','1876.00',1,'A','3W',1),(58,'6101213','SPACER  CLASSIC','18.50',1,'A','3W',1),(59,'6111266','SWITCH NEUTRAL CLASS','31.00',1,'A','3W',1),(60,'6111279','PICKUP ASSEMBLY 12V','73.00',1,'A','3W',1),(61,'6111350','CAP SPARK PLUG','62.00',1,'A','3W',1),(62,'6160713','SPRING FOR LOCK','0.90',25,'A','3W',1),(63,'6180303','SPRING','0.56',25,'A','3W',1),(64,'6191061','LUBRICATOR  ASSY','5.00',5,'A','3W',1),(65,'6191089','GRIP HAND  CLASSIC','43.00',1,'A','3W',1),(66,'6201082','LAMP 12V  5W','14.50',1,'A','3W',1),(67,'6201083','LAMP 12V  10W','17.00',1,'A','3W',1),(68,'6201204','REFLECTOR WITH GLASS','80.00',1,'A','3W',1),(69,'6221028','PAD SHOCK','1.50',1,'A','3W',1),(70,'7181009','BALL STEEL+NYLON CAG','18.00',1,'A','3W',1),(71,'8111018','COIL CHARGING','187.00',1,'A','3W',1),(72,'10111009','COIL PICKUP','49.00',1,'A','3W',1),(73,'13101024','SHAFT ROCKER ARM','22.50',1,'A','3W',1),(74,'13101031','CAP','39.00',1,'A','3W',1),(75,'13101165','GASKET','7.40',5,'A','3W',1),(76,'15101011','BEARING  BALL','93.00',1,'A','3W',1),(77,'15101122','GASKET','11.20',5,'A','3W',1),(78,'15101171','RING  SPACER','16.60',5,'A','3W',1),(79,'16111125','PLUG  SPARK WR4AC','75.00',1,'A','3W',1),(80,'16121138','NEEDLE ASSEMBLY','205.00',1,'A','3W',1),(81,'16201055','SPRING STOP SWITCH','3.40',5,'A','3W',1),(82,'18201044','LAMP :- 12V - 10W - ','16.00',1,'A','3W',1),(83,'19101003','GASKET HEAD CYLINDER','36.00',1,'A','3W',1),(84,'19101014','GEAR SPEED  1','381.00',1,'A','3W',1),(85,'19101016','RING  SHOULDER','14.00',1,'A','3W',1),(86,'19101017','RING  SHOULDER  NO. ','14.50',1,'A','3W',1),(87,'19101018','RING  SHOULDER  NO. ','15.00',1,'A','3W',1),(88,'19101019','RING  SHOULDER  NO. ','14.50',1,'A','3W',1),(89,'19101020','RING  SHOULDER  NO. ','15.50',1,'A','3W',1),(90,'19161151','RIVET PUSH (BLACK CO','0.60',10,'A','3W',1),(91,'20101020','GASKET ALUMINIUM','1.00',1,'A','3W',1),(92,'20201029','LAMP 12V  21/5W, P 2','23.50',1,'A','3W',1),(93,'21100324','CIRCLIP','2.00',10,'A','3W',1),(94,'21101408','SPRING  RETURN','28.00',1,'A','3W',1),(95,'21101427','SPRING','3.10',5,'A','3W',1),(96,'21101429','CLIP SPRING','0.85',10,'A','3W',1),(97,'21130110','BEARING  BALL','113.00',1,'A','3W',1),(98,'21150220','SPRING  RETURN','7.60',5,'A','3W',1),(99,'21150307','TYRE FOR 3 WHEELER','1504.00',1,'A','3W',1),(100,'21150404','PACKING INNER VALVE','1.00',10,'A','3W',1),(101,'21150406','BODY  VALVE','19.50',1,'A','3W',1),(102,'21150420','PIN FORK','1.60',10,'A','3W',1),(103,'21150422','PACKING WASHER COPPE','5.80',5,'A','3W',1),(104,'21160417','PLATE REINFORCEMENT','7.20',5,'A','3W',1),(105,'21170419','CIRCLIP','6.40',5,'A','3W',1),(106,'21180307','KNOB','5.80',5,'A','3W',1),(107,'21180308','SPRING','1.20',10,'A','3W',1),(108,'22100703','CROSS','187.00',1,'A','3W',1),(109,'22101038','PIN GEAR MULTIPLE','91.00',1,'A','3W',1),(110,'22101081','SPRING','0.94',25,'A','3W',1),(111,'22101085','PLATE SET CLUSTER GE','43.00',1,'A','3W',1),(112,'22101095','CYL BL PIST ASSY FE2','1923.00',1,'A','3W',1),(113,'22101198','CYL BLOCK ASSY FE2S3','2064.00',1,'A','3W',1),(114,'22101211','RING  PISTON  STD FE','118.00',1,'A','3W',1),(115,'22101423','PLUG','6.40',5,'A','3W',1),(116,'22111089','COIL PICKUP','78.00',1,'A','3W',1),(117,'22120504','NEEDLE','26.00',1,'A','3W',1),(118,'22121009','FILTER AIR CLEANER  ','422.00',1,'A','3W',1),(119,'22130129','LEVER AND SECTOR COM','70.00',1,'A','3W',1),(120,'22130147','CUP FOR SPRING','1.90',10,'A','3W',1),(121,'22130152','BLOCK  SLIDER','4.50',5,'A','3W',1),(122,'22131014','SPACER','14.50',1,'A','3W',1),(123,'22131018','GEAR SATELLITE','84.00',1,'A','3W',1),(124,'22150240','SPRING  RETURN','3.80',10,'A','3W',1),(125,'22150241','WASHER  PLAIN','0.48',50,'A','3W',1),(126,'22150242','SPRING','2.05',10,'A','3W',1),(127,'22150243','WASHER  SPECIAL','1.56',25,'A','3W',1),(128,'22150435','BOLT','0.76',25,'A','3W',1),(129,'22150439','PISTON 4S PETR / CNG','20.00',1,'A','3W',1),(130,'22150442','SCREW AIR OUTLET','8.00',5,'A','3W',1),(131,'22150451','SCREW CYLINDER SECUR','2.10',5,'A','3W',1),(132,'22150459','PISTON FOR MASTER CY','46.00',1,'A','3W',1),(133,'22150507','RATCHET','80.00',1,'A','3W',1),(134,'22151068','TYRE WITH TUBE','1921.50',1,'A','3W',1),(135,'22151081','DISC COMPLETE  LEFT','275.00',1,'A','3W',1),(136,'22151086','DISC COMPLETE  RIGHT','275.00',1,'A','3W',1),(137,'22151097','BOTTLE  BRAKE FLUID','58.00',1,'A','3W',1),(138,'22151106','DRUM BRAKE C.I.4S PE','774.00',1,'A','3W',1),(139,'22161193','STRIP - FOAM','1.00',1,'A','3W',1),(140,'22161221','NUMBER PLATE DIMENS','34.00',1,'A','3W',1),(141,'22161238','BRACKET FR NUMBR PL','35.00',1,'A','3W',1),(142,'22170115','SEAL  OIL','16.50',1,'A','3W',1),(143,'22170118','SPACER','4.20',5,'A','3W',1),(144,'22170345','PLATE LOCK','1.25',10,'A','3W',1),(145,'22170434','BOLT FOR AXLE','6.80',5,'A','3W',1),(146,'22171007','SEAL OIL','16.50',1,'A','3W',1),(147,'22171080','PLATE LOCK','1.65',10,'A','3W',1),(148,'22180219','PLATE LOCK STEERING','13.00',1,'A','3W',1),(149,'22181036','COLUMN STEERING FE 2','2232.00',1,'A','3W',1),(150,'22181058','ST LOCK PLATE ASSY','23.00',1,'A','3W',1),(151,'22191073','LEVER','48.00',1,'A','3W',1),(152,'22191096','CABLE SPEEDOMETER 4S','93.00',1,'A','3W',1),(153,'22191097','CABLE INNER SPEEDO F','34.00',1,'A','3W',1),(154,'22200161','GROMMET','4.10',5,'A','3W',1),(155,'22230635','WIPER ASSEMBLY','125.00',1,'A','3W',1),(156,'22231142','BEADING RUBBER + KEY','510.00',1,'A','3W',1),(157,'22231258','GLASS CENTRAL LAPPLE','822.25',4,'A','3W',1),(158,'22250132','ELECT CABLE ASSY','26.00',1,'A','3W',1),(159,'23161305','NIPPLE GREASE','4.90',5,'A','3W',1),(160,'24100305','BUSH','39.00',1,'A','3W',1),(161,'24100308','BEARING BALL','142.00',1,'A','3W',1),(162,'24100314','SEAL OIL','14.00',1,'A','3W',1),(163,'24100703','GEAR SPEED  4','233.00',1,'A','3W',1),(164,'24100704','GEAR SPEED  3','301.00',1,'A','3W',1),(165,'24100705','GEAR SPEED  2','329.00',1,'A','3W',1),(166,'24100808','PLATE THRUST','40.00',1,'A','3W',1),(167,'24100809','CLIP SPRING','3.50',5,'A','3W',1),(168,'24100907','LEVER INTERNAL','16.50',1,'A','3W',1),(169,'24100908','PLUNGER','87.00',1,'A','3W',1),(170,'24101049','GEAR SPEED 4','250.00',1,'A','3W',1),(171,'24101050','GEAR SHIFTER ASSY RE','229.00',1,'A','3W',1),(172,'24101054','GEAR MULTIPLE','1261.00',1,'A','3W',1),(173,'24101055','GEAR MULTIPLE','699.00',1,'A','3W',1),(174,'24101056','PIN GEAR MULTIPLE','102.00',1,'A','3W',1),(175,'24101064','LEVER INTERNAL','8.00',1,'A','3W',1),(176,'24101067','LEVER ASSY  CLUTCH E','63.00',1,'A','3W',1),(177,'24101069','BREATHER ASSEMBLY','18.00',1,'A','3W',1),(178,'24101076','GEAR ENGINE','261.00',1,'A','3W',1),(179,'24101077','GEAR SHIFTER ASSY RE','248.00',1,'A','3W',1),(180,'24101087','TUBE STARTING','289.00',1,'A','3W',1),(181,'24101096','SPRING  RETURN','5.40',5,'A','3W',1),(182,'24101100','SHAFT MAIN','787.00',1,'A','3W',1),(183,'24101111','BRACKET ASY ROLLER','11.50',1,'A','3W',1),(184,'24101114','KIT PLATE CLUSTER GE','56.00',1,'A','3W',1),(185,'24101121','BOLT   EYE WITH BUSH','46.00',1,'A','3W',1),(186,'24101122','BOLT  EYE WITH BUSH','45.00',1,'A','3W',1),(187,'24101155','COWLING .RE 2S','104.00',1,'A','3W',1),(188,'24101177','HANDLE STARTING WITH','296.00',1,'A','3W',1),(189,'24101201','GEAR ASSY  SECTOR','313.00',1,'A','3W',1),(190,'24101203','DOG DRIVEN','117.00',1,'A','3W',1),(191,'24101205','FAN COVER','80.00',1,'A','3W',1),(192,'24101206','CRANKSHAFT ASSY','1422.00',1,'A','3W',1),(193,'24101409','PIN LEVER SUPPORT','45.00',1,'A','3W',1),(194,'24101414','WASHER','14.20',5,'A','3W',1),(195,'24101416','TUBE CONNECTING','121.00',1,'A','3W',1),(196,'24101419','NUT HEX L H THREAD','3.10',5,'A','3W',1),(197,'24101421','PIN','9.00',5,'A','3W',1),(198,'24101422','PIN','8.50',1,'A','3W',1),(199,'24101545','PIVOT  CLUTCH','28.00',1,'A','3W',1),(200,'24101546','ROD-CONNECTING FOR `','276.00',1,'A','3W',1),(201,'24101547','CRANKSHAFT ASLY 3WH ','1309.00',1,'A','3W',1),(202,'24101552','GASKET FOR CCASE','35.80',10,'A','3W',1),(203,'24101557','GEAR ASSY MULTIPLE','1268.00',1,'A','3W',1),(204,'24101570','GEAR ENGINE 3WH2','250.00',1,'A','3W',1),(205,'24101571','CLUTCH ASSY RE2S CNG','883.00',1,'A','3W',1),(206,'24101590','CRANKSHAFT','1526.00',1,'A','3W',1),(207,'24101594','SPACER','15.50',1,'A','3W',1),(208,'24101595','COVER CLUTCH ASSLY','1012.00',1,'A','3W',1),(209,'24101597','BRACKET FOR ADJUSTER','15.00',1,'A','3W',1),(210,'24101598','PIPE BREATHER','23.50',1,'A','3W',1),(211,'24101599','BRACKET FOR ADJUSTER','36.00',1,'A','3W',1),(212,'24101601','CLUTCH HOUSING','464.00',1,'A','3W',1),(213,'24101611','PLATE CLUTCH','21.67',3,'A','3W',1),(214,'24101614','PLUNGER','91.00',1,'A','3W',1),(215,'24101615','TUBE CONNECTING ASSY','242.00',1,'A','3W',1),(216,'24101616','CONNECTOR   TUBE CON','42.00',1,'A','3W',1),(217,'24101621','BASE PLATE ASSLY','320.00',1,'A','3W',1),(218,'24101622','DRIVE SHAFT','23.50',1,'A','3W',1),(219,'24101623','GASKET CLUTCH COVER','64.00',1,'A','3W',1),(220,'24101624','CRANKCASE CLUTCH SID','3419.00',1,'A','3W',1),(221,'24101627','MULTIPLE GEAR PIN','100.00',1,'A','3W',1),(222,'24101628','LOCK WASHER','1.70',10,'A','3W',1),(223,'24101629','CYL BL PIST ASSY','1852.00',1,'A','3W',1),(224,'24101632','CYLINDER HEAD','518.00',1,'A','3W',1),(225,'24101633','CRANKCASE CLUTCH SID','3593.00',1,'A','3W',1),(226,'24101634','CRANKCASE MAGNETO SI','2149.00',1,'A','3W',1),(227,'24101635','NUT SPECIAL','12.50',1,'A','3W',1),(228,'24101636','WASHER PLAIN (SPRING','1.85',10,'A','3W',1),(229,'24101639','ASSLY ENGINE','25271.00',1,'C','3W',1),(230,'24101640','ASSEMBLY ENGINE','34519.00',1,'C','3W',1),(231,'24101645','SILENCER COMP. WITH','8484.00',1,'A','3W',1),(232,'24101674','CLUTCH COVER','274.00',1,'A','3W',1),(233,'24101676','CLUTCH LEVER  ASSY','72.00',1,'A','3W',1),(234,'24101681','CLUTCH HOUSING','534.00',1,'A','3W',1),(235,'24101687','DEFLECTOR FOR OIL','48.00',1,'A','3W',1),(236,'24101702','COLLAR','49.00',1,'A','3W',1),(237,'24101704','PLATE CLUTCH HUB','10.67',3,'A','3W',1),(238,'24101707','COLLAR FOR CLUTCH','73.00',1,'A','3W',1),(239,'24101711','NUT M14X1','17.00',1,'A','3W',1),(240,'24101712','LOCK WASHER','3.50',5,'A','3W',1),(241,'24101713','PIN MULTIPLE GEAR','103.00',1,'A','3W',1),(242,'24101714','WASHER   MG PIN','3.70',10,'A','3W',1),(243,'24101720','BUSH FOR EYE PIN','3.90',10,'A','3W',1),(244,'24101723','GASKET HEAD CYLINDER','46.00',1,'A','3W',1),(245,'24101725','SPACER HUB CLUTCH','28.00',1,'A','3W',1),(246,'24101726','HOLDER WHEEL CLUTCH','64.00',1,'A','3W',1),(247,'24101727','HOLDER BRG CLUTCH','39.00',1,'A','3W',1),(248,'24101736','PLATE CLUTCH ASSY','1043.00',1,'A','3W',1),(249,'24101737','HUB CLUTCH WITH ST G','571.00',1,'A','3W',1),(250,'24101741','SPRING CLUTCH','9.67',6,'A','3W',1),(251,'24101742','NUT CLUTCH M14X1','19.00',1,'A','3W',1),(252,'24101746','WHEEL CLUTCH','77.00',1,'A','3W',1),(253,'24101751','PLATE CLUTCH','37.00',1,'A','3W',1),(254,'24101764','CRANKCASE MAGNETO SI','1386.00',1,'A','3W',1),(255,'24101766','COVER SPARKPLUG FACE','71.00',1,'A','3W',1),(256,'24101767','CRANKSHAFT ASSLY FAC','1605.00',1,'A','3W',1),(257,'24101771','GROMMET COVER FAN FA','12.00',1,'A','3W',1),(258,'24101774','CYLINDER PISTON ASSY','1989.00',1,'A','3W',1),(259,'24101778','ASSLY SILENCER WITH ','4941.00',1,'A','3W',1),(260,'24101779','ASSLY MANIFOLD AIR I','304.00',1,'A','3W',1),(261,'24101781','CLUTCH COMPLETE','1082.00',1,'A','3W',1),(262,'24101782','GEAR ENGINE','257.00',1,'A','3W',1),(263,'24101784','ENGINE ASSLY COMPLET','32024.00',1,'C','3W',1),(264,'24101791','GEAR CORONA','478.00',1,'A','3W',1),(265,'24101792','GEAR MULTIPLE ASSY C','1360.00',1,'A','3W',1),(266,'24101793','ASSLY LEVER AND SECT','98.00',1,'A','3W',1),(267,'24101803','GEAR 4TH SPEED','251.00',1,'A','3W',1),(268,'24101804','GEAR 3RD SPEED','304.00',1,'A','3W',1),(269,'24101805','GEAR 2ND SPEED','333.00',1,'A','3W',1),(270,'24101806','GEAR 1ST SPEED','383.00',1,'A','3W',1),(271,'24101817','CRANKCASE MAGNETO SI','1384.00',1,'A','3W',1),(272,'24101825','ENGINE ASSLY COMPLET','28543.00',1,'C','3W',1),(273,'24101829','ASSLY SHAFT PROPELLE','424.00',1,'A','3W',1),(274,'24101830','ASSLY SHAFT PROPELLE','649.00',1,'A','3W',1),(275,'24101859','ASSLY FLANGE WHEEL S','467.00',1,'A','3W',1),(276,'24101865','HUB CLUTCH WITH STAR','530.00',1,'A','3W',1),(277,'24101866','ASSLY PLATE CLUTCH C','1056.00',1,'A','3W',1),(278,'24101867','ASSLY CLUTCH COMP-PE','1621.00',1,'A','3W',1),(279,'24101868','ASSLY CLUTCH COMP-CN','1621.00',1,'A','3W',1),(280,'24101870','ASSEY CRANKSHAFT COM','1460.00',1,'A','3W',1),(281,'24101871','DRIVE SHAFT','26.00',1,'A','3W',1),(282,'24101875','ASSLY SILENCER WITH ','8497.00',2,'A','3W',1),(283,'24101879','CLIP CABLE','15.00',1,'A','3W',1),(284,'24101880','ASSLY STARTING TUBE ','349.00',1,'A','3W',1),(285,'24101881','ASSLY STARTING TUBE ','297.00',1,'A','3W',1),(286,'24101899','PIN MULTIPLE GEAR','108.00',1,'A','3W',1),(287,'24101900','CRANKCASE CLUTCH SID','2317.00',1,'A','3W',1),(288,'24101901','COVER CLUTCH','356.00',1,'A','3W',1),(289,'24101925','ASSLY PISTON SAMKRG ','532.00',1,'A','3W',1),(290,'24101937','GEAR MULTIPLE ASSY C','1377.00',1,'A','3W',1),(291,'24101938','GEAR MULTIPLE RE145F','709.00',1,'A','3W',1),(292,'24101939','GEAR 2ND SPEED RE145','360.00',1,'A','3W',1),(293,'24101942','ASSLY MAIN SHAFT COM','2668.00',1,'A','3W',1),(294,'24110817','RING O','1.30',5,'A','3W',1),(295,'24111024','COIL CHARGING','224.00',1,'A','3W',1),(296,'24111062','COIL L.T.NO.1FOR12V','236.00',1,'A','3W',1),(297,'24111065','COIL L.T.NO.2FOR12V','234.00',1,'A','3W',1),(298,'24111095','MAGNETO ASSY  RE 2S','1778.00',1,'A','3W',1),(299,'24111099','CHARGING COIL','162.00',1,'A','3W',1),(300,'24111107','BOLT SPECIAL PL FAN','11.50',1,'A','3W',1),(301,'24111109','GROMMET (H.T.CABLE/C','7.40',5,'A','3W',1),(302,'24111113','RUBBER GROMMET (H.T.','5.60',5,'A','3W',1),(303,'24111117','ROTOR ASSEMBLY','880.00',1,'A','3W',1),(304,'24111119','CDI WITH DAMPER RE 2','849.00',1,'A','3W',1),(305,'24111120','CDI GAS CHOKE CONTRO','966.00',1,'A','3W',1),(306,'24111121','COIL H T RED FO','324.00',1,'A','3W',1),(307,'24111123','MAGNETO ASSEMBLY','1929.00',1,'A','3W',1),(308,'24111124','STATOR ASSYHI POWER','852.00',1,'A','3W',1),(309,'24111128','CDI WITH DAMPER(NEW)','245.00',1,'A','3W',1),(310,'24111132','CDI GAS PETR SOLEN','757.00',1,'A','3W',1),(311,'24111137','MOTOR STARTER','2978.00',1,'A','3W',1),(312,'24111140','DC CDI WITH STARTER ','1347.00',1,'A','3W',1),(313,'24111145','FAN(PLASTIC) (70 EX)','60.00',1,'A','3W',1),(314,'24111147','ROTOR ASSEMBLY','998.00',1,'A','3W',1),(315,'24111150','MAGNETO ASSLY','2193.00',1,'A','3W',1),(316,'24111151','STATOR ASSY','927.00',1,'A','3W',1),(317,'24111152','DC CDI<(>&<)>STARTER','957.00',1,'A','3W',1),(318,'24111154','MAGNETO ASSEMBLY','2160.00',1,'A','3W',1),(319,'24111155','ROTOR ASSEMBLY(25DEG','953.00',1,'A','3W',1),(320,'24111168','FIXING BRACKET ASSY','284.00',1,'A','3W',1),(321,'24111169','INTER BRACKET ASSY.','232.00',1,'A','3W',1),(322,'24111170','ARMATURE ASSY','728.00',1,'A','3W',1),(323,'24111171','GEAR SHAFT ASSY','1377.00',1,'A','3W',1),(324,'24111172','GEAR SHAFT UNIT','329.00',1,'A','3W',1),(325,'24111173','O RING FOR SPIGOT','1.70',10,'A','3W',1),(326,'24111174','SEAL KIT','29.00',1,'A','3W',1),(327,'24111188','CDI DC FOR RE 145CNG','1159.00',1,'A','3W',1),(328,'24111189','CDI DC FOR RE145 D P','882.00',1,'A','3W',1),(329,'24111190','CDI AC W/ DAMPER-RE1','363.00',1,'A','3W',1),(330,'24111192','MAGNETO ASSY RE145D','1950.00',1,'A','3W',1),(331,'24111194','ROTOR ASSY RE145D','982.00',1,'A','3W',1),(332,'24111195','MAGNETO ASSY RE145','1948.00',1,'A','3W',1),(333,'24111197','ROTOR ASY_15DEG_6P_R','943.00',1,'A','3W',1),(334,'24111198','STATOR ASLY_6P_RE145','955.00',1,'A','3W',1),(335,'24111200','COIL ASY PICK UP','55.00',1,'A','3W',1),(336,'24111201','MAGNETO ASSLY.','2518.00',1,'A','3W',1),(337,'24111202','ROTOR ASSY.COMPLETE','1730.00',1,'A','3W',1),(338,'24111205','STATOR ASSLY','786.00',1,'A','3W',1),(339,'24111207','H.T.COIL WITH CABLE ','269.00',1,'A','3W',1),(340,'24111208','MAGNETO ASSY.(15 DEG','1986.00',1,'A','3W',1),(341,'24111210','ROTOR ASSY. (15 DEG.','1015.00',1,'A','3W',1),(342,'24111211','STATOR ASSEMBLY','934.00',1,'A','3W',1),(343,'24111218','MAGNETO ASSLY.','2346.00',1,'A','3W',1),(344,'24111219','ASSLY ROTOR 1 PHASE ','1473.00',1,'A','3W',1),(345,'24116148','WASHER -IGLIDUR','34.00',1,'A','3W',1),(346,'24116149','PLUG SPARK (RL82C)','81.00',1,'A','3W',1),(347,'24121037','NEEDLE','26.00',1,'A','3W',1),(348,'24121049','BELLOW UCAL CARBU','28.00',1,'A','3W',1),(349,'24121060','CAP ASSY TOP','92.00',1,'A','3W',1),(350,'24121062','RING  O','4.70',5,'A','3W',1),(351,'24121064','SPRING','10.20',5,'A','3W',1),(352,'24121065','SCREW AIR','16.00',1,'A','3W',1),(353,'24121066','VALVE  PISTON','159.00',1,'A','3W',1),(354,'24121067','RING  O','5.20',5,'A','3W',1),(355,'24121069','PIN FLOAT','9.50',1,'A','3W',1),(356,'24121070','SEAT  VALVE VS','137.00',1,'A','3W',1),(357,'24121072','JET PILOT','36.00',1,'A','3W',1),(358,'24121073','GASKET','40.00',1,'A','3W',1),(359,'24121074','JET NEEDLE','117.00',1,'A','3W',1),(360,'24121075','NEEDLE JET','195.00',1,'A','3W',1),(361,'24121076','PACKING','12.50',1,'A','3W',1),(362,'24121077','JET MAIN','19.00',1,'A','3W',1),(363,'24121079','FLOAT ASSY','71.00',1,'A','3W',1),(364,'24121080','SCREW IDLING','15.50',1,'A','3W',1),(365,'24121117','DUCT  AIR INNTAKE','218.00',1,'A','3W',1),(366,'24121118','CARBURETTOR 3WH2SRE ','1349.00',1,'A','3W',1),(367,'24121127','NEEDLE JET','131.00',1,'A','3W',1),(368,'24121128','JET NEEDLE','101.00',1,'A','3W',1),(369,'24121145','ELEMENT AIR FILTER','167.00',1,'A','3W',1),(370,'24121166','HPR30+FILTER RE 2S C','1690.00',1,'A','3W',1),(371,'24121207','MANIFOLD ASSLY CNG','266.00',1,'A','3W',1),(372,'24121232','CARBURETTOR COMP FL','1546.00',1,'A','3W',1),(373,'24121235','FLEXIBLE HOSE ASSLY.','628.50',1,'A','3W',1),(374,'24121244','WASHER FOR FLEX HOSE','3.80',5,'A','3W',1),(375,'24121245','INSERT BELLOW','791.00',1,'A','3W',1),(376,'24121249','CASE UPP SEAL BOX VA','216.00',1,'A','3W',1),(377,'24121250','RING O TOP FOR SEAL','22.50',1,'A','3W',1),(378,'24121266','RETAINER MFVM/S. VA','49.00',1,'A','3W',1),(379,'24121267','KNOB MFV M/S.VANAZ','24.00',1,'A','3W',1),(380,'24121268','FILTER MFV VANAZ LPG','9.00',1,'A','3W',1),(381,'24121283','WASHER SEALING MFV V','5.60',5,'A','3W',1),(382,'24121290','SPRING CONICAL MFV','2.20',5,'A','3W',1),(383,'24121298','LEVER VANAZ LPG','31.00',1,'A','3W',1),(384,'24121299','PIN LEVER VANAZ LPG','11.50',1,'A','3W',1),(385,'24121303','GUIDE SPRING VANAZ','7.60',10,'A','3W',1),(386,'24121304','SPRING M/S LPG KIT','6.00',5,'A','3W',1),(387,'24121306','WASHER RUBBER','12.50',1,'A','3W',1),(388,'24121312','LEVER SUB ASSY 1ST S','34.00',1,'A','3W',1),(389,'24121313','SEAT 1ST STAGE VANA','39.00',1,'A','3W',1),(390,'24121314','RUBBER WASHER 1ST SA','13.00',1,'A','3W',1),(391,'24121315','WASHER COPPER LPG KI','6.50',1,'A','3W',1),(392,'24121316','CONNECTOR INLET  VAN','69.00',1,'A','3W',1),(393,'24121317','SPRING VACUUM - M/S.','8.40',5,'A','3W',1),(394,'24121318','DIAPHRAGM ASSY.VACU','241.00',1,'A','3W',1),(395,'24121319','PLUG LPG','28.00',1,'A','3W',1),(396,'24121321','RING O FL CON','13.00',1,'A','3W',1),(397,'24121327','PLUG PR CHECK','29.00',1,'A','3W',1),(398,'24121335','PUMP OIL RE2S CNG','537.00',1,'A','3W',1),(399,'24121337','CONNECTOR FILLER VA','207.00',1,'A','3W',1),(400,'24121342','DUCT INTEGRAL','364.00',1,'A','3W',1),(401,'24121354','CLIP LOW PR CNG HOS','28.00',1,'A','3W',1),(402,'24121356','MIXER TUBE (NYLON)','7.00',1,'A','3W',1),(403,'24121361','SEALCARBURETTOR','19.50',1,'A','3W',1),(404,'24121363','CAP CARBURATOR','24.00',1,'A','3W',1),(405,'24121365','FLOAT ASSEMBLY','271.00',1,'A','3W',1),(406,'24121368','NEEDLE JET','114.00',1,'A','3W',1),(407,'24121370','RING','17.50',1,'A','3W',1),(408,'24121371','JET NEEDLE','156.00',1,'A','3W',1),(409,'24121385','INTEGRAL DUCT ASSY','241.00',1,'A','3W',1),(410,'24121393','KNOB','25.00',1,'A','3W',1),(411,'24121394','CAP','44.00',1,'A','3W',1),(412,'24121398','RING O LPG FILTE','9.00',1,'A','3W',1),(413,'24121400','FILTER ELEMENT LPG','65.00',1,'A','3W',1),(414,'24121407','BRACKET FILLING VALV','170.00',1,'A','3W',1),(415,'24121413','ASSEMBLY 1ST STAGE R','3220.00',1,'A','3W',1),(416,'24121418','SEAL BOX ZERO DEG','506.00',1,'A','3W',1),(417,'24121427','REGULATOR LPG 2 STAG','3394.00',1,'A','3W',1),(418,'24121432','FILLER CONNECTOR WIT','954.00',1,'A','3W',1),(419,'24121434','HOSE MFV TO LPR','392.00',1,'A','3W',1),(420,'24121435','ADJUSTER WITH NUT','20.80',5,'A','3W',1),(421,'24121437','PUMP OIL ASSY','551.00',1,'A','3W',1),(422,'24121444','SCREW AIR','14.00',1,'A','3W',1),(423,'24121449','IDLING ADJUSTER KIT','24.00',1,'A','3W',1),(424,'24121456','CONNECTOR SS FOR CNG','118.00',1,'A','3W',1),(425,'24121457','CARBURETOR ASSEMBLY','1530.00',1,'A','3W',1),(426,'24121458','ASSEMBLY SAI','316.00',1,'A','3W',1),(427,'24121460','TUBE SAI INLET','57.00',1,'A','3W',1),(428,'24121461','TUBE SAI OUTLET','51.00',1,'A','3W',1),(429,'24121462','SILENCER FOR SAI','41.00',1,'A','3W',1),(430,'24121464','ASSEY COVER AIR FILT','53.00',1,'A','3W',1),(431,'24121465','FILTER AIR ASSY','676.00',1,'A','3W',1),(432,'24121466','PUMP OIL ASSY.','645.00',1,'A','3W',1),(433,'24121467','TUBE OIL ? INLET OIL','28.00',1,'A','3W',1),(434,'24121468','COMP INTEG','360.00',1,'A','3W',1),(435,'24121470','CARBURETTOR ASSY. 2S','1508.00',1,'A','3W',1),(436,'24121471','CARBURETTOR ASSY. 2S','1532.00',1,'A','3W',1),(437,'24121472','INTEGRAL DUCT','289.00',1,'A','3W',1),(438,'24121473','COMP. INTEGRAL DUCT','341.00',1,'A','3W',1),(439,'24121474','INSERT FOR BELLOW','56.00',1,'A','3W',1),(440,'24121476','SPRING BAND(DIA16.8)','12.00',1,'A','3W',1),(441,'24121477','CLAMP HOSE','3.90',5,'A','3W',1),(442,'24121484','FLOAT BODY ASSY. KIT','170.00',1,'A','3W',1),(443,'24121485','SCREW AIR  KIT','41.00',1,'A','3W',1),(444,'24121486','JET KIT','176.00',1,'A','3W',1),(445,'24121487','PISTON VALUE ASSLY K','305.00',1,'A','3W',1),(446,'24121488','MIXING CAP ASSLY. KI','158.00',1,'A','3W',1),(447,'24121490','JET MAIN (65) (MJ)','22.00',1,'A','3W',1),(448,'24121491','JET KIT','176.00',1,'A','3W',1),(449,'24121494','JET KIT','176.00',1,'A','3W',1),(450,'24121498','HOSE SOLENOID TO LPR','644.00',1,'A','3W',1),(451,'24121500','HOSE HPR TO SOLENOID','371.00',1,'A','3W',1),(452,'24121506','SCREW FLOW ADJUSTING','52.00',1,'A','3W',1),(453,'24121507','BODY -FLOW CONTROL','162.00',1,'A','3W',1),(454,'24121642','FILTER AIR SAI TYPE','542.00',1,'A','3W',1),(455,'24121645','DUCT INLET AIR FILTE','37.00',1,'A','3W',1),(456,'24121646','HOOK FOR SAI TUBE','4.50',5,'A','3W',1),(457,'24121648','BREATHER RESTRICTOR','13.20',5,'A','3W',1),(458,'24121649','HOSE  BREATHER','47.00',1,'A','3W',1),(459,'24121650','MANIFOLD','283.00',1,'A','3W',1),(460,'24121652','FILTER FUEL','20.50',1,'A','3W',1),(461,'24121655','KIT LPG V RE2S 3W UG','11466.00',1,'A','3W',1),(462,'24121656','PETR SOLENOID','688.00',1,'A','3W',1),(463,'24121659','FILTER AIR SAI TYPE','672.00',1,'A','3W',1),(464,'24121664','ASSLY COMP.INTEGRAL ','308.00',1,'A','3W',1),(465,'24121669','TUBE OIL CYL.BLOCK','12.50',1,'A','3W',1),(466,'24121670','TUBE OIL MANIFOLD','11.60',5,'A','3W',1),(467,'24121674','HOSE OIL OUT','28.00',1,'A','3W',1),(468,'24121676','CARBURETOR ASSY','1668.00',1,'A','3W',1),(469,'24121677','ASSLY CAP FL','15.80',5,'A','3W',1),(470,'24121682','ASSLY FUEL TANK WELD','841.00',1,'A','3W',1),(471,'24121695','ASSLY FUEL COCK FL','122.00',1,'A','3W',1),(472,'24121698','SEAL FUEL TAP FL','5.40',5,'A','3W',1),(473,'24121703','ASSLY BRACKET SAI. 1','49.00',1,'A','3W',1),(474,'24121704','TUBE SAI OUTLET 145F','49.00',1,'A','3W',1),(475,'24121709','SLEEVE CARBURETTOR F','38.00',1,'A','3W',1),(476,'24121716','TUBE S.A.I. INLET','36.00',1,'A','3W',1),(477,'24121721','BELLOW-ACC.CABLE','17.50',1,'A','3W',1),(478,'24121722','CLIP SPRING BAND','8.60',5,'A','3W',1),(479,'24121728','CLIP','12.50',1,'A','3W',1),(480,'24130105','BEARING  BALL','146.00',1,'A','3W',1),(481,'24130106','SHAFT SPLINED','313.00',1,'A','3W',1),(482,'24130111','BUSH HSG BEVEL GEAR','33.00',1,'A','3W',1),(483,'24130113','PIN','0.86',25,'A','3W',1),(484,'24130118','GEAR IDLER','294.00',1,'A','3W',1),(485,'24130129','SPRING TENSION','9.40',5,'A','3W',1),(486,'24130209','GEAR FARE METER','62.00',1,'A','3W',1),(487,'24130214','BUSH','99.00',1,'A','3W',1),(488,'24131002','PINION FARE METER','46.00',1,'A','3W',1),(489,'24131003','WIRE','0.75',30,'A','3W',1),(490,'24131004','SEAL OIL','23.00',1,'A','3W',1),(491,'24131007','BUSH','8.60',5,'A','3W',1),(492,'24131008','PLUG','45.00',1,'A','3W',1),(493,'24131009','GEAR BEVEL','218.00',1,'A','3W',1),(494,'24131016','GEAR REVERSE CON.','387.00',1,'A','3W',1),(495,'24131017','HSG SATELLITE GEAR','337.00',1,'A','3W',1),(496,'24131032','PIN GEAR BEVEL','35.00',1,'A','3W',1),(497,'24131046','LEVER AND SECTOR COM','71.00',1,'A','3W',1),(498,'24131055','RUBBER BUSH PROPELLE','22.50',1,'A','3W',1),(499,'24131069','BEVEL GEAR SAT GEAR ','309.00',1,'A','3W',1),(500,'24131070','BEVEL GEAR DIFF GEAR','336.00',1,'A','3W',1),(501,'24131072','SHAFT ASSY PROPELLER','344.00',1,'A','3W',1),(502,'24131074','BELLOW  PROPELLER SH','122.00',1,'A','3W',1),(503,'24131075','SEAL   OIL','40.00',1,'A','3W',1),(504,'24131078','COVER DIFFERENTIAL','552.00',1,'A','3W',1),(505,'24131079','DIP STICK FOR DIFFER','34.00',1,'A','3W',1),(506,'24131081','NIPPLE GREASE UJ KIT','15.00',1,'A','3W',1),(507,'24131088','COMP. REV. LEVER <(>','132.00',1,'A','3W',1),(508,'24131092','BKT. RESERSE CABLE','37.00',1,'A','3W',1),(509,'24131093','GEAR DIFFERENTIAL AS','2040.00',1,'A','3W',1),(510,'24131098','NIPPLE GREASE','7.50',1,'A','3W',1),(511,'24131101','BOLT FLANGE M7X1 80L','6.80',5,'A','3W',1),(512,'24131104','SHAFT PROPELLER ASSY','4464.00',1,'A','3W',1),(513,'24131105','YOKE SHAFT','926.00',1,'A','3W',1),(514,'24131106','YOKE END SUB ASSY.','702.00',1,'A','3W',1),(515,'24131107','SLEEVE YOKE SUB ASSY','632.00',1,'A','3W',1),(516,'24131110','SHAFT UJ ASSY WITH B','4153.00',1,'A','3W',1),(517,'24131116','BRACKET REVERSE CABL','38.00',1,'A','3W',1),(518,'24140102','TANK FUEL RE 2S','821.00',1,'A','3W',1),(519,'24140110','NUT ADAPTOR','40.00',1,'A','3W',1),(520,'24140112','CAP ASSY','10.50',1,'A','3W',1),(521,'24140115','RING  O','3.70',5,'A','3W',1),(522,'24141066','PIPE FUEL','28.00',1,'A','3W',1),(523,'24141070','COCK FUEL','102.00',1,'A','3W',1),(524,'24141072','TAP COCKASYFUEL','151.00',1,'A','3W',1),(525,'24141090','TANK FUEL RE 2S','641.00',1,'A','3W',1),(526,'24141091','CLIP SPRING','1.80',10,'A','3W',1),(527,'24141094','TANK FUEL 3 LITRE','348.00',1,'A','3W',1),(528,'24141099','TUBE FUEL COCK TO CA','20.00',1,'A','3W',1),(529,'24141109','FILTER  FUEL','21.00',1,'A','3W',1),(530,'24141115','TUBE BREATHER','24.50',1,'A','3W',1),(531,'24141120','FILTER ASSY 2T OIL R','20.00',1,'A','3W',1),(532,'24141121','TUBE OILTNK TO FLTR','22.50',1,'A','3W',1),(533,'24141122','TUBE BERATHER OIL FI','34.00',1,'A','3W',1),(534,'24141124','TUBE OIL TANK TO FIL','12.50',1,'A','3W',1),(535,'24141125','TUBE FUEL FILT TO SO','9.50',1,'A','3W',1),(536,'24141126','TUBE FUEL SOL TO CAR','24.00',1,'A','3W',1),(537,'24141130','TAP ASSEMBLY','104.00',1,'A','3W',1),(538,'24141132','PULLEY TAP SIDE','18.50',1,'A','3W',1),(539,'24141133','PULLEY KNOB SIDE','18.50',1,'A','3W',1),(540,'24141134','INSERT KNOB MOUNTING','20.00',1,'A','3W',1),(541,'24141135','SPACER FOR KNOB MOUN','10.00',1,'A','3W',1),(542,'24141136','BRACKET FUEL KNOB MT','61.00',1,'A','3W',1),(543,'24141137','KNOB FUEL TAP OPERAT','38.00',1,'A','3W',1),(544,'24141138','PIPE TANK FUEL TO CO','24.00',1,'A','3W',1),(545,'24141139','PIPE TANK FUEL TO CO','26.00',1,'A','3W',1),(546,'24141140','TUBE FUEL COCK FILTE','4.30',5,'A','3W',1),(547,'24141141','TUBE FUEL  FILTER TO','16.00',1,'A','3W',1),(548,'24141144','TUBE OIL TANK TO FIL','10.00',1,'A','3W',1),(549,'24141148','FUEL COCK WITH CABL','593.00',1,'A','3W',1),(550,'24141149','TANK ASSEMBLY COMP','761.00',1,'A','3W',1),(551,'24141152','ASSY PIPE FUEL WITH ','47.00',1,'A','3W',1),(552,'24141164','KNOB FUEL TAP OPERAT','45.00',1,'A','3W',1),(553,'24141165','ASSLY FUEL TAP','521.00',1,'A','3W',1),(554,'24141166','BRACKET FUEL KNOB MO','61.00',1,'A','3W',1),(555,'24141183','PLUG SEAT FUEL COCK ','2.05',10,'A','3W',1),(556,'24141184','ASSEMBLY FUEL COCK F','117.00',1,'A','3W',1),(557,'24150501','CABLE HAND BRAKE 4S ','213.00',1,'A','3W',1),(558,'24150506','SPRING  RETURN RH','13.50',1,'A','3W',1),(559,'24150507','SPRING  RETURN  LH','13.50',1,'A','3W',1),(560,'24151027','CYLINDER  WHEEL','178.00',1,'A','3W',1),(561,'24151045','CYLINDER  WHEEL','178.00',1,'A','3W',1),(562,'24151058','CABLE ASYHAND BRAKE','152.00',1,'A','3W',1),(563,'24151059','CABLE ASYREARLH','116.00',1,'A','3W',1),(564,'24151060','CABLE RE RH HAND BR','110.00',1,'A','3W',1),(565,'24151061','LEVER ASSY HAND BRAK','126.00',1,'A','3W',1),(566,'24151067','BRACKET RR CABLE','15.00',1,'A','3W',1),(567,'24151068','PIN REAR CABLE GUI','13.60',5,'A','3W',1),(568,'24151069','SPACER','3.60',5,'A','3W',1),(569,'24151071','SHOE BRAKE REAR RE 2','158.00',1,'A','3W',1),(570,'24151079','RING LOCK BOOT','2.00',5,'A','3W',1);
/*!40000 ALTER TABLE `rr_part_pricing` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-10-02 15:33:48
