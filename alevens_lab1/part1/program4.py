# 3.4 Dictionary
# Write a program to create a dictionary of names and birthdays. Upon execution, it should ask 
# the user to enter a name, and return the birthday of that person back to them.

birthdays = {
    "Albert Einstein": "03/14/1879",
    "Benjamin Franklin": "01/17/1706", 
    "Ada Lovelace": "12/10/1815",
}

print("Welcome to the birthday dictionary. We know the birthdays of: ")
for key in birthdays.keys():
    print(key)

print("Who's birthday do you want to look up? ")
person = input()
person_birthday = birthdays[person]
print(person +"'s birthday is " + person_birthday)