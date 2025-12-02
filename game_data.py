"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Jeremiah Cooper

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file and return a dict with lowercase keys.
    Numeric fields are converted to int.
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    quests = {}
    try:
        with open(filename, "r") as file:
            content = file.read()
    except Exception as e:
        raise CorruptedDataError(f"Unable to read quest file: {e}")

    quest_blocks = [block.strip() for block in content.split("\n\n") if block.strip()]

    for block in quest_blocks:
        quest_data = {}
        lines = block.split("\n")
        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid line format: {line}")
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            quest_data[key] = value

        # Convert numeric fields to int
        for num_field in ["reward_xp", "reward_gold", "required_level"]:
            try:
                quest_data[num_field] = int(quest_data[num_field])
            except ValueError:
                raise InvalidDataFormatError(
                    f"Numeric field has invalid value in quest '{quest_data.get('quest_id', '')}'"
                )

        quests[quest_data["quest_id"]] = quest_data

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file and return a dict with lowercase keys.
    Effect remains a string.
    Numeric fields are converted to int.
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    items = {}
    try:
        with open(filename, "r") as file:
            content = file.read()
    except Exception as e:
        raise CorruptedDataError(f"Unable to read item file: {e}")

    item_blocks = [block.strip() for block in content.split("\n\n") if block.strip()]

    for block in item_blocks:
        item_data = {}
        lines = block.split("\n")
        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid line format: {line}")
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            item_data[key] = value

        # Convert numeric fields
        try:
            item_data["cost"] = int(item_data["cost"])
        except ValueError:
            raise InvalidDataFormatError(
                f"COST field has invalid value in item '{item_data.get('item_id', '')}'"
            )

        items[item_data["item_id"]] = item_data

    return items


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or wrong types
    """
    
    required_fields = {
        "quest_id": str,
        "title": str,
        "description": str,
        "reward_xp": (int, float),
        "reward_gold": (int, float),
        "required_level": (int, float),
        "prerequisite": str,
    }

    if not isinstance(quest_dict, dict):
        raise InvalidDataFormatError("Quest data must be a dictionary.")

    for field, expected_type in required_fields.items():
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Missing required field: '{field}'")
        if not isinstance(quest_dict[field], expected_type):
            raise InvalidDataFormatError(
                f"Invalid type for '{field}': expected {expected_type}, got {type(quest_dict[field])}"
            )

    return True

def validate_item_data(item_dict):
    required_fields = {
        "item_id": str,
        "name": str,
        "type": str,
        "effect": str,  # <-- change from dict to str
        "cost": (int, float),
        "description": str
    }
    
    valid_types = {"weapon", "armor", "consumable"}

    if not isinstance(item_dict, dict):
        raise InvalidDataFormatError("Item data must be a dictionary.")

    for field, expected_type in required_fields.items():
        if field not in item_dict:
            raise InvalidDataFormatError(f"Missing required field: '{field}'")
        if not isinstance(item_dict[field], expected_type):
            raise InvalidDataFormatError(
                f"Invalid type for '{field}': expected {expected_type}, got {type(item_dict[field])}"
            )

    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")

    return True


def create_default_data_files():
    """
    Create default data files if they don't exist.
    This helps with initial setup and testing.
    """
    import os

    data_dir = "data"
    quests_file = os.path.join(data_dir, "quests.txt")
    items_file = os.path.join(data_dir, "items.txt")

    try:
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)

        # Create default quests.txt if missing
        if not os.path.exists(quests_file):
            with open(quests_file, "w") as f:
                f.write(
                    "QUEST_ID: first_quest\n"
                    "TITLE: The Beginning\n"
                    "DESCRIPTION: Start your journey by defeating 3 goblins.\n"
                    "REWARD_XP: 100\n"
                    "REWARD_GOLD: 50\n"
                    "REQUIRED_LEVEL: 1\n"
                    "PREREQUISITE: NONE\n\n"
                )

        # Create default items.txt if missing
        if not os.path.exists(items_file):
            with open(items_file, "w") as f:
                f.write(
                    "ITEM_ID: sword_basic\n"
                    "NAME: Basic Sword\n"
                    "TYPE: weapon\n"
                    "EFFECT: strength:5\n"
                    "COST: 50\n"
                    "DESCRIPTION: A simple sword to start your adventure.\n\n"
                    "ITEM_ID: potion_small\n"
                    "NAME: Small Healing Potion\n"
                    "TYPE: consumable\n"
                    "EFFECT: health:20\n"
                    "COST: 10\n"
                    "DESCRIPTION: Restores a small amount of health.\n\n"
                )

        print("Default data files created successfully (if they were missing).")

    except PermissionError as e:
        print(f"Permission error while creating data files: {e}")
    except OSError as e:
        print(f"OS error while creating data files: {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    from custom_exceptions import InvalidDataFormatError

    quest = {}
    numeric_fields = ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]

    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            if ": " not in line:
                raise InvalidDataFormatError(f"Line missing ': ': {line}")

            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip()

            if key in numeric_fields:
                try:
                    quest[key.lower()] = int(value)
                except ValueError:
                    raise InvalidDataFormatError(f"Expected numeric value for {key}, got '{value}'")
            else:
                quest[key.lower()] = value

        # Ensure all required fields exist
        required_fields = ["quest_id", "title", "description", "reward_xp",
                           "reward_gold", "required_level", "prerequisite"]
        for field in required_fields:
            if field not in quest:
                raise InvalidDataFormatError(f"Missing required field: {field}")

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing quest block: {e}")

    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    from custom_exceptions import InvalidDataFormatError

    item = {}
    numeric_fields = ["COST"]
    valid_types = ["weapon", "armor", "consumable"]

    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines

            if ": " not in line:
                raise InvalidDataFormatError(f"Line missing ': ': {line}")

            key, value = line.split(": ", 1)
            key = key.strip()
            value = value.strip()

            if key in numeric_fields:
                try:
                    item[key.lower()] = int(value)
                except ValueError:
                    raise InvalidDataFormatError(f"Expected numeric value for {key}, got '{value}'")
            else:
                item[key.lower()] = value

        # Ensure all required fields exist
        required_fields = ["item_id", "name", "type", "effect", "cost", "description"]
        for field in required_fields:
            if field not in item:
                raise InvalidDataFormatError(f"Missing required field: {field}")

        # Validate item type
        if item["type"].lower() not in valid_types:
            raise InvalidDataFormatError(f"Invalid item type: {item['type']}")

    except Exception as e:
        raise InvalidDataFormatError(f"Error parsing item block: {e}")

    return item

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")

