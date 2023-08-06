# FizzBuzz Game, by Al Sweigart al@inventwithpython.com

import time, sys

print("""FIZZBUZZ GAME
By Al Sweigart al@inventwithpython.com

Starting with 1, enter increasing numbers.
However, if the number is a multiple of 3, type "fizz" instead of
the number. If the number is a multiple of 5, type "buzz". If the
the number of is a multiple of 3 and 5, type "fizz buzz".

A doom clock is counting down. Entering correct responses gives you
more time. How long can you go?

Press Enter to start...""")
input()

number = 1
doomClock = time.time() + 10 # Player starts with 10 seconds.

while True:
    # Determine the correct response:
    if number % 3 == 0 and number % 5 == 0:
        correctResponse = 'fizzbuzz'
    elif number % 3 == 0:
        correctResponse = 'fizz'
    elif number % 5 == 0:
        correctResponse = 'buzz'
    else:
        correctResponse = str(number)

    # For the first 16 responses, give them the answer:
    if number <= 16:
        hint = f'(Enter {correctResponse}) '
    else:
        hint = ''

    # Get the player's response:
    response = input(f'Next response: {hint}').lower().replace(' ', '')

    # See if the player was correct:
    if response != correctResponse:
        print(f'NOOOOO! The correct response is {correctResponse}!')
        sys.exit()
    elif time.time() > doomClock:
        print('NOOOOO! You have run out of time!')
        sys.exit()

    # If the player was right, add 2 seconds to the doom clock.
    doomClock += 2
    print(f'DOOM CLOCK: {round(doomClock - time.time(), 1)} seconds remaining')
    print()

    number += 1 # Increment the number.
