""""
My first version of a text-based flashcard program, uses only an in-program dictionary that can't be saved elsewhere.

Bugs encountered and lessons learned:
experienced the need for encapsulation by separating the quiz functions from the main game code for improved readability

Learned to examine the code for repeated aspects and simplify. Originally had a different path for each menu option
ike "f" and "b", but discovered I could make what was different into a variable and change at the start of the function.

Experienced a bug in the way my multiple choice option builder 'multidict' filled its gaps. Used print() to discover
what was happening in the for loop.
    # Discovered that without making it fill the list randomly until its full, sometimes there'd be empty spots
        # Discovered that my for loop, although not adding in the answer word, it would overwrite the location

Used while loops to keep the user guessing until a proper input has been achieved.

"""

from random import randrange

deck = {"fire": "火 huo3",
        "water": "水 shui3",
        "earth": "土 tu3",
        "air": "气 qi4",
        }


def print_deck(deck_dict):
    printout = "Front --> Back:\n\n"
    for key, value in deck_dict.items():
        printout += key + " --> " + value + "\n"
    return printout


def multiple_choice_quiz(deck_dict, quiz_direction):
    """
    gives a flashcard quiz where quiz taker must type in the correct answer

    takes two args,
    deck_dict: A dictionary of word-definition pairs, must be at least 4 terms long
    quiz_direction: a string, "f" for front to back, and "b" for back to front """

    # Converts dict into list of key/value tuples
    tuple_pair_dict = []
    for pair in deck_dict.items():
        tuple_pair_dict.append(pair)
    # Cause our default mode is "f" so lets let f's backs and fronts be correct
    front = 0
    back = 1
    # And "b" will be flipped
    if quiz_direction == "b":
        front = 0
        back = 1
    score = 0
    top_score = len(tuple_pair_dict)
    print("\nQuiz --- Write tne answer\n----------------------------\n")
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    while len(tuple_pair_dict) > 0:
        # From the tuple list, select a random index,
        random_pair = tuple_pair_dict[randrange(0, len(tuple_pair_dict))]
        # list of random card backs/fronts, including one that is the answer
        multi_dict = [" ", " ", " ", " "]
        multi_dict[randrange(0, 4)] = random_pair[back]
        answer = multi_dict.index(random_pair[back])
        # Build the list from the whole deck (to entries that might have been deleted in tuple_pair_list)
        # Generate the random index for where to insert, skip if the same as the answer index
        while multi_dict.count(" ") > 0:
            for pair in deck_dict.items():
                fill_location = randrange(0, 4)
                if pair[back] not in multi_dict:
                    if fill_location != answer and multi_dict[fill_location] == " ":
                        multi_dict[fill_location] = pair[back]
        # The 0th value of the tuple is the card front
        keep_guessing = True
        while keep_guessing:
            guess = input(random_pair[front] + ": \na) " + multi_dict[0] + "\nb) " + multi_dict[1] + "\nc) "
                          + multi_dict[2] + "\nd) " + multi_dict[3] + "\n")
            guess_test = 0
            if guess == "a":
                guess_test = 0
                keep_guessing = False
            elif guess == "b":
                guess_test = 1
                keep_guessing = False
            elif guess == "c":
                guess_test = 2
                keep_guessing = False
            elif guess == "d":
                guess_test = 3
                keep_guessing = False
            else:
                keep_guessing = True
        if guess_test == answer:
            print("Correct!")
            score += 1
            tuple_pair_dict.remove(random_pair)
        else:
            print("Incorrect. The correct answer is ---> '" + random_pair[back] + "'")
            tuple_pair_dict.remove(random_pair)
    print("End of quiz. Your score was " + str(100 * score/top_score) + "%. You got " + str(score) +
          " out of " + str(top_score) + " questions correct.")


def write_answer_quiz(deck_dict, quiz_direction):
    """
    gives a flashcard quiz where quiz taker must type in the correct answer from a choice of four

    takes two args,
    deck_dict: A dictionary of word-definition pairs
    quiz_direction: a string, "f" for front to back, and "b" for back to front """

    # Converts dict into list of key/value tuples
    tuple_pair_dict = []
    for pair in deck_dict.items():
        tuple_pair_dict.append(pair)
    # Cause our default mode is "f" so lets let f's backs and fronts be correct
    front = 0
    back = 1
    # And "b" will be flipped
    if quiz_direction == "b":
        front = 0
        back = 1
    score = 0
    top_score = len(tuple_pair_dict)
    print("\nQuiz --- Write tne answer\n----------------------------\n")
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    while len(tuple_pair_dict) > 0:
        # From the tuple list, select a random index, and the 0th value of that (which is the card front)
        random_pair = tuple_pair_dict[randrange(0, len(tuple_pair_dict))]
        guess = input(random_pair[front] + ": ")
        if guess == random_pair[back]:
            print("Correct!")
            score += 1
            tuple_pair_dict.remove(random_pair)
        else:
            print("Incorrect. The correct answer is ---> '" + random_pair[back] + "'")
            tuple_pair_dict.remove(random_pair)
    print("End of quiz. Your score was " + str(100 * score/top_score) + "%. You got " + str(score) + " out of "
          + str(top_score) + " questions correct.")


