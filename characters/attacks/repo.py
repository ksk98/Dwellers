from characters.attacks.attack_arrow import AttackArrow
from characters.attacks.attack_bite import AttackBite
from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_drink_blood import AttackDrinkBlood
from characters.attacks.attack_fire import AttackFire
from characters.attacks.attack_fist import AttackFist
from characters.attacks.attack_heal import AttackHeal
from characters.attacks.attack_maul import AttackMaul
from characters.attacks.attack_slash import AttackSlash
from characters.attacks.attack_spit import AttackSpit

"""
Attack that should be available for player must be here.
"""

all_atacks = [
    AttackArrow(),
    AttackBite(),
    AttackCrush(),
    AttackDrinkBlood(),
    AttackFire(),
    AttackFist(),
    AttackHeal(),
    AttackMaul(),
    AttackSlash(),
    AttackSpit()]

# TODO short description for all attacks