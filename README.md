# Secret Santa

## Initial Setup

To begin, you need to create a virtual environment and install the dependencies.
This can be done with:

```shell
python3 -m venv venv
. venv/bin/activate
pip install -r requirements
```

## Running the Program

1. Create a copy of `config.example.py` in the root directory and name it `config.py`.
1. Fill in the details as per [People Setup](#people-setup) and [Email Setup](#email-setup).
1. Consider using the [fast solver](#fast-solver).
1. When ready, disable `DRY_RUN` in the config and run `secret_santa.py` with `python secret_santa.py` (or `py secret_santa.py` on Windows).

### People Setup

1. Set the names and emails of people in the `config.py` file you created based on the template in `config.example.py`.
Add or remove the default ones where you see fit.
This program can handle any number of players.
1. Each person has an optional parameter `exclude`.
Add the names of people that you don't want to give a gift to.
This is case-sensitive.
    - For instance, in [`config.example.py`](/config.example.py), Person1 will never be able to give a gift to Person2 or Person4.
    Person2 cannot give a gift to Person1.
    All other people, including Person4, can give gifts to everyone.

### Email Setup

1. Create a new Gmail account. Take a note of the password, though your friends would probably trust you not to peek if you change the password/delete the account afterwards. If you do change the password, you will not be able to [remove a player](#removing-players) at a later time.
1. In a browser that is logged into the new Gmail account, go to [this page](https://myaccount.google.com/lesssecureapps) and allow less secure apps. **THIS NO LONGER WORKS, see #13**
1. Enter the email address and password into `config.py`. Don't change the port unless you know what you are doing.

### Fast Solver

Although this tool was originally designed so that it would calculate *every* possible combination of Hamiltonian cycles following the `exclude` and `min_grouping` rules, it maybe isn't the best way to approach this problem.
If you try to run it with a lot of people ("a lot" == 8+ on my PC), it will start to take a noticeably long amount of time to process every cycle (understandably so, because there are `n!` cycles without even including the subgraph cycles).

To handle this issue, there is a fast solver, which can be enabled by setting `FAST_SOLVE = True` in the `config.py` file.
The fast solver doesn't attempt to calculate all of the possible Hamiltonian cycles, but rather tries to find just one random cycle/set of cycles.
It works by finding a vertex in the graph with the smallest number of outgoing edges and link to a neighbour with the smallest number of incoming edges.
This method still appears to work with the exclusion rules, however, `allow_pairs` must be configured instead of the `min_grouping` setting (see below).

And, do you wanna know the best part about it?
It looks like it works (if you allow a few *automatic* retries for the rare cases when it fails)!

### Min Grouping and Allow Pairs Setup

`min_grouping` is an optional configuration setting that can be changed if desired.
By default, it is set to 2.
It is only used if `FAST_SOLVE == False`.

When you think of Secret Santa, you might think of a result like `2->4->3->6->5->1->7` (and, implicitly, `7->2`).
In real life, you may draw your giftee out of a hat, so it is entirely possible to get smaller groups of results like `2->6->3->7` and `5->4->1`.
This could occur with a minimum grouping size of less than or equal to 3, as each group contains three people.

With `min_grouping = 2`, you can get groups like `1->4`, `2->6`, and `3->7->5`, or even `1->7->3` and `2->5->6->4`.
You can also get a single grouping containing all the people.

Note that by setting `min_grouping` to a number less than 2, you will get the exact same results as setting it to 2 (as there cannot be groups of 1).
Anything greater than half the number of people, will result in only a single group containing all the people being found (because it is not possible to split the main group into sub-groups that are more than half the size).
It can also be set to a very large integer if you want it to produce a single group regardless of the number of players.

If you are using fast solve (`FAST_SOLVE == True`), you should configure the `allow_pairs` setting.
By default, it is set to True.
This means that the solver can find sub-cycles of length 2, similar to when `min_grouping == 2`.
When set to False, the solver cannot find sub-cycles of length 2, but instead must find cycles of length 3 or more (equivalent to `min_grouping == 3`).

## Removing Players

Has there been a break-up or an unfortunate passing of someone in the game? If you think the best option is to remove that person from the game, you can do that with the `remove_player.py` script.

This will disobey some of the rules specified in your `config.py` file as it may not be able to prevent certain people from being paired up with each other without needing to completely reshuffle the allocations.
If a complete reshuffle is your preferred approach, you should just run the `secret_santa.py` script again.  
It is also possible that the reassignment to replace the missing player will result in a loop of size 1.
In this situation, you will be notified and no email will be sent.
If this happens, the recommendation is do a complete reshuffle by running `secret_santa.py` again.
