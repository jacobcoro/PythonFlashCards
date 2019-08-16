""""
added:
fixed bug with multiple choice game where the other three options would repeat

would still like to add:
More complex json files, that store notes and image
record words which user answered right and wrong in memory
make different quizzes into quiz class to cut down on length of functions
matching test
multitype combined quiz
"""
from random import randrange
import json
import glob
import os
import math
import copy


def import_quizlet_lineskip_fix(filepath, fbsep="\t", cardsep="\n"):
    """
    Take a Quizlet flashcard export either that by default uses tab for card front and back,
and linebreak for new card, or a custom export that uses custom characters to separate.

If a line doesnt have a tab, join with a "\n" to the line before it.

write a new file to same directory, using the same filename but changing the extension to .json

    :param str filepath: File path of file to be converted, must be a .txt file
    :param str fbsep: Separation value between front and back of card, default is tab "\t.
    :param str cardsep: Separation value between card and card, default is linebreak "\n".
    :return dict: converted dictionary.
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
                    data3[data3.index(itm0)-1] += "\n" + data3.pop(data3.index(itm0))
                    break
                elif fbsep in itm0:
                    clean_counter += 1
    # Then cull entries with too many fbsep's
    for itm1 in data3:
        if itm1.count(fbsep) > 1:
            # Reverse replace method
            data3[data3.index(itm1)] = "\n".join(itm1.rsplit(fbsep, 1))
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


def deck_menu_constructor(paths):
    """
    Takes a list of file paths and returns a three part tuple with a label number,
