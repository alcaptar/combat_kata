
class Character:
    MAX_HEALTH = 1000
    MIN_HEALTH = 0
    INITIAL_LEVEL = 1
    REDUCTION_COEFFICIENT = 0.5
    INCREASE_COEFFICIENT = 1.5
    LEVEL_BOUNDARY = 5

    def __init__(self):
        self.health = Character.MAX_HEALTH
        self.level = Character.INITIAL_LEVEL
        self.factions = set()

    def is_alive(self):
        return self.health > Character.MIN_HEALTH

    def attack(self, opponent, damage):
        if Character.characters_are_allies(self, opponent):
            return

        actual_damage = Character.increase_or_reduce_damage(damage, self.level, opponent.level)

        damaged_health = opponent.health - actual_damage
        opponent.health = max(damaged_health, Character.MIN_HEALTH)

    def heal(self, health_to_add, character=None):
        ally = character
        if not character:
            ally = self

        self._heal_ally(health_to_add, ally)

    def _heal_ally(self, health_to_add, character):
        if not character.is_alive() or not Character.characters_are_allies(self, character):
            return

        raised_health = health_to_add + character.health
        character.health = min(raised_health, Character.MAX_HEALTH)

    def join_factions(self, factions_to_join):
        self.factions = self.factions.union(factions_to_join)

    def leave_factions(self, factions_to_leave):
        self.factions = self.factions.symmetric_difference(factions_to_leave)

    @staticmethod
    def increase_or_reduce_damage(damage, attacker_level, target_level):
        if attacker_level - target_level >= Character.LEVEL_BOUNDARY:
            return damage * Character.INCREASE_COEFFICIENT

        if target_level - attacker_level >= Character.LEVEL_BOUNDARY:
            return damage * Character.REDUCTION_COEFFICIENT

        return damage

    @staticmethod
    def characters_are_allies(attacker, opponent):
        if attacker == opponent:
            return True
        return not attacker.factions.isdisjoint(opponent.factions)
