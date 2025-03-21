-- Group: 20
-- Members: Yasser Hernandez, Anish Ramanadham
-- Citation for all code below.
-- Date: 02/19/2025
-- Created as per instructions provided in the class
-- Note: DDL is modified to work as an import in PHPMyAdmin and as a source import in MariaDB

-- Disable commits and foreign key checks
SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- Table creation

-- Users Table
CREATE TABLE IF NOT EXISTS `Users`(
  `userId` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `firstName` varchar(255) DEFAULT 'None',
  `lastName` varchar(255) DEFAULT 'None',
  `userBio` varchar(255) DEFAULT 'None',
  PRIMARY KEY (`userId`),
  CONSTRAINT `username_UNIQUE` UNIQUE (`username`)
);

-- Artists Table
CREATE TABLE IF NOT EXISTS `Artists`(
  `artistId` int NOT NULL AUTO_INCREMENT,
  `artistName` varchar(255) NOT NULL,
  `artistBio` text,
  PRIMARY KEY (`artistId`),
  CONSTRAINT `artistName_UNIQUE` UNIQUE (`artistName`)
);

-- Playlists Table
CREATE TABLE IF NOT EXISTS `Playlists`(
  `playlistId` int NOT NULL AUTO_INCREMENT,
  `playlistTitle` varchar(255) NOT NULL DEFAULT 'Untitled',
  `userId` int DEFAULT NULL,
  PRIMARY KEY (`playlistId`),
  CONSTRAINT `fk_userId` FOREIGN KEY (`userId`) REFERENCES `Users` (`userId`) ON DELETE SET NULL
);

-- Songs Table
CREATE TABLE IF NOT EXISTS `Songs`(
  `songId` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `duration` time NOT NULL,
  `releaseDate` date NOT NULL,
  PRIMARY KEY (songId),
  CONSTRAINT `title_UNIQUE` UNIQUE (`title`)
);

-- PlaylistSongs Intersection table of Playlists and Songs
CREATE TABLE IF NOT EXISTS `PlaylistSongs`(
  `playlistSongsId` int NOT NULL AUTO_INCREMENT,
  `playlistId` int NOT NULL,
  `songId` int DEFAULT NULL,
  PRIMARY KEY (`playlistSongsId`),
  CONSTRAINT `fk_PlaylistSongs_Playlists` FOREIGN KEY (`playlistId`) REFERENCES `Playlists`(`playlistId`) ON DELETE CASCADE,
  CONSTRAINT `fk_PlaylistSongs_Songs` FOREIGN KEY (`songId`) REFERENCES `Songs`(`songId`) ON DELETE CASCADE
);

-- ArtistSongs Intersection table of Artists and Songs
CREATE TABLE IF NOT EXISTS  `ArtistSongs`(
  `artistSongsId` int NOT NULL AUTO_INCREMENT,
  `artistId` int NOT NULL,
  `songId` int NOT NULL,
  PRIMARY KEY (`artistSongsId`),
  CONSTRAINT `ArtistSong_Mapping` UNIQUE (`artistId`, `songId`),
  CONSTRAINT `fk_ArtistSongs_Artists` FOREIGN KEY (`artistId`) REFERENCES `Artists`(`artistId`) ON DELETE CASCADE,
  CONSTRAINT `fk_ArtistSongs_Songs` FOREIGN KEY (`songId`) REFERENCES `Songs`(`songId`) ON DELETE CASCADE
);

-- Insert Data
INSERT INTO `Users` (`username`, `firstName`, `lastName`, `userBio`) VALUES
("yasserD", "Yasser", "Hernandez", "Music enthusiast"),
("Anish22", "Anish", "Ramanadham", "Music connoisseur"),
("Qjones", "Quincy", "Jones", "Music Producer"),
("BR", "Bob", "Ross", DEFAULT);

INSERT INTO `Artists`(`artistName`, `artistBio`) VALUES
("Breaking Benjamin", "American Rock Band"),
("Mago de Oz", "Spanish folk metal band"),
("Johnny Cash", "American country singer"),
("Mumford & Sons", "British folk rock band");

INSERT INTO `Songs`(`title`, `duration`, `releaseDate`) VALUES
("Satania", "00:08:13", "2000-05-14"),
("I Will Not Bow", "00:03:36", "2009-09-29"),
("Hopeless Wanderer", "00:05:07", "2013-08-04"),
("Ain't No Grave", "00:02:53", "2010-02-23");

INSERT INTO `Playlists`(`playlistTitle`,`userId`) VALUES
("American Music", "2"),
("European Music", "1"),
("All Music", "3"),
(DEFAULT, "4"),
("MM Default", DEFAULT);

INSERT INTO `PlaylistSongs`(`playlistId`,`songId`) VALUES
("1","2"),
("1","4"),
("2","1"),
("2","3"),
("3","1"),
("3","2"),
("3","3"),
("3","4"),
("4","1"),
("4","2"),
("4","2"),
("5", DEFAULT);

INSERT INTO `ArtistSongs`(`artistId`,`songId`) VALUES
("1","2"),
("2","1"),
("3","4"),
("4","3");

-- Re-enable FK checks and commits
SET FOREIGN_KEY_CHECKS = 1;
COMMIT;