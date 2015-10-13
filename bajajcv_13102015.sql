-- MySQL dump 10.13  Distrib 5.5.44, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: bajajcv
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
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
INSERT INTO `auth_group` VALUES (1,'Admins'),(2,'AreaSalesManagers'),(3,'AreaServiceManagers'),(4,'AreaSparesManagers'),(5,'AuthorisedServiceCenters'),(6,'BrandManagers'),(7,'CircleHeads'),(8,'CountryDistributors'),(9,'CTSAdmins'),(10,'CxoAdmins'),(12,'DealerAdmins'),(13,'Dealers'),(11,'DependentAuthorisedServiceCenters'),(15,'DisitrbutorSalesReps'),(14,'Distributors'),(16,'DistributorStaffs'),(29,'EscalationAuthority'),(17,'FscAdmins'),(18,'FscSuperAdmins'),(21,'LogisticPartners'),(19,'LoyaltyAdmins'),(20,'LoyaltySuperAdmins'),(22,'MainCountryDealers'),(23,'NationalSparesManagers'),(24,'ReadOnly'),(25,'RedemptionEscalation'),(27,'RedemptionPartners'),(26,'RegionalManagers'),(28,'SdAdmins'),(30,'SdManagers'),(31,'SdOwners'),(32,'SdReadOnly'),(33,'SdSuperAdmins'),(34,'ServiceAdvisors'),(35,'SuperAdmins'),(36,'Supervisors'),(37,'Transporters'),(38,'Users'),(39,'VisualizationAdmins'),(40,'VisualizationStaffs'),(41,'VisualizationUsers'),(42,'WelcomeKitEscalation'),(43,'ZonalServiceManagers');
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
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
INSERT INTO `auth_group_permissions` VALUES (130,2,7),(131,2,8),(136,2,82),(137,2,83),(140,2,247),(141,2,248),(128,2,257),(132,2,275),(138,2,277),(139,2,278),(135,2,280),(142,2,281),(143,2,283),(144,2,284),(145,2,286),(146,2,287),(133,2,2251),(134,2,2252),(129,2,2852),(151,14,7),(152,14,8),(156,14,82),(157,14,83),(158,14,253),(159,14,254),(147,14,256),(148,14,257),(149,14,259),(150,14,260),(153,14,275),(160,14,287),(154,14,2251),(155,14,2252);
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
) ENGINE=InnoDB AUTO_INCREMENT=3406 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add client',8,'add_client'),(23,'Can change client',8,'change_client'),(24,'Can delete client',8,'delete_client'),(25,'Can add grant',9,'add_grant'),(26,'Can change grant',9,'change_grant'),(27,'Can delete grant',9,'delete_grant'),(28,'Can add access token',10,'add_accesstoken'),(29,'Can change access token',10,'change_accesstoken'),(30,'Can delete access token',10,'delete_accesstoken'),(31,'Can add refresh token',11,'add_refreshtoken'),(32,'Can change refresh token',11,'change_refreshtoken'),(33,'Can delete refresh token',11,'delete_refreshtoken'),(79,'Can add brand product category',27,'add_brandproductcategory'),(80,'Can change brand product category',27,'change_brandproductcategory'),(81,'Can delete brand product category',27,'delete_brandproductcategory'),(82,'Can add user profile',28,'add_userprofile'),(83,'Can change user profile',28,'change_userprofile'),(84,'Can delete user profile',28,'delete_userprofile'),(85,'Can add zonal service manager',29,'add_zonalservicemanager'),(86,'Can change zonal service manager',29,'change_zonalservicemanager'),(87,'Can delete zonal service manager',29,'delete_zonalservicemanager'),(88,'Can add area service manager',30,'add_areaservicemanager'),(89,'Can change area service manager',30,'change_areaservicemanager'),(90,'Can delete area service manager',30,'delete_areaservicemanager'),(91,'Can add circle head',31,'add_circlehead'),(92,'Can change circle head',31,'change_circlehead'),(93,'Can delete circle head',31,'delete_circlehead'),(94,'Can add regional manager',32,'add_regionalmanager'),(95,'Can change regional manager',32,'change_regionalmanager'),(96,'Can delete regional manager',32,'delete_regionalmanager'),(97,'Can add territory',33,'add_territory'),(98,'Can change territory',33,'change_territory'),(99,'Can delete territory',33,'delete_territory'),(100,'Can add state',34,'add_state'),(101,'Can change state',34,'change_state'),(102,'Can delete state',34,'delete_state'),(103,'Can add area sales manager',35,'add_areasalesmanager'),(104,'Can change area sales manager',35,'change_areasalesmanager'),(105,'Can delete area sales manager',35,'delete_areasalesmanager'),(106,'Can add dealer',36,'add_dealer'),(107,'Can change dealer',36,'change_dealer'),(108,'Can delete dealer',36,'delete_dealer'),(109,'Can add authorized service center',37,'add_authorizedservicecenter'),(110,'Can change authorized service center',37,'change_authorizedservicecenter'),(111,'Can delete authorized service center',37,'delete_authorizedservicecenter'),(112,'Can add service advisor',38,'add_serviceadvisor'),(113,'Can change service advisor',38,'change_serviceadvisor'),(114,'Can delete service advisor',38,'delete_serviceadvisor'),(115,'Can add brand department',39,'add_branddepartment'),(116,'Can change brand department',39,'change_branddepartment'),(117,'Can delete brand department',39,'delete_branddepartment'),(118,'Can add department sub categories',40,'add_departmentsubcategories'),(119,'Can change department sub categories',40,'change_departmentsubcategories'),(120,'Can delete department sub categories',40,'delete_departmentsubcategories'),(121,'Can add service desk user',41,'add_servicedeskuser'),(122,'Can change service desk user',41,'change_servicedeskuser'),(123,'Can delete service desk user',41,'delete_servicedeskuser'),(124,'Can add feedback',42,'add_feedback'),(125,'Can change feedback',42,'change_feedback'),(126,'Can delete feedback',42,'delete_feedback'),(127,'Can add activity',43,'add_activity'),(128,'Can change activity',43,'change_activity'),(129,'Can delete activity',43,'delete_activity'),(130,'Can add comment',44,'add_comment'),(131,'Can change comment',44,'change_comment'),(132,'Can delete comment',44,'delete_comment'),(133,'Can add feedback event',45,'add_feedbackevent'),(134,'Can change feedback event',45,'change_feedbackevent'),(135,'Can delete feedback event',45,'delete_feedbackevent'),(136,'Can add product type',46,'add_producttype'),(137,'Can change product type',46,'change_producttype'),(138,'Can delete product type',46,'delete_producttype'),(139,'Can add product data',47,'add_productdata'),(140,'Can change product data',47,'change_productdata'),(141,'Can delete product data',47,'delete_productdata'),(142,'Can add coupon data',48,'add_coupondata'),(143,'Can change coupon data',48,'change_coupondata'),(144,'Can delete coupon data',48,'delete_coupondata'),(145,'Can add service advisor coupon relationship',49,'add_serviceadvisorcouponrelationship'),(146,'Can change service advisor coupon relationship',49,'change_serviceadvisorcouponrelationship'),(147,'Can delete service advisor coupon relationship',49,'delete_serviceadvisorcouponrelationship'),(148,'Can add ucn recovery',50,'add_ucnrecovery'),(149,'Can change ucn recovery',50,'change_ucnrecovery'),(150,'Can delete ucn recovery',50,'delete_ucnrecovery'),(151,'Can add old fsc data',51,'add_oldfscdata'),(152,'Can change old fsc data',51,'change_oldfscdata'),(153,'Can delete old fsc data',51,'delete_oldfscdata'),(154,'Can add cdms data',52,'add_cdmsdata'),(155,'Can change cdms data',52,'change_cdmsdata'),(156,'Can delete cdms data',52,'delete_cdmsdata'),(157,'Can add otp token',53,'add_otptoken'),(158,'Can change otp token',53,'change_otptoken'),(159,'Can delete otp token',53,'delete_otptoken'),(160,'Can add message template',54,'add_messagetemplate'),(161,'Can change message template',54,'change_messagetemplate'),(162,'Can delete message template',54,'delete_messagetemplate'),(163,'Can add email template',55,'add_emailtemplate'),(164,'Can change email template',55,'change_emailtemplate'),(165,'Can delete email template',55,'delete_emailtemplate'),(166,'Can add asc temp registration',56,'add_asctempregistration'),(167,'Can change asc temp registration',56,'change_asctempregistration'),(168,'Can delete asc temp registration',56,'delete_asctempregistration'),(169,'Can add sa temp registration',57,'add_satempregistration'),(170,'Can change sa temp registration',57,'change_satempregistration'),(171,'Can delete sa temp registration',57,'delete_satempregistration'),(172,'Can add customer temp registration',58,'add_customertempregistration'),(173,'Can change customer temp registration',58,'change_customertempregistration'),(174,'Can delete customer temp registration',58,'delete_customertempregistration'),(175,'Can add customer update failure',59,'add_customerupdatefailure'),(176,'Can change customer update failure',59,'change_customerupdatefailure'),(177,'Can delete customer update failure',59,'delete_customerupdatefailure'),(178,'Can add customer update history',60,'add_customerupdatehistory'),(179,'Can change customer update history',60,'change_customerupdatehistory'),(180,'Can delete customer update history',60,'delete_customerupdatehistory'),(181,'Can add user preference',61,'add_userpreference'),(182,'Can change user preference',61,'change_userpreference'),(183,'Can delete user preference',61,'delete_userpreference'),(184,'Can add sms log',62,'add_smslog'),(185,'Can change sms log',62,'change_smslog'),(186,'Can delete sms log',62,'delete_smslog'),(187,'Can add email log',63,'add_emaillog'),(188,'Can change email log',63,'change_emaillog'),(189,'Can delete email log',63,'delete_emaillog'),(190,'Can add data feed log',64,'add_datafeedlog'),(191,'Can change data feed log',64,'change_datafeedlog'),(192,'Can delete data feed log',64,'delete_datafeedlog'),(193,'Can add feed failure log',65,'add_feedfailurelog'),(194,'Can change feed failure log',65,'change_feedfailurelog'),(195,'Can delete feed failure log',65,'delete_feedfailurelog'),(196,'Can add vin sync feed log',66,'add_vinsyncfeedlog'),(197,'Can change vin sync feed log',66,'change_vinsyncfeedlog'),(198,'Can delete vin sync feed log',66,'delete_vinsyncfeedlog'),(199,'Can add audit log',67,'add_auditlog'),(200,'Can change audit log',67,'change_auditlog'),(201,'Can delete audit log',67,'delete_auditlog'),(202,'Can add sla',68,'add_sla'),(203,'Can change sla',68,'change_sla'),(204,'Can delete sla',68,'delete_sla'),(205,'Can add service type',69,'add_servicetype'),(206,'Can change service type',69,'change_servicetype'),(207,'Can delete service type',69,'delete_servicetype'),(208,'Can add service',70,'add_service'),(209,'Can change service',70,'change_service'),(210,'Can delete service',70,'delete_service'),(211,'Can add constant',71,'add_constant'),(212,'Can change constant',71,'change_constant'),(213,'Can delete constant',71,'delete_constant'),(214,'Can add date dimension',72,'add_datedimension'),(215,'Can change date dimension',72,'change_datedimension'),(216,'Can delete date dimension',72,'delete_datedimension'),(217,'Can add coupon fact',73,'add_couponfact'),(218,'Can change coupon fact',73,'change_couponfact'),(219,'Can delete coupon fact',73,'delete_couponfact'),(220,'Can add transporter',74,'add_transporter'),(221,'Can change transporter',74,'change_transporter'),(222,'Can delete transporter',74,'delete_transporter'),(223,'Can add supervisor',75,'add_supervisor'),(224,'Can\n change supervisor',75,'change_supervisor'),(225,'Can delete supervisor',75,'delete_supervisor'),(226,'Can add container indent',76,'add_containerindent'),(227,'Can change container indent',76,'change_containerindent'),(228,'Can delete container indent',76,'delete_containerindent'),(229,'Can add container lr',77,'add_containerlr'),(230,'Can change container lr',77,'change_containerlr'),(231,'Can delete container lr',77,'delete_containerlr'),(232,'Can add container tracker',78,'add_containertracker'),(233,'Can change container tracker',78,'change_containertracker'),(234,'Can delete container tracker',78,'delete_containertracker'),(235,'Can add city',79,'add_city'),(236,'Can change city',79,'change_city'),(237,'Can delete city',79,'delete_city'),(238,'Can add national spares manager',80,'add_nationalsparesmanager'),(239,'Can change national spares manager',80,'change_nationalsparesmanager'),(240,'Can delete national spares manager',80,'delete_nationalsparesmanager'),(241,'Can add national sales manager',81,'add_nationalsalesmanager'),(242,'Can change national sales manager',81,'change_nationalsalesmanager'),(243,'Can delete national sales manager',81,'delete_nationalsalesmanager'),(244,'Can add area spares manager',82,'add_areasparesmanager'),(245,'Can change area spares manager',82,'change_areasparesmanager'),(246,'Can delete area spares manager',82,'delete_areasparesmanager'),(247,'Can add distributor',83,'add_distributor'),(248,'Can change distributor',83,'change_distributor'),(249,'Can delete distributor',83,'delete_distributor'),(250,'Can add distributor staff',84,'add_distributorstaff'),(251,'Can change distributor staff',84,'change_distributorstaff'),(252,'Can delete distributor staff',84,'delete_distributorstaff'),(253,'Can add distributor sales rep',85,'add_distributorsalesrep'),(254,'Can change distributor sales rep',85,'change_distributorsalesrep'),(255,'Can delete distributor sales rep',85,'delete_distributorsalesrep'),(256,'Can add retailer',86,'add_retailer'),(257,'Can change retailer',86,'change_retailer'),(258,'Can delete retailer',86,'delete_retailer'),(259,'Can add dsr work allocation',87,'add_dsrworkallocation'),(260,'Can change dsr work allocation',87,'change_dsrworkallocation'),(261,'Can delete dsr work allocation',87,'delete_dsrworkallocation'),(262,'Can add part models',88,'add_partmodels'),(263,'Can change part models',88,'change_partmodels'),(264,'Can delete part models',88,'delete_partmodels'),(265,'Can add categories',89,'add_categories'),(266,'Can change categories',89,'change_categories'),(267,'Can delete categories',89,'delete_categories'),(268,'Can add sub categories',90,'add_subcategories'),(269,'Can change sub categories',90,'change_subcategories'),(270,'Can delete sub categories',90,'delete_subcategories'),(271,'Can add part pricing',91,'add_partpricing'),(272,'Can change part pricing',91,'change_partpricing'),(273,'Can delete part pricing',91,'delete_partpricing'),(274,'Can add order part',92,'add_orderpart'),(275,'Can change order part',92,'change_orderpart'),(276,'Can delete order part',92,'delete_orderpart'),(277,'Can add alternate parts',93,'add_alternateparts'),(278,'Can change alternate parts',93,'change_alternateparts'),(279,'Can delete alternate parts',93,'delete_alternateparts'),(280,'Can add cv categories',94,'add_cvcategories'),(281,'Can change cv categories',94,'change_cvcategories'),(282,'Can delete cv categories',94,'delete_cvcategories'),(283,'Can add kit',95,'add_kit'),(284,'Can change kit',95,'change_kit'),(285,'Can delete kit',95,'delete_kit'),(286,'Can add part master cv',96,'add_partmastercv'),(287,'Can change part master cv',96,'change_partmastercv'),(288,'Can delete part master cv',96,'delete_partmastercv'),(289,'Can add member',97,'add_member'),(290,'Can change member',97,'change_member'),(291,'Can delete member',97,'delete_member'),(292,'Can add spare part master data',98,'add_sparepartmasterdata'),(293,'Can change spare part master data',98,'change_sparepartmasterdata'),(294,'Can delete spare part master data',98,'delete_sparepartmasterdata'),(295,'Can add spare part upc',99,'add_sparepartupc'),(296,'Can change spare part upc',99,'change_sparepartupc'),(297,'Can delete spare part upc',99,'delete_sparepartupc'),(298,'Can add spare part point',100,'add_sparepartpoint'),(299,'Can change spare part point',100,'change_sparepartpoint'),(300,'Can delete spare part point',100,'delete_sparepartpoint'),(301,'Can add accumulation request',101,'add_accumulationrequest'),(302,'Can change accumulation request',101,'change_accumulationrequest'),(303,'Can delete accumulation request',101,'delete_accumulationrequest'),(304,'Can add partner',102,'add_partner'),(305,'Can change partner',102,'change_partner'),(306,'Can delete partner',102,'delete_partner'),(307,'Can add product catalog',103,'add_productcatalog'),(308,'Can change product catalog',103,'change_productcatalog'),(309,'Can delete product catalog',103,'delete_productcatalog'),(310,'Can add redemption request',104,'add_redemptionrequest'),(311,'Can change redemption request',104,'change_redemptionrequest'),(312,'Can delete redemption request',104,'delete_redemptionrequest'),(313,'Can add welcome kit',105,'add_welcomekit'),(314,'Can change welcome kit',105,'change_welcomekit'),(315,'Can delete welcome kit',105,'delete_welcomekit'),(316,'Can add comment thread',106,'add_commentthread'),(317,'Can change comment thread',106,'change_commentthread'),(318,'Can delete comment thread',106,'delete_commentthread'),(319,'Can add loyalty sla',107,'add_loyaltysla'),(320,'Can change loyalty sla',107,'change_loyaltysla'),(321,'Can delete loyalty sla',107,'delete_loyaltysla'),(322,'Can add discrepant accumulation',108,'add_discrepantaccumulation'),(323,'Can change discrepant accumulation',108,'change_discrepantaccumulation'),(324,'Can delete discrepant accumulation',108,'delete_discrepantaccumulation'),(325,'Can add eco release',109,'add_ecorelease'),(326,'Can change eco release',109,'change_ecorelease'),(327,'Can delete eco release',109,'delete_ecorelease'),(328,'Can add eco implementation',110,'add_ecoimplementation'),(329,'Can change eco implementation',110,'change_ecoimplementation'),(330,'Can delete eco implementation',110,'delete_ecoimplementation'),(331,'Can add brand vertical',111,'add_brandvertical'),(332,'Can change brand vertical',111,'change_brandvertical'),(333,'Can delete brand vertical',111,'delete_brandvertical'),(334,'Can add brand product range',112,'add_brandproductrange'),(335,'Can change brand product range',112,'change_brandproductrange'),(336,'Can delete brand product range',112,'delete_brandproductrange'),(337,'Can add bom header',113,'add_bomheader'),(338,'Can change bom header',113,'change_bomheader'),(339,'Can delete bom header',113,'delete_bomheader'),(340,'Can add bom plate',114,'add_bomplate'),(341,'Can change bom plate',114,'change_bomplate'),(342,'Can delete bom plate',114,'delete_bomplate'),(343,'Can add bom part',115,'add_bompart'),(344,'Can change bom part',115,'change_bompart'),(345,'Can delete bom part',115,'delete_bompart'),(346,'Can add bom plate part',116,'add_bomplatepart'),(347,'Can change bom plate part',116,'change_bomplatepart'),(348,'Can delete bom plate part',116,'delete_bomplatepart'),(349,'Can add bom visualization',117,'add_bomvisualization'),(350,'Can change bom visualization',117,'change_bomvisualization'),(351,'Can delete bom visualization',117,'delete_bomvisualization'),(352,'Can add service circular',118,'add_servicecircular'),(353,'Can change service circular',118,'change_servicecircular'),(354,'Can delete service circular',118,'delete_servicecircular'),(355,'Can add manufacturing data',119,'add_manufacturingdata'),(356,'Can change manufacturing data',119,'change_manufacturingdata'),(357,'Can delete manufacturing data',119,'delete_manufacturingdata'),(913,'Can add brand product category',305,'add_brandproductcategory'),(914,'Can change brand product category',305,'change_brandproductcategory'),(915,'Can delete brand product category',305,'delete_brandproductcategory'),(916,'Can add user profile',306,'add_userprofile'),(917,'Can change user profile',306,'change_userprofile'),(918,'Can delete user profile',306,'delete_userprofile'),(919,'Can add country',307,'add_country'),(920,'Can change country',307,'change_country'),(921,'Can delete country',307,'delete_country'),(922,'Can add country distributor',308,'add_countrydistributor'),(923,'Can change country distributor',308,'change_countrydistributor'),(924,'Can delete country distributor',308,'delete_countrydistributor'),(925,'Can add main country dealer',309,'add_maincountrydealer'),(926,'Can change main country dealer',309,'change_maincountrydealer'),(927,'Can delete main country dealer',309,'delete_maincountrydealer'),(928,'Can add dealer',310,'add_dealer'),(929,'Can change dealer',310,'change_dealer'),(930,'Can delete dealer',310,'delete_dealer'),(931,'Can add service advisor',311,'add_serviceadvisor'),(932,'Can change service advisor',311,'change_serviceadvisor'),(933,'Can delete service advisor',311,'delete_serviceadvisor'),(934,'Can add product type',312,'add_producttype'),(935,'Can change product type',312,'change_producttype'),(936,'Can delete product type',312,'delete_producttype'),(937,'Can add product data',313,'add_productdata'),(938,'Can change product data',313,'change_productdata'),(939,'Can delete product data',313,'delete_productdata'),(940,'Can add fleet rider',314,'add_fleetrider'),(941,'Can change fleet rider',314,'change_fleetrider'),(942,'Can delete fleet rider',314,'delete_fleetrider'),(943,'Can add coupon data',315,'add_coupondata'),(944,'Can change coupon data',315,'change_coupondata'),(945,'Can delete coupon data',315,'delete_coupondata'),(946,'Can add service advisor coupon relationship',316,'add_serviceadvisorcouponrelationship'),(947,'Can change service advisor coupon relationship',316,'change_serviceadvisorcouponrelationship'),(948,'Can\n delete service advisor coupon relationship',316,'delete_serviceadvisorcouponrelationship'),(949,'Can add ucn recovery',317,'add_ucnrecovery'),(950,'Can change ucn recovery',317,'change_ucnrecovery'),(951,'Can delete ucn recovery',317,'delete_ucnrecovery'),(952,'Can add otp token',318,'add_otptoken'),(953,'Can change otp token',318,'change_otptoken'),(954,'Can delete otp token',318,'delete_otptoken'),(955,'Can add message template',319,'add_messagetemplate'),(956,'Can change message template',319,'change_messagetemplate'),(957,'Can delete message template',319,'delete_messagetemplate'),(958,'Can add email template',320,'add_emailtemplate'),(959,'Can change email template',320,'change_emailtemplate'),(960,'Can delete email template',320,'delete_emailtemplate'),(961,'Can add sms log',321,'add_smslog'),(962,'Can change sms log',321,'change_smslog'),(963,'Can delete sms log',321,'delete_smslog'),(964,'Can add email log',322,'add_emaillog'),(965,'Can change email log',322,'change_emaillog'),(966,'Can delete email log',322,'delete_emaillog'),(967,'Can add data feed log',323,'add_datafeedlog'),(968,'Can change data feed log',323,'change_datafeedlog'),(969,'Can delete data feed log',323,'delete_datafeedlog'),(970,'Can add feed failure log',324,'add_feedfailurelog'),(971,'Can change feed failure log',324,'change_feedfailurelog'),(972,'Can delete feed failure log',324,'delete_feedfailurelog'),(973,'Can add vin sync feed log',325,'add_vinsyncfeedlog'),(974,'Can change vin sync feed log',325,'change_vinsyncfeedlog'),(975,'Can delete vin sync feed log',325,'delete_vinsyncfeedlog'),(976,'Can add constant',326,'add_constant'),(977,'Can change constant',326,'change_constant'),(978,'Can delete constant',326,'delete_constant'),(979,'Can add customer update history',327,'add_customerupdatehistory'),(980,'Can change customer update history',327,'change_customerupdatehistory'),(981,'Can delete customer update history',327,'delete_customerupdatehistory'),(982,'Can add task state',328,'add_taskmeta'),(983,'Can change task state',328,'change_taskmeta'),(984,'Can delete task state',328,'delete_taskmeta'),(985,'Can add saved group result',329,'add_tasksetmeta'),(986,'Can change saved group result',329,'change_tasksetmeta'),(987,'Can delete saved group result',329,'delete_tasksetmeta'),(988,'Can add interval',330,'add_intervalschedule'),(989,'Can change interval',330,'change_intervalschedule'),(990,'Can delete interval',330,'delete_intervalschedule'),(991,'Can add crontab',331,'add_crontabschedule'),(992,'Can change crontab',331,'change_crontabschedule'),(993,'Can delete crontab',331,'delete_crontabschedule'),(994,'Can add periodic tasks',332,'add_periodictasks'),(995,'Can change periodic tasks',332,'change_periodictasks'),(996,'Can delete periodic tasks',332,'delete_periodictasks'),(997,'Can add periodic task',333,'add_periodictask'),(998,'Can change periodic task',333,'change_periodictask'),(999,'Can delete periodic task',333,'delete_periodictask'),(1000,'Can add worker',334,'add_workerstate'),(1001,'Can change worker',334,'change_workerstate'),(1002,'Can delete worker',334,'delete_workerstate'),(1003,'Can add task',335,'add_taskstate'),(1004,'Can change task',335,'change_taskstate'),(1005,'Can delete task',335,'delete_taskstate'),(1006,'Can add TOTP device',336,'add_totpdevice'),(1007,'Can change TOTP device',336,'change_totpdevice'),(1008,'Can delete TOTP device',336,'delete_totpdevice'),(2251,'Can add dsr scorecard report',337,'add_dsrscorecardreport'),(2252,'Can change dsr scorecard report',337,'change_dsrscorecardreport'),(2253,'Can delete dsr scorecard report',337,'delete_dsrscorecardreport'),(2851,'Can add retailer collection',338,'add_retailercollection'),(2852,'Can change retailer collection',338,'change_retailercollection'),(2853,'Can delete retailer collection',338,'delete_retailercollection');
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
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$pHQIxtUZyz16$DqtvN1C2rgJLW+YNvlLqk+q/KFCknCVf+YfY5Sc0h9Y=','2015-10-12 05:22:19',1,'bajajcv','','','',1,1,'2015-10-07 08:39:22'),(2,'pbkdf2_sha256$12000$duGIey91w1zv$gfzC5cYN9es64wQ6W7CZEPqbNhX0bjVToscvIMMVjoY=','2015-10-07 08:39:22',0,'gladminds','','','',1,1,'2015-10-07 08:39:22'),(3,'pbkdf2_sha256$12000$jxYdbTJScWzr$gN59ki0exeZ0rgGa5IEatwNEs/baSrlFkC5iZws32sw=','2015-10-07 08:39:23',0,'rkjena@bajajauto.co.in','Rajib Kumar Jena','','rkjena@bajajauto.co.in',1,1,'2015-10-07 08:39:23'),(4,'pbkdf2_sha256$12000$XtThtW2ZOTiG$Ot4DVC+XaNVymyBVEz59h/ONy6iopxgh8TS+OSWhDrE=','2015-10-07 08:39:23',0,'ipattabhi@bajajauto.co.in','I Pattabhiramaswamy','','ipattabhi@bajajauto.co.in',1,1,'2015-10-07 08:39:23'),(5,'pbkdf2_sha256$12000$Erxtt43nVXeR$Lb2BaHESmyzbf7abOZq9jXKJw+lm50sf9nWmIaT/GXk=','2015-10-07 08:39:23',0,'adubey@bajajauto.co.in','Awadesh Dubey','','adubey@bajajauto.co.in',1,1,'2015-10-07 08:39:23'),(6,'pbkdf2_sha256$12000$8RSNVnX4G13q$J4LD1rrMkh3BQVicLL5XB1Hj8Z3yRy3yi7xdv2Hickw=','2015-10-07 08:39:24',0,'rkrishnan@bajajauto.co.in','NSM002','','rkrishnan@bajajauto.co.in',1,1,'2015-10-07 08:39:24'),(7,'pbkdf2_sha256$12000$zyRdpUsrUj18$jVj4rxGJpoBM777eJaQwNywJUXeD+W+ii2gh1wSMdVY=','2015-10-07 08:39:24',0,'ssaha@bajajauto.co.in','NSM003','','ssaha@bajajauto.co.in',1,1,'2015-10-07 08:39:24'),(8,'pbkdf2_sha256$12000$P2grxWpsSyBz$JYnewJRYOEDdf5BodJcV+tG/wCuqUmN3squYGPdQ4rI=','2015-10-07 08:39:25',0,'prajurkar@bajajauto.co.in','ASM004','','prajurkar@bajajauto.co.in',1,1,'2015-10-07 08:39:25'),(9,'pbkdf2_sha256$12000$xwn9km19B7oK$Xd/7qSBX8ksM97CaP/autz0qfCA7skoK44k+/q0FzUk=','2015-10-12 09:23:23',0,'pattabi','pattabi','ramasamy','',1,1,'2015-10-07 23:36:10'),(10,'pbkdf2_sha256$12000$yNLsf7mPB4Lh$BQH9/zxckOE4PNEZYSnRNZOBUuSrQS1llFvZT0ZkMCI=','2015-10-12 07:49:48',0,'ashish','ashish','kumar','',1,1,'2015-10-08 04:01:32'),(11,'pbkdf2_sha256$12000$1nnzeq0Sb1nx$jwGmspNXyRZpBf/t1dL8tQAUHKDJyB3c21qfp+cQGsE=','2015-10-08 04:35:28',0,'mahaveer','Mahaveer','Automobiles','',0,1,'2015-10-08 04:35:28'),(12,'pbkdf2_sha256$12000$RfwOgUX7LdB8$vBr1JBPJ7cjNuSnfO2Fak8O/dQ73NY45EzNvuBflEXM=','2015-10-08 05:08:04',0,'naveen','Naveen','Shankar','',0,1,'2015-10-08 05:08:04'),(13,'pbkdf2_sha256$12000$CM0mdfEYv1NJ$78IqrbLCqBIlwQtzZg0P3hqev0la7c75gHJWd3sYxWY=','2015-10-09 08:25:00',0,'shreya','shreya','kundan','',0,1,'2015-10-09 08:25:00');
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
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
INSERT INTO `auth_user_groups` VALUES (1,1,35),(2,2,20),(3,3,20),(4,4,20),(5,5,20),(6,6,23),(7,7,23),(8,8,4),(10,9,2),(12,10,14);
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
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
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
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2015-10-07 23:36:11',1,3,'9','pattabi',1,''),(2,'2015-10-07 23:37:14',1,3,'9','pattabi',2,'Changed is_staff and groups.'),(3,'2015-10-07 23:37:47',1,3,'9','pattabi',2,'Changed first_name and last_name.'),(4,'2015-10-07 23:39:58',1,28,'9','080 - 78654323 pattabi',1,''),(5,'2015-10-08 00:10:39',1,35,'1','pattabi',1,''),(6,'2015-10-08 00:14:49',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(7,'2015-10-08 00:18:04',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(8,'2015-10-08 00:19:29',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(9,'2015-10-08 04:01:32',9,3,'10','win',1,''),(10,'2015-10-08 04:02:49',9,3,'10','win',2,'Changed first_name, last_name, is_staff and groups.'),(11,'2015-10-08 04:05:14',9,28,'10','044 - 24765898 win',1,''),(12,'2015-10-08 04:30:54',9,83,'2','400002 WIN AUTO',1,''),(13,'2015-10-08 04:35:28',9,3,'11','mahaveer',1,''),(14,'2015-10-08 04:35:59',9,3,'11','mahaveer',2,'Changed first_name and last_name.'),(15,'2015-10-08 04:38:32',9,28,'11','080 - 40960450 mahaveer',1,''),(16,'2015-10-08 04:42:52',1,2,'14','Distributors',2,'Changed permissions.'),(17,'2015-10-08 04:48:46',10,86,'1','60001 mahaveer',1,''),(18,'2015-10-08 05:07:27',1,2,'14','Distributors',2,'Changed permissions.'),(19,'2015-10-08 05:08:04',10,3,'12','naveen',1,''),(20,'2015-10-08 05:08:24',10,3,'12','naveen',2,'Changed first_name and last_name.'),(21,'2015-10-08 05:09:45',10,28,'12','080 - 77777756 naveen',1,''),(22,'2015-10-08 05:11:11',10,85,'1','500001 Naveen Shankar',1,''),(23,'2015-10-08 05:15:54',1,2,'14','Distributors',2,'No fields changed.'),(24,'2015-10-08 05:19:20',1,2,'14','Distributors',2,'Changed permissions.'),(25,'2015-10-08 05:20:39',10,87,'1','DSRWorkAllocation object',1,''),(26,'2015-10-08 13:30:38',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(27,'2015-10-08 16:24:26',9,3,'10','win',2,'Changed first_name and last_name.'),(28,'2015-10-08 17:55:26',1,2,'2','AreaSalesManagers',2,'No fields changed.'),(29,'2015-10-08 17:55:56',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(30,'2015-10-09 06:29:43',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(31,'2015-10-09 06:36:19',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(32,'2015-10-09 06:51:29',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(33,'2015-10-09 06:51:56',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(34,'2015-10-09 07:06:00',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(35,'2015-10-09 07:13:21',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(36,'2015-10-09 07:32:14',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(37,'2015-10-09 07:32:32',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(38,'2015-10-09 07:32:47',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(39,'2015-10-09 07:55:41',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(40,'2015-10-09 08:25:00',10,3,'13','shreya',1,''),(41,'2015-10-09 08:25:42',10,3,'13','shreya',2,'Changed first_name and last_name.'),(42,'2015-10-09 08:27:24',10,28,'13',' shreya',1,''),(43,'2015-10-09 08:29:48',10,86,'2','60002 shreyas Automobiles',1,''),(44,'2015-10-09 08:57:05',9,28,'11','080 - 40960450 mahaveer',2,'Changed image_url.'),(45,'2015-10-09 09:20:44',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(46,'2015-10-09 09:25:09',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(47,'2015-10-09 09:26:44',9,28,'10','044 - 24765898 win',2,'Changed image_url.'),(48,'2015-10-09 09:54:05',9,28,'11','080 - 40960450 mahaveer',2,'Changed image_url.'),(49,'2015-10-09 11:18:22',10,87,'2','DSRWorkAllocation object',1,''),(50,'2015-10-09 11:18:36',10,87,'3','DSRWorkAllocation object',1,''),(51,'2015-10-09 12:19:11',1,92,'16','OrderPart object',1,''),(52,'2015-10-10 07:27:11',10,87,'4','DSRWorkAllocation object',1,''),(53,'2015-10-10 07:27:36',10,87,'5','DSRWorkAllocation object',1,''),(54,'2015-10-10 07:27:56',10,87,'6','DSRWorkAllocation object',1,''),(55,'2015-10-10 09:05:36',1,2,'2','AreaSalesManagers',2,'Changed permissions.'),(56,'2015-10-10 09:27:39',1,92,'63','OrderPart object',2,'Changed delivered.'),(57,'2015-10-10 11:31:38',10,3,'14','retailer123',1,''),(58,'2015-10-10 11:33:09',10,28,'14','080 - 40960450 retailer123',1,''),(59,'2015-10-10 11:40:13',10,86,'3','600002 retailer123',1,''),(60,'2015-10-10 11:56:54',10,87,'7','DSRWorkAllocation object',1,''),(61,'2015-10-11 04:07:26',10,86,'4','600002 retailerbang',1,''),(62,'2015-10-11 04:11:23',10,86,'None','600002 sampleret',1,''),(63,'2015-10-11 04:14:21',10,86,'None','600003 shreya',1,''),(64,'2015-10-11 04:15:34',10,86,'5','600003 retailer123',1,''),(65,'2015-10-12 04:59:15',10,87,'8','DSRWorkAllocation object',1,''),(66,'2015-10-12 04:59:48',10,87,'9','DSRWorkAllocation object',1,''),(67,'2015-10-12 05:21:53',10,28,'11','080 - 40960450 mahaveer',2,'Changed address.'),(68,'2015-10-12 05:23:09',1,2,'14','Distributors',2,'Changed permissions.'),(69,'2015-10-12 08:04:34',10,86,'6','600003 e',1,'');
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
) ENGINE=InnoDB AUTO_INCREMENT=339 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'client','oauth2','client'),(9,'grant','oauth2','grant'),(10,'access token','oauth2','accesstoken'),(11,'refresh token','oauth2','refreshtoken'),(12,'industry','default','industry'),(13,'service type','default','servicetype'),(14,'service','default','service'),(15,'brand','default','brand'),(16,'brand product category','default','brandproductcategory'),(17,'brand service','default','brandservice'),(18,'gladminds user','default','gladmindsuser'),(19,'otp token','default','otptoken'),(20,'message template','default','messagetemplate'),(21,'email template','default','emailtemplate'),(22,'app preferences','default','apppreferences'),(23,'sms log','default','smslog'),(24,'email log','default','emaillog'),(25,'audit log','default','auditlog'),(26,'constant','default','constant'),(27,'brand product category','core','brandproductcategory'),(28,'user profile','core','userprofile'),(29,'zonal service manager','core','zonalservicemanager'),(30,'area service manager','core','areaservicemanager'),(31,'circle head','core','circlehead'),(32,'regional manager','core','regionalmanager'),(33,'territory','core','territory'),(34,'state','core','state'),(35,'area sales manager','core','areasalesmanager'),(36,'dealer','core','dealer'),(37,'authorized service center','core','authorizedservicecenter'),(38,'service advisor','core','serviceadvisor'),(39,'brand department','core','branddepartment'),(40,'department sub categories','core','departmentsubcategories'),(41,'service desk user','core','servicedeskuser'),(42,'feedback','core','feedback'),(43,'activity','core','activity'),(44,'comment','core','comment'),(45,'feedback event','core','feedbackevent'),(46,'product type','core','producttype'),(47,'product data','core','productdata'),(48,'coupon data','core','coupondata'),(49,'service advisor coupon relationship','core','serviceadvisorcouponrelationship'),(50,'ucn recovery','core','ucnrecovery'),(51,'old fsc data','core','oldfscdata'),(52,'cdms data','core','cdmsdata'),(53,'otp token','core','otptoken'),(54,'message template','core','messagetemplate'),(55,'email template','core','emailtemplate'),(56,'asc temp registration','core','asctempregistration'),(57,'sa temp registration','core','satempregistration'),(58,'customer temp registration','core','customertempregistration'),(59,'customer update failure','core','customerupdatefailure'),(60,'customer update history','core','customerupdatehistory'),(61,'user preference','core','userpreference'),(62,'sms log','core','smslog'),(63,'email log','core','emaillog'),(64,'data feed log','core','datafeedlog'),(65,'feed failure log','core','feedfailurelog'),(66,'vin sync feed log','core','vinsyncfeedlog'),(67,'audit log','core','auditlog'),(68,'sla','core','sla'),(69,'service type','core','servicetype'),(70,'service','core','service'),(71,'constant','core','constant'),(72,'date dimension','core','datedimension'),(73,'coupon fact','core','couponfact'),(74,'transporter','core','transporter'),(75,'supervisor','core','supervisor'),(76,'container indent','core','containerindent'),(77,'container lr','core','containerlr'),(78,'container tracker','core','containertracker'),(79,'city','core','city'),(80,'national spares manager','core','nationalsparesmanager'),(81,'national sales manager','core','nationalsalesmanager'),(82,'area spares manager','core','areasparesmanager'),(83,'distributor','core','distributor'),(84,'distributor staff','core','distributorstaff'),(85,'distributor sales rep','core','distributorsalesrep'),(86,'retailer','core','retailer'),(87,'dsr work allocation','core','dsrworkallocation'),(88,'part models','core','partmodels'),(89,'categories','core','categories'),(90,'sub categories','core','subcategories'),(91,'part pricing','core','partpricing'),(92,'order part','core','orderpart'),(93,'alternate parts','core','alternateparts'),(94,'cv categories','core','cvcategories'),(95,'kit','core','kit'),(96,'part master cv','core','partmastercv'),(97,'member','core','member'),(98,'spare part master data','core','sparepartmasterdata'),(99,'spare part upc','core','sparepartupc'),(100,'spare part point','core','sparepartpoint'),(101,'accumulation request','core','accumulationrequest'),(102,'partner','core','partner'),(103,'product catalog','core','productcatalog'),(104,'redemption request','core','redemptionrequest'),(105,'welcome kit','core','welcomekit'),(106,'comment thread','core','commentthread'),(107,'loyalty sla','core','loyaltysla'),(108,'discrepant accumulation','core','discrepantaccumulation'),(109,'eco release','core','ecorelease'),(110,'eco implementation','core','ecoimplementation'),(111,'brand vertical','core','brandvertical'),(112,'brand product range','core','brandproductrange'),(113,'bom header','core','bomheader'),(114,'bom plate','core','bomplate'),(115,'bom part','core','bompart'),(116,'bom plate part','core','bomplatepart'),(117,'bom visualization','core','bomvisualization'),(118,'service circular','core','servicecircular'),(119,'manufacturing data','core','manufacturingdata'),(120,'brand product category','bajaj','brandproductcategory'),(121,'user profile','bajaj','userprofile'),(122,'zonal service manager','bajaj','zonalservicemanager'),(123,'circle head','bajaj','circlehead'),(124,'regional manager','bajaj','regionalmanager'),(125,'territory','bajaj','territory'),(126,'state','bajaj','state'),(127,'national sales manager','bajaj','nationalsalesmanager'),(128,'area sales manager','bajaj','areasalesmanager'),(129,'area service manager','bajaj','areaservicemanager'),(130,'dealer','bajaj','dealer'),(131,'authorized service center','bajaj','authorizedservicecenter'),(132,'service advisor','bajaj','serviceadvisor'),(133,'service desk user','bajaj','servicedeskuser'),(134,'brand department','bajaj','branddepartment'),(135,'department sub categories','bajaj','departmentsubcategories'),(136,'feedback','bajaj','feedback'),(137,'activity','bajaj','activity'),(138,'comment','bajaj','comment'),(139,'feedback event','bajaj','feedbackevent'),(140,'product type','bajaj','producttype'),(141,'product data','bajaj','productdata'),(142,'coupon data','bajaj','coupondata'),(143,'service advisor coupon relationship','bajaj','serviceadvisorcouponrelationship'),(144,'ucn recovery','bajaj','ucnrecovery'),(145,'old fsc data','bajaj','oldfscdata'),(146,'cdms data','bajaj','cdmsdata'),(147,'otp token','bajaj','otptoken'),(148,'message template','bajaj','messagetemplate'),(149,'email template','bajaj','emailtemplate'),(150,'asc temp registration','bajaj','asctempregistration'),(151,'sa temp registration','bajaj','satempregistration'),(152,'customer temp registration','bajaj','customertempregistration'),(153,'customer update failure','bajaj','customerupdatefailure'),(154,'customer update history','bajaj','customerupdatehistory'),(155,'user preference','bajaj','userpreference'),(156,'sms log','bajaj','smslog'),(157,'email log','bajaj','emaillog'),(158,'data feed log','bajaj','datafeedlog'),(159,'feed failure log','bajaj','feedfailurelog'),(160,'vin sync feed log','bajaj','vinsyncfeedlog'),(161,'audit log','bajaj','auditlog'),(162,'sla','bajaj','sla'),(163,'service type','bajaj','servicetype'),(164,'service','bajaj','service'),(165,'constant','bajaj','constant'),(166,'date dimension','bajaj','datedimension'),(167,'coupon fact','bajaj','couponfact'),(168,'transporter','bajaj','transporter'),(169,'supervisor','bajaj','supervisor'),(170,'container indent','bajaj','containerindent'),(171,'container lr','bajaj','containerlr'),(172,'container tracker','bajaj','containertracker'),(173,'city','bajaj','city'),(174,'national spares manager','bajaj','nationalsparesmanager'),(175,'area spares manager','bajaj','areasparesmanager'),(176,'distributor','bajaj','distributor'),(177,'distributor staff','bajaj','distributorstaff'),(178,'distributor sales rep','bajaj','distributorsalesrep'),(179,'retailer','bajaj','retailer'),(180,'dsr work allocation','bajaj','dsrworkallocation'),(181,'part models','bajaj','partmodels'),(182,'categories','bajaj','categories'),(183,'sub categories','bajaj','subcategories'),(184,'part pricing','bajaj','partpricing'),(185,'member','bajaj','member'),(186,'spare part master data','bajaj','sparepartmasterdata'),(187,'order part','bajaj','orderpart'),(188,'spare part upc','bajaj','sparepartupc'),(189,'spare part point','bajaj','sparepartpoint'),(190,'accumulation request','bajaj','accumulationrequest'),(191,'partner','bajaj','partner'),(192,'product catalog','bajaj','productcatalog'),(193,'redemption request','bajaj','redemptionrequest'),(194,'welcome kit','bajaj','welcomekit'),(195,'comment thread','bajaj','commentthread'),(196,'loyalty sla','bajaj','loyaltysla'),(197,'email token','bajaj','emailtoken'),(198,'discrepant accumulation','bajaj','discrepantaccumulation'),(199,'eco release','bajaj','ecorelease'),(200,'eco implementation','bajaj','ecoimplementation'),(201,'brand vertical','bajaj','brandvertical'),(202,'brand product range','bajaj','brandproductrange'),(203,'bom header','bajaj','bomheader'),(204,'bom plate','bajaj','bomplate'),(205,'bom part','bajaj','bompart'),(206,'bom plate part','bajaj','bomplatepart'),(207,'bom visualization','bajaj','bomvisualization'),(208,'service circular','bajaj','servicecircular'),(209,'manufacturing data','bajaj','manufacturingdata'),(210,'brand product category','demo','brandproductcategory'),(211,'user profile','demo','userprofile'),(212,'zonal service manager','demo','zonalservicemanager'),(213,'area service manager','demo','areaservicemanager'),(214,'dealer','demo','dealer'),(215,'authorized service center','demo','authorizedservicecenter'),(216,'service advisor','demo','serviceadvisor'),(217,'brand\n department','demo','branddepartment'),(218,'department sub categories','demo','departmentsubcategories'),(219,'service desk user','demo','servicedeskuser'),(220,'feedback','demo','feedback'),(221,'activity','demo','activity'),(222,'comment','demo','comment'),(223,'feedback event','demo','feedbackevent'),(224,'product type','demo','producttype'),(225,'product data','demo','productdata'),(226,'coupon data','demo','coupondata'),(227,'service advisor coupon relationship','demo','serviceadvisorcouponrelationship'),(228,'ucn recovery','demo','ucnrecovery'),(229,'old fsc data','demo','oldfscdata'),(230,'cdms data','demo','cdmsdata'),(231,'otp token','demo','otptoken'),(232,'message template','demo','messagetemplate'),(233,'email template','demo','emailtemplate'),(234,'asc temp registration','demo','asctempregistration'),(235,'sa temp registration','demo','satempregistration'),(236,'customer temp registration','demo','customertempregistration'),(237,'user preference','demo','userpreference'),(238,'sms log','demo','smslog'),(239,'email log','demo','emaillog'),(240,'data feed log','demo','datafeedlog'),(241,'feed failure log','demo','feedfailurelog'),(242,'vin sync feed log','demo','vinsyncfeedlog'),(243,'audit log','demo','auditlog'),(244,'sla','demo','sla'),(245,'service type','demo','servicetype'),(246,'service','demo','service'),(247,'constant','demo','constant'),(248,'national spares manager','demo','nationalsparesmanager'),(249,'area spares manager','demo','areasparesmanager'),(250,'territory','demo','territory'),(251,'state','demo','state'),(252,'city','demo','city'),(253,'distributor','demo','distributor'),(254,'retailer','demo','retailer'),(255,'member','demo','member'),(256,'spare part master data','demo','sparepartmasterdata'),(257,'spare part upc','demo','sparepartupc'),(258,'spare part point','demo','sparepartpoint'),(259,'accumulation request','demo','accumulationrequest'),(260,'partner','demo','partner'),(261,'product catalog','demo','productcatalog'),(262,'redemption request','demo','redemptionrequest'),(263,'welcome kit','demo','welcomekit'),(264,'date dimension','demo','datedimension'),(265,'coupon fact','demo','couponfact'),(266,'loyalty sla','demo','loyaltysla'),(267,'comment thread','demo','commentthread'),(268,'discrepant accumulation','demo','discrepantaccumulation'),(269,'industry','afterbuy','industry'),(270,'brand','afterbuy','brand'),(271,'brand product category','afterbuy','brandproductcategory'),(272,'product type','afterbuy','producttype'),(273,'consumer','afterbuy','consumer'),(274,'user product','afterbuy','userproduct'),(275,'product support','afterbuy','productsupport'),(276,'registration certificate','afterbuy','registrationcertificate'),(277,'product insurance info','afterbuy','productinsuranceinfo'),(278,'product warranty info','afterbuy','productwarrantyinfo'),(279,'pollution certificate','afterbuy','pollutioncertificate'),(280,'license','afterbuy','license'),(281,'invoice','afterbuy','invoice'),(282,'support','afterbuy','support'),(283,'product specification','afterbuy','productspecification'),(284,'product feature','afterbuy','productfeature'),(285,'recommended part','afterbuy','recommendedpart'),(286,'otp token','afterbuy','otptoken'),(287,'user notification','afterbuy','usernotification'),(288,'user mobile info','afterbuy','usermobileinfo'),(289,'user preference','afterbuy','userpreference'),(290,'brand preference','afterbuy','brandpreference'),(291,'interest','afterbuy','interest'),(292,'sell information','afterbuy','sellinformation'),(293,'user product images','afterbuy','userproductimages'),(294,'service type','afterbuy','servicetype'),(295,'service','afterbuy','service'),(296,'message template','afterbuy','messagetemplate'),(297,'email template','afterbuy','emailtemplate'),(298,'sms log','afterbuy','smslog'),(299,'email log','afterbuy','emaillog'),(300,'audit log','afterbuy','auditlog'),(301,'constant','afterbuy','constant'),(302,'email token','afterbuy','emailtoken'),(303,'service center location','afterbuy','servicecenterlocation'),(304,'service history','afterbuy','servicehistory'),(305,'brand product category','bajajib','brandproductcategory'),(306,'user profile','bajajib','userprofile'),(307,'country','bajajib','country'),(308,'country distributor','bajajib','countrydistributor'),(309,'main country dealer','bajajib','maincountrydealer'),(310,'dealer','bajajib','dealer'),(311,'service advisor','bajajib','serviceadvisor'),(312,'product type','bajajib','producttype'),(313,'product data','bajajib','productdata'),(314,'fleet rider','bajajib','fleetrider'),(315,'coupon data','bajajib','coupondata'),(316,'service advisor coupon relationship','bajajib','serviceadvisorcouponrelationship'),(317,'ucn recovery','bajajib','ucnrecovery'),(318,'otp token','bajajib','otptoken'),(319,'message template','bajajib','messagetemplate'),(320,'email template','bajajib','emailtemplate'),(321,'sms log','bajajib','smslog'),(322,'email log','bajajib','emaillog'),(323,'data feed log','bajajib','datafeedlog'),(324,'feed failure log','bajajib','feedfailurelog'),(325,'vin sync feed log','bajajib','vinsyncfeedlog'),(326,'constant','bajajib','constant'),(327,'customer update history','bajajib','customerupdatehistory'),(328,'task state','djcelery','taskmeta'),(329,'saved group result','djcelery','tasksetmeta'),(330,'interval','djcelery','intervalschedule'),(331,'crontab','djcelery','crontabschedule'),(332,'periodic tasks','djcelery','periodictasks'),(333,'periodic task','djcelery','periodictask'),(334,'worker','djcelery','workerstate'),(335,'task','djcelery','taskstate'),(336,'TOTP device','otp_totp','totpdevice'),(337,'dsr scorecard report','core','dsrscorecardreport'),(338,'retailer collection','core','retailercollection');
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
INSERT INTO `django_session` VALUES ('4jm0sbq9w9z3vghj1tg9rn7rxcvbliw4','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-10-22 04:27:12'),('5o7ykmztjx6h4wlpnli7ynm2je91gxnb','ZWIxZWM4OGZhZTIyYTNkZWQzZjM3NzMzNWNjYzAwMGY4NmZhY2EyZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6OX0=','2015-10-26 09:23:23'),('817j2g85e584kziniyo4t6xh7y4a4aa0','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-10-26 05:41:43'),('9mavlgxd8iwvlm1p5bjku3e7rco31h0u','MmE2YzJmMTdjN2I2NmUwM2I4NTQwMTI0OTU3ZmMyZjE3ZTQwYjAwZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MTB9','2015-10-24 11:54:45'),('bxutamju8m6sgk0ydva10yki1reyw3a9','ZWIxZWM4OGZhZTIyYTNkZWQzZjM3NzMzNWNjYzAwMGY4NmZhY2EyZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6OX0=','2015-10-25 06:50:29'),('f9vhdwyls4adw5sko0xg68tjo0jgeukb','MmE2YzJmMTdjN2I2NmUwM2I4NTQwMTI0OTU3ZmMyZjE3ZTQwYjAwZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MTB9','2015-10-26 05:23:27'),('ijqm6oiwdbm69q5t8xila9wo8w89q3gz','NTM5MmMyZmRiNzViN2M2Y2Y2MzhkNGFmNTc4ODA0Y2NhZGMyNjYwYTp7fQ==','2015-10-25 06:49:21'),('jpmscfz5794njx8mp8rhjld7krrx7xuj','ZWIxZWM4OGZhZTIyYTNkZWQzZjM3NzMzNWNjYzAwMGY4NmZhY2EyZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6OX0=','2015-10-25 10:25:21'),('qznyvpn5fr9bybayv718oy730ynt8dq1','MmE2YzJmMTdjN2I2NmUwM2I4NTQwMTI0OTU3ZmMyZjE3ZTQwYjAwZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MTB9','2015-10-26 07:42:15');
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
  CONSTRAINT `member_id_refs_id_0ee003a9` FOREIGN KEY (`member_id`) REFERENCES `gm_member` (`id`),
  CONSTRAINT `asm_id_refs_id_eb867905` FOREIGN KEY (`asm_id`) REFERENCES `gm_areasparesmanager` (`id`)
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
-- Table structure for table `gm_alternateparts`
--

