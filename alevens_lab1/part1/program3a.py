# 3.3.1 While loop
# Write a program to get Fibonacci series between 0 to a user input number using while loop

num_fibnums = int(input('How many Fibonacci numbers would you like to generate? '))

fibseq = [1,1]

while (len(fibseq) < num_fibnums):
    new = fibseq[len(fibseq) - 1] + fibseq[len(fibseq) - 2]
    fibseq.append(new)
    
print("The Fibonacci Sequence is: " + str(fibseq).strip('[]'))
    
