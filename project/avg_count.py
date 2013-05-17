#!/usr/bin/python

import csv
import re

year = '2012'
in_file = 'dataset.csv'
dataset = csv.reader(open(in_file, 'rU'))

result = {  'A': [0, 0],
            'B': [0, 0],
            'C': [0, 0],
            'D': [0, 0],
            'F': [0, 0]}

places = {}
if year == '2012':
    grade_index = 3
    frl = 12
elif year == '2011':
    grade_index = 6
    frl = 13
else:
    grade_index = 9
    frl = 14

for line in dataset:
    if 'School' not in line[0]:
        mstr = re.match('(\d+\.\d*)%', line[frl]).groups()[0]
        if not mstr:
            print "[Err] line missing frl vaule"
            continue

        grade = int(line[grade_index])
        if grade >= 11:
            level = 'A'
        elif grade >= 8 and grade <= 10:
            level = 'B'
        elif grade >= 5 and grade <= 7:
            level = 'C'
        elif grade >= 2 and grade <= 4:
            level = 'D'
        else:
            level = 'F'
            if places.has_key(line[2]):
                places[line[2]] += 1
            else:
                places[line[2]] = 1
        
        result[level][0] += 1
        result[level][1] += float(mstr)

for level in ['A', 'B', 'C', 'D', 'F']:
    print "Level %s\ncount: %d, avg-frl: %.2f" % (level, result[level][0], 
        result[level][1] / result[level][0])

print "F schools:"
print places