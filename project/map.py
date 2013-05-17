#!/usr/bin/python

import csv
import re

file_dir = 'ColoradoSchoolGrades_20121210/'

map_data = open('district.csv', 'rU')
school_map = csv.reader(line.replace('\0', '') for line in map_data)
grade_file = open("%s2012_final_grade.csv" % file_dir, 'rU')
# grade = csv.reader(grade_file)

grade = []
for line in grade_file:
    grade.append(line.strip().split(','))

dataset = []
for line in school_map:
    if line:
        mstr = line[1]
        submstr = re.sub("(\w+)-(\d+)$", "\\1 \\2", line[1])
        for eachline in grade:
            if (mstr.upper() in eachline[2].upper() 
                or submstr.upper() in eachline[2].upper()):
                dataset.append(line + [eachline[1]])
                break
        else:
            dataset.append(line)

writer = csv.writer(open('school_map.csv', 'wb'))
for eachline in dataset:
    writer.writerow(eachline)
