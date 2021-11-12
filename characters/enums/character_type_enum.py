from enum import Enum


# Used to distinguish enemies.
class Type(Enum):
    # Skeletons, hard to burn
    # "Smack them and watch the bones fly"
    UNDEAD = 0
    # Regular human being
    HUMAN = 1
    # Greater beings of significant strength and posture alike
    # Resist crush attacks pretty good
    ABOMINATION = 2
    # Giant insects that developed strong chitin armor, resistant to slash damage
    # Susceptible to crush attacks and fire
    INSECT = 3
