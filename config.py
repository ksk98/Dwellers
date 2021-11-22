# Config is non-editable by the user.
config = {
    "VERSION": "v0.99.§R6.9§0",                         # Used in menu to display version with logo
    "SPLASH": "§rL§bP§gG §mUpdate §0- §yNow with colors!§0",      # Splash text in main menu
    "INTERFACE_COLOR": "CYAN",                      # Color of the interface (e.g. selected button);
                                                    # For available colors see views/colors_enum.py
    "MAX_PLAYERS": 4,                               # Max players allowed in hosted lobby
    "CONNECTION_TIMEOUT_TIME": 5,                   # Used in logic.game.join_external_lobby
    "HIGH_PORTS_BASE": 46887,                       # Used in generating ports for player sockets as host
}
