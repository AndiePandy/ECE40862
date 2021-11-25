# 3.3.2 For loop
# Write a program that generates a random number (0-10) and asks the user to guess it within 
# three chances. If user guesses correctly, print 'You win!', otherwise print ‘You lose!’

from random import randint

rand_num = randint(0,10)

for i in range(3):
    guess = int(input('Enter your guess: '))
    if (guess == rand_num):
        print('You win!')
        break
    
if (guess != rand_num):
    print('You lose!')
