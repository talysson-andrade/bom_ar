


DROP TABLE IF EXISTS `Ambiente`;

CREATE TABLE `Ambiente` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) COLLATE utf8mb3_bin NOT NULL,
  `temperatura_desejada` decimal(3,1) NOT NULL,
  `cidade` varchar(45) COLLATE utf8mb3_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `nome_UNIQUE` (`nome`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;
--

LOCK TABLES `Ambiente` WRITE;
INSERT INTO `Ambiente` VALUES (1,'Sala de Estar',23.0,'Rio de Janeiro'),(2,'Quarto',21.5,'Rio de Janeiro'),(3,'Cozinha',23.0,'Rio de Janeiro');
UNLOCK TABLES;

--
-- Table structure for table `Ar_condicionado`
--

DROP TABLE IF EXISTS `Ar_condicionado`;
CREATE TABLE `Ar_condicionado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) COLLATE utf8mb3_bin NOT NULL,
  `marca` varchar(45) COLLATE utf8mb3_bin NOT NULL,
  `capacidade` int NOT NULL,
  `ambiente_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `ambiente_id_idx` (`ambiente_id`),
  CONSTRAINT `ambiente_id` FOREIGN KEY (`ambiente_id`) REFERENCES `Ambiente` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_bin;

--
-- Dumping data for table `Ar_condicionado`
--

LOCK TABLES `Ar_condicionado` WRITE;
/*!40000 ALTER TABLE `Ar_condicionado` DISABLE KEYS */;
INSERT INTO `Ar_condicionado` VALUES (1,'Ar Sala 1','Daikin',9000,1),(2,'Ar Sala 2','Daikin',9000,1),(3,'Ar cozinha','Daikin',9000,3),(4,'Ar Quarto','Samsung',7500,2);
/*!40000 ALTER TABLE `Ar_condicionado` ENABLE KEYS */;
UNLOCK TABLES;
ambiente