DROP TABLE IF EXISTS `gm_alternateparts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_alternateparts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `part_number` varchar(255) NOT NULL,
  `part_name` varchar(255) NOT NULL,
  `old_part_number` varchar(255) NOT NULL,
  `model_name` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_alternateparts`
--

LOCK TABLES `gm_alternateparts` WRITE;
/*!40000 ALTER TABLE `gm_alternateparts` DISABLE KEYS */;
INSERT INTO `gm_alternateparts` VALUES (1,'2015-09-21 00:00:00','2015-09-21 00:00:00','36224005','KIT LOCK :- TOOL BOX :- PLASTIC WITH KEY','22161202','COMPACT 2S, DSL (SHL)',1),(2,'2015-09-21 00:00:00','2015-09-21 00:00:00','36244022','part name','24181029','RE 145 PET UG,RE2S CNG',1),(3,'2015-09-21 00:00:00','2015-09-21 00:00:00','36244023','KIT Ignition parking switch','24181029','RE 145 GAS',1),(4,'2015-09-21 00:00:00','2015-09-21 00:00:00','36244024','KIT LOCK FOR DOOR WITH KEY','24230197','COMPACT',1),(5,'2015-09-21 00:00:00','2015-09-21 00:00:00','36244042','KIT St lock (24181016) with key - Small','24181016','ALL SMALL & MEDIUM MODELS',1),(6,'2015-09-21 00:00:00','2015-09-21 00:00:00','36244043','KIT Ignition switch (24201387) with key','24201387','RE 145 KS FL,LPG,CNGUG,',1),(7,'2015-09-21 00:00:00','2015-09-21 00:00:00','36244044','KIT Lock fuel filling door (24181144) wi','24181144','COMPACT2S,4S PETROL, 145D, 445',1),(8,'2015-09-21 00:00:00','2015-09-21 00:00:00','36244045','KIT Ignition Switch (24201328) with key','24201328','RE 145 UG',1),(9,'2015-09-21 00:00:00','2015-09-21 00:00:00','52210040','ASSEMBLY MUD REAR ASY ED COAT 25231062','25231062','Compact 2S,4s,dsl',1),(10,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240645','WIND SHIELD REFL ED COATED','24231593','All FL models',1),(11,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240664','DOOR REAR DOOR ED COATED ( BA231058)','BA231058','RearCompact 2S/4S,dsl',1),(12,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240667','ASSEMBLY FRAME ASSLY ED COATED BB161084','BB161084','Maxima diesel',1),(13,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240668','BODY ASSLY ED COATED BB231351 REFL','BB231351','Maxima diesel',1),(14,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240669','DOOR ENGINE FOR TRAY ED COATED BB231215','BB231215','Maxima diesel',1),(15,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240670','DOOR ASSLY REAR ED COATED BB231216 REFL','BB231216','Maxima diesel',1),(16,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240674','BARE CHASSIS ED COATED BA161160 REFL','BA161160','Compactdiesel SHL',1),(17,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240675','BODY COMPLETE ED COATED BA23112','BA231125','Compact diesel',1),(18,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240678','BARE CHSSIS ED COATED AF161114 REFL','AF161114','Compact4S cng,lpg',1),(19,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240681','ASSEMBLYBARE CHASSIS COMP AA161210 REFL','AA161210','Compact4S pet',1),(20,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240743','ASSEMBLY CHASSIS REFL ED COATED','AS160027','Compact2S cng,lpg ,es,ks',1),(21,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240743','ASSEMBLY CHASSIS REFL ED COATED','AS160015','Compact2S cng,lpg ,es,ks',1),(22,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240746','ASSEMBLY CHASSIS REFL ED COATED','BA160006','Compactdiesel THL',1),(23,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240748','ASSEMBLY DOOR REAR LOWER','BH211148','Optima diesel',1),(24,'2015-09-21 00:00:00','2015-09-21 00:00:00','52240760','ED COATED BUMPER 24165137','24165137','All Compact Model',1),(25,'2015-09-21 00:00:00','2015-09-21 00:00:00','52244040','ED COATED FR MUDGUARD AA161183','AA161183','Compact 4S,dsl, thl',1),(26,'2015-09-21 00:00:00','2015-09-21 00:00:00','52244058','ED COATED ASSEMBLY CHASSIS BARE','24165271','Compact2Spet es ks',1),(27,'2015-09-21 00:00:00','2015-09-21 00:00:00','52244058','ED COATED ASSEMBLY CHASSIS BARE','24165175','Compact2Spet es ks',1),(28,'2015-09-21 00:00:00','2015-09-21 00:00:00','52244065','ED COATED BODY AA231249','AA231216','Compact 2s/4Spet',1),(29,'2015-09-21 00:00:00','2015-09-21 00:00:00','52244065','ED COATED BODY AA231249','AA231249','Compact 2s/4Spet',1),(30,'2015-09-21 00:00:00','2015-09-21 00:00:00','52244066','ED COATED BODY AF231177','AF231171','Compact 2s/4Scng,lpg',1),(31,'2015-09-21 00:00:00','2015-09-21 00:00:00','52244066','ED COATED BODY AF231177','AF231177','Compact 2s/4Scng,lpg',1),(32,'2015-09-21 00:00:00','2015-09-21 00:00:00','36AA4014','KIT Ignition parking switch','AA181012','RE 205 PET',1),(33,'2015-09-21 00:00:00','2015-09-21 00:00:00','36AA4015','KIT Lock Fuel filling door WITH KEY','AA181014','OPTIMA 4S',1),(34,'2015-09-21 00:00:00','2015-09-21 00:00:00','36AA4028','KIT Ignition switch (AA201254) with key','AA201254','ALL MODELS ES MODEL',1),(35,'2015-09-21 00:00:00','2015-09-21 00:00:00','36AF0018','KIT Ignition parking switch','AF181011','RE205 LPG,CNG',1);
/*!40000 ALTER TABLE `gm_alternateparts` ENABLE KEYS */;
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `gm_areasalesmanager_59c17353` (`rm_id`),
  CONSTRAINT `user_id_refs_user_id_ffe86796` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `rm_id_refs_id_e278611d` FOREIGN KEY (`rm_id`) REFERENCES `gm_regionalmanager` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_areasalesmanager`
--

LOCK TABLES `gm_areasalesmanager` WRITE;
/*!40000 ALTER TABLE `gm_areasalesmanager` DISABLE KEYS */;
INSERT INTO `gm_areasalesmanager` VALUES (1,'2015-10-08 00:10:39','2015-10-08 00:10:39',9,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_areasalesmanager_state`
--

