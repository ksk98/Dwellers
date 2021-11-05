from enum import Enum


# Used in the views to distinguish the types of selectable options.
class Input(Enum):
    SELECT = 0              # Enter usually leads the user to another view (or at least tries to)
    TEXT_FIELD = 1          # Enter toggles writing mode
    TOGGLE = 2              # Enter toggles a true/false option
    MULTI_TOGGLE = 3        # Enter cycles trough given options
    LEFT_RIGHT_ENTER = 4   # Enter fires a linked lambda, left and right arrow keys cycle trough given options
