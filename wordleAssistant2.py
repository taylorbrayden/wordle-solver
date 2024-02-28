"""
Brayden Taylor
Wordle Assistant 2
February 2024
"""

import os
from collections import Counter
os.system("")

# Assigning every 5 letter word to "fiveLetterWords"
file = open("five_letter_words.txt")
fiveLetterWords = file.read().split("\",\"")
file.close()
fiveLetterWords.sort()

# Assigning five letter words with frequency in a tuple format to mostFrequentWords
mostFrequentWords = []
f = open("freq_five_letters_2.txt", "r")
for line in f:
    line = line.strip("\n")
    mostFrequentWords.append((line[:5], int(line[6:])))
f.close()

# This first portion is just going to find all possible answers
# First grab the user input for green
userGreen = input("Green letters: ")

# Check input against database of all five letter words and add possible words to new list
greenCheckWords = []
for word in fiveLetterWords:
    bad = False
    for count, letter in enumerate(word):
        # Ignore spaces
        if userGreen[count] == "-":
            continue
        # Mismatch = bad
        if userGreen[count] != letter:
            bad = True
    # Checks for mismatch
    if not bad:
        greenCheckWords.append(word)

# If there is a green letter in some position, then we don't ever have to check that position again, we know it is right
# So, create possiblePositions to iterate through later on
possiblePositions = []
for count, character in enumerate(userGreen):
    if character == "-":
        possiblePositions.append(count)

# Take input of yellow letters
userYellow = input("Yellow letters: ").split(" ")
if userYellow == [""]:
    userYellow = []
if len(userYellow) > 0:
    userYellow0 = (userYellow[0], input("Position(s) of yellow \"" + userYellow[0][0] + "\": ").split(" "))
    userYellow[0] = userYellow0
if len(userYellow) > 1:
    userYellow1 = (userYellow[1], input("Position(s) of yellow \"" + userYellow[1][0] + "\": ").split(" "))
    userYellow[1] = userYellow1
if len(userYellow) > 2:
    userYellow2 = (userYellow[2], input("Position(s) of yellow \"" + userYellow[2][0] + "\": ").split(" "))
    userYellow[2] = userYellow2
if len(userYellow) > 3:
    userYellow3 = (userYellow[3], input("Position(s) of yellow \"" + userYellow[3][0] + "\": ").split(" "))
    userYellow[3] = userYellow3
if len(userYellow) > 4:
    userYellow4 = (userYellow[4], input("Position(s) of yellow \"" + userYellow[4][0] + "\": ").split(" "))
    userYellow[4] = userYellow4

# Entirely too many for loops
# Checks if letters match from the working words list and the yellow letters
# If the letters match and are in the same position, then it cannot be an answer
yellowCheckWords1 = []
for word in greenCheckWords:
    breakOutFlag = False
    for count, letter in enumerate(word):
        for yellowLetter in userYellow:
            positions = yellowLetter[1]
            if letter == yellowLetter[0] and str(count+1) in positions:
                breakOutFlag = True
                break
        if breakOutFlag:
            break
    if not breakOutFlag:
        yellowCheckWords1.append(word)

# If the yellow letter isn't in the word, then it can't be an answer
yellowCheckWords2 = []
for word in yellowCheckWords1:
    breakOutFlag = False
    for yellowLetter in userYellow:
        if yellowLetter[0] not in word:
            breakOutFlag = True
            break
    if not breakOutFlag:
        yellowCheckWords2.append(word)

# Black letters
userBlack = input("Black letters: ").split(" ")

# Here's where some issues arise. The basic mindset is that if there is a black letter in a word,
# then it can't be an answer.
# This doesn't work if there is a letter that is black and green (or yellow).
# So, if the letter is green, then don't check that position
# I'm not sure if there is an issue with yellow letters yet, so I won't touch it
blackCheckWords = []
for word in yellowCheckWords2:
    breakOutFlag = False
    for position in possiblePositions:
        for blackLetter in userBlack:
            if blackLetter == word[position]:
                breakOutFlag = True
                break
        if breakOutFlag:
            break
    if not breakOutFlag:
        blackCheckWords.append(word)

# At this point, this is all possible answers, but I do still want to incorporate most information
# as well as the frequency of the words, just to filter them out a bit
print(blackCheckWords[0:100])

# Finding most information can be done by skipping over green letters using possiblePositions again
# I would check the answers (blackCheckWords) and give each letter a point, while skipping greens
letterFreq = Counter("".join(blackCheckWords))
greenLetters = []
for char in userGreen:
    if char != "-":
        greenLetters.append(char)
for letter in greenLetters:
    del letterFreq[letter]

# Now, from all five letter words, find the words that contain the most points according to their
# letters and their point values from letterFreq.
# If there are multiple of the same letter, the letter will only give more info if it is in the word.
# So, the letter's point value should be divided by the len(letterFreq)^occurences (or just not added)
myDict = {}
for word in fiveLetterWords:
    points = 0
    previousLetters = []
    for letter in word:
        if letter not in previousLetters:
            points += letterFreq[letter]
            previousLetters.append(letter)
    myDict[word] = points

print(sorted(myDict.items(), key=lambda item: item[1], reverse=True)[0:30])