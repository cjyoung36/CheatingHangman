# Name: Christopher Young
# Date: Feb 28 2022
# Purpose: Creating a "cheating" hangman game
import random


def main():
    play_again = True
    while play_again:
        # Initialize game parameters
        word_size, word_list = game_init()
        num_guesses, guessed_letters, solution = param_init(word_size)

        # Debug mode
        debug_mode = input("Would you like to play with debug mode? (Y/N): ")
        if debug_mode == "Y":
            debug_mode = True
            print(word_list)
        else:
            debug_mode = False

        # Play game
        has_won, remaining_words = start_game(guessed_letters, word_list, solution, num_guesses, debug_mode)

        # Victory/Defeat
        if has_won:
            print("Congratulations! You won the game!")
        else:
            print("You ran out of guesses!")
            # Find random word from remaining list
            bogus_word = find_random(remaining_words)
            print("The correct word was", bogus_word)

        # Play again
        play_again_input = input("\nWould you like to play again? (Y/N): ")
        if play_again_input == "N":
            play_again = False


def find_random(word_list):
    return random.choice(word_list)


def start_game(guessed_letters, word_list, solution, num_guesses, debug_mode):
    letter = get_guess(guessed_letters)
    new_list, new_key = partition_list(letter, word_list)
    solution = check_key(letter, new_key, solution)
    if debug_mode:
        print(new_key)
        print(new_list)
    num_guesses = check_correct_guess(new_key, num_guesses)
    display_game_stats(num_guesses, guessed_letters, solution)
    while num_guesses > 0:
        letter = get_guess(guessed_letters)
        new_list, new_key = partition_list(letter, new_list)
        solution = check_key(letter, new_key, solution)
        if debug_mode:
            print(new_key)
            print(new_list)
        num_guesses = check_correct_guess(new_key, num_guesses)
        display_game_stats(num_guesses, guessed_letters, solution)
        has_won = check_win(solution)
        if has_won is True:
            return True, new_list
    return False, new_list


def game_init():
    # Validate word size and word list
    valid_init = False
    while valid_init is False:
        word_size = get_size()
        word_list = get_init_list(word_size)
        if len(word_list) != 0:
            valid_init = True
        else:
            print("No words of size", word_size, "found")
    return word_size, word_list


def param_init(word_size):
    # Initialize game parameters
    num_guesses = 10
    guessed_letters = []
    solution = ""
    for i in range(0, word_size):
        solution += "_"
    return num_guesses, guessed_letters, solution


def check_win(solution):
    if "_" not in solution:
        return True
    return False


def check_correct_guess(key, num_guesses):
    if len(key) == 0:
        num_guesses -= 1
    return num_guesses


def check_key(letter, key, solution):
    if len(key) > 0:
        for value in key:
            solution = solution[:value] + letter + solution[value+1:]
    return solution


def get_size():
    is_valid_size = False
    size = input("Please select the length of the hidden word: ")
    while is_valid_size is False:
        if not size.isnumeric():
            print("Invalid value detected")
            size = input("Please select the length of the hidden word: ")
        else:
            is_valid_size = True
    return int(size)


def get_init_list(size):
    init_list = []
    scrabble_words = open("dictionary.txt")
    for line in scrabble_words:
        word = line.strip("\n")
        if len(word) == size:
            init_list.append(word)
    return init_list


def get_guess(guessed_letters):
    letter = input("Guess a letter: ")
    is_valid_letter = False
    while is_valid_letter is False:
        if letter in guessed_letters:
            print("You've already guessed", letter)
            letter = input("Guess a letter: ")
        elif not letter.isalpha():
            print("Invalid input detected")
            letter = input("Guess a letter: ")
        elif len(letter) != 1:
            print("Invalid input detected")
            letter = input("Guess a letter: ")
        else:
            guessed_letters.append(letter)
            is_valid_letter = True
    return letter


def get_index(letter, word):
    index = []
    for i, character in enumerate(word):
        if character == letter:
            index.append(i)
    return index


def partition_list(letter, word_list):
    partition_map = {}
    # Initial partitioning
    for word in word_list:
        index = get_index(letter, word)
        index = tuple(index)
        if index not in partition_map.keys():
            partition_map.setdefault(index, [])
            partition_map[index].append(word)
        else:
            partition_map[index].append(word)
    # Find the largest set within the partition
    max_list = []
    max_size = 0
    max_key = ()
    for key in partition_map:
        if len(partition_map[key]) > max_size:
            max_size = len(partition_map[key])
            max_list = partition_map[key]
            max_key = tuple(key)
    return max_list, max_key


def display_game_stats(num_guesses, guessed_letters, solution):
    print("\nYou have", num_guesses, "incorrect guesses remaining")
    if len(guessed_letters) == 0:
        print("You have not guessed any letters yet")
    else:
        print("Letters guessed:", *guessed_letters, sep=" ")
    print("Current solution: ", *solution, sep="")


main()