LOCK TABLES `gm_areasalesmanager_state` WRITE;
/*!40000 ALTER TABLE `gm_areasalesmanager_state` DISABLE KEYS */;
INSERT INTO `gm_areasalesmanager_state` VALUES (1,1,1);
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
  KEY `gm_areaservicemanager_6340c63c` (`user_id`),
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
  CONSTRAINT `user_id_refs_user_id_192897bb` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `nsm_id_refs_id_11a233d9` FOREIGN KEY (`nsm_id`) REFERENCES `gm_nationalsparesmanager` (`id`)
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
  CONSTRAINT `user_id_refs_user_id_adb8c76a` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `asm_id_refs_id_dea638d3` FOREIGN KEY (`asm_id`) REFERENCES `gm_areaservicemanager` (`id`),
  CONSTRAINT `dealer_id_refs_user_id_77b70a48` FOREIGN KEY (`dealer_id`) REFERENCES `gm_dealer` (`user_id`)
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
  CONSTRAINT `plate_id_refs_id_76e0311d` FOREIGN KEY (`plate_id`) REFERENCES `gm_bomplate` (`id`),
  CONSTRAINT `bom_id_refs_id_df9dddce` FOREIGN KEY (`bom_id`) REFERENCES `gm_bomheader` (`id`),
  CONSTRAINT `part_id_refs_id_e473efb5` FOREIGN KEY (`part_id`) REFERENCES `gm_bompart` (`id`)
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_brandproductcategory`
--

LOCK TABLES `gm_brandproductcategory` WRITE;
/*!40000 ALTER TABLE `gm_brandproductcategory` DISABLE KEYS */;
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_categories`
--

