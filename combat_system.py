"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Jeremiah Cooper

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""
import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type

    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100

    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """

    enemy_types = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100},
    }

    # Ensure type exists
    if enemy_type not in enemy_types:
        raise InvalidTargetError(f"Unknown enemy type: '{enemy_type}'")

    base = enemy_types[enemy_type]

    # Construct the enemy dictionary
    enemy = {
    "name": enemy_type.capitalize(),
    "health": base["health"],
    "max_health": base["health"],
    "strength": base["strength"],
    "magic": base["magic"],
    "xp_reward": base["xp_reward"],
    "gold_reward": base["gold_reward"]
}

    return enemy

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1–2: Goblins
    Level 3–5: Orcs
    Level 6+: Dragons

    Returns: Enemy dictionary
    """

    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"

    return create_enemy(enemy_type)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    Manages combat between character and enemy
    """

    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        """
        Start the combat loop
        
        Returns: {
            'winner': 'player' | 'enemy',
            'xp_gained': int,
            'gold_gained': int
        }
        """
        if self.character["health"] <= 0:
            raise CharacterDeadError("You cannot start a battle while dead!")

        print(f"A wild {self.enemy['name']} appears!")
        print("Battle begins!")

        # Main combat loop
        while self.combat_active:

            print(f"\n--- Turn {self.turn} ---")

            # Player turn
            self.player_turn()
            if self.enemy["health"] <= 0:
                print(f"\nYou defeated the {self.enemy['name']}!")
                self.combat_active = False
                return {
                    "winner": "player",
                    "xp_gained": self.enemy["xp_reward"],
                    "gold_gained": self.enemy["gold_reward"],
                }

            # Enemy turn
            self.enemy_turn()
            if self.character["health"] <= 0:
                print("\nYou have been defeated...")
                self.combat_active = False
                return {
                    "winner": "enemy",
                    "xp_gained": 0,
                    "gold_gained": 0,
                }

            self.turn += 1

    def player_turn(self):
        """
        Handle player's turn
        """
        if not self.combat_active:
            raise CombatNotActiveError("No active battle.")

        print("\nYour Turn:")
        print("1. Basic Attack")
        print("2. Special Ability (Not implemented)")
        print("3. Try to Run")

        choice = input("Choose an action: ")

        if choice == "1":
            # Basic Attack
            dmg = self.character["strength"]
            self.enemy["health"] -= dmg
            print(f"You attack the {self.enemy['name']} for {dmg} damage!")

        elif choice == "2":
            print("Special ability not implemented. You lose your turn!")

        elif choice == "3":
            # Run chance = 50%
            if random.random() < 0.5:
                print("You successfully escaped!")
                self.combat_active = False
                raise CombatNotActiveError("Battle ended: player escaped.")
            else:
                print("You failed to escape!")

        else:
            print("Invalid input — you miss your turn!")

    def enemy_turn(self):
        """
        Enemy attacks
        """
        if not self.combat_active:
            raise CombatNotActiveError("No active battle.")

        dmg = self.enemy["strength"]
        self.character["health"] -= dmg
        print(f"The {self.enemy['name']} hits you for {dmg} damage!")
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack using provided formula.
        """
        base = attacker["strength"]
        reduction = defender["strength"] // 4

        damage = base - reduction
        damage = max(1, damage)  # Minimum damage is 1

        return damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage and prevent negative health.
        """
        target["health"] -= damage
        if target["health"] < 0:
            target["health"] = 0
    
    def check_battle_end(self):
        """
        Check if battle is over.
        """
        if self.enemy["health"] <= 0:
            return "player"

        if self.character["health"] <= 0:
            return "enemy"

        return None  # Battle continues
    
    def attempt_escape(self):
        """
        50% chance to escape battle.
        """
        success = random.random() < 0.5

        if success:
            print("You successfully escaped!")
            self.combat_active = False
            return True
        else:
            print("Escape failed!")
            return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: A string describing the result
    """

    char_class = character.get("class", "").lower()

    # WARRIOR — Power Strike
    if char_class == "warrior":
        damage = character["strength"] * 2
        enemy["health"] = max(0, enemy["health"] - damage)
        return f"Warrior uses Power Strike and deals {damage} damage!"

    # MAGE — Fireball (magic attack)
    elif char_class == "mage":
        damage = character["magic"] * 2
        enemy["health"] = max(0, enemy["health"] - damage)
        return f"Mage casts Fireball and burns enemy for {damage} damage!"

    # ROGUE — Critical Strike (50% chance)
    elif char_class == "rogue":
        import random
        if random.random() < 0.5:
            # Success: 3x damage
            damage = character["strength"] * 3
            enemy["health"] = max(0, enemy["health"] - damage)
            return f"Rogue lands a CRITICAL STRIKE for {damage} damage!"
        else:
            return "Rogue attempted a Critical Strike but missed!"

    # CLERIC — Heal (restore 30 HP)
    elif char_class == "cleric":
        healed = 30
        new_health = min(character["max_health"], character["health"] + healed)
        actual_healed = new_health - character["health"]
        character["health"] = new_health
        return f"Cleric heals for {actual_healed} health!"

    else:
        return "This character class has no special ability."

def warrior_power_strike(character, enemy):
    """Warrior special ability: Power Strike (2x strength damage)"""
    damage = character["strength"] * 2
    enemy["health"] = max(0, enemy["health"] - damage)
    return f"Warrior uses Power Strike and deals {damage} damage!"

def mage_fireball(character, enemy):
    """Mage special ability: Fireball (2x magic damage)"""
    damage = character["magic"] * 2
    enemy["health"] = max(0, enemy["health"] - damage)
    return f"Mage casts Fireball and deals {damage} damage!"

def rogue_critical_strike(character, enemy):
    """Rogue special ability: Critical Strike (50% chance for 3x strength damage)"""
    if random.random() < 0.5:
        damage = character["strength"] * 3
        enemy["health"] = max(0, enemy["health"] - damage)
        return f"Rogue lands a CRITICAL STRIKE for {damage} damage!"
    else:
        return "Rogue attempted a Critical Strike but missed!"

def cleric_heal(character):
    """Cleric special ability: Heal (restore 30 HP, capped at max_health)"""
    heal_amount = 30
    new_health = min(character["max_health"], character["health"] + heal_amount)
    actual_healed = new_health - character["health"]
    character["health"] = new_health
    return f"Cleric heals for {actual_healed} health!"

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    return character.get("health", 0) > 0


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0)
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    print("\n=== Combat Stats ===")
    print(f"{character['name']}: HP={character['health']}/{character['max_health']}, STR={character['strength']}, MAG={character['magic']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}, STR={enemy['strength']}, MAG={enemy['magic']}")
    print("===================")

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

