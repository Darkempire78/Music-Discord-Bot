<img src="https://github.com/Darkempire78/Music-Discord-Bot/blob/main/Assets/Banner.png"/>

![](https://img.shields.io/codefactor/grade/github/Darkempire78/Music-Discord-Bot?style=for-the-badge) ![](https://img.shields.io/github/repo-size/Darkempire78/Music-Discord-Bot?style=for-the-badge) ![](https://img.shields.io/badge/SOURCERY-ENABLED-green?style=for-the-badge) <a href="https://discord.com/invite/sPvJmY7mcV"><img src="https://img.shields.io/discord/831524351311609907?color=%237289DA&label=DISCORD&style=for-the-badge"></a>

* **INVITE :** https://top.gg/bot/796749718217555978
* **SUPPORT SERVER :** https://discord.com/invite/sPvJmY7mcV

# Music Discord Bot

A Discord bot with more than 30+ commands which allows to play music on your server efficiently. Supports Youtube, Spotify, Deezer and Soundcloud links. Skips intros and blanks in the music with [Sponsorblock](https://sponsor.ajay.app/) (optional).

## Installation

* create a discord application / bot [here](https://discord.com/developers/applications)
* Install all dependencies : ``pip install -r requirements.txt``.
* Download [Lavalink](https://github.com/freyacodes/Lavalink).
* Install Java 11+
* Create a MySQL database and use the ``Scripts/generateDatabase.sql`` file to create the table.
* Edit `configuration example.json` :

```Javascript
{
    "token": "", // Your bot token
    "prefix": "?", // Your prefix
    
    "playlistLimit": "15", // Optional - Defaults to 15 if not provided 0 is unlimited
    "sponsorblock": true, // True if you want to skip intros and blanks in the music

    // Spotify => https://developer.spotify.com/dashboard/ 
    "spotifyClientId": "", // Your Spotify ID (OPTIONAL : Spotify links support)
    "spotifyClientSecret": "", // Your Spotify secret (OPTIONAL : Spotify links support)
    
    "MySQLHost": "", // Your MySQL host
    "MySQLLogin": "", // Your MySQL login
    "MySQLPasword": "", // Your MySQL password
    "MySQLDatabase": "" // Your MySQL database
}
```

* Rename it to `configuration.json`.
* Edit `emojis.json`

Finally, host the bot and invite it to your own server.

## Run the bot

* Run `Lavalink.jar` (from [Lavalink](https://github.com/freyacodes/Lavalink)) with `java -jar Lavalink.jar `
  * Note: you will likely want to use a [config file](application.yml) in the same directory as `Lavalink.jar` to control its settings
* Run the bot `python3 main.py`


## Run in docker

* skip all but the first installation steps above
* [install docker](https://docs.docker.com/get-docker/)
* [install docker-compose](https://docs.docker.com/compose/install/#install-compose)
* copy the [configuration.docker.json](configuration.docker.json) file to `./configuration.json`
* fill in your discord bot token 
  * optionally the spotify client id/secret && dbl tokens
* run `docker-compose build`
* run `docker-compose up -d db`
* run `docker-compose up -d`

> Note: In theory you can skip `docker-compose up -d db` and just run `docker-compose up -d` but the timing of the db startup and running of the generateDatabase.sql on initial startup can sometimes cause the music bot to fail to start so its best to just start the db first to give it enough time

### Docker running / debugging tips
* you can run `docker-compose logs` to view logs for all services
* you can run `docker-compose logs <service>` eg: `docker-compose logs musicbot` to see the logs for a specific service (look in the compose file for the service names)
* you can run `docker-compose stop` to stop the music bot / db / lavalink containers
* you can run `docker-compose start` to start the music bot / db / lavalink after stopping

## Features

* Play music from YouTube
* Support links from YouTube, Spotify, Deezer and Soudcloud 
* Support YouTube lives
* Support playlists from Spotify, Deezer, Soundcloud and YouTube
* Playlist system
* Sponsorblock integration to skip intros and blanks in the music
* Many commands
* Complex queue commands


## Preview

<img src="https://github.com/Darkempire78/Music-Discord-Bot/blob/main/Assets/capture1.png" width="600"/>

<img src="https://github.com/Darkempire78/Music-Discord-Bot/blob/main/Assets/capture2.png" width="600"/>


## Commands

```
?play <Url/Query> : Search on youtube and play the music.
?search <Query> : Search a song on youtube.
?nowplaying : Display data about the current song.
?join : Add the bot to your voice channel.
?leave : Remove the bot of your voice channel.
?pause : Pause the current song.
?resume : Resume the current song.
?volume <0-100> : Change the bot's volume.
?queue : Display the queue.
?shuffle : Shuffle the queue.
?move <IndexFrom> <IndexTo> : Move a song in the queue.
?remove <Index> : Remove the song with its index.
?removedupes : Remove all duplicates song from the queue.
?leavecleanup : Remove absent user's songs from the queue.
?clear : Clear the queue.
?replay : Replay the current song.
?reload : Reload the current song.
?loop : Enable or disable the loop mode.
?loopqueue : Enable or disable the loop queue mode.

?playlist add <Url> : Add a track to your playlist.
?playlist remove <Index> : Remove a track to your playlist.
?playlist display : Display playlist's songs.
?playlist load : Add the whole playlist to the queue.

?stats : Display the bot's stats.
?support : Give a link to join the support server.
?invite : Give a link to invite the bot.
?vote : Give the Top.gg link to vote for the bot.
?help : Display the help.

?logout : Stop the bot process.
```

[![Discord Bots](https://top.gg/api/widget/796749718217555978.svg)](https://top.gg/bot/796749718217555978)


## Soon

**Project :** https://github.com/Darkempire78/Music-Discord-Bot/projects/2

## Discord

Join the Discord server !

[![](https://i.imgur.com/UfyvtOL.png)](https://discord.gg/sPvJmY7mcV)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## License

This project is under [GPLv3](https://github.com/Darkempire78/Raid-Protect-Discord-Bot/blob/master/LICENSE).


# Advice :

You should use [Discord Tools](https://marketplace.visualstudio.com/items?itemName=Darkempire78.discord-tools) to code your Discord bots on Visual Studio Code easier.
Works for Python (Discord.py), Javascript (Discord.js) and Java (JDA). Generate template bot and code (snippets).
- **Download :** https://marketplace.visualstudio.com/items?itemName=Darkempire78.discord-tools
- **Repository :** https://github.com/Darkempire78/Discord-Tools
