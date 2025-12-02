"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Fixed Version

Name: Jeremiah Cooper

AI Usage: [Document any AI assistance used]
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError,
    InvalidDataFormatError
)

MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    inventory = character.get("inventory", [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Cannot add '{item_id}': inventory is full.")
    inventory.append(item_id)
    character["inventory"] = inventory
    return True

def remove_item_from_inventory(character, item_id):
    inventory = character.get("inventory", [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in inventory.")
    inventory.remove(item_id)
    character["inventory"] = inventory
    return True

def has_item(character, item_id):
    return item_id in character.get("inventory", [])

def count_item(character, item_id):
    return character.get("inventory", []).count(item_id)

def get_inventory_space_remaining(character):
    return max(0, MAX_INVENTORY_SIZE - len(character.get("inventory", [])))

def clear_inventory(character):
    removed_items = character.get("inventory", []).copy()
    character["inventory"] = []
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"{character['name']} does not have item '{item_id}'.")
    item_info = item_data
    if item_info.get("type") != "consumable":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a consumable.")
    effect_str = item_info.get("effect", "")
    if ":" not in effect_str:
        raise InvalidItemTypeError(f"Item effect format invalid: '{effect_str}'")
    stat_name, value_str = effect_str.split(":", 1)
    stat_name = stat_name.strip().lower()
    try:
        value = int(value_str.strip())
    except ValueError:
        raise InvalidItemTypeError(f"Effect value is not an integer: '{value_str}'")
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
    character["inventory"].remove(item_id)
    return result_msg

def equip_weapon(character, item_id, item_data):
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"{character['name']} does not have weapon '{item_id}' in inventory.")
    item_info = item_data
    if item_info.get("type") != "weapon":
        raise InvalidItemTypeError(f"Item '{item_id}' is not a weapon.")
    result_msg = ""
    if "equipped_weapon" in character and character["equipped_weapon"]:
        old_weapon_id = character["equipped_weapon"]
        old_weapon_info = item_data if old_weapon_id == item_id else {}
        if old_weapon_info:
            stat, val = parse_item_effect(old_weapon_info.get("effect", ""))
            if stat in character:
                character[stat] -= val
        character["inventory"].append(old_weapon_id)
        result_msg += f"Unequipped {old_weapon_info.get('name', old_weapon_id)}. "
    stat, val = parse_item_effect(item_info.get("effect", ""))
    if stat in character:
        character[stat] += val
    character["equipped_weapon"] = item_id
    character["inventory"].remove(item_id)
    result_msg += f"Equipped {item_info.get('name', item_id)}."
    return result_msg

def equip_armor(character, item_id, item_data):
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"{character['name']} does not have armor '{item_id}' in inventory.")
    item_info = item_data
    if item_info.get("type") != "armor":
        raise InvalidItemTypeError(f"Item '{item_id}' is not armor.")
    result_msg = ""
    if "equipped_armor" in character and character["equipped_armor"]:
        old_armor = character["equipped_armor"]
        old_info = item_data if old_armor == item_id else {}
        if old_info:
            stat, val = parse_item_effect(old_info.get("effect", ""))
            if stat in character:
                character[stat] -= val
        character["inventory"].append(old_armor)
        result_msg += f"Unequipped {old_info.get('name', old_armor)}. "
    stat, val = parse_item_effect(item_info.get("effect", ""))
    if stat in character:
        character[stat] += val
    character["equipped_armor"] = item_id
    character["inventory"].remove(item_id)
    result_msg += f"Equipped {item_info.get('name', item_id)}."
    return result_msg

def unequip_weapon(character, item_data=None, max_inventory_size=MAX_INVENTORY_SIZE):
    weapon = character.get("equipped_weapon")
    if not weapon:
        return None
    if len(character.get("inventory", [])) >= max_inventory_size:
        raise InventoryFullError("Cannot unequip weapon: inventory is full.")
    if item_data:
        stat, val = parse_item_effect(item_data.get("effect", ""))
        if stat in character:
            character[stat] -= val
    character.setdefault("inventory", []).append(weapon)
    character["equipped_weapon"] = None
    return weapon

def unequip_armor(character, item_data=None, max_inventory_size=MAX_INVENTORY_SIZE):
    armor = character.get("equipped_armor")
    if not armor:
        return None
    if len(character.get("inventory", [])) >= max_inventory_size:
        raise InventoryFullError("Cannot unequip armor: inventory is full.")
    if item_data:
        stat, val = parse_item_effect(item_data.get("effect", ""))
        if stat in character:
            character[stat] -= val
    character.setdefault("inventory", []).append(armor)
    character["equipped_armor"] = None
    return armor

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data, max_inventory_size=MAX_INVENTORY_SIZE):
    cost = item_data.get("cost", 0)
    if character.get("gold", 0) < cost:
        raise InsufficientResourcesError(f"Not enough gold to purchase '{item_id}'.")
    if len(character.get("inventory", [])) >= max_inventory_size:
        raise InventoryFullError("Cannot purchase item: inventory is full.")
    character["gold"] -= cost
    character.setdefault("inventory", []).append(item_id)
    return True

def sell_item(character, item_id, item_data):
    if item_id not in character.get("inventory", []):
        raise ItemNotFoundError(f"Character does not have item '{item_id}'.")
    sell_price = item_data.get("cost", 0) // 2
    character["inventory"].remove(item_id)
    character["gold"] = character.get("gold", 0) + sell_price
    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    try:
        stat_name, value_str = effect_string.split(":")
        return stat_name.strip().lower(), int(value_str.strip())
    except Exception as e:
        raise ValueError(f"Invalid effect string '{effect_string}': {e}")

def apply_stat_effect(character, stat_name, value):
    if stat_name not in ["health", "max_health", "strength", "magic"]:
        raise ValueError(f"Invalid stat name: {stat_name}")
    character[stat_name] += value
    if stat_name == "health":
        character["health"] = min(character["health"], character["max_health"])
    character[stat_name] = max(0, character[stat_name])
