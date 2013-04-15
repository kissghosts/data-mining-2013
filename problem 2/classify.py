#!/usr/bin/python

info_file = open('courses_details.txt', 'r')
infile = open('courses_num.txt', 'r')
outfile = open('classified.txt', 'w')
advfile = open('adv_courses.txt', 'w')

course_info = {}
for line in info_file:
    if line:
        info = line.strip().split()
        course_info[info[0]] = info[4]

adv_courses = []
for each in course_info:
    if course_info[each] == 'L':
        adv_courses.append(int(each))

for each in sorted(adv_courses):
    advfile.write("%s\n" % each)

for line in infile:
    if line:
        transaction = line.strip().split()
        for each in transaction:
            if course_info.has_key(each) and course_info[each] == 'L':
                outfile.write(line)
                break