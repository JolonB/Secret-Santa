# People involved in Secret Santa
people = {
    "Person1": {"email": "Person1@email.com", "exclude": ("Person2", "Person4")},
    "Person2": {"email": "Person2@email.com", "exclude": ("Person1")},
    "Person3": {"email": "Person3@email.com", "exclude": ()},
    "Person4": {"email": "Person4@email.com",},
    "Person5": {"email": "Person5@email.com",},
    "Person6": {"email": "Person6@email.com",},
}

# Credentials for email sending service
email = {
    "address": "sending_address@email.com",
    "password": "password",
    "port": 465,  # this can normally be left at 465
}

# Minimum grouping size
min_grouping = 2
