# 3.2 Lists and Conditional Statements
# Write a program to initiate a list of numbers, print the list, and ask the user for a number and 
# return a list that contains only elements from the original list that are smaller than the number 
# given by the user.

a = [1,1,2,3,5,8,13,21,34,55,89]
print("a = "+str(a))
num = int(input('Enter number: '))

new_list = []
for elem in a:
    if (elem < num):
        new_list.append(elem)
        
print('The new list is ' + str(new_list))
        