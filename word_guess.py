import csv
import random
import re


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
        result.append(False)
    selected_puzzle['result'] = result


def get_input():
    letter = raw_input('Enter a letter: ')
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
    print('Category: ' + selected_puzzle['category'] + ' (' + str(len(selected_puzzle['puzzle'])) + ' letters)')
    displayed = ''
    for i in range(0, len(selected_puzzle['puzzle'])):
        if selected_puzzle['result'][i]:
            displayed += selected_puzzle['puzzle'][i]
        else:
            displayed += '.'
    print(displayed)


def main():
    print('Welcome to the Guess the word game!')

    puzzles = load_puzzles('puzzles.csv')
    play_again = 'y'

    while play_again == 'y':
        puzzle = draw_puzzle(puzzles)
        init_result(puzzle)
        failures = 0

        while False in puzzle['result']:
            print('\nFailures: ' + str(failures))
            display_puzzle(puzzle)
            letter = get_input()
            contains = check_letter(letter, puzzle)
            if not contains:
                print('The word does not contain letter ' + letter)
                failures += 1
            if failures > 5:
                break

        if False in puzzle['result']:
            print('\nGame over! The word was: ' + puzzle['puzzle'])
        else:
            print('\nCongrats, you won! The word was: ' + puzzle['puzzle'])
        play_again = raw_input('Would you like to play again (y/n)? ')
        play_again = play_again[0].lower()
        print('\n\n')

main()
