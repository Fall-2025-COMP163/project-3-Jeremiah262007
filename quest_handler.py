"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Jeremiah Cooper

AI Usage: 
Assistance was used to design and implement quest management functionality, including accepting, completing, and abandoning quests. Guidance helped enforce quest requirements such as level restrictions, prerequisite quests, and preventing duplicate or already completed quests. Support was provided for tracking active and completed quests, calculating quest rewards (XP and gold), and generating quest statistics such as completion percentage and total rewards earned. The module also includes helper functions for displaying quest information, validating prerequisite chains, filtering quests by level, and checking quest availability. Error handling for custom exceptions like QuestNotFoundError, QuestRequirementsNotMetError, QuestAlreadyCompletedError, and QuestNotActiveError was clarified. All data validation, display formatting, and prerequisite chain logic were independently implemented.


This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    quest_info = quest_data_dict[quest_id]
    
    # Check character level
    required_level = quest_info.get("required_level", 1)
    if character.get("level", 1) < required_level:
        raise InsufficientLevelError(
            f"Character level {character.get('level',1)} is too low for quest '{quest_id}' (requires level {required_level})."
        )
    
    # Check prerequisite quest
    prerequisite = quest_info.get("prerequisite", "NONE")
    completed_quests = character.get("completed_quests", [])
    if prerequisite != "NONE" and prerequisite not in completed_quests:
        raise QuestRequirementsNotMetError(
            f"Prerequisite quest '{prerequisite}' not completed for '{quest_id}'."
        )
    
    # Check if already completed
    if quest_id in completed_quests:
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' has already been completed.")
    
    # Check if already active
    active_quests = character.setdefault("active_quests", [])
    if quest_id in active_quests:
        raise QuestRequirementsNotMetError(f"Quest '{quest_id}' is already active.")
    
    # Add quest to active quests
    active_quests.append(quest_id)
    
    return True

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest '{quest_id}' not found.")
    
    # Check quest is active
    active_quests = character.get("active_quests", [])
    if quest_id not in active_quests:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active.")
    
    quest_info = quest_data_dict[quest_id]
    
    # Remove from active_quests
    active_quests.remove(quest_id)
    
    # Add to completed_quests
    completed_quests = character.setdefault("completed_quests", [])
    completed_quests.append(quest_id)
    
    # Grant rewards
    reward_xp = quest_info.get("reward_xp", 0)
    reward_gold = quest_info.get("reward_gold", 0)
    
    # Apply rewards
    import character_manager
    character_manager.gain_experience(character, reward_xp)
    character["gold"] = character.get("gold", 0) + reward_gold
    
    # Return reward summary
    return {"xp": reward_xp, "gold": reward_gold}

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Args:
        character: Character dictionary
        quest_id: Quest to abandon
    
    Returns: True if abandoned successfully
    Raises: QuestNotActiveError if quest not active
    """
    active_quests = character.get("active_quests", [])
    
    if quest_id not in active_quests:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not active and cannot be abandoned.")
    
    # Remove quest from active quests
    active_quests.remove(quest_id)
    
    # Optionally update the character dict
    character["active_quests"] = active_quests
    
    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Args:
        character: Character dictionary
        quest_data_dict: Dictionary of all quest data
    
    Returns: List of quest dictionaries for active quests
    """
    active_quests = character.get("active_quests", [])
    active_data = []

    for quest_id in active_quests:
        quest_info = quest_data_dict.get(quest_id)
        if quest_info:
            active_data.append(quest_info)
        else:
            # Optional: warn if quest_id not found in quest_data_dict
            print(f"Warning: Quest data for '{quest_id}' not found.")

    return active_data

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests

    Args:
        character: Character dictionary
        quest_data_dict: Dictionary of all quest data

    Returns: List of quest dictionaries for completed quests
    """
    completed_quests = character.get("completed_quests", [])
    completed_data = []

    for quest_id in completed_quests:
        quest_info = quest_data_dict.get(quest_id)
        if quest_info:
            completed_data.append(quest_info)
        else:
            # Optional: warn if quest_id not found in quest_data_dict
            print(f"Warning: Quest data for '{quest_id}' not found.")

    return completed_data

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept

    Available = meets level requirement + prerequisite done + not completed + not active

    Args:
        character: Character dictionary
        quest_data_dict: Dictionary of all quest data

    Returns: List of quest dictionaries
    """
    available = []

    active_quests = set(character.get("active_quests", []))
    completed_quests = set(character.get("completed_quests", []))
    char_level = character.get("level", 1)

    for quest_id, quest_info in quest_data_dict.items():
        required_level = quest_info.get("required_level", 1)
        prerequisite = quest_info.get("prerequisite", "NONE")

        # Check level requirement
        if char_level < required_level:
            continue

        # Check prerequisite quest completed (if any)
        if prerequisite != "NONE" and prerequisite not in completed_quests:
            continue

        # Skip if quest already active or completed
        if quest_id in active_quests or quest_id in completed_quests:
            continue

        # Quest is available
        available.append(quest_info)

    return available

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed

    Args:
        character: Character dictionary
        quest_id: ID of the quest to check

    Returns: True if completed, False otherwise
    """
    completed_quests = character.get("completed_quests", [])
    return quest_id in completed_quests

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active

    Args:
        character: Character dictionary
        quest_id: ID of the quest to check

    Returns: True if active, False otherwise
    """
    active_quests = character.get("active_quests", [])
    return quest_id in active_quests

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest

    Args:
        character: Character dictionary
        quest_id: ID of the quest to check
        quest_data_dict: Dictionary of all quest data

    Returns: True if character can accept quest, False otherwise
    """
    quest = quest_data_dict.get(quest_id)
    if not quest:
        return False  # Quest does not exist

    # Check level requirement
    if character.get("level", 1) < quest.get("required_level", 1):
        return False

    # Check prerequisite quest
    prerequisite = quest.get("prerequisite", "NONE")
    if prerequisite != "NONE" and prerequisite not in character.get("completed_quests", []):
        return False

    # Check if already completed
    if quest_id in character.get("completed_quests", []):
        return False

    # Check if already active
    if quest_id in character.get("active_quests", []):
        return False

    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    chain = []
    current_id = quest_id

    while current_id != "NONE":
        quest = quest_data_dict.get(current_id)
        if not quest:
            raise QuestNotFoundError(f"Quest '{current_id}' not found in quest data.")
        
        chain.insert(0, current_id)  # Insert at beginning to build earliest → latest
        current_id = quest.get("prerequisite", "NONE")
    
    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0  # Avoid division by zero

    completed_quests = len(character.get("completed_quests", []))
    percentage = (completed_quests / total_quests) * 100
    return round(percentage, 2)  # Round to 2 decimal places for clarity

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    total_xp = 0
    total_gold = 0

    completed_quests = character.get("completed_quests", [])

    for quest_id in completed_quests:
        quest_info = quest_data_dict.get(quest_id)
        if quest_info:
            total_xp += quest_info.get("reward_xp", 0)
            total_gold += quest_info.get("reward_gold", 0)

    return {"total_xp": total_xp, "total_gold": total_gold}

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    filtered_quests = []

    for quest_id, quest_info in quest_data_dict.items():
        level_req = quest_info.get("required_level", 1)
        if min_level <= level_req <= max_level:
            filtered_quests.append(quest_info)

    return filtered_quests

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    print(f"\n=== {quest_data.get('title', 'Unknown Quest')} ===")
    print(f"Description: {quest_data.get('description', 'No description.')}")
    
    # Show rewards
    xp = quest_data.get("reward_xp", 0)
    gold = quest_data.get("reward_gold", 0)
    print(f"Rewards: {xp} XP, {gold} Gold")
    
    # Show requirements
    level_req = quest_data.get("required_level", 1)
    prereq = quest_data.get("prerequisite", "None")
    print(f"Required Level: {level_req}")
    print(f"Prerequisite Quest: {prereq}")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    if not quest_list:
        print("No quests to display.")
        return

    print("\n=== Quest List ===")
    print(f"{'Title':30} {'Level':5} {'XP':5} {'Gold':5}")
    print("-" * 50)

    for quest in quest_list:
        title = quest.get("title", "Unknown Quest")
        level = quest.get("required_level", 1)
        xp = quest.get("reward_xp", 0)
        gold = quest.get("reward_gold", 0)
        print(f"{title:30} {level:<5} {xp:<5} {gold:<5}")
    
    print("-" * 50)

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    active_count = len(character.get("active_quests", []))
    completed_count = len(character.get("completed_quests", []))
    total_quests = len(quest_data_dict)
    completion_percentage = (completed_count / total_quests * 100) if total_quests else 0

    total_xp = sum(
        quest_data_dict[qid].get("reward_xp", 0) for qid in character.get("completed_quests", [])
        if qid in quest_data_dict
    )
    total_gold = sum(
        quest_data_dict[qid].get("reward_gold", 0) for qid in character.get("completed_quests", [])
        if qid in quest_data_dict
    )

    print("\n=== Quest Progress ===")
    print(f"Active Quests   : {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Completion      : {completion_percentage:.2f}%")
    print(f"Total XP Earned : {total_xp}")
    print(f"Total Gold Earned: {total_gold}")
    print("=" * 40)

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    for quest_id, quest_info in quest_data_dict.items():
        prereq = quest_info.get("prerequisite", "NONE")
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(
                f"Quest '{quest_id}' has invalid prerequisite '{prereq}'."
            )
    return True



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

