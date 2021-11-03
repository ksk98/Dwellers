from characters.attacks.attack_arrow import AttackArrow
from characters.attacks.attack_batter import AttackBatter
from characters.attacks.attack_impale import AttackImpale
from characters.attacks.attack_crush import AttackCrush
from characters.attacks.attack_fire import AttackFire
from characters.attacks.attack_fist import AttackFist
from characters.attacks.attack_heal import AttackHeal
from characters.attacks.attack_maul import AttackMaul
from characters.attacks.attack_slash import AttackSlash
from characters.attacks.attack_whomp import AttackWhomp

"""
Attack that should be available for player must be here.
"""

all_atacks = [
    AttackArrow(),
    AttackBatter(),
    AttackCrush(),
    AttackFire(),
    AttackFist(),
    AttackHeal(),
    AttackImpale(),
    AttackMaul(),
    AttackSlash(),
    AttackWhomp()
]

# TODO short description for all attacks