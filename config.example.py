# fmt: off
# People involved in Secret Santa
people = {
    "Person1": {"email": "Person1@email.com", "exclude": ("Person2", "Person4")},
    "Person2": {"email": "Person2@email.com", "exclude": ("Person1")},
    "Person3": {"email": "Person3@email.com", "exclude": ()},
    "Person4": {"email": "Person4@email.com", },
    "Person5": {"email": "Person5@email.com", },
    "Person6": {"email": "Person6@email.com", },
}

# Credentials for email sending service
email = {
    "address": "sending_address@email.com",
    "password": "password",
    "port": 465,  # this can normally be left at 465
}

# You should enable this depending on your CPU
# A dense (i.e. very few excludes) 8 person graph will take several minutes
# If is recommened that you set this to True for a graph of that size or larger
FAST_SOLVE = True

# Minimum grouping size (FAST_SOLVE==False only)
# The minimum cycle size that is allowed
min_grouping = 2

# Allow groups of 2 (when FAST_SOLVE==True)
# Similar to the min_grouping value above: True -> min_grouping=2, False -> min_grouping=3
allow_pairs = True

# Don't send emails, but print results to terminal if True
DRY_RUN = True
