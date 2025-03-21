-- All queries use : to denote variables gathered through the UI

------------ Users -----------

-- Read 
SELECT userId, username, firstName, lastName, userBio
FROM Users;

-- Create
INSERT INTO Users(username, firstName, lastName, userBio)
VALUES(:usernameInput, :firstNameInput, :lastNameInput, :userBioInput);

-- Update
UPDATE Users 
SET username = :usernameInput, firstName = :firstNameInput, lastName = :lastNameInput, userBio = :userBioInput
WHERE userId = :userId;

-- Delete
DELETE FROM Users
WHERE userId = :userId;

-------------- Playlists ---------
-- Read
SELECT playlistId, playlistTitle, Users.username
FROM Playlists
INNER JOIN Users ON Playlists.playlistId = Users.userId;

-- Create with drop down selection of username
INSERT INTO Playlists(playlistTitle, userId)
VALUES(:playlistTitleInput,
    (SELECT userId FROM Users where username = :usernameDropDown)
);

-- :usernameDropDown
SELECT username FROM Users;

-- Update
UPDATE Playlists
SET playlistTitle = :playlistTitleInput
WHERE playlistId = :playlistIdInput
AND (userId = (SELECT userId FROM Users where username = :usernameDropDown) OR userId is NULL)

-- Delete
DELETE FROM Playlists
WHERE playlistId = :playlistIdInput

-------- Songs -----------

-- Read
SELECT songId, title, duration, releaseDate 
FROM Songs

-- Create
INSERT INTO Songs(title, duration, releaseDate)
VALUES(:titleInput, :durationInput, :releaseDateInput)

-- Update
UPDATE Songs
SET title = :titleInput, duration = :durationInput, releaseDate = :releaseDateInput
WHERE songId = :songIdInput

-- Delete
DELETE FROM Songs
WHERE songId = :songIdInput

------------ Artists -----------

-- Read
SELECT artistId, artistName, artistBio
FROM Artists

-- Create
INSERT INTO Artists(artistName, artistBio)
VALUES (:artistNameInput, :artistBioInput)

-- Update
UPDATE Artists
SET artistName = :artistNameInput, artistBio = :artistBioInput
WHERE artistId = :artistIdInput

-- Delete
DELETE FROM Artists
WHERE artistId = :artistIdInput

-------- Playlist Songs -----------

-- Read
SELECT playlistSongsId, Playlists.playlistTitle, Songs.title as songTitle
FROM PlaylistSongs
INNER JOIN Playlists on PlaylistSongs.playlistId = Playlists.playlistId
INNER JOIN Songs on PlaylistSongs.songId = Songs.songId;

-- Create
INSERT INTO PlaylistSongs(playlistId, songId)
VALUES (
    (SELECT playlistId FROM Playlists where playlistTitle = :playlistTitleDropDown),
    (SELECT songId FROM Songs where title = :songTitleDropDown)
);
--Updated Create query for PlaylistSongs(above one does not seem to work)
INSERT INTO PlaylistSongs (playlistId, songId) VALUES (%s, %s);

-- :playlistTitleDropDown
SELECT playlistTitle FROM Playlists

-- :songTitleDropDown
SELECT title FROM Songs

-- Update
UPDATE PlaylistSongs
SET playlistTitle = :playlistTitleDropDown, songTitle = :songTitleDropDown
WHERE playlistSongsId = :playlistSongsIdInput
AND playlistId = (SELECT playlistId FROM Playlists WHERE playlistTitle = :playlistTitleDropDown)

-- Delete
DELETE FROM PlaylistSongs
WHERE playlistSongsId = :playlistSongsIdInput

---------- Artist Songs ---------

-- Read
SELECT artistSongsId, Artists.artistName, Songs.title as 'Song Title'
FROM ArtistSongs
INNER JOIN Artists on ArtistSongs.artistId = Artists.artistId
INNER JOIN Songs on ArtistSongs.songId = Songs.songId;

-- Create
INSERT INTO ArtistSongs(artistId, songId)
VALUES (
    (SELECT artistId FROM Artists WHERE artistName = :artistNameDropDown),
    (SELECT songId FROM Songs where title = :songTitleDropDown)
);

-- :artistNameDropDown
SELECT artistId, artistName FROM Artists;

-- :songTitleDropDown
SELECT songId, title FROM Songs;

-- Update
UPDATE ArtistSongs
SET artistName = :artistNameDropDown, songTitle = :songTitleDropDown
WHERE artistSongsId = :artistSongsIdInput
AND artistId = (SELECT artistId FROM Artists WHERE artistName = :artistNameDropDown)

-- Delete
DELETE FROM ArtistSongs
WHERE artistSongsId = :artistSongsIdInput