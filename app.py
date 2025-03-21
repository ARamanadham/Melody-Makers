# Group: 20
# Members: Yasser Hernandez, Anish Ramanadham
# Citation for all code below.
# Date: 02/23/2025
# Adapted from code provided in Class
# The DB credentials have been removed for secuirty, the secret_key has also been changed and left for demonstration purposes

from flask import Flask, render_template, json, redirect, flash
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

# Prevent duplicates via secret key
app.secret_key = 'testingpurpose'

app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes
@app.route("/")
def home():
    # Renders Home page
    return render_template("index.j2")

# route for users page
@app.route("/users.j2", methods=["POST", "GET"])
def users():
    if request.method == "POST":
        # Executes if the Save new User button is pressed
        if request.form.get("NewUser"):
            # Assigns the input data from the user form
            username = request.form["username"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            userBio = request.form["userBio"]

            # setting defaults of firstname, lastName and userBio to None:
            if not firstName:
                firstName = 'None'

            if not lastName:
                lastName = 'None'

            if not userBio:
                userBio = 'None'

            # preventing duplicate usernames
            try:
                # Insert data from form into the database
                query = "INSERT INTO Users (username, firstName, lastName, userBio) VALUES (%s, %s,%s,%s)"          
                cur = mysql.connection.cursor()
                cur.execute(query, (username, firstName, lastName, userBio))
                mysql.connection.commit()
            except mysql.connection.IntegrityError:
                flash(f"{username} already exists! Please pick a different username")

            return redirect("/users.j2")

    if request.method == "GET":
        # Query to selects all the users from Users table
        query = "SELECT userId, username, firstName, lastName, userBio FROM Users order by userId asc;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Renders user table
        return render_template("users.j2", data=data)

# route for deleting user
@app.route("/DeleteUserInfo/<int:userId>", methods=["POST"])
def DeleteUserInfo(userId):
    # Query to delete user by userId
    query = "DELETE FROM Users WHERE userId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (userId,))
    mysql.connection.commit()

    return redirect("/users.j2")

# route for updating user
@app.route("/UpdateUserInfo/<int:userId>", methods=["POST", "GET"])
def UpdateUserInfo(userId):

    if request.method == "POST":
        # Assigns the input data from the user form
        username = request.form["username"]
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        userBio = request.form["userBio"]

        # setting the defaults if the user does not enter a value
        if not firstName:
            firstName = 'None'

        if not lastName:
            lastName = 'None'

        if not userBio:
            userBio = 'None'

        # Try-Except block to handle duplicates based on unique username
        try:
            # Query to update a user's information by userId
            query = "UPDATE Users SET username = %s, firstName = %s, lastName = %s, userBio = %s WHERE userId = '%s';"
            cur = mysql.connection.cursor()
            cur.execute(query, (username, firstName, lastName, userBio, userId))
            mysql.connection.commit()
        except mysql.connection.IntegrityError:
            flash(f"{username} already exists! Please pick a different username")

        return redirect("/users.j2")

# route for playlists page
@app.route("/playlists.j2", methods=["POST", "GET"])
def playlists():
    if request.method == "POST":
        # Assigns the input data from the playlist form
        if request.form.get("AddPlaylists"):
            playlistTitle = request.form["playlistTitle"]
            userId = request.form.get("userId")

            # setting the defaults if the user does not enter a value
            if not playlistTitle:
                playlistTitle = 'Untitled'

            # Insert
            query = "INSERT INTO Playlists (playlistTitle, userId) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (playlistTitle, userId))
            mysql.connection.commit()

            return redirect("/playlists.j2")

    if request.method == "GET":
        # Query to select Playlists table using a left join so that 'None' user playslists still show up
        query = "SELECT playlistId, playlistTitle, Users.username FROM Playlists LEFT JOIN Users on Playlists.userId = Users.userId ORDER BY playlistId asc;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Query to select userId, username from Users
        usersUsernameQuery = "SELECT userId, username FROM Users;"
        cur = mysql.connection.cursor()
        cur.execute(usersUsernameQuery)
        userUsernameData = cur.fetchall()

        return render_template("playlists.j2", data=data, userUsernameData=userUsernameData)

# route for deleting playlists
@app.route("/DeletePlaylistInfo/<int:playlistId>", methods=["POST"])
def DeletePlaylistInfo(playlistId):
    # Query to delete playlist by playlistId
    query = "DELETE FROM Playlists WHERE playlistId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (playlistId,))
    mysql.connection.commit()

    return redirect("/playlists.j2")

# route for updating playlists
@app.route("/UpdatePlaylistInfo/<int:playlistId>", methods=["POST", "GET"])
def UpdatePlaylistInfo(playlistId):
    if request.method == "GET":
        # Query to select a playlist from Playlists table by playlistId
        query = "SELECT * FROM Playlists WHERE playlistId = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (playlistId,))
        playlistUpdateData = cur.fetchall()

        return render_template("/playlists.j2", playlistUpdateData=playlistUpdateData)

    if request.method == "POST":
        # Assing inputs from playlists
        playlistTitle = request.form["playlistTitle"] 
        userId = request.form["userId"]

        # Query
        query = "UPDATE Playlists SET playlistTitle = %s, userId = %s WHERE playlistId = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (playlistTitle, userId, playlistId))
        mysql.connection.commit()

        return redirect("/playlists.j2")

# route for PlaylistSongs page
@app.route("/playlistsongs.j2", methods=["POST", "GET"])
def playlistsongs():
    if request.method == "POST":
        # Executes if the Save new PlaylistSongs button is pressed
        if request.form.get("AddPlaylistSong"):
            # Assigns the input data from the playlistsongs form
            playlistId = request.form["playlistId"]
            songId = request.form["songId"]

            # Insert data from form into the database
            query = "INSERT INTO PlaylistSongs (playlistId, songId) VALUES (%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (playlistId, songId))
            mysql.connection.commit()

            return redirect("/playlistsongs.j2")

    if request.method == "GET":
        # Query to join Playlists and Songs tables to display in playlistSongs table using LEFT + INNER to ensure empty playlists still show up
        query = "SELECT playlistSongsId, Playlists.playlistTitle, Songs.title as songTitle FROM PlaylistSongs INNER JOIN Playlists on PlaylistSongs.playlistId = Playlists.playlistId LEFT JOIN Songs on PlaylistSongs.songId = Songs.songId ORDER BY playlistTitle, title asc;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        playlistSongsData = cur.fetchall()

        # Query to selects playlistId, playlistTitle from Playlists table
        playlistTitleQuery = "SELECT playlistId, playlistTitle FROM Playlists;"
        cur = mysql.connection.cursor()
        cur.execute(playlistTitleQuery)
        playlistTitleData = cur.fetchall()

        # Query to selects songId, title from Songs table
        playlistTitleQuery = "SELECT songId, title FROM Songs;"
        cur = mysql.connection.cursor()
        cur.execute(playlistTitleQuery)
        songsData = cur.fetchall()

        # Renders playlistsongs table page
        return render_template("playlistsongs.j2", playlistSongsData=playlistSongsData, playlistTitleData=playlistTitleData, songsData=songsData)

# route for deleting PlaylistSongs
@app.route("/DeletePlaylistSongs/<int:playlistSongsId>", methods=["POST"])
def DeletePlaylistSongs(playlistSongsId):
    # Query to delete user by userId
    query = "DELETE FROM PlaylistSongs WHERE playlistSongsId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (playlistSongsId,))
    mysql.connection.commit()

    return redirect("/playlistsongs.j2")

# route for updating PlaylistSongs
@app.route("/UpdatePlaylistSong/<int:playlistSongsId>", methods=["POST", "GET"])
def UpdatePlaylistSong(playlistSongsId):
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute("SELECT playlistId, songId FROM PlaylistSongs WHERE playlistSongsId = %s", (playlistSongsId,))
        current_values = cur.fetchone()

        # Assigns the input data from the PlaylistSongs form
        playlistId = request.form.get("playlistId") or current_values['playlistId']
        songId = request.form.get("songId")

        # Explicitly convert empty string to None (which maps to NULL in SQL)
        if songId == "" or songId is None:
            songId = None

        # Query to update a PlaylistSongs's information by playlistSongsId
        query = """
            UPDATE PlaylistSongs 
            SET playlistId = %s, songId = CASE WHEN %s IS NULL THEN NULL ELSE %s END
            WHERE playlistSongsId = %s;
        """

        cur.execute(query, (playlistId, songId, songId, playlistSongsId))
        mysql.connection.commit()

        return redirect("/playlistsongs.j2")


# route for songs page
@app.route("/songs.j2", methods=["POST", "GET"])
def songs():
    if request.method == "POST":
        # Executes if the Save new User button is pressed
        if request.form.get("NewSong"):
            # Assigns the input data from the user form
            title = request.form["title"]
            hrs = request.form["hours"]
            mins = request.form["minutes"]
            secs = request.form["seconds"]
            duration = f"{int(hrs):02d}:{int(mins):02d}:{int(secs):02d}"
            releaseDate = request.form["releaseDate"]

            try:
                # Insert data from form into the database
                query = "INSERT INTO Songs(title, duration, releaseDate) VALUES(%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (title, duration, releaseDate))
                mysql.connection.commit()
            except mysql.connection.IntegrityError:
                flash(f"{title} already exists! Please only enter records for New Songs")

            return redirect("/songs.j2")

    if request.method == "GET":
        # Query to selects all the users from Users table
        query = "SELECT songId, title, duration, releaseDate FROM Songs ORDER BY songId asc;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Renders songs table page
        return render_template("songs.j2", data=data)

# route for deleting a Song
@app.route("/DeleteSongInfo/<int:songId>", methods=["POST"])
def DeleteSongInfo(songId):
    # Query to delete a Song by songId
    query = "DELETE FROM Songs WHERE songId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (songId,))
    mysql.connection.commit()

    return redirect("/songs.j2")

# route for updating Songs
@app.route("/UpdateSongs/<int:songId>", methods=["POST", "GET"])
def UpdateSongs(songId):
    if request.method == "POST":
        # Assigns the input data from the Songs form
        title = request.form["title"]
        duration = request.form["duration"]
        releaseDate = request.form["releaseDate"]

        try:
            # Query to update a Songs's information by songId
            query = "UPDATE Songs SET title = %s, duration = %s, releaseDate = %s WHERE songId = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (title, duration, releaseDate, songId))
            mysql.connection.commit()
        except mysql.connection.IntegrityError:
            flash(f"{title} already exists! Please only enter records for New Songs")

        return redirect("/songs.j2")

# route for ArtistSongs page
@app.route("/artistsongs.j2", methods=["POST", "GET"])
def artistsongs():
    if request.method == "POST":
        if request.form.get("AddArtistSong"):
            # assigns input from the forms
            artistId = request.form["artistId"]
            songId = request.form["songId"]

            try:        
                # insert based on these
                query = "INSERT INTO ArtistSongs (artistId, songId) VALUES (%s,%s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (artistId, songId))
                mysql.connection.commit()
            except mysql.connection.IntegrityError:
                flash("This Artist Song connection already exists!")

            return redirect("/artistsongs.j2")

    if request.method == "GET":
        query = "SELECT artistSongsId, Artists.artistName, Songs.title as songTitle FROM ArtistSongs INNER JOIN Artists on ArtistSongs.artistId = Artists.artistId INNER JOIN Songs on ArtistSongs.songId = Songs.songId order by artistName, artistSongsId asc;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        artistSongsData = cur.fetchall()
        print(artistSongsData)
        # getting dropdowns
        artistNameQuery = "SELECT artistId, artistName FROM Artists;"
        cur = mysql.connection.cursor()
        cur.execute(artistNameQuery)
        artistNameData = cur.fetchall()

        songTitleQuery = "SELECT songId, title FROM Songs;"
        cur = mysql.connection.cursor()
        cur.execute(songTitleQuery)
        songsData = cur.fetchall()

        return render_template("artistsongs.j2", artistSongsData=artistSongsData, artistNameData=artistNameData, songsData=songsData)

# route for deleting ArtistSongs
@app.route("/DeleteArtistSongs/<int:artistSongsId>", methods=["POST"])
def DeleteArtistSongs(artistSongsId):
    query = "DELETE FROM ArtistSongs WHERE artistSongsId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (artistSongsId, ))
    mysql.connection.commit()

    return redirect("/artistsongs.j2")

# route for updating ArtistSongs
@app.route("/UpdateArtistSong/<int:artistSongsId>", methods=["POST", "GET"])
def UpdateArtistSong(artistSongsId):
    if request.method == "POST":
        # get current values for if/else
        cur = mysql.connection.cursor()
        cur.execute("SELECT artistId, songId FROM ArtistSongs WHERE artistSongsId = %s", (artistSongsId,))
        current_values = cur.fetchone()

        # Assigns the input data from the PlaylistSongs form
        artistId = request.form.get("artistId") or current_values['artistId']
        songId = request.form.get("songId") or current_values['songId']

        try:
            # Query to update a PlaylistSongs's information by playlistSongsId
            query = "UPDATE ArtistSongs SET artistId = %s, songId = %s WHERE artistSongsId = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (artistId, songId, artistSongsId))
            mysql.connection.commit()
        except mysql.connection.IntegrityError:
            flash("This Artist Song connection already exists!")

        return redirect("/artistsongs.j2")

# route for Artists page
@app.route("/artists.j2", methods=["POST", "GET"])
def artists():
    if request.method == "POST":
        # assign inputs
        artistName = request.form["artistName"]
        artistBio = request.form["artistBio"]

        if not artistBio:
            artistBio = 'None'

        try:
            # insert
            query = "INSERT INTO Artists (artistName, artistBio) VALUES (%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (artistName, artistBio))
            mysql.connection.commit()
        except mysql.connection.IntegrityError:
            flash(f"{artistName} already exists! Please only enter records for New Artists")

        return redirect("/artists.j2")

    if request.method == "GET":
        query = "SELECT artistId, artistName, artistBio FROM Artists ORDER BY artistId asc;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Renders artists table page
        return render_template("artists.j2", data=data)

# route for deleting Artists
@app.route("/DeleteArtistInfo/<int:artistId>", methods=["POST"])
def DeleteArtistInfo(artistId):
    # Query to delete artist by id
    query = "DELETE FROM Artists WHERE artistId = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (artistId,))
    mysql.connection.commit()

    return redirect("/artists.j2")

# route for updating Artists
@app.route("/UpdateArtistInfo/<int:artistId>", methods=["POST", "GET"])
def UpdateArtistInfo(artistId):
    if request.method == "GET":
        # get artist based on artistId
        query = "SELECT * FROM Artists WHERE artistId = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (artistId,))
        artistUpdate = cur.fetchall()

        return render_template("/artists.j2", artistUpdate=artistUpdate)

    if request.method == "POST":
        # Assings inupt data
        artistName = request.form["artistName"]
        artistBio = request.form["artistBio"]

        if not artistBio:
            artistBio = 'None'

        try:
            # update artist info by artistId
            query = "UPDATE Artists SET artistName = %s, artistBio = %s WHERE artistID = '%s';"
            cur = mysql.connection.cursor()
            cur.execute(query, (artistName, artistBio, artistId))
            mysql.connection.commit()
        except mysql.connection.IntegrityError:
            flash(f"{artistName} already exists! Please only enter records for New Artists")

        return redirect("/artists.j2")

if __name__ == "__main__":
    #Start app on port 56983, will be different once hosted
    app.run(port=56989, debug=True)