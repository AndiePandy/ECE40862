# 3.1 Character Input
# Write a program that asks the user to enter name and age. Prints out a message that tells the 
# year the user will turn 100 years old.

name = input('What is your name? ')
age_curr = int(input('How old are you? '))
year_curr = 2021
year_future = str(year_curr - age_curr + 100)
print(name + ' will be 100 years old in the year ' + year_future)