the truncated filename, and the file path.

    :param list paths: a list of file file paths, must be json files containing dictionaries
    :return: a list of three part tuples (number, filename, file path)
    """
    output_list = []
    counter = 1
    for path in paths:
        file_name_w_ext = os.path.basename(path)
        file_name, file_ext = os.path.splitext(file_name_w_ext)
        tup = (counter, file_name, path)
        counter += 1
        output_list.append(tup)
    return output_list


def card_displayer(card):
    """Take a string and put a box graphic around it. Returns a multiline string"""
    def grid_builder(cardstr, rowlen=80):
        """Take a string and make it into a list of items not more than rowlen long"""
        initial_grid = cardstr.split("\n")
        grid = []
        for itm in initial_grid:
            if len(itm) <= rowlen:
                grid.append(itm)
            else:
                to_grid = []
                x = 0
                times_through = 1
                while len(to_grid) < len(itm) // rowlen + 1:
                    if len(itm[x:]) > rowlen:
                        if itm[x + rowlen -1].isalpha() and itm[x + rowlen] != " ":
                            to_grid.append(itm[x: x + rowlen].lstrip() + "-")
                            x += rowlen
                        else:
                            to_grid.append(itm[x: x + rowlen].lstrip())
                            x += rowlen
                    else:
                        to_grid.append(itm[x:].lstrip())

                for itm2 in to_grid:
                    grid.append(itm2)
        return grid

    def out_put_builder(grid):
        """Put lines around strings in a grid"""
        output = ""
        longest_line = 0
        for itm3 in grid:
            if len(itm3) > longest_line:
                longest_line = len(itm3)
        top_line = '\n__' + ('_' * longest_line) + '__\n'
        empty_line = '| ' + (' ' * longest_line) + ' |\n'
        bottom_line = '|_' + ('_' * longest_line) + '_|\n'

        def text_line(column):
            white_space = longest_line - len(grid[column])
            text_lne = '| ' + (grid[column]) + " " * white_space + ' |\n'
            return text_lne

        output += top_line + empty_line
        for row in grid:
            output += text_line(grid.index(row))
        output += bottom_line
        return output

    return out_put_builder(grid_builder(card))


def display_deck(deck_dict):
    """Display all of the card pairs in the deck, separated by a '-->'."""
    printout = card_displayer("Front") + '   |\n   V' + card_displayer("Back") + '\n'
    for key, value in deck_dict.items():
        printout += card_displayer(key) + '   |\n   V' + card_displayer(value) + "\n"
    return printout


def multiple_choice_quiz(deck_dict, quiz_direction):
    """
    give a flashcard quiz where quiz taker must type in the correct answer exactly as written on the card

    :param dict deck_dict: A dictionary of word-definition pairs, must be at least 4 terms long.
    :param str quiz_direction:  "f" for front to back, and "b" for back to front.
    """
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
    print("\nQuiz --- Multiple Choice\n----------------------------\n")
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
            guess = input(card_displayer(random_pair[front]) + "\na) " + multi_dict[0] + "\nb) " + multi_dict[1] + "\nc) "
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
            multi_dict = [" ", " ", " ", " "]
        else:
            print(f"Incorrect. The correct answer is：{card_displayer(random_pair[back])}")
            f_b_pairs.remove(random_pair)
            multi_dict = [" ", " ", " ", " "]
    print(f"End of quiz. Your score was {str(round(100 * score / top_score, 2))}%. "
          f"You got {str(score)} out of {str(top_score)} questions correct.")


def write_answer_quiz(deck_dict, quiz_direction):
    """
    give a flashcard quiz where quiz taker must pick the correct answer from a choice of four.

    :param dict deck_dict: A dictionary of word-definition pairs, must be at least 4 terms long.
    :param str quiz_direction:  "f" for front to back, and "b" for back to front.
    """
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
        guess = input(card_displayer(random_pair[front]) + "\n: ")
        if guess == random_pair[back]:
            print("Correct!")
            score += 1
            f_b_pairs.remove(random_pair)
        else:
            print(f"Incorrect. The correct answer is：{card_displayer(random_pair[back])}")
            f_b_pairs.remove(random_pair)
    print(f"End of quiz. Your score was {str(round(100 * score / top_score, 2))}%. "
          f"You got {str(score)} out of {str(top_score)} questions correct.")


def self_report_quiz(deck_dict, quiz_direction):
    """
    give a flashcard quiz where quiz taker guesses the word and records him/herself whether the answer was correct.

    :param dict deck_dict: A dictionary of word-definition pairs, must be at least 4 terms long.
    :param str quiz_direction:  "f" for front to back, and "b" for back to front.
    """
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
        response = input(card_displayer(random_pair[front]) + "Input any key to show answer:")
        stop = False
        while len(response) >= 0 and not stop:
            correct_or_not = input(f"The answer is: {card_displayer(random_pair[back])} \nDid you guess correctly? "
                                   f"Answer y for yes and n for no: \n")
            if correct_or_not == "y":
                score += 1
                f_b_pairs.remove(random_pair)
                stop = True
            elif correct_or_not == "n":
                f_b_pairs.remove(random_pair)
                stop = True
            else:
                print("Incorrect input.")
    print(f"End of quiz. Your score was {str(round(100 * score / top_score, 2))}%. "
          f"You got {str(score)} out of {str(top_score)} questions correct.")


def memory_game(deck_dict):
    """
    Plays a game of 'memory'

    :param deck_dict: a dictionary containing pairs of flashcards.
    """
    # Choose cards from deck
    # Converts dict into list of key/value tuples
    initial_pairs0 = [(i for i in pair) for pair in deck_dict.items()]
    initial_pairs = [[i for i in pair] for pair in initial_pairs0]
    # Make user choose quiz length
    length_chosen = False
    while not length_chosen:
        game_length = input("Please choose how many cards you'd like to include in the game, between 5 and 24")
        if game_length.isdigit():
            if 24 >= int(game_length) >= 5 and int(game_length) < len(initial_pairs):
                length_chosen = True
        else:
            print("Please pick again")
    # Add as many questions to the quiz as the user had specified
    f_b_pairs = []
    while len(f_b_pairs) < int(game_length):
        quest_to_add = initial_pairs[randrange(len(initial_pairs))]
        if quest_to_add not in f_b_pairs:
            f_b_pairs.append(quest_to_add)
    # Calculate the board size
    # Columns_count will be width, rows_count height
    columns_count = math.floor(math.sqrt(int(game_length) * 2))
    rows_count = math.ceil((int(game_length) * 2) / columns_count)
    # Because we pop out elements of the list when filling the grid, we need to copy for later reference.
    f_b_pairs1 = copy.deepcopy(f_b_pairs)

    def grid_maker(h, w):
        grid1 = [["0" for i in range(w)] for i in range(h)]
        return grid1

    def print_grid(grid2):
        y = 0
        print("\n      columns\n      ", end="")
        for i in range(columns_count):
            # 'a' is ord(97), chr(97) is 'a'
            print(chr(97 + y), end="  ")
            y += 1
        print()
        x = 1
        for row1 in grid2:
            print("row " + str(x), end=" ")
            x += 1
            for e in row1:
                # Print a blank if the card is empty, otherwise print a square
                if e == "0":
                    print("   ", end="")
                else:
                    print("口 ", end="")
            print()

    grid = grid_maker(rows_count, columns_count)
    # Fill grid, make sure the target location is empty ("0"), pop the itm and fill till each item in the list is empty
    for itm4 in f_b_pairs:
        while len(itm4) > 0:
            target_row = randrange(rows_count)
            target_col = randrange(columns_count)
            target = grid[target_row][target_col]
            if target == "0":
                grid[target_row][target_col] = itm4.pop()

    # Start the game here
    print("Pick two cards. Try to find the pairs!\nWhen guessing, input row # and column letter"
          "\neg. Row 3, Column b would be '3b' ")
    game_round = 0
    game_over = False
    while not game_over:
        game_round += 1
        print_grid(grid)
        # Pick first card
        valid_choice = False
        while not valid_choice:
            choice1 = input("Please pick a card to turn over:   ")
            if choice1[0].isdigit() and choice1[1].isalpha():
                if len(choice1) == 2 and int(choice1[0]) <= rows_count and ord(choice1[1]) < columns_count + 97:
                    choice1_picked = grid[int(choice1[0]) - 1][ord(choice1[1]) - 97]
                    if choice1_picked != "0":
                        valid_choice = True

        print(card_displayer(choice1_picked))
        # Pick second card
        valid_choice2 = False
        while not valid_choice2:
            choice2 = input("Try to find the match!:   ")
            if choice2[0].isdigit() and choice2[1].isalpha():
                if len(choice2) == 2 and int(choice2[0]) <= rows_count and ord(choice2[1]) < columns_count + 97:
                    choice2_picked = grid[int(choice2[0]) - 1][ord(choice2[1]) - 97]
                    if choice2_picked != "0" and choice2_picked != choice1_picked:
                        valid_choice2 = True
        print(card_displayer(choice2_picked))
        is_match = False
        for itm5 in f_b_pairs1:
            if choice1_picked in itm5 and choice2_picked in itm5:
                is_match = True

        if is_match:
            print("Congratulations! You found a match!")
            grid[int(choice1[0]) - 1][ord(choice1[1]) - 97] = "0"
            grid[int(choice2[0]) - 1][ord(choice2[1]) - 97] = "0"
        else:
            print("Sorry, please try again.")

        for row in grid:
            for itm6 in row:
                if itm6 == "0":
                    game_over = True
                else:
                    game_over = False
        if game_over:
            print(f"Congratulations, you won! It took you {str(game_round)} rounds.")


try:
    program_directory = os.path.dirname(os.path.abspath(__file__))
except Exception:
    program_directory = os.getcwd()

welcome = """
      Welcome to

