from characters.enums.attack_type_enum import Type as AttType

class Hit:
    def __init__(self, target_id: int, damage: int, damage_type: AttType, attacker: str, attack: str, energy_damage: int = 0):
        self.target_id = target_id
        self.damage = damage
        self.damage_type = damage_type
        self.attacker = attacker
        self.attack = attack
        self.energy_damage = energy_damage
