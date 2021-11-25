from collections import defaultdict
# 3.5 Class and Functions
# Write a program to create a Python class to find a pair of elements (indices of the two numbers) 
# from a given list of numbers whose sum equals a specific target number.
# Use this list in your program: [10,20,10,40,50,60,70]

num_target = int(input("What is your target number? "))

addends = [10,20,10,40,50,60,70]

# dictionary of val: ind of addends who are less than target
possible_addends = defaultdict(list) 

# generate possible_addends dictionary
for i, addend in enumerate(addends):
    if addend <= num_target:
        possible_addends[addend].append(i)

# check what addends from possible_addends can add up to target_num
for addend, list_index in possible_addends.items():
    if (num_target - addend in possible_addends):
        
        # if two of same addend is solution and it is in the list twice
        if ((num_target - addend) == addend and (len(possible_addends[addend]) > 1)):
            print("index1 = %d, index2 = %d" % (possible_addends[addend][0], possible_addends[addend][1]))
            
        # if two of same addend is solution and isn't in list twice
        elif ((num_target - addend) == addend and (len(possible_addends[addend]) == 1)):
            print("No solution.")
        
        else: # two different addends
            print("index1 = %d, index2 = %d" % (possible_addends[addend][0], possible_addends[num_target - addend][0]))
        break
    

if (len(possible_addends.items()) <= 1):
    print("No solution.")
            