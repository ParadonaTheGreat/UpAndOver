# Up and Over Game

## How to play

One user starts off by making a room. This user that made the room selects the number of people in the room and the target number everyone is playing to (alternatively, the user can play against the computer). Another user can join this room by putting in the same room code. If the room is full, the user will return to the home screen. Whoever is player one starts the game by choosing a number one, two or three. This number is then added to the game's total. Each user takes turns adding to the number. The first user to add a number equal to or past the target number loses. The game can handle many simultaneous games at once. Any number of groups can make their own room code and play different games. 

## Project

This game was made using Python's Flask library. It is hosted on Python Anywhere and is available to play at: https://paradonathegreat.pythonanywhere.com/. The game uses a dictionary and the room code to differentiate between the multiple concurrent games. After the game ends, the dictionary is cleared. 
