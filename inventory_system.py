"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Jeremiah Cooper

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory

    Args:
        character: Character dictionary
        item_id: Unique item identifier

    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    from custom_exceptions import InventoryFullError

    inventory = character.get("inventory", [])

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Cannot add '{item_id}': inventory is full.")

    inventory.append(item_id)
    character["inventory"] = inventory
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    from custom_exceptions import ItemNotFoundError

    inventory = character.get("inventory", [])

    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")

    inventory.remove(item_id)
    character["inventory"] = inventory
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    return item_id in character.get("inventory", [])



def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    return character.get("inventory", []).count(item_id)


def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    current_inventory = character.get("inventory", [])
    return max(0, MAX_INVENTORY_SIZE - len(current_inventory))

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    removed_items = character.get("inventory", []).copy()  # Save current items
    character["inventory"] = []  # Clear inventory
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # Check if item exists in inventory
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"{character['name']} does not have item '{item_id}'.")

    # Validate item type
    item_info = item_data.get(item_id)
    if not item_info:
        raise InvalidItemTypeError(f"Item '{item_id}' data not found.")
    if item_info.get("type") != "consumable":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a consumable.")

    # Parse effect
    effect_str = item_info.get("effect", "")
    if ":" not in effect_str:
        raise InvalidItemTypeError(f"Item effect format invalid: '{effect_str}'")

    stat_name, value_str = effect_str.split(":", 1)
    stat_name = stat_name.strip().lower()
    try:
        value = int(value_str.strip())
    except ValueError:
        raise InvalidItemTypeError(f"Effect value is not an integer: '{value_str}'")

    # Apply effect
    if stat_name not in character:
        raise InvalidItemTypeError(f"Character has no stat '{stat_name}'")
    
    if stat_name == "health":
        max_health = character.get("max_health", 0)
        old_health = character["health"]
        character["health"] = min(max_health, old_health + value)
        actual_healed = character["health"] - old_health
        result_msg = f"{character['name']} used {item_info.get('name', item_id)} and restored {actual_healed} HP."
    else:
        character[stat_name] = character.get(stat_name, 0) + value
        result_msg = f"{character['name']} used {item_info.get('name', item_id)} and gained {value} {stat_name}."

    # Remove item from inventory
    character["inventory"].remove(item_id)

    return result_msg

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # Check if character has the weapon
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"{character['name']} does not have weapon '{item_id}' in inventory.")

    # Validate item type
    item_info = item_data.get(item_id)
    if not item_info or item_info.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon.")

    # Unequip current weapon if exists
    result_msg = ""
    if "equipped_weapon" in character and character["equipped_weapon"]:
        old_weapon_id = character["equipped_weapon"]
        old_weapon_info = item_data.get(old_weapon_id, {})
        effect_str = old_weapon_info.get("effect", "")
        if ":" in effect_str:
            stat_name, value_str = effect_str.split(":", 1)
            stat_name = stat_name.strip().lower()
            try:
                value = int(value_str.strip())
            except ValueError:
                value = 0
            # Remove old weapon bonus
            if stat_name in character:
                character[stat_name] -= value
        # Add old weapon back to inventory
        character["inventory"].append(old_weapon_id)
        result_msg += f"Unequipped {old_weapon_info.get('name', old_weapon_id)}. "

    # Apply new weapon effect
    effect_str = item_info.get("effect", "")
    if ":" in effect_str:
        stat_name, value_str = effect_str.split(":", 1)
        stat_name = stat_name.strip().lower()
        try:
            value = int(value_str.strip())
        except ValueError:
            value = 0
        if stat_name in character:
            character[stat_name] += value

    # Set equipped weapon and remove from inventory
    character["equipped_weapon"] = item_id
    character["inventory"].remove(item_id)

    result_msg += f"Equipped {item_info.get('name', item_id)}."
    return result_msg

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "health:10" or similar
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"{character['name']} does not have armor '{item_id}' in inventory.")

    info = item_data.get(item_id)
    if not info or info.get("type") != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor.")

    # Unequip current armor if exists
    result_msg = ""
    if "equipped_armor" in character and character["equipped_armor"]:
        old_armor = character["equipped_armor"]
        old_info = item_data.get(old_armor, {})
        effect_str = old_info.get("effect", "")
        if ":" in effect_str:
            stat, val = effect_str.split(":")
            stat = stat.strip().lower()
            val = int(val.strip())
            if stat in character:
                character[stat] -= val
        character["inventory"].append(old_armor)
        result_msg += f"Unequipped {old_info.get('name', old_armor)}. "

    # Apply new armor effect
    effect_str = info.get("effect", "")
    if ":" in effect_str:
        stat, val = effect_str.split(":")
        stat = stat.strip().lower()
        val = int(val.strip())
        if stat in character:
            character[stat] += val

    # Equip new armor
    character["equipped_armor"] = item_id
    character["inventory"].remove(item_id)

    result_msg += f"Equipped {info.get('name', item_id)}."
    return result_msg

