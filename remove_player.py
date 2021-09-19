
import sys

from lib import emailsvc
from lib import store_allocation

if __name__ == "__main__":
    # Request the allocation file name
    filename = input("Enter the name of the allocation file: ")

    # Get the old allocations from allocations.ssalloc
    if filename:
        allocations_dict = store_allocation.decode_data(filename)
    else:
        # Use the default if no name is given
        allocations_dict = store_allocation.decode_data()

    # Print the names of all the players
    print("Current players:")
    print("\n".join(allocations_dict.keys()))

    # Get the name of the player to remove
    player_to_remove = input("\nEnter the name of the player to remove from the list above: ")
    while player_to_remove not in allocations_dict.keys():
        player_to_remove = input("\nThat was not a valid name. Enter the name of the player to remove: ")

    # Get the details of the person receiving the gift from the removed person
    recipient = allocations_dict[player_to_remove]["recipient"]
    # Find the person giving the gift to the removed person
    for gifter, details in allocations_dict.items():
        if details["recipient"] == player_to_remove:
            break
    
    # If the recipient and gifter are the same, warn the user
    if recipient == gifter:
        print("\nWARNING: The person giving and receiving a gift from {} are" \
            " the same person. There is currently no way to deal with this," \
            " so the best option is to reallocate everyone.".format(player_to_remove), file=sys.stderr)
        sys.exit(1)
        
    # Remove the player from the allocations and update the recipient for the gifter
    del allocations_dict[player_to_remove]
    allocations_dict[gifter]["recipient"] = recipient

    # Send an email about the removal of the player
    emailsvc.remove_person(allocations_dict, player_to_remove, recipient, gifter)

    # Write the new allocations to allocations.ssalloc
    if filename:
        new_allocation_str = store_allocation.encode_data(allocations_dict, "new_{}".format(filename))
    else:
        new_allocation_str = store_allocation.encode_data(allocations_dict, "new_allocations")

    emailsvc.send_allocations(new_allocation_str)
