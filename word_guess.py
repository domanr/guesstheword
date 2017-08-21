import csv
import random
import re
import os

def load_puzzles(filename):
    with open(filename) as puzzles_file:
        puzzle_reader = csv.reader(puzzles_file, delimiter=',')
        puzzles = []
        for row in puzzle_reader:
            next_puzzle = dict(zip(['puzzle', 'category'], row))
            puzzles.append(next_puzzle)
    return puzzles


def draw_puzzle(puzzles):
    index = random.randint(0, len(puzzles)-1)
    return puzzles[index]


def init_result(selected_puzzle):
    result = []
    for i in range(0, len(selected_puzzle['puzzle'])):
        # Space shall not be taken into consideration, let's mark it as true
        if selected_puzzle['puzzle'][i] == ' ':
            result.append(True)
        else:
            result.append(False)
    selected_puzzle['result'] = result


def get_input():
    while True:
        letter = raw_input('Enter a letter: ')
        if len(letter) < 1:
            print('Nothing was entered, please try again!')
            continue
        if not letter.isalpha():
            print('This is not a letter, please try again!')
            continue
        break
    return letter[0]


def check_letter(letter, puzzle):
    letter = letter.lower()
    text = puzzle['puzzle'].lower()
    contains = False
    for m in re.finditer(letter, text):
        contains = True
        puzzle['result'][m.start()] = True
    return contains


def display_puzzle(selected_puzzle):
    print('Category: ' + selected_puzzle['category'])
    displayed = ''
    for i in range(0, len(selected_puzzle['puzzle'])):
        if selected_puzzle['result'][i]:
            displayed += selected_puzzle['puzzle'][i]
        else:
            displayed += '.'
    print(displayed)


def main():
    puzzles = load_puzzles('puzzles.csv')
    play_again = 'y'

    while play_again == 'y':
        puzzle = draw_puzzle(puzzles)
        init_result(puzzle)
        failures = 0
        letters_tried = []

        while False in puzzle['result']:
            print('Welcome to the Guess the word game!')
            print('\nFailures: ' + str(failures))
            print('Letters you tried: ' + ', '.join(letters_tried))
            display_puzzle(puzzle)
            letter = get_input()
            letters_tried.append(letter)
            contains = check_letter(letter, puzzle)
            if not contains:
                print('The word does not contain letter ' + letter)
                failures += 1
            if failures > 5:
                break
            os.system('cls')

        if False in puzzle['result']:
            print('\nGame over! The word was: ' + puzzle['puzzle'])
        else:
            print('\nCongrats, you won! The word was: ' + puzzle['puzzle'])
        play_again = raw_input('Would you like to play again (y/n)? ')
        play_again = play_again[0].lower()
        os.system('cls')

main()
