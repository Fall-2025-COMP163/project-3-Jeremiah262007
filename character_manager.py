"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Jeremiah Cooper

AI Usage:

AI assistance was used to help understand and clarify the logic behind character management functions. Specifically, it helped explain:

* **Character Creation** – Validating classes, setting base stats, initializing fields.
* **Gold Operations** – Adding or spending gold with validation to prevent negative totals.
* **Save/Load System** – Converting dictionaries to file format, parsing saved data, and validating integrity.
* **Exception Handling** – Understanding when exceptions like `InvalidCharacterClassError`, `CharacterDeadError`, `InvalidSaveDataError`, and `CharacterNotFoundError` should be raised.
All final code logic, implementation, and testing were completed independently.


This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80,  "strength": 8,  "magic": 20},
        "Rogue": {"health": 90,  "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15}
    }
    
    # Validate class
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"'{character_class}' is not a valid class.")
    
    base_stats = valid_classes[character_class]
    
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base_stats["health"],
        "max_health": base_stats["health"],
        "strength": base_stats["strength"],
        "magic": base_stats["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    
    return character

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    """

    os.makedirs(save_directory, exist_ok=True)

    filename = f"{character['name']}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # Convert list fields to comma-separated strings
    inventory_str = ",".join(character.get("inventory", []))
    active_q_str = ",".join(character.get("active_quests", []))
    completed_q_str = ",".join(character.get("completed_quests", []))

    # Prepare file content
    content = (
        f"NAME: {character['name']}\n"
        f"CLASS: {character['class']}\n"
        f"LEVEL: {character['level']}\n"
        f"HEALTH: {character['health']}\n"
        f"MAX_HEALTH: {character['max_health']}\n"
        f"STRENGTH: {character['strength']}\n"
        f"MAGIC: {character['magic']}\n"
        f"EXPERIENCE: {character['experience']}\n"
        f"GOLD: {character['gold']}\n"
        f"INVENTORY: {inventory_str}\n"
        f"ACTIVE_QUESTS: {active_q_str}\n"
        f"COMPLETED_QUESTS: {completed_q_str}\n"
    )

    # Write the file
    with open(filepath, "w") as file:
        file.write(content)

    return True
def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Returns a character dictionary.
    """
    
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # 1. Check if file exists
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"No save file found for '{character_name}'.")

    # 2. Try reading file
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except Exception as e:
        raise SaveFileCorruptedError(f"Unable to read save file: {e}")

    # 3. Parse file content
    character = {}
    try:
        for line in lines:
            if ":" not in line:
                raise InvalidSaveDataError("Invalid line format in save file.")

            key, value = line.strip().split(":", 1)
            value = value.strip()

            if key == "NAME":
                character["name"] = value
            elif key == "CLASS":
                character["class"] = value
            elif key == "LEVEL":
                character["level"] = int(value)
            elif key == "HEALTH":
                character["health"] = int(value)
            elif key == "MAX_HEALTH":
                character["max_health"] = int(value)
            elif key == "STRENGTH":
                character["strength"] = int(value)
            elif key == "MAGIC":
                character["magic"] = int(value)
            elif key == "EXPERIENCE":
                character["experience"] = int(value)
            elif key == "GOLD":
                character["gold"] = int(value)
            elif key == "INVENTORY":
                character["inventory"] = value.split(",") if value else []
            elif key == "ACTIVE_QUESTS":
                character["active_quests"] = value.split(",") if value else []
            elif key == "COMPLETED_QUESTS":
                character["completed_quests"] = value.split(",") if value else []
            else:
                raise InvalidSaveDataError(f"Unexpected field: {key}")

    except Exception as e:
        raise InvalidSaveDataError(f"Invalid save data: {e}")

    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """

    if not os.path.exists(save_directory):
        return []

    saved_characters = []

    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            # Remove the suffix
            name = filename.replace("_save.txt", "")
            saved_characters.append(name)

    return saved_characters

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """

    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    # Check if file exists
    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"No save file found for '{character_name}'.")

    # Try deleting file
    os.remove(filepath)

    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    """

    # 1. Check if character is dead
    if character["health"] <= 0:
        raise CharacterDeadError("Character is dead and cannot gain experience.")

    # 2. Add experience
    character["experience"] += xp_amount

    # 3. Handle multiple possible level-ups
    leveled_up = True
    while leveled_up:
        leveled_up = False

        level_up_requirement = character["level"] * 100

        if character["experience"] >= level_up_requirement:
            # Deduct required XP and level up
            character["experience"] -= level_up_requirement
            character["level"] += 1

            # Increase stats
            character["max_health"] += 10
            character["strength"] += 2
            character["magic"] += 2

            # Restore HP to full
            character["health"] = character["max_health"]

            leveled_up = True  # Continue loop in case they can level again

    return character

def add_gold(character, amount):
    """
    Add gold to character's inventory

    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)

    Returns: New gold total
    Raises: ValueError if result would be negative
    """

    new_total = character.get("gold", 0) + amount

    if new_total < 0:
        raise ValueError("Character cannot have negative gold.")

    character["gold"] = new_total
    return new_total

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """

    current_hp = character["health"]
    max_hp = character["max_health"]

    # How much room there is to heal
    missing_hp = max_hp - current_hp

    # Actual healing cannot exceed missing_hp
    actual_heal = min(amount, missing_hp)

    # Apply healing
    character["health"] += actual_heal

    return actual_heal

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character["health"] <= 0

def revive_character(character):
    """ 
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # Only revive if the character is dead
    if character["health"] > 0:
        return False  # Can't revive someone who's alive
    
    # Restore health to half of max_health
    character["health"] = character["max_health"] * 0.5
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """

    required_fields = {
        "name": str,
        "class": str,
        "level": (int, float),
        "health": (int, float),
        "max_health": (int, float),
        "strength": (int, float),
        "magic": (int, float),
        "experience": (int, float),
        "gold": (int, float),
        "inventory": list,
        "active_quests": list,
        "completed_quests": list,
    }

    # Ensure the argument is a dictionary
    if not isinstance(character, dict):
        raise InvalidSaveDataError("Character data must be a dictionary.")

    # Check for required fields and type validation
    for field, expected_type in required_fields.items():
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: '{field}'")

        if not isinstance(character[field], expected_type):
            raise InvalidSaveDataError(
                f"Invalid type for '{field}': expected {expected_type}, got {type(character[field])}"
            )

    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