def unequip_weapon(character, item_data=None, max_inventory_size=MAX_INVENTORY_SIZE):
    """
    Remove equipped weapon and return it to inventory
    """
    equipped_weapon = character.get("equipped_weapon")
    if not equipped_weapon:
        return None  # Nothing to unequip

    # Check inventory space
    if len(character.get("inventory", [])) >= max_inventory_size:
        raise InventoryFullError("Cannot unequip weapon: inventory is full.")

    # Remove weapon bonuses if item_data provided
    if item_data and equipped_weapon in item_data:
        effect_str = item_data[equipped_weapon].get("effect", "")
        if ":" in effect_str:
            stat_name, value_str = effect_str.split(":", 1)
            stat_name = stat_name.strip().lower()
            try:
                value = int(value_str.strip())
            except ValueError:
                value = 0
            if stat_name in character:
                character[stat_name] -= value

    # Add weapon back to inventory
    character.setdefault("inventory", []).append(equipped_weapon)

    # Clear equipped weapon
    character["equipped_weapon"] = None

    return equipped_weapon

def unequip_armor(character,item_data=None, max_inventory_size=MAX_INVENTORY_SIZE):
    """
    Remove equipped armor and return it to inventory
    
    Args:
        character: Character dictionary
        max_inventory_size: Maximum allowed inventory size
        item_data: Optional dictionary of game items to adjust stats
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    equipped_armor = character.get("equipped_armor")
    if not equipped_armor:
        return None  # Nothing to unequip

    # Check if inventory is full
    if len(character.get("inventory", [])) >= max_inventory_size:
        raise InventoryFullError("Cannot unequip armor: inventory is full.")

    # Remove armor bonuses if item_data provided
    if item_data and equipped_armor in item_data:
        effect_str = item_data[equipped_armor].get("effect", "")
        if ":" in effect_str:
            stat_name, value_str = effect_str.split(":", 1)
            stat_name = stat_name.strip().lower()
            try:
                value = int(value_str.strip())
            except ValueError:
                value = 0
            if stat_name in character:
                character[stat_name] -= value

    # Add armor back to inventory
    character.setdefault("inventory", []).append(equipped_armor)

    # Clear equipped armor
    character["equipped_armor"] = None

    return equipped_armor

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
        max_inventory_size: Maximum allowed inventory size
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # Ensure item exists in item_data
    if item_id not in item_data:
        raise ValueError(f"Item '{item_id}' not found in item data.")

    cost = item_data[item_id].get("cost", 0)

    # Check if character has enough gold
    if character.get("gold", 0) < cost:
        raise InsufficientResourcesError(f"Not enough gold to purchase '{item_id}'.")

    # Check if inventory has space
    if len(character.get("inventory", [])) >= max_inventory_size:
        raise InventoryFullError("Cannot purchase item: inventory is full.")

    # Subtract gold
    character["gold"] -= cost

    # Add item to inventory
    character.setdefault("inventory", []).append(item_id)

    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # Check if character has the item
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"Character does not have item '{item_id}'.")

    # Ensure item exists in item_data
    if item_id not in item_data:
        raise ValueError(f"Item '{item_id}' not found in item data.")

    # Calculate sell price
    cost = item_data[item_id].get("cost", 0)
    sell_price = cost // 2

    # Remove item from inventory
    character["inventory"].remove(item_id)

    # Add gold to character
    character["gold"] = character.get("gold", 0) + sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    
    Raises: ValueError if format is invalid or value is not an integer
    """
    try:
        stat_name, value_str = effect_string.split(":")
        value = int(value_str)
        return stat_name.strip(), value
    except Exception as e:
        raise ValueError(f"Invalid effect string '{effect_string}': {e}")

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    if stat_name not in ["health", "max_health", "strength", "magic"]:
        raise ValueError(f"Invalid stat name: {stat_name}")

    # Apply the value
    character[stat_name] += value

    # Ensure health does not exceed max_health
    if stat_name == "health":
        character["health"] = min(character["health"], character["max_health"])

    # Ensure stats do not drop below 0
    if stat_name in ["health", "max_health", "strength", "magic"]:
        character[stat_name] = max(0, character[stat_name])

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    from collections import Counter

    inventory = character.get("inventory", [])
    if not inventory:
        print(f"{character['name']}'s inventory is empty.")
        return

    # Count how many of each item the character has
    item_counts = Counter(inventory)

    print(f"\n{character['name']}'s Inventory:")
    print("-" * 40)
    print(f"{'Item Name':20} {'Type':10} {'Qty':>3}")
    print("-" * 40)

    for item_id, count in item_counts.items():
        item_info = item_data_dict.get(item_id, {})
        name = item_info.get("name", item_id)
        item_type = item_info.get("type", "unknown")
        print(f"{name:20} {item_type:10} {count:>3}")

    print("-" * 40)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    test_char = {
        'name': 'Hero',
        'inventory': [],
        'gold': 100,
        'health': 70,
        'max_health': 80
    }

    test_item_data = {
        'health_potion': {
            'name': 'Health Potion',
            'type': 'consumable',
            'effect': 'health:20'
        }
    }

    # Add item to inventory
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory after adding item: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")

    # Use item
    try:
        result = use_item(test_char, "health_potion", test_item_data)
        print(result)
        print(f"Inventory after using item: {test_char['inventory']}")
        print(f"Character health: {test_char['health']}/{test_char['max_health']}")
    except ItemNotFoundError:
        print("Item not found")
    except InvalidItemTypeError as e:
        print(f"Invalid item type: {e}")

