# This library performs the function of assigning the people to secret santa lists
import random
from typing import Dict, List, Tuple

# Testing for storing results in memory
assigned_adults = {}
assigned_children = {}

def assign_participants(pool: Dict[int, Tuple[str, str, str]]) -> Dict[str, str]:
    """
    Assigns participants to each other while ensuring they are not assigned to family members.
    Returns a dictionary where the key is the giver's name and the value is the assigned receiver's name.
    """
    participant_ids = list(pool.keys())
    random.shuffle(participant_ids)

    assignments = {}
    for i in range(len(participant_ids)):
        # Get the current participant's details
        current_id = participant_ids[i]
        giver_name, _, family_email = pool[current_id]

        # Get the assigned participant's details (using wrap-around with %)
        assigned_id = participant_ids[(i + 1) % len(participant_ids)]
        receiver_name = pool[assigned_id][0]  # Name of the assigned participant

        # Add to assignments
        assignments[giver_name] = receiver_name

    # Verify that no one is assigned to a family member
    conflict_found = False
    for giver_name, receiver_name in assignments.items():
        # Get the family email for both the giver and the receiver
        giver_family_email = next(data[2] for id, data in pool.items() if data[0] == giver_name)
        receiver_family_email = next(data[2] for id, data in pool.items() if data[0] == receiver_name)

        if giver_family_email == receiver_family_email:
            conflict_found = True
            break

    if not conflict_found:
        return assignments
    
def run_assignments(adults: Dict[str, dict], children_data: Dict[str, dict], max_retries: int = 15):
    global assigned_adults, assigned_children
    
    for _ in range(max_retries):
        assigned_adults = assign_participants(adults)
        if assigned_adults:
            break
    else:
        raise Exception("Unable to find valid assignments after multiple attempts. Please try again.")
    for _ in range(max_retries):    
        assigned_children = assign_participants(children_data)
        if assigned_adults and assigned_children:
            return assigned_adults, assigned_children

    raise Exception("Unable to find valid assignments after multiple attempts. Please try again.")
