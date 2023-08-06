# Multiplicative Persistence, by Al Sweigart al@inventwithpython.com
# For more information about this topic, see https://youtu.be/Wim9WJeDTHQ

import time, sys

print('''MULTIPLICATIVE PERSISTENCE
By Al Sweigart al@inventwithpython.com
''')

while True:
    print('Try to get the longest multiplicative persistence chain possible!')
    print('(Try 277777788888899, which has the longest known chain length.')
    while True:
        print('Enter a number (or "quit" to quit):')
        try:
            response = input()
            if response.lower().startswith('q'):
                sys.exit()
            number = int(response)
        except ValueError:
            continue # If the user entered a non-integer, ask again.
        break

    chainLength = 0
    while number > 9: # Keep looping as long as number is 2 or more digits.
        chainLength += 1
        print(number, end='', flush=True)
        time.sleep(0.2)
        print(' -> ', end='', flush=True)
        time.sleep(0.2)
        print('*'.join(list(str(number))), end='', flush=True)
        time.sleep(0.2)
        print(' = ', end='', flush=True)
        time.sleep(0.2)

        # Calculate the next number in the multiplicative persistence chain by
        # multiplying all of the digits in the number.
        product = 1
        for digit in str(number):
            product *= int(digit)
        number = product

        print(number, flush=True)
        time.sleep(0.6)

    print(number)
    print('Length of', response, 'chain:', chainLength)
    print()