LOCK TABLES `gm_categories` WRITE;
/*!40000 ALTER TABLE `gm_categories` DISABLE KEYS */;
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
  CONSTRAINT `user_id_refs_id_d9f0d698` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `redemption_id_refs_transaction_id_a5a677f5` FOREIGN KEY (`redemption_id`) REFERENCES `gm_redemptionrequest` (`transaction_id`),
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
  PRIMARY KEY (`id`)
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
  CONSTRAINT `service_advisor_id_refs_user_id_f9cb3c7a` FOREIGN KEY (`service_advisor_id`) REFERENCES `gm_serviceadvisor` (`user_id`),
  CONSTRAINT `product_id_refs_id_b447d7b8` FOREIGN KEY (`product_id`) REFERENCES `gm_productdata` (`id`)
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
-- Table structure for table `gm_cvcategories`
--

DROP TABLE IF EXISTS `gm_cvcategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_cvcategories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `name` varchar(255) NOT NULL,
  `usps` longtext,
  `importance` longtext,
  `image_url` varchar(255) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_cvcategories`
--

LOCK TABLES `gm_cvcategories` WRITE;
/*!40000 ALTER TABLE `gm_cvcategories` DISABLE KEYS */;
INSERT INTO `gm_cvcategories` VALUES (1,'2015-08-12 00:00:00','2015-08-12 00:00:00','AIR FILTER','High quality filter paper grade & larger filtration area for better filtration.','Ensures dust free intake air for longer life of Engine','img/products/airfilter.jpg',1),(2,'2015-08-12 00:00:00','2015-08-12 00:00:00','FILTER OIL','Better quality filter paper filters finer dust particle available in fuel and helps in maintaining longer , Paper  design with larger surface area helps in improving filtration efficiency, Controlled flow rate and pressure drop helps in smooth engine driving.','Ensure better Oil flow rate, Minimize oil Wastage, Ensure 100% Cooling','img/products/filteroil.jpg',1),(3,'2015-08-12 00:00:00','2015-08-12 00:00:00','FILTER (STRAINER) OIL','Magnet provided in Filtration area helps in capturing suspended metallic debris in oil, Coarse filter paper helps in filtering particles from sump oil.','Improves Performance of Vehicle.','img/products/straineroil.jpg',1),(4,'2015-08-12 00:00:00','2015-08-12 00:00:00','SEAL OIL ALL TYPES','Better material (Synthetic Rubber) of seal leap ensures less wear of leap and higher sealing pressure, Controlled lip pressure helps lower friction.','Leak proof design ensures no leakage through seal.','img/products/sealoil.jpg',1),(5,'2015-08-12 00:00:00','2015-08-12 00:00:00','BELLOWs','Wear resistance material help in lesser wear with dust particle ,Leap at smaller end of bellow stops water and mud seepage in to bellow.','Ensure Dust free environment and higher grease life.','img/products/bellows.jpg',1),(6,'2015-08-12 00:00:00','2015-08-12 00:00:00','BEARINGS','high Grade Material, Corrosive resistance Material.','Heavy Load Carrying capacity reduce Jerk.','img/products/bearings.jpg',1),(7,'2015-08-12 00:00:00','2015-08-12 00:00:00','DRUM BRAKES & SHOES','Cast Iron for Durability, Controlled geometric tolerances to ensure good braking performance','','img/products/drumbrakesandshoes.jpg',1),(8,'2015-08-12 00:00:00','2015-08-12 00:00:00','SHOCK ABSORBER',' Internal rebound stopper with better material  for longer life for rear shock absorbers of Maxima & Optima, Antifriction bush for rod guide for improved life, avoiding leakage.','Absorbs abnormal shocks for better and comfort ride.','img/products/SHOCKABSORBER.jpg',1),(9,'2015-08-12 00:00:00','2015-08-12 00:00:00','GASKETS','Controlled material property of sealing ring for better sealing of combustion gases leading to less power loss.','Superior sealing material for better sealing  to ensures no oil leakage.','img/products/gaskets.jpg',1),(10,'2015-08-12 00:00:00','2015-08-12 00:00:00','GEAR AND ASSEMBLIES','Accurately designed gears for strength and wear with best design software\'s to ensure  better and longer life.','Accurately designed gears for strength and wear with best design software\'s to ensure  better and longer life.','img/products/gearandassemblies.jpg',1),(11,'2015-08-12 00:00:00','2015-08-12 00:00:00','CLUTCH AND ASSEMBLIES','Finely tuned damper springs for jerk reduction, Superior quality friction material for long life.','Uniform Transmission and jerk reduction.','img/products/clutchandassemblies1.jpg',1),(12,'2015-08-12 00:00:00','2015-08-12 00:00:00','VALVES','Accurate geometry of Valve seat & run out for Better contact between Valve seat and Valve guide leading to less wear of Valve seat and no leakage.','Ensure High Engine Performance.','img/products/valves.jpg',1),(13,'2015-08-12 00:00:00','2015-08-12 00:00:00','PISTON AND RINGS','High Crown thickness for Better Heat Dissipation, Controlled ring groove profile for better ring dynamic, Better Piston Pin Surface finish for lesse friction force.','','img/products/pistonandrings.jpg',1),(14,'2015-08-12 00:00:00','2015-08-12 00:00:00','CRANK CASE',' Heat Resisting Durable material finish.','Heat Resisting Durable material finish.','img/products/crankcase.jpg',1),(15,'2015-08-12 00:00:00','2015-08-12 00:00:00','CRANKSHAFTS','Better crank balancing ensures no engine vibrations, Increased dynamic load capacity and better durability of crank pin and bearing.','better durability','img/products/cranckshafts.jpg',1),(16,'2015-08-12 00:00:00','2015-08-12 00:00:00','CYLINDER BLOCK AND KITS','Precisely controlled honing pattern to ensure minimal wear of liner and ring.','High Engine Life.','img/products/CYLINDERBLOCKANDKITS.jpg',1),(17,'2015-08-12 00:00:00','2015-08-12 00:00:00','CAMSHAFTS','Precisely maintained Cam profile through contour grinding to ensure precise intake & exhaust process and  helps in improving volumetric efficiency.','Ensure Best Timing ','img/products/camshafts.jpg',1),(18,'2015-08-12 00:00:00','2015-08-12 00:00:00','CARBURETTOR','Able to handle the rigors of daily driving while delivering consistent, reliable street performance from day to day','','img/products/CARBURETTOR.jpg',1),(19,'2015-08-12 00:00:00','2015-08-12 00:00:00','CONNECTING ROD ','Designed to handle power levels far beyond the original component\'s? ratings in order to ensure reliability','ensure reliability','img/products/connectingrod.jpg',1),(20,'2015-08-12 00:00:00','2015-08-12 00:00:00','SPARK PLUG','Superior quality material(Copper cored nickel alloy) for electrodes.','Uniform Spark yield to better combustion.','img/products/sparkplug.jpg',1),(21,'2015-08-12 00:00:00','2015-08-12 00:00:00','GUIDE CHAIN','Uniform Drive.','Uniform Drive.','img/products/guidechan.jpg',1),(22,'2015-08-12 00:00:00','2015-08-12 00:00:00','SLEEVE','High Tensile strength and Hardness, Excellent Corrosive and wear resistance','High Tensile strength and Hardness, Excellent Corrosive and wear resistance','img/products/sleeve.jpg',1),(23,'2015-08-12 00:00:00','2015-08-12 00:00:00','CYLINDER HEADS','Corrugated fins with higher surface area for better head dissipation, Higher life of valve seat and guides due to controlled machining parameters & material.','Corrugated fins with higher surface area for better head dissipation, Higher life of valve seat and guides due to controlled machining parameters & material.  ','img/products/cylinderheads.jpg',1),(24,'2015-08-12 00:00:00','2015-08-12 00:00:00','CABLES ALL TYPES','Pre-stretched clutch / gear  inner cable to avoid elongation in operation, which would avoid frequent adjustment.','Friction free  for smooth operations.','img/products/cables.jpg',1),(25,'2015-08-12 00:00:00','2015-08-12 00:00:00','STARTER MOTOR','','','img/products/startermotor.jpg',1),(26,'2015-08-12 00:00:00','2015-08-12 00:00:00','MAGNETOS','','','img/products/magnetos.jpg',1),(27,'2015-08-12 00:00:00','2015-08-12 00:00:00','HT COILS','','','img/products/htcoils.jpg',1),(28,'2015-08-12 00:00:00','2015-08-12 00:00:00','SWITCHES ALL TYPES','','','img/products/switches.jpg',1),(29,'2015-08-12 00:00:00','2015-08-12 00:00:00','TAIL LIGHT','High illumination, Fine Finish, Easy to Fit.','','img/products/taillight.jpg',1),(30,'2015-08-12 00:00:00','2015-08-12 00:00:00','HEAD LIGHT & LAMPS','High illumination, Fine Finish, Easy to Fit.','High illumination, Fine Finish, Easy to Fit.','img/products/headlightsandlamps.jpg',1),(31,'2015-08-12 00:00:00','2015-08-12 00:00:00','RELAYS','Effectively design to switch signal-level loads.','','img/products/relays.jpg',1),(32,'2015-08-12 00:00:00','2015-08-12 00:00:00','WIRING HARNESS','Harness protected by  standard fuses ratings restrict burn cases during short circuit case .Outer face completely protected by Conduit & Sleeve, Wire size used considering adequate safety factor.','Ensure High Safety.','img/products/wiringharness.jpg',1),(33,'2015-08-12 00:00:00','2015-08-12 00:00:00','BEADING','High quality rubber offer perfect grip, Made from superior quality rubber to ensure long working life.',' Ensure 100% grip to ensure perfect grip and nil leakage','img/products/beading.jpg',1),(34,'2015-08-12 00:00:00','2015-08-12 00:00:00','WIPER AND ASSEMBLIES','High content of natural rubber in the blade, combined with a synthetic additive to prolong lifespan.','High content of natural rubber in the blade, combined with a synthetic additive to prolong lifespan.','img/products/wiperandassemblies.jpg',1),(35,'2015-08-12 00:00:00','2015-08-12 00:00:00','COVERS ALL TYPES','','','img/products/covers.jpg',1),(36,'2015-08-12 00:00:00','2015-08-12 00:00:00','WINDSHIELD','High strength to ensure pressure of wind.','High strength to ensure pressure of wind.','img/products/windshield.jpg',1),(37,'2015-08-12 00:00:00','2015-08-12 00:00:00','SIDE GLASS','','','img/products/placeholder.jpg',1),(38,'2015-08-12 00:00:00','2015-08-12 00:00:00','BOLTS ALL TYPES','High Quality ,Durable Material .',' Ensure Best Fit.','img/products/bolts.jpg',1),(39,'2015-08-12 00:00:00','2015-08-12 00:00:00','BRACKETS ALL TYPE','High Durability and Fitment','High Durability and Fitment','img/products/brackets.jpg',1),(40,'2015-08-12 00:00:00','2015-08-12 00:00:00','TUBES ALL TYPES','','Perfect Fit, Ensure No leakage','img/products/tubes.jpg',1),(41,'2015-08-12 00:00:00','2015-08-12 00:00:00','BUSHES ALL TYPES','','','img/products/bushes.jpg',1),(42,'2015-08-12 00:00:00','2015-08-12 00:00:00','SILENCER','','Noise absorption with better fitment','img/products/silencer.jpg',1),(43,'2015-08-12 00:00:00','2015-08-12 00:00:00','STEERING COLUMN','','','img/products/steeringcolumn.jpg',1),(44,'2015-08-12 00:00:00','2015-08-12 00:00:00','PROPELLER SHAFT','','Heavy Load reliability,Accurate Fit, Long Life','img/products/propellershaft.jpg',1),(45,'2015-08-12 00:00:00','2015-08-12 00:00:00','SLIDER BLOCK USP','','Made of superior steel with best suitable heat treatments provides better wear resistance, Precisely machined grooves on inner and outer surfaces, Optimized geometry with close tolerances for better control on clearances.','img/products/sliderblockusp.jpg',1),(46,'2015-08-12 00:00:00','2015-08-12 00:00:00','HOUSING','','','img/products/housing.jpg',1),(47,'2015-08-12 00:00:00','2015-08-12 00:00:00','LEVERS\n ALL TYPES','','','img/products/levers.jpg',1),(48,'2015-08-12 00:00:00','2015-08-12 00:00:00','PIPE ALL TYPES','Better fit, Withstand Vibrations  . ','Ensure Nil leakage.','img/products/pipes.jpg ',1),(49,'2015-08-12 00:00:00','2015-08-12 00:00:00','AXLES','','','img/products/axels.jpg',1),(50,'2015-08-12 00:00:00','2015-08-12 00:00:00','LOCK SETS','','','img/products/locksets.jpg',1),(51,'2015-08-12 00:00:00','2015-08-12 00:00:00','MANIFOLD','High Capacity of Withstanding Pressure','','img/products/manifolsusp.jpg',1),(52,'2015-08-12 00:00:00','2015-08-12 00:00:00','ARM  ','High Tensile strength and reliability','High Tensile strength and reliability','img/products/arm.jpg',1);
/*!40000 ALTER TABLE `gm_cvcategories` ENABLE KEYS */;
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
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `dealer_id` (`dealer_id`),
  KEY `gm_dealer_dae8f18d` (`asm_id`),
  CONSTRAINT `user_id_refs_user_id_861bfaa3` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `asm_id_refs_id_f73bb336` FOREIGN KEY (`asm_id`) REFERENCES `gm_areaservicemanager` (`id`)
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
  CONSTRAINT `upc_id_refs_id_ea999ee6` FOREIGN KEY (`upc_id`) REFERENCES `gm_sparepartupc` (`id`),
  CONSTRAINT `accumulation_request_id_refs_transaction_id_2d21a456` FOREIGN KEY (`accumulation_request_id`) REFERENCES `gm_accumulationrequest` (`transaction_id`),
  CONSTRAINT `new_member_id_refs_id_8954529b` FOREIGN KEY (`new_member_id`) REFERENCES `gm_member` (`id`)
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
  `distributor_id` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `sent_to_sap` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `mobile` varchar(15) NOT NULL,
  `profile` varchar(15) NOT NULL,
  `language` varchar(10) DEFAULT NULL,
  `territory` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_distributor_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_bb62621f` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_distributor`
