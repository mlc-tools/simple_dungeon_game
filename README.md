# Simple Dungeon Game Online #

### Description ###

An example of using the [mlc-tools](https://bitbucket.org/VolodarDev/tools-mlc) library.

The game shows how to launch of a game written on the Python,
which communicates with the servers on the Python or the PHP.

Both servers use one code that is translated into the server language


### How to Launch The Game with Python Server: ###

 - ``` python generate.py ``` command to generate the code
 - ``` cd server; python main.py``` to launch Python Http Server
 - Uncomment ```Controller.SERVER_URL = 'http://localhost ...``` line in file **client/game.php**
 - ``` cd client; python game.py``` to launch Dungeon Game


### How to Launch The Game with PHP Server: ###
 - ``` python generate.py ``` command to generate the code
 - Copy all files from **server_php** folder to your site
 - Uncomment ```Controller.SERVER_URL = 'http://localhost ...``` line in file **client/game.php**
 - ``` cd client; python game.py``` to launch Dungeon Game
