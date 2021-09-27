import sys

from lib import emailsvc
from lib import store_allocation

if __name__ == "__main__":
    # Request the allocation file name
    filename = input("Please enter the name of the allocation file: ")

    # Get the old allocations from allocations.ssalloc
    if filename:
        allocations = store_allocation.decode_data(filename)
    else:
        allocations = store_allocation.decode_data()

    print(allocations)

    # Print the names of all players and their email addresses
    print("Current players:")
    for name, data in allocations.items():
        print(name, ":", data["email"])

    # Request a player name
    player_name = input("Please enter the name of the player: ")
    # Request a new email address
    new_email = input("Please enter the new email address: ")

    # Change the email address for the player
    allocations[player_name]["email"] = new_email

    # Email the player who has changed their email address
    emailsvc.email_people({player_name:allocations[player_name]})

    # Write the new allocations to allocations.ssalloc
    if filename:
        new_allocation_str = store_allocation.encode_data(allocations, "new_{}".format(filename))
    else:
        new_allocation_str = store_allocation.encode_data(allocations, "new_allocations")
    
    # Backup allocations in the Secret Santa email address
    emailsvc.send_allocations(new_allocation_str)
