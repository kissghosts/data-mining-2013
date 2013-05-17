#!/usr/bin/python

import csv

file_dir = 'ColoradoSchoolGrades_20121210/'

grade_file_2012 = open("%s2012_final_grade.csv" % file_dir, 'rU')
grade_file_2011 = open("%s2011_final_grade.csv" % file_dir, 'rU')
grade_file_2010 = open("%s2010_final_grade.csv" % file_dir, 'rU')
school_map = open('school_map.csv', 'rU')

district = {}
for line in school_map:
    line = line.strip().split('\t')
    district[int(line[2])] = line[0]

dataset = {}
grade_2012 = csv.reader(grade_file_2012)
grade_2011 = csv.reader(grade_file_2011)
grade_2010 = csv.reader(grade_file_2010)
for line in grade_2012:
    if (line[5].upper() == 'E' and not dataset.has_key(line[3]) 
        and line[9] != '' and district.has_key(int(line[1]))):
        dataset[int(line[3])] = [int(line[1]), district[int(line[1])], 
                                int(line[9]), int(line[11]), int(line[16])]

for line in grade_2011:
    if (line[3].upper() == 'E' and dataset.has_key(int(line[5])) 
        and line[14] != '' and line[16] != '' and line[21] != ''):
        dataset[int(line[5])] += [int(line[14]), int(line[16]), int(line[21])]
for key in dataset.keys():
    if len(dataset[key]) != 8:
        dataset.pop(key)

for line in grade_2010:
    if (line[3].upper() == 'E' and dataset.has_key(int(line[5])) 
        and line[15] != '' and line[17] != '' and line[22] != ''):
        dataset[int(line[5])] += [int(line[15]), int(line[17]), int(line[22])]
for key in dataset.keys():
    if len(dataset[key]) != 11:
        dataset.pop(key)

count = 0
for key in dataset.keys():
    if dataset[key][2] > 7 and dataset[key][2] < 11:
        count += 1
print "2012 B level school: %d" % count

for year in ['2012', '2011', '2010']:
    frl_file = open("%s_k_12_FRL.csv" % (file_dir + year), 'rU')
    frl = csv.reader(frl_file)
    for line in frl:
        if ('SCHOOL' not in line[2].upper() and line[2] != '' 
            and dataset.has_key(int(line[2]))):
            dataset[int(line[2])].append(line[4])
    for key in dataset.keys():
        if len(dataset[key]) == 11 + 2012 - int(year):
            dataset[key].append('')

for year in ['2012', '2011', '2010']:
    enrl_file = open("%s_enrl_working.csv"% (file_dir + year), 'rU')
    enrl = csv.reader(enrl_file)
    for line in enrl:
        if (line[2].isdigit() and dataset.has_key(int(line[2]))):
            for i in range(6, 10):
                dataset[int(line[2])].append(line[i])

writer = csv.writer(open('dataset.csv', 'wb'))
writer.writerow(['School Code', 'District Code', 'Region', 'Grade 2012', 
    'Ach 2012', 'Grth 2012', 'Grade 2011', 'Ach 2011', 'Grth 2011', 
    'Grade 2010', 'Ach 2010', 'Grth 2010', 'FRL 2012', 'FRL 2011', 'FRL 2010', 
    'Asian 2012', 'Black 2012', 'hisp 2012', 'White 2012', 
    'Asian 2011', 'Black 2011', 'hisp 2011', 'White 2011',
    'Asian 2010', 'Black 2010', 'hisp 2010', 'White 2010'])
lines = [[key] + dataset[key] for key in dataset.keys()]
for line in lines:
    writer.writerow(line)