ABOUT:
    Dwellers is a turn based dungeon crawler.
    Create your character and gather your party
    to purge the randomly generated dungeon of
    any creature that comes your way!

HOW TO LAUNCH
    Just run dist\main.exe.
    It may occur that the executable will be out of date.
    In that case the file can be recreated.

HOW TO CREATE EXECUTABLE
    1. venv\Scripts\activate
    2. python setup.py install (or py setup.py install)
    3. python setup.py py2exe

HOW TO COMPILE FROM CONSOLE
    May require to install jsonpickle (pip install jsonpickle)
    1. venv\Scripts\activate
    2. py main.py

HOW TO PLAY:
    - Create a character and distribute skillpoints
    - Create or join a lobby
    - Press ready and start the game
    - Host leads the party trough the rooms
    - When hostiles will be met in a room, a fight will break
    - Each participant of the fight gets one chance to do something during the round
        * Unless the fight ends before his/her turn
    - Fight continues until one side is defeated
    - Dungeon ends after the last room and the score is displayed
    - The lobby is disbanded

NETWORK DOCUMENTATION:
    SEE network.documentation

GAME MECHANICS:
    - Certain enemies are more vulnerable/resistant to certain types of attack
    - Attacks can deal regular damage and/or energy(stamina) damage
    - Every attack costs a given amount of energy
    - A character can rest for a turn to replenish part of energy
    - Players can heal each other thus regenerating health and energy of the target
    - Enemies display certain behaviour, encouraging prioritization of targets
    - The more strength a character has, the more energy it restores during rest
    - Strength increases amount of damage dealt by most attacks
    - Energy increases amount of damage dealt by some attacks