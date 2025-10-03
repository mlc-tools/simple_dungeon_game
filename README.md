# Simple Dungeon Game Online #

### Description ###

An example of using the [mlc-tools](https://github.com/mlc-tools/mlc-cpp) utility.

The game shows how to launch of a game written on the Python,
which communicates with the servers on Python or C++.

All servers use one code of game logic that is translated into the server language


### Install mlc: ###
 - See repo https://github.com/mlc-tools/mlc-cpp


### How to Launch The Game with C++ Server: ###

 - ``` mlc --config mlc.json ``` command to generate the code
 - ``` cd server_cpp; mkdir build; cd build; cmake ..; make -j8``` to build C++ Http Server with cmake
 - ``` cd server_cpp/build; ./server ../``` to launch C++ server
 - Uncomment ```Controller.SERVER_URL = 'http://127.0.0.1 ...``` line in file **client/game.py**
 - ``` cd client; python game.py``` to launch Dungeon Game


### How to Launch The Game with Python Server: ###

 - ``` mlc --config mlc.json ``` command to generate the code
 - ``` cd server; python main.py``` to launch Python Http Server
 - Uncomment ```Controller.SERVER_URL = 'http://127.0.0.1 ...``` line in file **client/game.py**
 - ``` cd client; python game.py``` to launch Dungeon Game