--

LOCK TABLES `gm_distributor` WRITE;
/*!40000 ALTER TABLE `gm_distributor` DISABLE KEYS */;
INSERT INTO `gm_distributor` VALUES (1,'2015-10-08 04:29:27','2015-10-08 04:29:27','400001','WIN AUTO','winauto@bajajauto.in','+9104424765432','chennai',0,10,'9880791278','Distributor','Tamil','south');
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
  `distributor_sales_code` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `distributor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_distributorsalesrep_6340c63c` (`user_id`),
  KEY `gm_distributorsalesrep_818f5865` (`distributor_id`),
  CONSTRAINT `distributor_id_refs_id_1410ee34` FOREIGN KEY (`distributor_id`) REFERENCES `gm_distributor` (`id`),
  CONSTRAINT `user_id_refs_user_id_1e769373` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_distributorsalesrep`
--

LOCK TABLES `gm_distributorsalesrep` WRITE;
/*!40000 ALTER TABLE `gm_distributorsalesrep` DISABLE KEYS */;
INSERT INTO `gm_distributorsalesrep` VALUES (1,'2015-10-08 05:11:11','2015-10-08 05:11:11','500001',1,'naveen@gladminds.co',12,1);
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
  `distributor_staff_code` varchar(50) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `distributor_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_distributorstaff_6340c63c` (`user_id`),
  KEY `gm_distributorstaff_818f5865` (`distributor_id`),
  CONSTRAINT `user_id_refs_user_id_2c82df01` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `distributor_id_refs_id_841530ad` FOREIGN KEY (`distributor_id`) REFERENCES `gm_distributor` (`id`)
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
-- Table structure for table `gm_dsrscorecardreport`
--

DROP TABLE IF EXISTS `gm_dsrscorecardreport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_dsrscorecardreport` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `serial_number` varchar(5) NOT NULL,
  `goals` varchar(255) DEFAULT NULL,
  `target` varchar(255) DEFAULT NULL,
  `actual` varchar(255) DEFAULT NULL,
  `measures` varchar(255) DEFAULT NULL,
  `weight` varchar(255) DEFAULT NULL,
  `total_score` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_dsrscorecardreport`
