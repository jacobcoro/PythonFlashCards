""""to add:
User can now choose deck at the start.
User can now choose quiz length
Deck is turned into a dict for the length of the session, then back to json after.
Added a converter to turn txt files into json files.
    Converter takes messy quizlet exports and makes them into local usable format,
    even if car contains linebreaks.
"""
from random import randrange
import json
import glob
import os


def deck_menu_constructor(paths):
    """arg: paths, a list of file pathnames, must be json files containing dictionaries

    Makes a list of three part tuples (number, filename, filepath)"""
    output_list = []
    counter = 1
    for path in paths:
        file_name_w_ext = os.path.basename(path)
        file_name, file_ext = os.path.splitext(file_name_w_ext)
        tup = (counter, file_name, path)
        counter += 1
        output_list.append(tup)
    return output_list


def import_quizlet_lineskip_fix(filepath, fbsep="\t", cardsep="\n"):
    """Takes a quizlet flashcard export that uses tab for card front and back, and linebreak for new card
    if a line doesnt have a tab, it's joined with a ";\n" to the line before it

    args- filepath of file to be converted,
    a choice for card front and back separation (fbsep) and for card seperation values (cardsep)

    output- writes file to same directory, using same filename but changing the extension to .json
    returns- the converted dictionary
    """
    with open(filepath) as fileobj:
        data0 = fileobj.readlines()
    # First combine all lines into a long string.
    data1 = ""
    for line1 in data0:
        data1 += line1
    # Then split by the cardsep
    data3 = data1.split(cardsep)
    # For default setting, we must rejoin the lines that were separated by a linebreak
    if cardsep == "\n":
        clean_counter = 0
        while clean_counter < len(data3):
            clean_counter = 0
            for itm0 in data3:
                if fbsep not in itm0:
                    data3[data3.index(itm0)-1] += ";\n" + data3.pop(data3.index(itm0))
                    break
                elif fbsep in itm0:
                    clean_counter += 1
    # Then cull entries with too many fbsep's
    for itm1 in data3:
        if itm1.count(fbsep) > 1:
            # Reverse replace method
            data3[data3.index(itm1)] = ";\n".join(itm1.rsplit(fbsep, 1))
    # Then separate by fbsep, culling trailing punctuation on the way
    data4 = []
    for itm2 in data3:
        if itm2 is not "" and itm2 is not "\n" and itm2 is not "":
            data4.append(itm2.split(fbsep))
    # Then clean out wrong sized items, making sure our list of paired strings lists are all len(2) pairs
    data5 = []
    for itm3 in data4:
        if len(itm3) != 2:
            print(f"Item: '{itm3}' was not included in the deck.")
        else:
            data5.append(itm3)
    # Finally make the dictionary
    data6 = dict(data5)
    # Write the dictionary to a new file with the same name, but a .json extension
    write_file_path = os.path.splitext(filepath)[0] + ".json"
    write_to_file = open(write_file_path, 'w+')
    write_to_file.write(json.dumps(data6, sort_keys=True, indent=4))
    write_to_file.close()
    return data6


def display_deck(deck_dict):
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
    initial_pairs = [pair for pair in deck_dict.items()]
    # Make use choose quiz length
    length_chosen = False
    while not length_chosen:
        quiz_length = input("Please choose how many cards you'd like to include in the quiz")
        if int(quiz_length) > 0 and int(quiz_length) < len(initial_pairs):
            length_chosen = True
    # Add as many questions to the quiz as the user had specified
    f_b_pairs = []
    while len(f_b_pairs) < int(quiz_length):
        quest_to_add = initial_pairs[randrange(len(initial_pairs))]
        if quest_to_add not in f_b_pairs:
            f_b_pairs.append(quest_to_add)
    # Cause our default mode is "f" so lets let f's backs and fronts be correct
    front = 0
    back = 1
    # And "b" will be flipped
    if quiz_direction == "b":
        front = 0
        back = 1
    score = 0
    top_score = len(f_b_pairs)
    print("\nQuiz --- Write tne answer\n----------------------------\n")
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    while len(f_b_pairs) > 0:
        # From the tuple list, select a random index,
        random_pair = f_b_pairs[randrange(0, len(f_b_pairs))]
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
            f_b_pairs.remove(random_pair)
        else:
            print("Incorrect. The correct answer is ---> '" + random_pair[back] + "'")
            f_b_pairs.remove(random_pair)
    print("End of quiz. Your score was " + str(100 * score / top_score) + "%. You got " + str(score) +
          " out of " + str(top_score) + " questions correct.")


