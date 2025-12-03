# **Quest Chronicles – README**

## **Module Architecture**

This project is organized into modular Python files, each responsible for a separate part of the game. This structure improves readability, testing, and scalability.

---

## **1. `main.py`**

Central entry point of the game.  
Handles:

* Main menu navigation
* Character creation/loading
* Starting combat, quests, and inventory interactions
* Coordinating all modules

---

## **2. `custom_exceptions.py`**

Defines all custom exceptions used across the game.  
Exception categories include:

* Game errors
* Data errors
* Character errors
* Combat errors
* Quest errors
* Inventory errors
* Save/load errors

This structure allows consistent and clean error handling.

---

## **3. `character_manager.py`**

Manages all character-related actions:

* Creating characters
* Leveling up and XP progression
* Stat management
* Displaying character information

---

## **4. `combat_system.py`**

Implements all turn‑based combat mechanics:

* Enemy creation
* Turn handling
* Ability usage and cooldowns
* Damage calculations
* Win/lose conditions

---

## **5. `inventory_system.py`**

Responsible for:

* Adding/removing items
* Using items
* Capacity management
* Validating item types

Raises clear exceptions for missing items, invalid types, or full inventories.

---

## **6. `quest_handler.py`**

Controls the entire quest system:

* Accepting quests
* Completing quests
* Tracking available, active, and completed quests
* Granting rewards
* Checking prerequisites

---

# **Exception Strategy**

The project uses a robust, module-specific exception hierarchy to ensure consistent, predictable error handling. Each module raises errors within its own domain to maintain logical game flow.

### **When and Why Exceptions Are Raised**

* **Invalid Data**  
  - `InvalidDataFormatError`: Raised when loading malformed or corrupted files. Prevents crashes and ensures data integrity.

* **Character Issues**  
  - `CharacterDeadError`: Raised when attempting actions with a dead character. Ensures game rules are respected.  
  - `InsufficientLevelError`: Raised when attempting quests or actions above the character’s level. Guides progression.

* **Combat Problems**  
  - `InvalidTargetError`: Raised when attacking invalid or nonexistent targets.  
  - `AbilityOnCooldownError`: Raised when using abilities still on cooldown.  
  - `CombatNotActiveError`: Raised when performing combat actions outside of an active battle.

* **Quest System Errors**  
  - `QuestNotFoundError`: Raised when referencing a non-existent quest.  
  - `QuestRequirementsNotMetError`: Raised when prerequisites are not fulfilled.  
  - `QuestAlreadyCompletedError`: Raised when accepting a quest already completed.  
  - `QuestNotActiveError`: Raised when attempting to complete or abandon inactive quests.

* **Inventory Errors**  
  - `InventoryFullError`: Raised when trying to add an item to a full inventory.  
  - `ItemNotFoundError`: Raised when using or removing items not in inventory.  
  - `InvalidItemTypeError`: Raised when using an item inappropriately.  
  - `InsufficientResourcesError`: Raised when attempting to purchase without enough gold.

### **Benefits**

* Provides clear feedback to players
* Keeps modules isolated and logic consistent
* Simplifies debugging and maintenance
* Ensures predictable gameplay flow

---

# **Design Choices**

### **1. Dictionary-Based Models**

Characters, enemies, and quests use dictionaries rather than classes.

* Simplifies the design
* Matches course expectations
* Easier debugging

### **2. Modular Architecture**

Each system is isolated in its own module, allowing independent development.

### **3. Custom Exception Hierarchy**

Every error inherits from a central base exception, keeping `main.py` clean.

### **4. Menu-Driven Loop**

The player always returns to a central menu for consistent flow.

### **5. Data-Driven Quests**

Quests are stored as dictionaries for easy expansion.

---

# **AI Usage Statement**

*Modify this as needed.*

Some assistance was used from ChatGPT to help debug modules, explain exceptions, improve organization, and refine code structure. All final logic, game mechanics, and implementation decisions were written, tested, and verified by me.

---

# **How to Play**

## **1. Running the Game**

From the project directory, run:

```bash
python3 main.py