--

LOCK TABLES `gm_dsrscorecardreport` WRITE;
/*!40000 ALTER TABLE `gm_dsrscorecardreport` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_dsrscorecardreport` ENABLE KEYS */;
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
  `distributor_id` int(11) NOT NULL,
  `dsr_id` int(11) NOT NULL,
  `retailer_id` int(11) NOT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_dsrworkallocation_818f5865` (`distributor_id`),
  KEY `gm_dsrworkallocation_9f70fd12` (`dsr_id`),
  KEY `gm_dsrworkallocation_64f72e30` (`retailer_id`),
  CONSTRAINT `distributor_id_refs_id_87f3180d` FOREIGN KEY (`distributor_id`) REFERENCES `gm_distributor` (`id`),
  CONSTRAINT `dsr_id_refs_id_99351d5e` FOREIGN KEY (`dsr_id`) REFERENCES `gm_distributorsalesrep` (`id`),
  CONSTRAINT `retailer_id_refs_id_270a146f` FOREIGN KEY (`retailer_id`) REFERENCES `gm_retailer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_dsrworkallocation`
--

LOCK TABLES `gm_dsrworkallocation` WRITE;
/*!40000 ALTER TABLE `gm_dsrworkallocation` DISABLE KEYS */;
INSERT INTO `gm_dsrworkallocation` VALUES (8,'2015-10-12 04:59:15','2015-10-12 04:59:15','Open',1,1,1,'2015-10-12 06:30:00'),(9,'2015-10-12 04:59:48','2015-10-12 04:59:48','Open',1,1,2,'2015-10-12 07:30:00');
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
  CONSTRAINT `previous_assignee_id_refs_id_8d45642a` FOREIGN KEY (`previous_assignee_id`) REFERENCES `gm_servicedeskuser` (`id`),
  CONSTRAINT `assignee_id_refs_id_8d45642a` FOREIGN KEY (`assignee_id`) REFERENCES `gm_servicedeskuser` (`id`),
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
-- Table structure for table `gm_kit`
--

DROP TABLE IF EXISTS `gm_kit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_kit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `part_number` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `kit_applicability` longtext NOT NULL,
  `mrp` varchar(255) NOT NULL,
  `valid_from` varchar(255) NOT NULL,
  `part_models` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_kit`
--

LOCK TABLES `gm_kit` WRITE;
/*!40000 ALTER TABLE `gm_kit` DISABLE KEYS */;
INSERT INTO `gm_kit` VALUES (1,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BH0019 ','CV SHAFT REPAIR KIT or OPTIMA or MAXIMA','','0','0000-00-00 00:00:00','',0),(2,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BH0006','CV SHAFT REAPIR KIT OPTIMA or MAXIMA','','0','0000-00-00 00:00:00','',0),(3,'2015-08-12 00:00:00','2015-08-12 00:00:00','24151171','KIT SHOE BRAKE','','0','0000-00-00 00:00:00','',0),(4,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AN0013','VALVE KIT CNG','','0','0000-00-00 00:00:00','',0),(5,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BA4002','KIT STEERING CONE RE','','0','0000-00-00 00:00:00','',0),(6,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AL0001','KIT SLIDER BLOCK MAC','','0','0000-00-00 00:00:00','',0),(7,'2015-08-12 00:00:00','2015-08-12 00:00:00','36244016','KIT PIVOT PIN WITH B','','0','0000-00-00 00:00:00','',0),(8,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA4016','KIT PLATE FRICTION R','','0','0000-00-00 00:00:00','',0),(9,'2015-08-12 00:00:00','2015-08-12 00:00:00','AB151074','KIT MINOR TANDOM MAS','','0','0000-00-00 00:00:00','',0),(10,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA1003','KIT GASKET RE 4S','','0','0000-00-00 00:00:00','',0),(11,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA4020','KIT CHAIN TENSIONER ','','0','0000-00-00 00:00:00','',0),(12,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AL0003','KIT STEERING CONE GC','','0','0000-00-00 00:00:00','',0),(13,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA4017','KIT PLATE FRICTION R','','0','0000-00-00 00:00:00','',0),(14,'2015-08-12 00:00:00','2015-08-12 00:00:00','24101114','KIT PLATE CLUSTER GE','','0','0000-00-00 00:00:00','',0),(15,'2015-08-12 00:00:00','2015-08-12 00:00:00','36241002','KIT ROLLER BRACKET 3','','0','0000-00-00 00:00:00','',0),(16,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BB0012','KIT RING PISTON STD ','','0','0000-00-00 00:00:00','',0),(17,'2015-08-12 00:00:00','2015-08-12 00:00:00','36241001','KIT DRIVE PLATES RE ','','0','0000-00-00 00:00:00','',0),(18,'2015-08-12 00:00:00','2015-08-12 00:00:00','36224004','KIT BUSH INNER RACE ','','0','0000-00-00 00:00:00','',0),(19,'2015-08-12 00:00:00','2015-08-12 00:00:00','36172201','KIT BEARING FR WHEEL','','0','0000-00-00 00:00:00','',0),(20,'2015-08-12 00:00:00','2015-08-12 00:00:00','36152203','KIT LINER / RIVET 3W','','0','0000-00-00 00:00:00','',0),(21,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AN0010','KIT CYLINDER BLOCK P','','0','0000-00-00 00:00:00','',0),(22,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA4025','KIT FRICTION PLATE K','','0','0000-00-00 00:00:00','',0),(23,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AN0009','KIT CYLINDER BLOCK P','','0','0000-00-00 00:00:00','',0),(24,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AB4001','KIT BUSH PIVOT PIN 3','','0','0000-00-00 00:00:00','',0),(25,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BB0037','KIT_ MAXIMA MATTS','','0','0000-00-00 00:00:00','',0),(26,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AP0002','KIT CG PLATE NEW','','0','0000-00-00 00:00:00','',0),(27,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA4021','KIT CHAIN TENSIONER ','','0','0000-00-00 00:00:00','',0),(28,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AF0019','LOCK CNG FILLING COV','','0','0000-00-00 00:00:00','',0),(29,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA4019','KIT CHAIN TENSIONER ','','0','0000-00-00 00:00:00','',0),(30,'2015-08-12 00:00:00','2015-08-12 00:00:00','36224001','KIT WHEEL RIM 3WH','','0','0000-00-00 00:00:00','',0),(31,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AL0008','KIT BEARING RACE MOD','','0','0000-00-00 00:00:00','',0),(32,'2015-08-12 00:00:00','2015-08-12 00:00:00','36222256','KIT PLATE SPRING NEW','','0','0000-00-00 00:00:00','',0),(33,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AL0002','KIT SHAFT DECOMP GC ','','0','0000-00-00 00:00:00','',0),(34,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA4007','KIT SPRING DAMPER CL','','0','0000-00-00 00:00:00','',0),(35,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AE0001','KIT CLUTCH PLATE KIT','','0','0000-00-00 00:00:00','',0),(36,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BG0005','KIT PLATE FRICTION R','','0','0000-00-00 00:00:00','',0),(37,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AA4022','KIT R VALVE & VALVE ','','0','0000-00-00 00:00:00','',0),(38,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BG0009','KIT SLIDER PROP 600 ','','0','0000-00-00 00:00:00','',0),(39,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AB4007','KIT STG CONE SET FOR','','0','0000-00-00 00:00:00','',0),(40,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AB4005','KIT STG CONE SET RE','','0','0000-00-00 00:00:00','',0),(41,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BH0006','KIT BOOT ALL','','0','0000-00-00 00:00:00','',0),(42,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AL0020','KIT STG CONE SET FOR','','0','0000-00-00 00:00:00','',0),(43,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BH0019','KIT ROLLER','','0','0000-00-00 00:00:00','',0),(44,'2015-08-12 00:00:00','2015-08-12 00:00:00','36BH0011','KIT OBJ & TRIPOD-MEG','','0','0000-00-00 00:00:00','',0),(45,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AL0004','KIT PLATE ISOLATOR ','','0','0000-00-00 00:00:00','',0),(46,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AB4001','KIT BUSH PIVOT 3WH','','268','0000-00-00 00:00:00','24,AA,AC,AF,AM,AP,AS,BA',1),(47,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AB4002','KIT  Brg Race Upper GC-RE','','239','0000-00-00 00:00:00','24,AA,AF,AL,AM,AN,AP,AS,AT,AU,AZ,BA,BB,BG,BH,RA,RC',1),(48,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AB4005','KIT Stg Cone Set RE 2S Petrol / CNG / LP','','465','0000-00-00 00:00:00','24,AA,AF,AM,AP,AS,AZ,BA,BG,BH,RA,RC',1),(49,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AB4006','KIT Stg Cone Set RE Diesel / GC / Mega','','484','0000-00-00 00:00:00','24,AA,AF,AM,AP,AS,AZ,BA,BG,BH,RA,RC',1),(50,'2015-08-12 00:00:00','2015-08-12 00:00:00','36AB4007','KIT Stg Cone Set Fork (Big) RE 145 D / R','','489','0000-00-00 00:00:00','22,23,24,AA,AB,AC,AF,AK,AM,AP,AS,AU,AZ,BA,BG,BH,RA,RC',1);
/*!40000 ALTER TABLE `gm_kit` ENABLE KEYS */;
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
  CONSTRAINT `state_id_refs_id_44480de4` FOREIGN KEY (`state_id`) REFERENCES `gm_state` (`id`),
  CONSTRAINT `preferred_retailer_id_refs_id_531cb0fb` FOREIGN KEY (`preferred_retailer_id`) REFERENCES `gm_retailer` (`id`),
  CONSTRAINT `registered_by_distributor_id_refs_id_7926f143` FOREIGN KEY (`registered_by_distributor_id`) REFERENCES `gm_distributor` (`id`)
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
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_nationalsalesmanager_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_user_id_4fb5e7a8` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_nationalsalesmanager`
--

LOCK TABLES `gm_nationalsalesmanager` WRITE;
/*!40000 ALTER TABLE `gm_nationalsalesmanager` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_nationalsalesmanager_territory`
--

LOCK TABLES `gm_nationalsalesmanager_territory` WRITE;
/*!40000 ALTER TABLE `gm_nationalsalesmanager_territory` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_nationalsparesmanager`
--

LOCK TABLES `gm_nationalsparesmanager` WRITE;
/*!40000 ALTER TABLE `gm_nationalsparesmanager` DISABLE KEYS */;
INSERT INTO `gm_nationalsparesmanager` VALUES (1,'2015-10-07 08:39:24','2015-10-07 08:39:24','NSM002','Raghunath','rkrishnan@bajajauto.co.in',NULL,6),(2,'2015-10-07 08:39:24','2015-10-07 08:39:25','NSM003','Sourav Saha','ssaha@bajajauto.co.in',NULL,7);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_nationalsparesmanager_territory`
--

LOCK TABLES `gm_nationalsparesmanager_territory` WRITE;
/*!40000 ALTER TABLE `gm_nationalsparesmanager_territory` DISABLE KEYS */;
INSERT INTO `gm_nationalsparesmanager_territory` VALUES (1,1,2),(2,2,1);
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
  `order_id` varchar(40) NOT NULL,
  `order_date` date NOT NULL,
  `part_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(5,2) NOT NULL,
  `line_total` decimal(8,2) DEFAULT NULL,
  `fullfill` tinyint(1) DEFAULT NULL,
  `delivered` int(11) DEFAULT NULL,
  `no_fullfill_reason` varchar(300) DEFAULT NULL,
  `dsr_id` int(11) DEFAULT NULL,
  `accept` tinyint(1) NOT NULL,
  `retailer_id` int(11) NOT NULL,
  `distributor_id` int(11) DEFAULT NULL,
  `total_amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_orderpart_8c28136d` (`part_id`),
  KEY `gm_orderpart_9f70fd12` (`dsr_id`),
  KEY `gm_orderpart_64f72e30` (`retailer_id`),
  CONSTRAINT `dsr_id_refs_id_a1b19d5a` FOREIGN KEY (`dsr_id`) REFERENCES `gm_distributorsalesrep` (`id`),
  CONSTRAINT `part_id_refs_id_ecbbd780` FOREIGN KEY (`part_id`) REFERENCES `gm_partmastercv` (`id`),
  CONSTRAINT `retailer_id_refs_id_473cb4b6` FOREIGN KEY (`retailer_id`) REFERENCES `gm_retailer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_orderpart`
