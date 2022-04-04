import pytest as pytest

from character.character import Character


class TestCharacter:

    def test_new_character_has_default_attributes(self):
        character = Character()

        assert character.health == 1000
        assert character.level == 1
        assert character.is_alive
        assert len(character.factions) == 0

    @pytest.mark.parametrize('initial_character2_health, damage', [
        (1000, 5)
    ])
    def test_damage_extracted_from_health(self, initial_character2_health, damage):
        character1 = Character()
        character2 = Character()

        character1.attack(character2, damage)

        assert character2.health == initial_character2_health - damage

    @pytest.mark.parametrize('damage', [
        1005
    ])
    def test_character_deads_when_damage_exceeds_health(self, damage):
        character1 = Character()
        character2 = Character()

        character1.attack(character2, damage)

        assert not character2.is_alive()

    @pytest.mark.parametrize('damage', [
        1005
    ])
    def test_character_cannot_damage_himself(self, damage):
        character = Character()
        character.attack(character, damage)

        assert character.health == 1000

    @pytest.mark.parametrize('damage', [
        10
    ])
    def test_damage_increase_if_target_level_below_attacker(self, damage):
        target = Character()
        attacker = Character()
        attacker.level += 5
        actual_damage = damage*1.5

        attacker.attack(target, damage)

        assert target.health == 1000 - actual_damage

    @pytest.mark.parametrize('damage', [
        10
    ])
    def test_damage_reduced_if_target_level_above_attacker(self, damage):
        target = Character()
        attacker = Character()
        target.level += 5
        actual_damage = damage * 0.5

        attacker.attack(target, damage)

        assert target.health == 1000 - actual_damage

    def test_allies_cannot_damage_to_one_another(self):
        target = Character()
        attacker = Character()
        target.factions = {0, 1}
        attacker.factions = {1, 2}

        attacker.attack(target, 5)

        assert target.health == 1000

    def test_dead_character_cannot_heal(self):
        character = Character()
        character.health = 0

        character.heal(100)

        assert not character.is_alive()

    def test_character_can_heal(self):
        character = Character()
        character.health = 5

        health_to_add = 100
        initial_character_health = character.health

        character.heal(health_to_add)
        assert character.health == initial_character_health + health_to_add

    def test_character_can_heal_ally(self):
        character1 = Character()
        character2 = Character()
        character1.factions = {0, 1}
        character2.factions = {1, 2}
        character2.health = 500

        character1.heal(100, character2)

        assert character2.health == 600

    def test_character_cannot_heal_enemy(self):
        character1 = Character()
        character2 = Character()
        character1.factions = {0, 1}
        character2.factions = {2}
        character2.health = 500

        character1.heal(100, character2)

        assert character2.health == 500

    def test_character_health_doesnt_exceed_1000(self):
        character = Character()

        health_to_add = 100

        character.heal(health_to_add)
        assert character.health == 1000

    def test_character_can_join_factions(self):
        character = Character()
        character.factions = {0}

        character.join_factions({1, 2})

        assert character.factions == {0, 1, 2}

    def test_character_can_leave_factions(self):
        character = Character()
        character.factions = {0, 1, 2}

        character.leave_factions({1, 2})

        assert character.factions == {0}