#!/usr/bin/python
import argparse
import sys
import copy
from sets import Set

def support_counting(sequence, course, maxgap, sequences):
    """calc support for sequence -> course
    """

    support_count = 0
    for each_sequence in sequences:
        # set timing constraints
        for i in range(len(each_sequence)):
            if course in each_sequence[i]:
                end = i
                start = 0 if i < (maxgap - 1) else (i - maxgap -1)
                break

        # 1-size sequence
        if isinstance(sequence, int):
            for each_term in each_sequence[start:end]:
                if sequence in each_term:
                    support_count += 1
                    break
        # sequence which contains more than 1 course
        else:
            super_s = copy.deepcopy(each_sequence[start:end])
            if is_sub(sequence, super_s):
                support_count += 1

    return support_count

def is_sub(sequence1, sequence2):
    """check whether sequence2 is the super set of sequence 1,
    return True or False
    """
    for each in sequence1:
        for i in range(len(sequence2)):
            # use built-in Set class
            a = Set(each)
            b = Set(sequence2[i])
            if b.issuperset(a):
                # delete the terms before i, and then move to check 
                # next course(term) in sequence1
                sequence2 = sequence2[(i + 1):]
                break
        else:
            return False

    return True

def gen_candidate(sequences):
    """generate candidates
    """

    candidates = []
    num = len(sequences)

    # the combination method used for k = 1 is different 
    if len(sequences[0]) == 1 and len(sequences[0][0]) == 1:
        for n in range(num - 1):
            for m in range(n + 1, num):
                candidates.append([sequences[n][0], sequences[m][0]])
                candidates.append([sequences[m][0], sequences[n][0]])
                if sequences[n][0][0] < sequences[m][0][0]:
                    candidates.append([[sequences[n][0][0], sequences[m][0][0]]])
                else:
                    candidates.append([[sequences[m][0][0], sequences[n][0][0]]])
    else:
        for n in range(num - 1):
            for m in range(n + 1, num):
                if len(sequences[n][0]) > 1:
                    s1 = [sequences[n][0][1:]] + sequences[n][1:]
                else:
                    s1 = sequences[n][1:]

                if len(sequences[m][-1]) > 1:
                    s2 = sequences[m][:-1] + [sequences[m][-1][:-1]]
                else:
                    s2 = sequences[m][:-1]

                if s1 == s2 and sequences[n][0][0] != sequences[m][-1][-1]:
                    if len(sequences[m][-1]) == 1:
                        msequence = sequences[n] + [sequences[m][-1]]
                    else:
                        last_element = sequences[n][-1] + [sequences[m][-1][-1]]
                        msequence = sequences[n][:-1] + [sorted(last_element)]

                    # use contiguous subsequence to prune
                    csub = contiguous_sub(msequence)
                    for each in csub:
                        if each not in sequences:
                            break
                    else:
                        candidates.append(msequence)

    return candidates

def contiguous_sub(sequence):
    """generate contiguous subsequence, return a list
    """

    csub = []
    # condition 1 in book
    if len(sequence[0]) == 1:
        csub.append(sequence[1:])
    if len(sequence[-1]) == 1:
        csub.append(sequence[:-1])

    # condition 2 in book
    for i in range(len(sequence)):
        if len(sequence[i]) > 1:
            for each in sequence[i]:
                copied = copy.copy(sequence[i])
                copied.remove(each)
                sub = sequence[:i] + [copied] + sequence[(i + 1):]
                if sub not in csub:
                    csub.append(sub)

    return csub


# main func
if __name__ == '__main__':
    # option parser
    parser = argparse.ArgumentParser(description='description: '
        'Apriori-like algorithm to find pre-requested course(s)')
    parser.add_argument('--s', dest='support', type=int, default=50, 
        help="support value, default value is 50 (50 percent)")
    parser.add_argument('infile', type=argparse.FileType('r'), 
        help='path of input file')
    parser.add_argument('outfile', type=argparse.FileType('w'), 
        help='path of output file')
    parser.add_argument('course', type=int, help="id of the "
        "objective course")
    parser.add_argument('--ctoken', type=str, default=' ', 
        help="string used for splitting each course, e.g. ',', "
        "default value is space")
    parser.add_argument('--ttoken', type=str, default=', ', 
        help="string used for splitting each course, e.g. ',', "
        "default value is ', '")
    parser.add_argument('--mingap', type=int, default=0, help="mingap")
    parser.add_argument('--maxgap', type=int, default=3, help="maxgap, "
        "0 means no maxgap")
    
    args = parser.parse_args()
    
    if args.mingap < 0:
        print "error: mingap should not be smaller than 0"
        sys.exit(1)

    # pre-process the input data
    minsup = args.support / 100.0
    course = args.course
    if args.maxgap <= 0:
        maxgap = 0
    else:
        maxgap = args.maxgap
    mingap = args.mingap

    if maxgap > 0 and mingap > maxgap:
        print "error: mingap should not be larger than maxgap"
        sys.exit(1)

    sequences = []
    k1_items = []
    frequent_sequences = {}
    for line in args.infile:
        if "%s" % course in line:
            sequence = []
            term = line.strip().split(args.ttoken)
            for each in term:
                str_list = each.split(args.ctoken)
                sequence.append([int(c) for c in str_list])
            sequences.append(sequence)

            for x in range(len(sequence)):
                if course in sequence[x]:
                    end = x
                    start = 0 if x < (maxgap - 1) else (x - maxgap -1)
                    break        
            
            for i in range(start, end):
                for each in sequence[i]:
                    if each not in k1_items:
                        k1_items.append(each)

    # generate the 1-size frequent sequence
    count = len(sequences) + 0.0
    frequent_sequences[1] = []
    for each in k1_items:
        if each != course:
            sup = support_counting(each, course, maxgap, sequences) / count
            if sup > minsup:
                frequent_sequences[1].append([[[each]], sup])

    if not frequent_sequences[1]:
        print "no sequence generated"
        sys.exit(0)

    # generate all frequent sequences
    n = 1
    while True:
        frequent_sequences[n + 1] = []
        k_freq_sequences = []
        for each in frequent_sequences[n]:
            k_freq_sequences.append(each[0])

        candidates = gen_candidate(k_freq_sequences)

        for each in candidates:
            sup = support_counting(each, course, maxgap, sequences) / count
            if sup > minsup:
                frequent_sequences[n + 1].append([each, sup])

        if frequent_sequences[n + 1] == []:
            frequent_sequences.pop(n + 1)
            break

        n += 1

    # write the result
    output = {}
    for key in frequent_sequences.keys():
        for each in frequent_sequences[key]:
            if not output.has_key(each[1]):
                output[each[1]] = [each[0]]
            else:
                output[each[1]].append(each[0]) 

    num = 0
    for key in sorted(output.keys(), reverse=True):
        for each in output[key]:
            args.outfile.write("%s, %s\n" % (each, key))
            num += 1
        
    print "%s set(s) generated" % num

