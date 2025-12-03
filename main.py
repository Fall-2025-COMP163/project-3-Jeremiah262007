"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Jeremiah Cooper

AI Usage:
Assistance was used to structure the main game flow, integrating modules for character management, inventory, quests, combat, and game data. Guidance helped implement menus for starting a new game, loading saved games, and navigating in-game actions (viewing stats, managing inventory, quests, exploring, and shopping). Support included handling user input validation, orchestrating game loops, saving/loading game state, and implementing character death and revival logic. Error handling for custom exceptions such as InvalidCharacterClassError, CharacterNotFoundError, and SaveFileCorruptedError was clarified. All menu interactions, helper functions, and integration logic were independently implemented.


This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
Display main menu and get player choice
Options:
1. New Game
2. Load Game
3. Exit

Returns: Integer choice (1-3)
"""
    while True:
        print("\n=== Main Menu ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
    
        choice = input("Enter your choice (1-3): ").strip()
    
        if choice in {"1", "2", "3"}:
            return int(choice)
        else:
            print("Invalid input. Please enter 1, 2, or 3.")  
    

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character

     # Get character name
    name = input("Enter your character's name: ").strip()

    # Get character class
    while True:
        print("Choose your class:")
        print("1. Warrior")
        print("2. Mage")
        print("3. Rogue")
        print("4. Cleric")
        class_choice = input("Enter the number corresponding to your class: ").strip()
        class_map = {"1": "Warrior", "2": "Mage", "3": "Rogue", "4": "Cleric"}
        if class_choice in class_map:
            char_class = class_map[class_choice]
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    # Create character (handle exceptions if needed)
    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"Character '{name}' the {char_class} has been created!")
    except InvalidCharacterClassError as e:
        print(f"Error creating character: {e}")
        return

    # Start the game loop (stub)
    # game_loop(current_character)


def load_game():
    """
    Load an existing saved game.

    Shows list of saved characters and prompts user to select one.
    """
    global current_character

    # Get list of saved characters
    saved_characters = character_manager.list_saved_characters()
    if not saved_characters:
        print("No saved characters found.")
        return

    # Display saved characters
    print("\nSaved Characters:")
    for idx, char_name in enumerate(saved_characters, 1):
        print(f"{idx}. {char_name}")

    # Get user choice
    while True:
        choice = input("Enter the number of the character to load: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(saved_characters):
            selected_name = saved_characters[int(choice) - 1]
            break
        else:
            print(f"Invalid choice. Enter a number between 1 and {len(saved_characters)}.")

    # Load character
    try:
        current_character = character_manager.load_character(selected_name)
        print(f"Character '{selected_name}' loaded successfully!")
    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"Error loading character: {e}")
        return

    # Start the game loop (stub)
    # game_loop(current_character)

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character

    if not current_character:
        print("No character loaded. Start a new game or load a saved game first.")
        return

    game_running = True

    while game_running:
        # Display game menu
        print("\n=== Game Menu ===")
        print("1. View Character")
        print("2. Inventory")
        print("3. Quests")
        print("4. Explore / Battle")
        print("5. Save Game")
        print("6. Exit to Main Menu")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            # Display character stats
            character_manager.display_character(current_character)
        elif choice == "2":
            # Display inventory
            display_inventory(current_character, item_data)
        elif choice == "3":
            # Display quests (stub)
            print("Quest log is under construction.")
        elif choice == "4":
            # Explore / battle (stub)
            print("Exploration and battles are under construction.")
        elif choice == "5":
            # Save character
            try:
                character_manager.save_character(current_character)
                print(f"Character '{current_character['name']}' saved successfully.")
            except Exception as e:
                print(f"Error saving character: {e}")
        elif choice == "6":
            print("Exiting to main menu...")
            game_running = False
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

def game_menu():
    """
    Display game menu and get player choice

    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit

    Returns: Integer choice (1-6)
    """
    while True:
        print("\n=== Game Menu ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice in {"1", "2", "3", "4", "5", "6"}:
            return int(choice)
        else:
            print("Invalid input. Please enter a number between 1 and 6.")
# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character

    if not current_character:
        print("No character loaded.")
        return

    print("\n=== Character Stats ===")
    print(f"Name: {current_character.get('name', 'Unknown')}")
    print(f"Class: {current_character.get('class', 'Unknown')}")
    print(f"Level: {current_character.get('level', 1)}")
    print(f"XP: {current_character.get('xp', 0)}")
    print(f"Health: {current_character.get('health', 0)}/{current_character.get('max_health', 0)}")
    print(f"Strength: {current_character.get('strength', 0)}")
    print(f"Magic: {current_character.get('magic', 0)}")
    print(f"Gold: {current_character.get('gold', 0)}")

    # Show equipped items
    equipped_weapon = current_character.get("equipped_weapon")
    equipped_armor = current_character.get("equipped_armor")
    print(f"Weapon: {equipped_weapon if equipped_weapon else 'None'}")
    print(f"Armor: {equipped_armor if equipped_armor else 'None'}")

    # Optionally, show quest progress if quest_handler is available
    if "quests" in current_character:
        print("\nActive Quests:")
        for quest_id, status in current_character["quests"].items():
            print(f"- {quest_id}: {status}")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items

    if not current_character:
        print("No character loaded.")
        return

    while True:
        print("\n=== Inventory ===")
        # Display inventory using the inventory system helper
        inventory_system.display_inventory(current_character, all_items)

        print("\nOptions:")
        print("1. Use Item")
        print("2. Equip Weapon")
        print("3. Equip Armor")
        print("4. Drop Item")
        print("5. Return to Game Menu")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            item_id = input("Enter the ID of the item to use: ").strip()
            try:
                result = inventory_system.use_item(current_character, item_id, all_items)
                print(result)
            except (ItemNotFoundError, InvalidItemTypeError) as e:
                print(f"Error: {e}")

        elif choice == "2":
            item_id = input("Enter the ID of the weapon to equip: ").strip()
            try:
                result = inventory_system.equip_weapon(current_character, item_id, all_items)
                print(result)
            except (ItemNotFoundError, InvalidItemTypeError) as e:
                print(f"Error: {e}")

        elif choice == "3":
            item_id = input("Enter the ID of the armor to equip: ").strip()
            try:
                result = inventory_system.equip_armor(current_character, item_id, all_items)
                print(result)
            except (ItemNotFoundError, InvalidItemTypeError) as e:
                print(f"Error: {e}")

        elif choice == "4":
            item_id = input("Enter the ID of the item to drop: ").strip()
            try:
                inventory_system.remove_item_from_inventory(current_character, item_id)
                print(f"Dropped {item_id}.")
            except ItemNotFoundError as e:
                print(f"Error: {e}")

        elif choice == "5":
            break
        else:
            print("Invalid choice. Please enter 1-5.")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests

    if not current_character:
        print("No character loaded.")
        return

    while True:
        print("\n=== Quest Menu ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (testing)")
        print("7. Back to Game Menu")

        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                active = quest_handler.list_active_quests(current_character)
                if active:
                    print("\nActive Quests:")
                    for q in active:
                        print(f"- {q['name']}: {q['description']} (Progress: {q.get('progress', 0)}%)")
                else:
                    print("No active quests.")

            elif choice == "2":
                available = quest_handler.list_available_quests(current_character)
                if available:
                    print("\nAvailable Quests:")
                    for q in available:
                        print(f"- {q['name']}: {q['description']}")
                else:
                    print("No quests available at the moment.")

            elif choice == "3":
                completed = quest_handler.list_completed_quests(current_character)
                if completed:
                    print("\nCompleted Quests:")
                    for q in completed:
                        print(f"- {q['name']}")
                else:
                    print("No quests completed yet.")

            elif choice == "4":
                quest_id = input("Enter the ID of the quest to accept: ").strip()
                quest_handler.accept_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' accepted!")

            elif choice == "5":
                quest_id = input("Enter the ID of the quest to abandon: ").strip()
                quest_handler.abandon_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' abandoned.")

            elif choice == "6":
                quest_id = input("Enter the ID of the quest to complete (testing): ").strip()
                quest_handler.complete_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' marked as completed!")

            elif choice == "7":
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        except Exception as e:
            print(f"Error: {e}")

def explore():
    """Find and fight random enemies"""
    global current_character

    if not current_character:
        print("No character loaded.")
        return

    print("\nExploring the area...")

    try:
        # Generate enemy based on character level
        char_level = current_character.get("level", 1)
        enemy_level = max(1, char_level + random.randint(-1, 2))  # Enemy level varies a bit
        enemy = combat_system.generate_enemy(level=enemy_level)

        print(f"You encountered a {enemy['name']} (Level {enemy['level']})!")

        # Start combat
        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start()

        # Handle combat results
        if result == "victory":
            xp_gain = enemy.get("xp_reward", 0)
            gold_gain = enemy.get("gold_reward", 0)
            current_character["xp"] = current_character.get("xp", 0) + xp_gain
            current_character["gold"] = current_character.get("gold", 0) + gold_gain
            print(f"You defeated the {enemy['name']}! Gained {xp_gain} XP and {gold_gain} gold.")
        elif result == "defeat":
            print("You were defeated! Returning to town...")
            current_character["health"] = max(1, current_character.get("health", 1))  # prevent death for now
        else:
            print("Combat ended unexpectedly.")

    except Exception as e:
        print(f"Error during exploration: {e}")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items

    if not current_character:
        print("No character loaded.")
        return

    while True:
        print("\n=== Shop ===")
        print(f"Gold: {current_character.get('gold', 0)}")
        print("Available items:")

        # Display all items for purchase
        for item_id, info in all_items.items():
            cost = info.get("cost", 0)
            name = info.get("name", item_id)
            print(f"- {name} (ID: {item_id}) - {cost} gold")

        print("\nOptions:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Exit Shop")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            item_id = input("Enter the ID of the item to buy: ").strip()
            try:
                inventory_system.purchase_item(current_character, item_id, all_items)
                print(f"Purchased {all_items[item_id].get('name', item_id)}!")
            except (inventory_system.InsufficientResourcesError, inventory_system.InventoryFullError) as e:
                print(f"Cannot purchase item: {e}")
            except KeyError:
                print(f"Item '{item_id}' does not exist.")

        elif choice == "2":
            if not current_character.get("inventory"):
                print("Your inventory is empty. Nothing to sell.")
                continue

            print("\nYour inventory:")
            inventory_system.display_inventory(current_character, all_items)

            item_id = input("Enter the ID of the item to sell: ").strip()
            try:
                gold_received = inventory_system.sell_item(current_character, item_id, all_items)
                print(f"Sold {item_id} for {gold_received} gold.")
            except inventory_system.ItemNotFoundError as e:
                print(f"Cannot sell item: {e}")
            except KeyError:
                print(f"Item '{item_id}' does not exist.")

        elif choice == "3":
            print("Exiting shop...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character

    if not current_character:
        print("No character loaded. Nothing to save.")
        return

    try:
        character_manager.save_character(current_character)
        print(f"Game saved successfully for '{current_character.get('name', 'Unknown')}'.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    """Shop menu for buying/selling items"""
    global current_character, all_items

    if not current_character:
        print("No character loaded.")
        return

    while True:
        print("\n=== Shop ===")
        print(f"Gold: {current_character.get('gold', 0)}")
        print("Available items:")

        # Display all items for purchase
        for item_id, info in all_items.items():
            cost = info.get("cost", 0)
            name = info.get("name", item_id)
            print(f"- {name} (ID: {item_id}) - {cost} gold")

        print("\nOptions:")
        print("1. Buy Item")
        print("2. Sell Item")
        print("3. Exit Shop")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            item_id = input("Enter the ID of the item to buy: ").strip()
            try:
                inventory_system.purchase_item(current_character, item_id, all_items)
                print(f"Purchased {all_items[item_id].get('name', item_id)}!")
            except (inventory_system.InsufficientResourcesError, inventory_system.InventoryFullError) as e:
                print(f"Cannot purchase item: {e}")
            except KeyError:
                print(f"Item '{item_id}' does not exist.")

        elif choice == "2":
            if not current_character.get("inventory"):
                print("Your inventory is empty. Nothing to sell.")
                continue

            print("\nYour inventory:")
            inventory_system.display_inventory(current_character, all_items)

            item_id = input("Enter the ID of the item to sell: ").strip()
            try:
                gold_received = inventory_system.sell_item(current_character, item_id, all_items)
                print(f"Sold {item_id} for {gold_received} gold.")
            except inventory_system.ItemNotFoundError as e:
                print(f"Cannot sell item: {e}")
            except KeyError:
                print(f"Item '{item_id}' does not exist.")

        elif choice == "3":
            print("Exiting shop...")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.")

def handle_character_death():
    """Handle character death"""
    global current_character, game_running

    if not current_character:
        print("No character loaded.")
        return

    print(f"\n{current_character.get('name', 'Your character')} has fallen in battle!")

    while True:
        print("\nOptions:")
        print("1. Revive (costs 50 gold)")
        print("2. Quit to Main Menu")

        choice = input("Enter your choice (1-2): ").strip()

        if choice == "1":
            if current_character.get("gold", 0) >= 50:
                current_character["gold"] -= 50
                try:
                    character_manager.revive_character(current_character)
                    print(f"{current_character['name']} has been revived!")
                    return  # Resume game
                except Exception as e:
                    print(f"Revive failed: {e}")
                    return
            else:
                print("Not enough gold to revive.")
        elif choice == "2":
            print("Exiting to main menu...")
            game_running = False
            return
        else:
            print("Invalid choice. Please enter 1 or 2.")

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