--

LOCK TABLES `gm_orderpart` WRITE;
/*!40000 ALTER TABLE `gm_orderpart` DISABLE KEYS */;
INSERT INTO `gm_orderpart` VALUES (99,'2015-10-12 08:19:18','2015-10-12 08:19:18',' 5000011','2015-10-12',43,12,20.00,240.00,NULL,NULL,NULL,1,0,2,1,NULL),(100,'2015-10-12 08:19:18','2015-10-12 08:19:18',' 5000011','2015-10-12',46,12,118.00,1416.00,NULL,NULL,NULL,1,0,2,1,NULL),(101,'2015-10-12 08:20:04','2015-10-12 08:20:04',' 5000012','2015-10-12',3,12,19.50,234.00,NULL,NULL,NULL,1,0,2,1,NULL),(102,'2015-10-12 08:20:04','2015-10-12 08:20:04',' 5000012','2015-10-12',8,12,13.50,162.00,NULL,NULL,NULL,1,0,2,1,NULL),(103,'2015-10-12 08:20:58','2015-10-12 08:20:58',' 6000011','2015-10-12',3,12,19.50,234.00,NULL,NULL,NULL,NULL,0,1,1,NULL),(104,'2015-10-12 08:20:58','2015-10-12 08:20:58',' 6000011','2015-10-12',7,15,695.00,10425.00,NULL,NULL,NULL,NULL,0,1,1,NULL),(105,'2015-10-12 08:21:30','2015-10-12 08:21:30',' 6000012','2015-10-12',2,15,670.00,10050.00,NULL,NULL,NULL,NULL,0,1,1,NULL),(106,'2015-10-12 08:21:30','2015-10-12 08:21:30',' 6000012','2015-10-12',7,10,695.00,6950.00,NULL,NULL,NULL,NULL,0,1,1,NULL),(107,'2015-10-12 09:32:39','2015-10-12 09:32:39',' 5000013','2015-10-12',2,15,670.00,10050.00,NULL,NULL,NULL,1,0,1,1,NULL),(108,'2015-10-12 09:32:40','2015-10-12 09:32:40',' 5000013','2015-10-12',4,15,257.00,3855.00,NULL,NULL,NULL,1,0,1,1,NULL),(109,'2015-10-12 09:36:11','2015-10-12 09:36:11',' 5000014','2015-10-12',2,15,670.00,10050.00,NULL,NULL,NULL,1,0,1,1,NULL),(110,'2015-10-12 09:36:11','2015-10-12 09:36:11',' 5000014','2015-10-12',4,15,257.00,3855.00,NULL,NULL,NULL,1,0,1,1,NULL),(111,'2015-10-12 09:39:43','2015-10-12 09:39:43',' 5000015','2015-10-12',69,12,68.00,816.00,NULL,NULL,NULL,1,0,1,1,NULL);
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
-- Table structure for table `gm_partmastercv`
--

DROP TABLE IF EXISTS `gm_partmastercv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_partmastercv` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `bajaj_id` int(11) NOT NULL,
  `part_number` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `part_model` longtext NOT NULL,
  `valid_from` date NOT NULL,
  `part_models` varchar(255) NOT NULL,
  `category_id` int(11) NOT NULL,
  `mrp` varchar(255) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_partmastercv_6f33f001` (`category_id`),
  CONSTRAINT `category_id_refs_id_67dcf35f` FOREIGN KEY (`category_id`) REFERENCES `gm_cvcategories` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_partmastercv`
--

LOCK TABLES `gm_partmastercv` WRITE;
/*!40000 ALTER TABLE `gm_partmastercv` DISABLE KEYS */;
INSERT INTO `gm_partmastercv` VALUES (1,'2015-09-21 00:00:00','2015-09-21 00:00:00',1,'24121642','ASSEMBLY AIR FILTER-SAI TYPE','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-02-18','24',1,'541',1),(2,'2015-09-21 00:00:00','2015-09-21 00:00:00',2,'24121659','ASSEMBLY AIR FILTER-SAI TYPE','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-01-01','24,AP,AS',1,'670',1),(3,'2015-09-21 00:00:00','2015-09-21 00:00:00',3,'24141120','FILTER ASSY. - 2T OIL FOR RE2S CNG/LPG','ASSEMBLY 3WRE 2SUG LPG EL START-NO COLOR','2005-07-01','24,AG,AS',1,'19.5',1),(4,'2015-09-21 00:00:00','2015-09-21 00:00:00',4,'AA121056','ELEMENT AIR FILTER','3W RE/AR WITH 4 STROKE PETROL ENGINE+ANT','2004-10-01','AF,AM,AA',1,'257',1),(5,'2015-09-21 00:00:00','2015-09-21 00:00:00',5,'AA121126','ASSEMBLY AIR FILTER','ASSEMBLY 3WRE 2SUG CNG EL START-NO COLOR','2010-07-31','24,AA,AF,AM',1,'602',1),(6,'2015-09-21 00:00:00','2015-09-21 00:00:00',6,'AA121150','ELEMENT AIR FILTER','ASSEMNLY 3W 4S','0000-00-00','24,AA,AF,AG',1,'297',1),(7,'2015-09-21 00:00:00','2015-09-21 00:00:00',7,'AA121151','ASSEMBLY AIR FILTER','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2012-11-17','AA,AZ',1,'695',1),(8,'2015-09-21 00:00:00','2015-09-21 00:00:00',8,'AF121393','FILTER AIR CARBURETTOR','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2007-09-01','AA,RC',1,'13.5',1),(9,'2015-09-21 00:00:00','2015-09-21 00:00:00',9,'AF121505','ASSEMBLY AIR FILTER','RE COMPACT PETROL','2013-07-06','AF,AM,AZ,RA',1,'713',1),(10,'2015-09-21 00:00:00','2015-09-21 00:00:00',10,'AL121060','FILTER AIR ASSEMBLY','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2006-03-01','24',1,'597',1),(11,'2015-09-21 00:00:00','2015-09-21 00:00:00',11,'AL121062','ELEMENT AIR FILTER','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2009-03-14','AA,AB,BG,BH,RC',1,'307',1),(12,'2015-09-21 00:00:00','2015-09-21 00:00:00',12,'AP121132','ELEMENT AIR FILTER (TWIN)','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-01-04','24,AP',1,'84',1),(13,'2015-09-21 00:00:00','2015-09-21 00:00:00',13,'AP231046','FOAM AIR FILTER','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-01-01','24,AG,AS',1,'44',1),(14,'2015-09-21 00:00:00','2015-09-21 00:00:00',14,'BA122192','ELEMENT ASSEMBLY','ASSEMBLY 3W GDI','2015-01-30','AL,AN,AT,BA,BB',1,'250',1),(15,'2015-09-21 00:00:00','2015-09-21 00:00:00',15,'BB201024','FILTER AIR CHOKE CONTROL UNIT','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2007-06-01','24',1,'304.5',1),(16,'2015-09-21 00:00:00','2015-09-21 00:00:00',16,'RC581007','ASSEMBLY AIR FILTER','RE COMPACT CNG 4S-NO COLOR','2013-10-09','AF',1,'706',1),(17,'2015-09-21 00:00:00','2015-09-21 00:00:00',17,'AA121006','ELEMENT COMPLETE - OIL FILTER','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AB,AC,AF,AM,AN,AT',2,'29',1),(18,'2015-09-21 00:00:00','2015-09-21 00:00:00',18,'AN101190','FILTER ASSEMBLY - OIL','RE COMPACT PETROL 4S','2012-04-15','AA,AF,AM',2,'159',1),(19,'2015-09-21 00:00:00','2015-09-21 00:00:00',19,'AP121067','OIL FILTER','RE COMPACT PETROL','2007-09-01','24,AG,AP,AS',2,'27.5',1),(20,'2015-09-21 00:00:00','2015-09-21 00:00:00',20,'BA102079','FILTER (OIL)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AA,AB,AC,AN,AF,AT',2,'140',1),(21,'2015-09-21 00:00:00','2015-09-21 00:00:00',21,'BA102113','CARTRIDGE FILTER OIL','RE DIESEL','2015-01-30','MEGA MAX,',2,'216',1),(22,'2015-09-21 00:00:00','2015-09-21 00:00:00',22,'BA122209','ASSEMBLY OIL FILTER','ASSLY RE 900 WITH DOOR HI-DECK','2009-03-14','AL,BA,BB,BG,BH',2,'581',1),(23,'2015-09-21 00:00:00','2015-09-21 00:00:00',23,'24121652','FUEL FILTER','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2008-04-01','24,AA,AF,AG,AM,AN,AS',3,'20.5',1),(24,'2015-09-21 00:00:00','2015-09-21 00:00:00',24,'24141109','FILTER : FUEL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2006-08-01','24,AA,AF,AG',3,'20.5',1),(25,'2015-09-21 00:00:00','2015-09-21 00:00:00',25,'AF121133','FILTER COMPLETE - FUEL FOR 3WH-RE-4S-CNG','RE COMPACT CNG 4S-NO COLOR','2008-01-01','AF,AG,AM,AN,AS',3,'12.5',1),(26,'2015-09-21 00:00:00','2015-09-21 00:00:00',26,'BB121043','FILTER FUEL- 0.5 L','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2004-10-01','24,AA,AF,AG,AM,AS,BA',3,'757',1),(27,'2015-09-21 00:00:00','2015-09-21 00:00:00',27,'22171007','SEAL - OIL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','22,24,AA,BB,AC,AF',4,'14.5',1),(28,'2015-09-21 00:00:00','2015-09-21 00:00:00',28,'24100314','SEAL - OIL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AS',4,'12',1),(29,'2015-09-21 00:00:00','2015-09-21 00:00:00',29,'24131004','SEAL - OIL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AS',4,'20.5',1),(30,'2015-09-21 00:00:00','2015-09-21 00:00:00',30,'24131075','SEAL - OIL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-01-04','24,RC',4,'39',1),(31,'2015-09-21 00:00:00','2015-09-21 00:00:00',31,'24171024','SEAL - OIL :- 48 DIA.','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AA,AF,AG,BA,BG,BH',4,'19.5',1),(32,'2015-09-21 00:00:00','2015-09-21 00:00:00',32,'36102401','KIT OIL SEAL RE 2S','ASSEMBLY 3W','0000-00-00','24',4,'92',1),(33,'2015-09-21 00:00:00','2015-09-21 00:00:00',33,'36241010','KIT OIL SEAL MOD. RE','ASSMBL 3W','0000-00-00','24,AG',4,'87',1),(34,'2015-09-21 00:00:00','2015-09-21 00:00:00',34,'39103519','SEAL OIL','3W MEGA MAX','0000-00-00','',4,'27.5',1),(35,'2015-09-21 00:00:00','2015-09-21 00:00:00',35,'39149819','SEAL - OIL','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB',4,'8.2',1),(36,'2015-09-21 00:00:00','2015-09-21 00:00:00',36,'39149919','SEAL - OIL','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2003-06-16','AL,BA,BB,BG',4,'31',1),(37,'2015-09-21 00:00:00','2015-09-21 00:00:00',37,'39153519','SEAL - OIL :- 20 X 35 X 7','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AA,AF,AN,AT',4,'14',1),(38,'2015-09-21 00:00:00','2015-09-21 00:00:00',38,'39171519','SEAL - OIL','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2002-04-01','AA,AB,AC,AF',4,'11',1),(39,'2015-09-21 00:00:00','2015-09-21 00:00:00',39,'39171619','SEAL - OIL','3W4S RE A/R AD EXP WITH CAT SRILANKA','2002-04-01','AA,AB,AC,AK,AT,AU,RA,RC',4,'11.5',1),(40,'2015-09-21 00:00:00','2015-09-21 00:00:00',40,'39173719','SEAL OIL 26 X 42 X 8','RE 4S 600','0000-00-00','',4,'17.5',1),(41,'2015-09-21 00:00:00','2015-09-21 00:00:00',41,'39174419','SEAL - OIL','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2002-04-01','AA,AB,AC,AK,AT,AU,RA,RC',4,'9',1),(42,'2015-09-21 00:00:00','2015-09-21 00:00:00',42,'39187019','SEAL - OIL :- 33 X 50 X 6.5','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2002-04-01','AA,AF,AM',4,'32',1),(43,'2015-09-21 00:00:00','2015-09-21 00:00:00',43,'39191719','SEAL - OIL','3W4S RE A/R AD EXP WITH CAT SRILANKA','2002-04-01','AA,AF,AN,AZ',4,'20',1),(44,'2015-09-21 00:00:00','2015-09-21 00:00:00',44,'39201719','SEAL OIL','3W ASSEMBLY','0000-00-00','AA,AF,AZ',4,'28.5',1),(45,'2015-09-21 00:00:00','2015-09-21 00:00:00',45,'59190002','SEAL OIL DIA. 50X10','BAJA RE DIESEL,RE MAX 400 LPG','0000-00-00','BA,BB,BG,BH',4,'25',1),(46,'2015-09-21 00:00:00','2015-09-21 00:00:00',46,'36AA1004','KIT OILSEAL RE 4S','ASSEMBLY 4S 3WH','0000-00-00','AA,AB,AN,AM,AT',4,'118',1),(47,'2015-09-21 00:00:00','2015-09-21 00:00:00',47,'AL171019','SEAL - OIL FOR TRAILING ARM (DIA. 52)','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2003-06-16','AL,AN,AT',4,'16.5',1),(48,'2015-09-21 00:00:00','2015-09-21 00:00:00',48,'AP101049','OIL SEAL CLUTCH SIDE','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2006-05-01','24,AG,AP',4,'59',1),(49,'2015-09-21 00:00:00','2015-09-21 00:00:00',49,'AP101074','SEAL OIL 22X47X7','RE COMPACT PETROL','2006-05-01','24,AG,AP,AT',4,'30',1),(50,'2015-09-21 00:00:00','2015-09-21 00:00:00',50,'AP101226','OIL SEAL CLUTCH SIDE','RE COMPACT PETROL','2006-05-01','24,AG,AP,AS',4,'34',1),(51,'2015-09-21 00:00:00','2015-09-21 00:00:00',51,'AP101268','OIL SEAL MAG SIDE','RE COMPACT PETROL','2008-04-01','24,A,AF,AG,AM,AN,AP',4,'11',1),(52,'2015-09-21 00:00:00','2015-09-21 00:00:00',52,'BA132257','OIL SEAL- 50X10','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2008-04-01','AL,BA,BB,BG,BH',4,'34',1),(53,'2015-09-21 00:00:00','2015-09-21 00:00:00',53,'BB121083','SEAL OIL -SHAFT GOVERNOR','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2010-03-01','AL,AB,BB,BG',4,'10',1),(54,'2015-09-21 00:00:00','2015-09-21 00:00:00',54,'BF551613','SEAL OIL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2008-04-01','RA,BH,BB,BA,AZ,AS,AM,AG,AF,AA,24',4,'42',1),(55,'2015-09-21 00:00:00','2015-09-21 00:00:00',55,'24121721','BELLOW - ACC. CABLE','RE COMPACT PETROL','2013-11-30','AA,AF,AM',5,'17',1),(56,'2015-09-21 00:00:00','2015-09-21 00:00:00',56,'24131074','BELLOW -PROPELLER SHAFT','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2010-02-18','24,AA',5,'121',1),(57,'2015-09-21 00:00:00','2015-09-21 00:00:00',57,'AA101484','BELLOW','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AB,AC,AF,AK,AM,AN,AT,RA,RC',5,'15.5',1),(58,'2015-09-21 00:00:00','2015-09-21 00:00:00',58,'AA131024','BELLOW - DIFFERENTIAL FLANGE','3W4S RE A/R AD EXP WITH CAT ','2008-04-01','AA,AF,AN',5,'44',1),(59,'2015-09-21 00:00:00','2015-09-21 00:00:00',59,'AF121328','BELLOW FOR ACCELERATOR CABLE','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2007-10-01','24,AG,AN,AP,AS',5,'14.5',1),(60,'2015-09-21 00:00:00','2015-09-21 00:00:00',60,'1100342','BEARING - BALL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AA,AF,AG,AM,AS,BA,BG,RA,BH',6,'108.5',1),(61,'2015-09-21 00:00:00','2015-09-21 00:00:00',61,'3100338','BEARING WITH STEEL CAGE :- CRANKSHAFT','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AP,AS',6,'124',1),(62,'2015-09-21 00:00:00','2015-09-21 00:00:00',62,'5101018','BEARING - NEEDLE ROLLER','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AS',6,'159',1),(63,'2015-09-21 00:00:00','2015-09-21 00:00:00',63,'6101009','BEARING BALL','ASSEMBLY 3W RE','2002-04-01','22,24,AG,AS',6,'82',1),(64,'2015-09-21 00:00:00','2015-09-21 00:00:00',64,'15101011','BEARING BALL','ASSEMBLY 3W RE','2002-04-01','22,24,AA,BB',6,'105',1),(65,'2015-09-21 00:00:00','2015-09-21 00:00:00',65,'21130110','BEARING - BALL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','22,24,AG,AS',6,'112',1),(66,'2015-09-21 00:00:00','2015-09-21 00:00:00',66,'24100308','BEARING - BALL FOR MAINSHAFT','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AG,AS,',6,'108',1),(67,'2015-09-21 00:00:00','2015-09-21 00:00:00',67,'24130105','BEARING - BALL','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2002-04-01','24,AA,AB,AC,AF,AG,AM,AN,AP,AS,AT,BA,BG,BH,RA',6,'137',1),(68,'2015-09-21 00:00:00','2015-09-21 00:00:00',68,'24181046','RACE UPPER BEARING','ASSEMBLY 3WRE2S UG NON-ES-NO COLOR','2009-03-14','24,AA,AF,AG,AL,AM,AN,AP,AS,AT,AU,AZ,BA,RC',6,'76',1),(69,'2015-09-21 00:00:00','2015-09-21 00:00:00',69,'30151065','BEARING BALL','ASSEMBLY 3W RE','2002-04-01','AL,BA,BB,BG',6,'68',1),(70,'2015-09-21 00:00:00','2015-09-21 00:00:00',70,'39100120','BEARING BALL','ASSEMBLY 3W RE','2002-04-01','24,AG,AS',6,'79',1),(71,'2015-09-21 00:00:00','2015-09-21 00:00:00',71,'39121420','BEARING BALL 20X42X1','ASSEMBLY 3W RE','2002-04-01','22,24,AA,BB,BG',6,'83',1),(72,'2015-09-21 00:00:00','2015-09-21 00:00:00',72,'39132420','BEARING - BALL :- 25 X 62 X 17','ASSEMBLY 3WRE4S UG, 200CC ENGIN-NO COLOR','2002-04-01','AA,AB,AC,AF,AM,AN,AT,BA,BG,BH,RC',6,'209',1),(73,'2015-09-21 00:00:00','2015-09-21 00:00:00',73,'39143520','BEARING - NEEDLE ROLLER','3W4S RE A/R AD EXP WITH CAT ','2002-04-01','AA,AB,AC,AF,AM,AN,AT,BA,BB,BG,RA,RB,RC',6,'41',1),(74,'2015-09-21 00:00:00','2015-09-21 00:00:00',74,'39143620','BEARING - NEEDLE ROLLER','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BA,BB,BG,BH',6,'40',1),(75,'2015-09-21 00:00:00','2015-09-21 00:00:00',75,'39148720','BEARING - BALL :- 30 X 55 X 9','ASSEMBLY 3WREGC/DOOR,WIDER TRAY-NO COLOR','2002-04-01','AL,BB,BH,BA',6,'160',1);
/*!40000 ALTER TABLE `gm_partmastercv` ENABLE KEYS */;
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_partmodels`
--

LOCK TABLES `gm_partmodels` WRITE;
/*!40000 ALTER TABLE `gm_partmodels` DISABLE KEYS */;
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_partpricing`
--