def self_report_quiz(deck_dict, quiz_direction):
    """
    gives a flashcard quiz where quiz taker guesses the word and records him/herself
    whether the right answer was raised

    takes two args,
    deck_dict: A dictionary of word-definition pairs
    quiz_direction: a string, "f" for front to back, and "b" for back to front """

    # Converts dict into list of key/value tuples
    tuple_pair_dict = []
    for pair in deck_dict.items():
        tuple_pair_dict.append(pair)

    # Cause our default mode is "f" so lets let f's backs and fronts be correct
    front = 0
    back = 1
    # And "b" will be flipped
    if quiz_direction == "b":
        front = 0
        back = 1
    score = 0
    top_score = len(tuple_pair_dict)
    print("\nQuiz --- Self report\n----------------------------\n")
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    while len(tuple_pair_dict) > 0:
        # From the tuple list, select a random index, and the 0th value of that (which is the card front)
        random_pair = tuple_pair_dict[randrange(0, len(tuple_pair_dict))]
        response = input(random_pair[front] + "\nInput any key to show answer:")
        stop = False
        while len(response) >= 0 and not stop:
            correct_or_not = input("The answer is---> " + random_pair[back] + "\nDid you guess correctly? "
                                   "Answer y for yes and n for no: \n")
            if correct_or_not == "y":
                score += 1
                tuple_pair_dict.remove(random_pair)
                stop = True
            elif correct_or_not == "n":
                tuple_pair_dict.remove(random_pair)
                stop = True
            else:
                print("Incorrect input.")
    print("End of quiz. Your score was " + str(100 * score / top_score) + "%. You got " + str(score) +
          " out of " + str(top_score) + " questions correct.")


welcome = """
      Welcome to
      
^_^   Flashcards   ^_^
"""

menu = """\nmenu:

1. View deck
2. Add item
3. Delete item
4. Quiz yourself
5. Quit

Your choice: """

test_type_prompt = """\nPlease choose quiz type:

1. Multiple choice
2. Write the answer
3. Self report

Your choice: """

front_to_back_prompt = """\nPlease choose whether you'd like to be presented with 
the front and guess the back, or vice versa:

f. See front, guess back
b. See back, guess front

your choice:"""

print(welcome)
running = True
while running:
    menu_choice = input(menu)
    if menu_choice == "1":
        print("\n" + "Current deck:\n" + print_deck(deck), "\n")
    elif menu_choice == "2":
        new_item_front = input("Please type the card front: ")
        new_item_back = input("Please type the card back: ")
        if new_item_front not in deck:
            deck[new_item_front] = new_item_back
            print("Added successfully!")
        else:
            print("Word already in deck")
    elif menu_choice == "3":
        remove = input("Please input the card front you'd like to remove: ")
        if remove in deck:
            print("Removed " + remove, "--->", deck[remove])
            del deck[remove]
        else:
            print("Word not in deck")
    elif menu_choice == "4":
        test_type = True
        while test_type:
            test_type = input(test_type_prompt)
            if test_type == "1":
                direction = input(front_to_back_prompt)
                if direction == "f" or direction == "b":
                    multiple_choice_quiz(deck, direction)
                    test_type = False
                else:
                    print("Invalid entry")
            elif test_type == "2":
                direction = input(front_to_back_prompt)
                if direction == "f" or direction == "b":
                    write_answer_quiz(deck, direction)
                    test_type = False
                else:
                    print("Invalid entry")
            elif test_type == "3":
                direction = input(front_to_back_prompt)
                if direction == "f" or direction == "b":
                    self_report_quiz(deck, direction)
                    test_type = False
                else:
                    print("Invalid entry")
            else:
                print("Invalid choice")
    elif menu_choice == "5":
        print("Thanks for playing, see you next time!")
        running = False
    else:
        print("Invalid entry")





