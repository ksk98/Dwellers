from enum import Enum


# Used to distinguish enemies.
class Type(Enum):
    # Deceased human beings, often fragile due to rotting
    UNDEAD = 0
    # Regular human being
    HUMAN = 1
    # Greater beings of significant strength and posture alike
    ABOMINATION = 2