LOCK TABLES `gm_partpricing` WRITE;
/*!40000 ALTER TABLE `gm_partpricing` DISABLE KEYS */;
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
  CONSTRAINT `product_type_id_refs_id_25086b41` FOREIGN KEY (`product_type_id`) REFERENCES `gm_producttype` (`id`),
  CONSTRAINT `dealer_id_id_refs_user_id_21ad52d3` FOREIGN KEY (`dealer_id_id`) REFERENCES `gm_dealer` (`user_id`)
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_producttype`
--

LOCK TABLES `gm_producttype` WRITE;
/*!40000 ALTER TABLE `gm_producttype` DISABLE KEYS */;
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
  CONSTRAINT `partner_id_refs_id_ddca6ab4` FOREIGN KEY (`partner_id`) REFERENCES `gm_partner` (`id`),
  CONSTRAINT `member_id_refs_id_2df21631` FOREIGN KEY (`member_id`) REFERENCES `gm_member` (`id`),
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
  CONSTRAINT `user_id_refs_user_id_98e4870b` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `circle_head_id_refs_id_e1123413` FOREIGN KEY (`circle_head_id`) REFERENCES `gm_circlehead` (`id`)
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
  `retailer_code` varchar(50) NOT NULL,
  `retailer_name` varchar(50) NOT NULL,
  `retailer_town` varchar(50) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `billing_code` varchar(15) NOT NULL,
  `distributor_id` int(11) NOT NULL,
  `approved` smallint(5) unsigned NOT NULL,
  `territory` varchar(15) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `mobile` varchar(15) NOT NULL,
  `profile` varchar(15) DEFAULT NULL,
  `latitude` decimal(10,6) DEFAULT NULL,
  `longitude` decimal(11,6) DEFAULT NULL,
  `language` varchar(10) DEFAULT NULL,
  `rejected_reason` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_retailer_6340c63c` (`user_id`),
  KEY `gm_retailer_818f5865` (`distributor_id`),
  CONSTRAINT `distributor_id_refs_id_35c45a77` FOREIGN KEY (`distributor_id`) REFERENCES `gm_distributor` (`id`),
  CONSTRAINT `user_id_refs_user_id_de75d784` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_retailer`
--

LOCK TABLES `gm_retailer` WRITE;
/*!40000 ALTER TABLE `gm_retailer` DISABLE KEYS */;
INSERT INTO `gm_retailer` VALUES (1,'2015-10-08 04:48:46','2015-10-08 04:48:46','600001','Mahaveer Auto','bangalore',1,11,'MAHA',1,2,'south','mahaveer@bajajauto.in','9880154420','Retailer',12.958411,77.577634,'kannada',NULL),(2,'2015-10-09 08:29:47','2015-10-09 08:29:47','600002','Shreyas Automobiles','bangalore',1,13,'SHREYA',1,2,'south','shreyas@bajajauto.in','9591106103','Retailer',13.009765,77.525396,'kannada',NULL);
/*!40000 ALTER TABLE `gm_retailer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gm_retailercollection`
--

DROP TABLE IF EXISTS `gm_retailercollection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `gm_retailercollection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_date` datetime NOT NULL,
  `modified_date` datetime NOT NULL,
  `retailer_id` int(11) NOT NULL,
  `dsr_id` int(11) NOT NULL,
  `order_amount` varchar(20) NOT NULL,
  `collected_amount` varchar(20) NOT NULL,
  `outstanding_amount` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_retailercollection_64f72e30` (`retailer_id`),
  KEY `gm_retailercollection_9f70fd12` (`dsr_id`),
  CONSTRAINT `retailer_id_refs_id_003a542b` FOREIGN KEY (`retailer_id`) REFERENCES `gm_retailer` (`id`),
  CONSTRAINT `dsr_id_refs_id_b8e6506e` FOREIGN KEY (`dsr_id`) REFERENCES `gm_distributorsalesrep` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_retailercollection`
--

LOCK TABLES `gm_retailercollection` WRITE;
/*!40000 ALTER TABLE `gm_retailercollection` DISABLE KEYS */;
/*!40000 ALTER TABLE `gm_retailercollection` ENABLE KEYS */;
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
  CONSTRAINT `user_id_refs_user_id_265434d4` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `asc_id_refs_user_id_7d52fad5` FOREIGN KEY (`asc_id`) REFERENCES `gm_authorizedservicecenter` (`user_id`),
  CONSTRAINT `dealer_id_refs_user_id_b6a97602` FOREIGN KEY (`dealer_id`) REFERENCES `gm_dealer` (`user_id`)
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
  CONSTRAINT `servicecircular_id_refs_id_44e83a32` FOREIGN KEY (`servicecircular_id`) REFERENCES `gm_servicecircular` (`id`),
  CONSTRAINT `brandproductrange_id_refs_id_e4279033` FOREIGN KEY (`brandproductrange_id`) REFERENCES `gm_brandproductrange` (`id`)
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
  `sub_department_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `gm_servicedeskuser_82936d91` (`user_profile_id`),
  KEY `gm_servicedeskuser_d81e6292` (`sub_department_id`),
  CONSTRAINT `user_profile_id_refs_user_id_efdb6067` FOREIGN KEY (`user_profile_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `sub_department_id_refs_id_a92b4d31` FOREIGN KEY (`sub_department_id`) REFERENCES `gm_departmentsubcategories` (`id`)
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_sparepartmasterdata`
--

LOCK TABLES `gm_sparepartmasterdata` WRITE;
/*!40000 ALTER TABLE `gm_sparepartmasterdata` DISABLE KEYS */;
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
  UNIQUE KEY `part_number_id` (`part_number_id`,`territory`),
  KEY `gm_sparepartpoint_b1e99e52` (`part_number_id`),
  CONSTRAINT `part_number_id_refs_id_69f218e8` FOREIGN KEY (`part_number_id`) REFERENCES `gm_sparepartmasterdata` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_sparepartpoint`
--

LOCK TABLES `gm_sparepartpoint` WRITE;
/*!40000 ALTER TABLE `gm_sparepartpoint` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_state`
--

LOCK TABLES `gm_state` WRITE;
/*!40000 ALTER TABLE `gm_state` DISABLE KEYS */;
INSERT INTO `gm_state` VALUES (1,'2015-10-08 00:00:00','2015-10-08 00:00:00','karnataka','krn',2);
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_subcategories`
--

LOCK TABLES `gm_subcategories` WRITE;
/*!40000 ALTER TABLE `gm_subcategories` DISABLE KEYS */;
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
  CONSTRAINT `user_id_refs_user_id_905df947` FOREIGN KEY (`user_id`) REFERENCES `gm_userprofile` (`user_id`),
  CONSTRAINT `transporter_id_refs_id_75ea9d80` FOREIGN KEY (`transporter_id`) REFERENCES `gm_transporter` (`id`)
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gm_territory`
--

LOCK TABLES `gm_territory` WRITE;
/*!40000 ALTER TABLE `gm_territory` DISABLE KEYS */;
INSERT INTO `gm_territory` VALUES (1,'2015-10-07 08:39:22','2015-10-07 08:39:22','North'),(2,'2015-10-07 08:39:22','2015-10-07 08:39:22','South'),(3,'2015-10-07 08:39:22','2015-10-07 08:39:22','East'),(4,'2015-10-07 08:39:22','2015-10-07 08:39:22','West');
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
INSERT INTO `gm_userprofile` VALUES ('2015-10-10 08:55:02','2015-10-10 08:55:02',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,'',0,NULL,NULL,2),('2015-10-10 08:55:02','2015-10-10 08:55:02',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,'',0,NULL,NULL,3),('2015-10-10 08:55:02','2015-10-10 08:55:02',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,'',0,NULL,NULL,4),('2015-10-10 08:55:02','2015-10-10 08:55:02',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,'',0,NULL,NULL,5),('2015-10-10 08:55:02','2015-10-10 08:55:02',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,'',0,NULL,NULL,6),('2015-10-10 08:55:02','2015-10-10 08:55:02',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,'',0,NULL,NULL,7),('2015-10-10 08:55:02','2015-10-10 08:55:02',NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,0,NULL,'',0,NULL,NULL,8),('2015-10-07 23:39:58','2015-10-07 23:39:58','080 - 78654323','','#213, Johnson street,\r\nBangalore','karnataka','India','560078',NULL,0,0,'','',0,NULL,'M',9),('2015-10-08 04:05:14','2015-10-09 09:26:44','044 - 24765898','','WIN AUTO, 5, THIRD STREET,  GILL NAGAR, CHOOLAIMEDU, CHENNAI','Tamil Nadu','India','600032',NULL,0,0,'','image/win.jpg',0,NULL,'M',10),('2015-10-08 04:38:32','2015-10-12 05:21:53','080 - 40960450','','#215, Hongasandra, Bommanahalli, Bangalore','karnataka','India','560068',NULL,0,0,'','image/mahaveer.png',0,NULL,'M',11),('2015-10-08 05:09:45','2015-10-08 05:09:45','080 - 77777756','','#213, Fifth street, Rajeswari Nagar,\r\nBangalore','karnataka','India','560090',NULL,0,0,'','',0,NULL,'M',12),('2015-10-09 08:27:24','2015-10-09 08:27:24','','','#42, Johnson Market,\r\nBangalore','karnataka','India','560068',NULL,0,0,'','',0,NULL,'M',13);
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
  CONSTRAINT `partner_id_refs_id_f635793b` FOREIGN KEY (`partner_id`) REFERENCES `gm_partner` (`id`),
  CONSTRAINT `member_id_refs_id_e5808864` FOREIGN KEY (`member_id`) REFERENCES `gm_member` (`id`)
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
  KEY `gm_zonalservicemanager_6340c63c` (`user_id`),
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
  CONSTRAINT `user_id_refs_id_71306ac9` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `client_id_refs_id_dffc817d` FOREIGN KEY (`client_id`) REFERENCES `oauth2_client` (`id`)
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
  CONSTRAINT `user_id_refs_id_8a95efb3` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `client_id_refs_id_098c2f19` FOREIGN KEY (`client_id`) REFERENCES `oauth2_client` (`id`)
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
  CONSTRAINT `user_id_refs_id_e0af9726` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `access_token_id_refs_id_b5577697` FOREIGN KEY (`access_token_id`) REFERENCES `oauth2_accesstoken` (`id`),
  CONSTRAINT `client_id_refs_id_3730d4ce` FOREIGN KEY (`client_id`) REFERENCES `oauth2_client` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth2_refreshtoken`
--

LOCK TABLES `oauth2_refreshtoken` WRITE;
/*!40000 ALTER TABLE `oauth2_refreshtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth2_refreshtoken` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-10-13 10:03:54
