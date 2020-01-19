import os, os.path
import re
import matplotlib.pyplot as plt

DIR = 'data'
number_of_files = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
name_of_files=[name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]
ages_and_score = {}

# Read each data file
for i in range(number_of_files):
    f = open(DIR+"\\"+name_of_files[i],"r")
    line = f.readline()
    # Read each line of a data file and search for the age of the player and his score
    while line :
        if re.match(r"(.)*AGE_PLAYER(.)*", line):
            age=int(re.findall("([0-9]+)", line)[1]) 
        if re.match(r"(.)*SCORE_PLAYER(.)*", line):
            numbers=re.findall("([0-9]+)", line)
            # Score in percentage
            score=int(numbers[1])/int(numbers[2])*100
        line = f.readline() 
    ages_and_score[age]=score

lists = sorted(ages_and_score.items()) # sorted by key, return a list of tuples

ages,scores = zip(*lists)

# Display the curve
plt.xlabel('age (in years)')
plt.ylabel('score (in percentage)')
plt.plot(ages, scores)
plt.show()