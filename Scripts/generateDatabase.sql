
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Listage de la structure de la base pour BetterMusic
CREATE DATABASE IF NOT EXISTS `BetterMusic` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `BetterMusic`;

-- Listage de la structure de la table BetterMusic. playlist
CREATE TABLE IF NOT EXISTS `playlist` (
  `user` varchar(32) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `title` varchar(512) DEFAULT NULL,
  `link` varchar(128) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table BetterMusic. queue
CREATE TABLE IF NOT EXISTS `queue` (
  `server` varchar(32) NOT NULL,
  `isPlaying` tinyint(4) DEFAULT NULL,
  `requester` varchar(50) DEFAULT NULL,
  `textChannel` varchar(50) DEFAULT NULL,
  `track` varchar(128) DEFAULT NULL,
  `title` varchar(512) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `index` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table BetterMusic. server
CREATE TABLE IF NOT EXISTS `server` (
  `server` varchar(32) NOT NULL,
  `prefix` varchar(10) DEFAULT NULL,
  `loop` tinyint(4) DEFAULT NULL,
  `loopQueue` tinyint(4) DEFAULT NULL,
  `djRole` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table BetterMusic. skip
CREATE TABLE IF NOT EXISTS `skip` (
  `server` varchar(50) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Les données exportées n'étaient pas sélectionnées.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
