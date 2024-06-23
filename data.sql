-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.27-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table helmet_detection.detection_result
CREATE TABLE IF NOT EXISTS `detection_result` (
  `id_data` int(11) NOT NULL AUTO_INCREMENT,
  `uploaded_image_path` text DEFAULT NULL,
  `helmet_count` int(11) DEFAULT NULL,
  `no_helmet_count` int(11) DEFAULT NULL,
  `detected_image_path` text DEFAULT NULL,
  `date_detection` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id_data`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table helmet_detection.detection_result: ~3 rows (approximately)
INSERT INTO `detection_result` (`id_data`, `uploaded_image_path`, `helmet_count`, `no_helmet_count`, `detected_image_path`, `date_detection`) VALUES
	(1, 'static/uploads\\upload_20231221_213445_0.jpg', 1, 0, 'static/result\\result_20231221_213445_0.jpg', '2023-12-21 21:34:51'),
	(2, 'static/uploads/upload_20231221_213632_0.jpg', 1, 0, 'static/result\\result_20231221_213632_0.jpg', '2023-12-21 21:36:37'),
	(3, 'static/uploads/upload_20231221_213816_0.jpg', 1, 0, 'static/result/result_20231221_213816_0.jpg', '2023-12-21 21:38:21'),
	(4, 'static/uploads/upload_20231221_213904_0.jpg', 4, 3, 'static/result/result_20231221_213904_0.jpg', '2023-12-21 21:39:11');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
