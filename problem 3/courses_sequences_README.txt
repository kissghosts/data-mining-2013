The files courses_sequences_text.txt, courses_sequences_num.txt and courses_sequences_mapping.txt contain sequential data about the courses taken by students.

The files courses_sequences_text.txt and courses_sequences_num.txt contain sequences of sets of courses.
Each line correspond to one student and contain the courses he attended. The courses are grouped by semesters. For example, the following line:
'{ biological_sequence_analysis elements_of_bioinformatics }{ practical_course_in_biodatabases }{ programming_in_python }{ unsupervised_machine_learning }'
indicates that the student has studied two courses ('biological_sequence_analysis' and 'elements_of_bioinformatics') during his first study term, one course ('practical_course_in_biodatabases') during his second study term and so on.
Terms are spring, summer and fall. The starting year is not indicated nor gaps in the study.
In our example, the first set could refer to spring term 2005 and the second to spring term 2006 if the student has not attended any course in between.

Both files contain the same information, except for the fact that the courses are identified by text ids (lowercased simplified names) in the former and by numerical ids in the latter. Therefore, the first one might be useful to get an insight in the data and formulate the problem, while the other is probably better suited for automatic processing.

The file courses_sequences_mapping.txt contains the mapping between the numerical id, lowercased simplified course name and original course id. Several courses with different original ids, and possibly different original names, are mapped to the same lowercased simplified name and therefore to the same numerical id.