def write_answer_quiz(deck_dict, quiz_direction):
    """
    gives a flashcard quiz where quiz taker must type in the correct answer from a choice of four

    takes two args,
    deck_dict: A dictionary of word-definition pairs
    quiz_direction: a string, "f" for front to back, and "b" for back to front """
    # Converts dict into list of key/value tuples
    initial_pairs = [pair for pair in deck_dict.items()]
    # Make use choose quiz length
    length_chosen = False
    while not length_chosen:
        quiz_length = input("Please choose how many cards you'd like to include in the quiz")
        if int(quiz_length) > 0 and int(quiz_length) < len(initial_pairs):
            length_chosen = True
    # Add as many questions to the quiz as the user had specified
    f_b_pairs = []
    while len(f_b_pairs) < int(quiz_length):
        quest_to_add = initial_pairs[randrange(len(initial_pairs))]
        if quest_to_add not in f_b_pairs:
            f_b_pairs.append(quest_to_add)
    # Cause our default mode is "f" so lets let f's backs and fronts be correct
    front = 0
    back = 1
    # And "b" will be flipped
    if quiz_direction == "b":
        front = 0
        back = 1
    score = 0
    top_score = len(f_b_pairs)
    print("\nQuiz --- Write tne answer\n----------------------------\n")
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    while f_b_pairs:
        # From the tuple list, select a random index, and the 0th value of that (which is the card front)
        random_pair = f_b_pairs[randrange(0, len(f_b_pairs))]
        guess = input(random_pair[front] + ": ")
        if guess == random_pair[back]:
            print("Correct!")
            score += 1
            f_b_pairs.remove(random_pair)
        else:
            print("Incorrect. The correct answer is ---> '" + random_pair[back] + "'")
            f_b_pairs.remove(random_pair)
    print("End of quiz. Your score was " + str(100 * score / top_score) + "%. You got " + str(score) + " out of "
          + str(top_score) + " questions correct.")


def self_report_quiz(deck_dict, quiz_direction):
    """
    gives a flashcard quiz where quiz taker guesses the word and records him/herself
    whether the right answer was raised

    takes two args,
    deck_dict: A dictionary of word-definition pairs
    quiz_direction: a string, "f" for front to back, and "b" for back to front """

    # Converts dict into list of key/value tuples
    initial_pairs = [pair for pair in deck_dict.items()]
    # Make use choose quiz length
    length_chosen = False
    while not length_chosen:
        quiz_length = input("Please choose how many cards you'd like to include in the quiz")
        if int(quiz_length) > 0 and int(quiz_length) < len(initial_pairs):
            length_chosen = True
    # Add as many questions to the quiz as the user had specified
    f_b_pairs = []
    while len(f_b_pairs) < int(quiz_length):
        quest_to_add = initial_pairs[randrange(len(initial_pairs))]
        if quest_to_add not in f_b_pairs:
            f_b_pairs.append(quest_to_add)
    # Cause our default mode is "f" so lets let f's backs and fronts be correct
    front = 0
    back = 1
    # And "b" will be flipped
    if quiz_direction == "b":
        front = 0
        back = 1
    score = 0
    top_score = len(f_b_pairs)
    print("\nQuiz --- Self report\n----------------------------\n")
    # Front to back. Display front of card(key) in prompt, and answer must be its value
    while len(f_b_pairs) > 0:
        # From the tuple list, select a random index, and the 0th value of that (which is the card front)
        random_pair = f_b_pairs[randrange(0, len(f_b_pairs))]
        response = input(random_pair[front] + "\nInput any key to show answer:")
        stop = False
        while len(response) >= 0 and not stop:
            correct_or_not = input("The answer is---> " + random_pair[back] + "\nDid you guess correctly? "
                                                                              "Answer y for yes and n for no: \n")
            if correct_or_not == "y":
                score += 1
                f_b_pairs.remove(random_pair)
                stop = True
            elif correct_or_not == "n":
                f_b_pairs.remove(random_pair)
                stop = True
            else:
                print("Incorrect input.")
    print("End of quiz. Your score was " + str(100 * score / top_score) + "%. You got " + str(score) +
          " out of " + str(top_score) + " questions correct.")

