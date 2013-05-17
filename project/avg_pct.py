#!/usr/bin/python

import csv
import re

year = '2012'
in_file = 'dataset.csv'
dataset = csv.reader(open(in_file, 'rU'))

result = {  'A': [],
            'B': [],
            'C': [],
            'D': [],
            'F': []}

grade_index = 3
pct_asian_index = 15
pct_black_index = 16
pct_hisp_index = 17
pct_white_index = 18

for line in dataset:
    if 'School' not in line[0]:
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
        
        result[level].append(line)

for key in sorted(result.keys()):
    pct_white_sum = 0
    pct_asian_sum = 0
    pct_black_sum = 0
    pct_hisp_sum = 0
    for each in result[key]:
        pct_asian_sum += float(each[pct_asian_index])
        pct_black_sum += float(each[pct_black_index])
        pct_hisp_sum += float(each[pct_hisp_index])
        pct_white_sum += float(each[pct_white_index])

    size = len(result[key])
    print "%s: asian -- %.4f" % (key, pct_asian_sum / size)
    print "%s: black -- %.4f" % (key, pct_black_sum / size)
    print "%s: hisp -- %.4f" % (key, pct_hisp_sum / size)
    print "%s: white -- %.4f" % (key, pct_white_sum / size)