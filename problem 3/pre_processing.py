#!/usr/bin/python

import re
import copy

infile = open('courses_sequences_num.txt', 'r')
outfile = open('courses.txt', 'w')

for line in infile:
    if line.count('{') > 1:
        line = line.strip()
        substr = re.sub('^{\s|\s}$', '', line)
        sublist = substr.split(' }{ ')
        
        transaction = []
        for each in sublist:
            if ' ' in each:
                term = each.split()
                copyterm = copy.copy(term)
                for course in term:
                    count = copyterm.count(course)
                    if count > 1:
                        copyterm.remove(course)

                transaction.append(copyterm)
            else:
                transaction.append([each])

        output = ''
        length = len(transaction)
        for i in range(length):
            for item in transaction[i]:
                if item == transaction[i][-1]:
                    output += item
                else:
                    output += item + ' '

            if i != length - 1:
                output += ', '
            else:
                output += '\n'

        outfile.write(output)
