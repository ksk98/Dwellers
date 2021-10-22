
class Hit:
    """
    Class containing all values that might be modified during attack
    """
    def __init__(self,
                 user_id: int,
                 energy_cost: int,
                 target_id: int,
                 damage: int,
                 user_damage: int = 0,
                 energy_damage: int = 0):

        self.user_id = user_id
        self.energy_cost = energy_cost
        self.user_damage = user_damage
        self.target_id = target_id
        self.damage = damage
        self.energy_damage = energy_damage