program_directory = "/Users/chenlu/PycharmProjects/experiments1/Flashcards_0.1/"
welcome = """
      Welcome to

^_^   Flashcards   ^_^
"""


menu = """\nmenu:

1. View deck
2. Add item
3. Delete item
4. Quiz yourself
5. Switch decks
6. Import and convert decks
7. Quit

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
running1 = True
while running1:
    # Find all json files in local directory, decks will be a list of their paths
    decks = glob.glob(program_directory + "*.json")
    numbered_paths_and_names = deck_menu_constructor(decks)
    # makes a variable to hold the list of deck names with a given number starting at 1
    decks_choice_display = ""
    for name_path_tup in numbered_paths_and_names:
        decks_choice_display += str(name_path_tup[0]) + ") " + str(name_path_tup[1]) + "\n"
    # Deck choice menu prompt
    deck_choice = input(f"Please choose a deck: \n{decks_choice_display}")
    # The number the user enters will be 1 more than the index for the tuple where the path is the 2th entry
    file_to_open = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'r')
    deck = json.loads(file_to_open.read())
    file_to_open.close()
    running2 = True
    while running2:
        menu_choice = input(menu)
        if menu_choice == "1":
            print(f"\nCurrent deck:\n{display_deck(deck)} \n")
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
                print(f"Removed {remove} ---> {deck[remove]}")
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
            # Before switching to a new deck, or when closing the session, write the changes.
            file_to_write = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'w+')
            file_to_write.write(json.dumps(deck, sort_keys=True, indent=4))
            file_to_write.close()
            running2 = False
        elif menu_choice == "6":
            # Find all txt files in local directory, txts variable will be a list of their paths
            txts = glob.glob(program_directory + "*.txt")
            numbered_paths_and_names1 = deck_menu_constructor(txts)
            # makes a variable to hold the list of file names with a given number starting at 1
            files_choice_display = ""
            for name_path_tup in numbered_paths_and_names1:
                files_choice_display += str(name_path_tup[0]) + ") " + str(name_path_tup[1]) + "\n"
            # File choice menu prompt
            file_choice = input(f"Please choose a file: \n{files_choice_display}")
            is_quizlet = input("Is the file a Quizlet export or in the Quizlet export format?"
                               "\nEnter y for yes or n for no: ")
            if is_quizlet == "y":
                is_default = input("Did you export using the default Quizlet export?\n"
                                   "Separating cards with spaces and card front and backs with tabs?")
                if is_default == "y":
                    # The number the user enters will be 1 more than the index for the
                    # tuple where the path is the 2th entry
                    if numbered_paths_and_names1[int(file_choice) - 1][2] in program_directory:
                        overwrite = input("File already exists. Overwrite?"
                                          "\nEnter y for yes or n for no: ")
                        if overwrite == "y":
                            print("Importing...")
                            import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2])
                    else:
                        print("Importing...")
                        import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2])
                else:
                    ask_fbsep = input("Please input the separator you used between card fronts and backs: ")
                    ask_cardsep = input("Please input the separator you used between cards: ")
                    print("Importing...")
                    import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2], fbsep=ask_fbsep, cardsep=ask_cardsep)
            else:
                print("Unsupported file type.")
        elif menu_choice == "7":
            print("Thanks for playing, see you next time!")
            # Before switching to a new deck, or when closing the session, write the changes.
            file_to_write = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'w+')
            file_to_write.write(json.dumps(deck, sort_keys=True, indent=4))
            file_to_write.close()
            running1 = False
            running2 = False
        else:
            print("Invalid entry")