^_^   Flashcards   ^_^
"""


menu = """\nmenu:

1. View deck
2. Add item
3. Delete item
4. Quiz yourself
5. Play a game
6. Switch decks
7. Import and convert decks
8. Quit

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
    decks = glob.glob(program_directory + "/*.json")
    numbered_paths_and_names = deck_menu_constructor(decks)
    # makes a variable to hold the list of deck names with a given number starting at 1
    decks_choice_display = ""
    for name_path_tup in numbered_paths_and_names:
        decks_choice_display += str(name_path_tup[0]) + ") " + str(name_path_tup[1]) + "\n"
    # Deck choice menu prompt
    deck_chosen = False
    while not deck_chosen:
        deck_choice = input(f"Please choose a deck: \n{decks_choice_display}\nOr type 'i' to skip to deck importer")
        if deck_choice == "i" or int(deck_choice) <= len(decks):
            deck_chosen = True
    running2 = True
    while running2:
        if deck_choice == "i":
            menu_choice = "6"
        else:
            # The number the user enters will be 1 more than the index for the tuple where the path is the 2th entry
            file_to_open = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'r')
            menu_choice = input(menu)
            deck = json.loads(file_to_open.read())
            file_to_open.close()
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
            memory_game(deck)
        elif menu_choice == "6":
            # Before switching to a new deck, or when closing the session, write the changes.
            file_to_write = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'w+')
            file_to_write.write(json.dumps(deck, sort_keys=True, indent=4))
            file_to_write.close()
            running2 = False
        elif menu_choice == "7":
            # Find all txt files in local directory, txts variable will be a list of their paths
            txts = glob.glob(program_directory + "/*.txt")
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
                            running2 = False
                    else:
                        print("Importing...")
                        import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2])
                        running2 = False
                else:
                    ask_fbsep = input("Please input the separator you used between card fronts and backs: ")
                    ask_cardsep = input("Please input the separator you used between cards: ")
                    print("Importing...")
                    import_quizlet_lineskip_fix(numbered_paths_and_names1[int(file_choice) - 1][2],
                                                fbsep=ask_fbsep, cardsep=ask_cardsep)
                    running2 = False
            else:
                print("Unsupported file type.")
                running2 = False
        elif menu_choice == "8":
            print("Thanks for playing, see you next time!")
            # Before switching to a new deck, or when closing the session, write the changes.
            file_to_write = open(numbered_paths_and_names[int(deck_choice) - 1][2], 'w+')
            file_to_write.write(json.dumps(deck, sort_keys=True, indent=4))
            file_to_write.close()
            running1 = False
            running2 = False
        else:
            print("Invalid entry")