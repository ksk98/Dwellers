# Dwellers

## Table of contents
  * [About](#about)
  * [Game mechanics](#game-mechanics)
  * [How to ...](#how-to-)
    * [How to launch](#how-to-launch)
    * [How to create executable](#how-to-create-executable)
    * [How to compile from console](#how-to-compile-from-console)
    * [How to play](#how-to-play)
  * [Network documentation](#network-documentation)

## About
Dwellers is a turn based dungeon crawler.
Create your character and gather your party
to purge the randomly generated dungeon of
any creature that comes your way!


## Game mechanics
  * Certain enemies are more vulnerable/resistant to certain types of attack
  * Attacks can deal regular damage and/or energy(stamina) damage
  * Every attack costs a given amount of energy
  * A character can rest for a turn to replenish part of energy
  * Players can heal each other thus regenerating health and energy of the target
  * Enemies display certain behaviour, encouraging prioritization of targets
  * The more strength a character has, the more energy it restores during rest
  * Strength increases amount of damage dealt by most attacks
  * Energy increases amount of damage dealt by some attacks

## Screenshots
![Main menu](https://i.imgur.com/iaqdMH4.png)

![Character creation](https://i.imgur.com/GzmHN3n.png)

![Gameplay](https://i.imgur.com/C1gh7Wr.png)

## How to ...

### How to launch
Just run [main.exe](dist/main.exe).
It may occur that the executable will be out of date.
In that case the file can be recreated.

### How to create executable
```
venv/Scripts/activate
python setup.py install
python setup.py py2exe
```

### How to compile from console
May require to install jsonpickle (`pip install jsonpickle`)
```
venv/Scripts/activate
py main.py
```

### How to play
  * Create a character and distribute skillpoints
  * Create or join a lobby
  * Press ready and start the game
  * Host leads the party trough the rooms
  * When hostiles will be met in a room, a fight will break
  * Each participant of the fight gets one chance to do something during the round
    * Unless the fight ends before his/her turn
  * Fight continues until one side is defeated
  * Dungeon ends after the last room and the score is displayed
  * The lobby is disbanded

## Network documentation
See [here](network/documentation)
