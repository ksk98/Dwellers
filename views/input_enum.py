from enum import Enum


# Used in the views to distinguish the types of selectable options.
class Input(Enum):
    SELECT = 0          # Enter usually leads the user to another view (or at least tries to)
    TEXT_FIELD = 1
    TOGGLE = 2
    MULTI_TOGGLE = 3
