# Secret Santa

## Running the Program

1. Create a copy of `config.example.py` in the root directory and name it `config.py`.
1. Fill in the details as per [People Setup](#people-setup) and [Email Setup](#email-setup).
1. Run `secret_santa.py` with `python secret_santa.py` (or `py secret_santa.py` on Windows).

### People Setup

1. Set the names and emails of people.
Add or remove them at will.
1. Each person has an optional parameter `exclude`.
Add the names of people that you don't want to give a gift to.
This is case-sensitive.
    - For instance, in `config.example.py`, Person1 will never be able to give a gift to Person2 or Person4.
    Person2 cannot give a gift to Person1.
    All other people, including Person4, can give gifts to everyone.

### Email Setup

1. Create a new Gmail account. Take a note of the password, though your friends would probably trust you not to peek if you change the password/delete the account afterwards.
1. In a browser that is logged into the new Gmail account, go to [this page](https://myaccount.google.com/lesssecureapps) and allow less secure apps.
1. Enter the email address and password into `config.py`. Don't change the port.

### Min Grouping Setup

`min_grouping` is an optional configuration setting that can be changed if desired.
By default, it is set to 2.

When you think of Secret Santa, you might think of a result like `2->4->3->6->5->1->7` (and, implicitly, `7->2`).
In real life, you may draw your giftee out of a hat, so it is entirely possible to get smaller groups of results like `2->6->3->7` and `5->4->1`.
This could occur with a minimum grouping size of less than or equal to 3, as each group contains three people.

With `min_grouping = 2`, you can get groups like `1->4`, `2->6`, and `3->7->5`, or even `1->7->3` and `2->5->6->4`.
You can also get a single grouping containing all the people.

Note that by setting `min_grouping` to a number less than 2, you will get the exact same results as setting it to 2 (as there cannot be groups of 1).
Anything greater than half the number of people, will result in only a single group containing all the people being found (because it is not possible to split the main group into sub-groups that are more than half the size).