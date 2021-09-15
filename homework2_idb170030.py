# Name: Isaac Blackwood
# NetID: idb170030
# File: homework2

import sys
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk import FreqDist
import random


def main():
    # Get the relative path to the data file
    if len(sys.argv) <= 1:
        print("You must specify a path to the data file.")
        exit()
    path = sys.argv[1]
    if not path:
        print("You must specify a path to the data file.")
        exit()
    file = open(path, 'r')
    if not file:
        print("The specified data file could not be opened.")
        exit()

    # read the whole file raw, then tokenize it
    raw = file.read()
    tokens = word_tokenize(raw)

    # calculate number of unique tokens
    lexical_diversity = len(set(tokens)) / len(tokens)
    print("Lexical Diversity of tokenized raw text: " + "{:.2f}".format(lexical_diversity))

    # preprocess text
    (ptokens, nouns) = preprocess(tokens)

    # Make a dictionary
    count_dict = dict((noun, count) for noun, count in FreqDist(ptokens).items() if noun in nouns)
    sorted_dict = sorted(count_dict.items(), key=lambda d: (d[1], d[0]), reverse=True)
    game_words = [noun for noun, count in sorted_dict[:50]]
    print(game_words)

    # play guessing game
    guessing_game(game_words)


def preprocess(tokens):
    # preprocess the text
    # part 3a of assignment
    ptokens = [t.lower() for t in tokens if t.isalpha() and len(t) > 5]

    # part 3b
    wnl = WordNetLemmatizer()
    lemmas = set([wnl.lemmatize(t) for t in ptokens])

    # part 3c
    tags = pos_tag(lemmas)
    print(tags[:20])

    # part 3d
    nouns = [l for (l, t) in tags if t.startswith('NN')]

    # part 3e
    print("Number of tokens from step a: " + str(len(ptokens)))
    print("Number of nouns from step d: " + str(len(nouns)))

    # part 3f
    return ptokens, nouns


def guessing_game(game_words):
    # start with 5 points
    points = 5

    # choose a random word to start guessing
    random.seed()
    word = game_words[random.randint(0, len(game_words) - 1)]
    print("Let's play a word guessing game!")
    guessed = []

    # enter game loop
    while points >= 0:
        word_output = ""
        for letter in list(word):
            if letter in guessed:
                word_output += letter
            else:
                word_output += '_'
        if '_' not in word_output:
            print("You solved it!")
            print("Current score: " + str(points))
            guessed = []
            word = game_words[random.randint(0, len(game_words) - 1)]
        print(str(word_output))
        l = input("Guess a letter:")
        if l == '!':
            print("Bye!")
            exit()
        if l in guessed:
            print("Already guessed")
            continue
        guessed.append(l)
        if l in word:
            points += 1
            print("Right! Score is " + str(points))
        else:
            points -= 1
            if points < 0:
                print("You lose.")
                exit()
            else:
                print("Sorry, guess again. Score is " + str(points))



main()
