#!/usr/bin/python
from pylab import *

openpath = 'course-text.txt'
openf = open(openpath, 'r')
student_count = {}

students = 0
for line in openf:
    students += 1
    count = len(line.strip().split())
    if not student_count.has_key(count):
        student_count[count] = 1
    else:
        student_count[count] += 1

course_sum = 0
n = 0
for key in student_count.keys():
    course_sum += key * student_count[key]
    n += student_count[key]

print "avg: %s, students: %s" % (course_sum / students, n)

# x = student_count.keys()
# y = student_count.values()

# bar(x, y, facecolor='#9999ff', edgecolor='white')
# plt.xlabel('Course number')
# plt.ylabel('student number')
# show()