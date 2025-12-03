# **Quest Chronicles – README**

**By: Jeremiah Cooper**
**Date: 12/2/25** 

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

During the development of **Quest Chronicles**, I utilized AI assistance from ChatGPT to support multiple aspects of the project, primarily for conceptual understanding, debugging, code organization, and documentation. The assistance provided was structured, guided, and served as a learning tool rather than replacing any coding work.  

### **1. Understanding Coding Logic**

ChatGPT helped me:

* **Break down complex modules** – For example, the `quest_handler.py` and `combat_system.py` contain multiple interdependent functions and exceptions. AI guidance helped me understand the flow of:
  - How quests are accepted, completed, and tracked  
  - How prerequisites are validated  
  - How combat actions interact with character stats and abilities

* **Clarify exception handling** – By explaining **why and when specific exceptions are raised**, I gained a better understanding of the underlying game logic, such as:
  - `InsufficientLevelError` ensures that a character cannot bypass progression  
  - `QuestRequirementsNotMetError` enforces logical quest order  
  - `AbilityOnCooldownError` maintains fair combat mechanics  

* **Reinforce debugging practices** – AI suggested structured strategies for checking character dictionaries, validating input data, and verifying function outputs step by step. This strengthened my ability to reason through errors systematically.

---

### **2. Code Organization and Best Practices**

AI assisted in:

* **Module structuring** – Helping separate systems into self-contained files (`character_manager.py`, `quest_handler.py`, `combat_system.py`, `inventory_system.py`) and explaining the benefits of modularity for readability, testing, and scalability.
* **Naming conventions and function clarity** – Suggested meaningful function and variable names to improve readability and maintainability.
* **Dictionary-based design justification** – Reinforced why using dictionaries for characters, quests, and enemies made debugging easier and aligned with course expectations.

---

### **3. Documentation and README Development**

ChatGPT guided me in creating a **comprehensive, GitHub-ready README** that includes:

* Clear explanations of **module responsibilities**
* Detailed **exception strategy**, explaining when and why errors are raised
* Step-by-step **How to Play instructions**
* Tables and lists for readability and structured presentation
* Professional styling suitable for submission and sharing

The AI helped turn technical details into accessible language while maintaining accuracy, ensuring that both code and documentation demonstrate a deep understanding of the project.

---

### **4. Learning and Problem Solving**

The assistance went beyond simply providing solutions:

* AI prompted me to think critically about game mechanics and logic sequencing.  
* Encouraged me to reason through prerequisites and dependencies in quests.  
* Helped me verify edge cases, such as handling empty quest lists or invalid actions.  
* Provided iterative feedback on formatting, organization, and clarity for both code and documentation.

---

### **Summary**

ChatGPT acted as a **learning partner and guide**, not a replacement for my work. It helped me:

* Deepen my understanding of Python logic and modular programming  
* Refine code structure and exception handling  
* Create professional, polished documentation  
* Develop reasoning skills for debugging and problem solving  

All final game logic, implementations, and testing were completed independently, ensuring that I fully grasped every aspect of the project.

---

# **How to Play**

## **1. Running the Game**

From the project directory, run:

```bash
python3 main.py

# **2. Main Menu Options**
Start New Game – Create a character and begin playing.
Load Game – Load an existing save (if implemented).
View Character – Display stats, level, XP, gold.
Enter Combat – Fight enemies and earn rewards.
Manage Inventory – Use or add items.
Quest Menu – Accept or complete quests.
Quit Game – Exit safely.

---

# **3. Combat Overview**
Pick attacks or abilities
Manage cooldowns
Defeat enemies for XP and gold

---

# **4. Quests**
Accept quests from the quest list
Fulfill objectives
Earn gold and XP rewards

---

# **5. Inventory**
Use healing items and consumables
Check storage capacity
Add new items as rewards
