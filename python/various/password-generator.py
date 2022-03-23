'''This program is for practice, I do not recommend
   this script to generate a password.'''

import random
import string
import os

#This function contains the program name.
def program_name():
    os.system('clear')
    print('✴ ✴ ✴ Password generator ✴ ✴ ✴\n')

#This function shows the menu.
def menu():
    program_name()
    password1 = int(input('\nHow many digits do you want in your password?: '))
    while True:
        print('\nHow do you want your password?:\n\
\n1. Only upper and lower case letters.\n2. Letters with numbers\n\
3. Letters, numbers and special characters (Recommended).\n\
4. Modify the number of digits for the password.\n5. Exit.')
        password = input('\n---> ')
        if password == "1":
            print('\nPassword:',"".join(random.choices(string.ascii_letters, k = password1)))
        elif password == "2":
            print('\nPassword:',"".join(random.choices(string.hexdigits, k = password1)))
        elif password == "3":
            digits = string.hexdigits+string.punctuation
            print('\nPassword:',"".join(random.choices(digits, k = password1)))
        elif password == "4":
            password1 = int(input('\nHow many digits do you want in your password?: '))
            program_name()
        elif password == "5":
            print('Exiting...')
            break
        else:
            input('\nERROR! Press ENTER to continue: ')
            program_name()
menu()
