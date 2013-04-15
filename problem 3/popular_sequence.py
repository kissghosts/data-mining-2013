#!/usr/bin/python
import argparse
import sys
import copy
import time
from sets import Set

def support_counting(sequence, sequences):
    """calc support for sequence
    """

    support_count = 0
    for each_sequence in sequences:
        # 1-size sequence
        if isinstance(sequence, int):
            for each_term in each_sequence:
                if sequence in each_term:
                    support_count += 1
                    break
        # sequence which contains more than 1 course
        else:
            super_s = copy.deepcopy(each_sequence)
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
                    subs = sub_sequence(msequence)
                    for each in subs:
                        if each not in sequences:
                            break
                    else:
                        candidates.append(msequence)

    return candidates

def sub_sequence(sequence):
    """generate subsequence for pruning, return a list
    """

    subs = []
    num = len(sequence)
    for i in range(num):
        if i == 0 and len(sequence[i]) > 1:
            for each in sequence[i][1:]:
                copied = copy.copy(sequence[i])
                copied.remove(each)
                sub = [copied] + sequence[(i + 1):]
                if sub not in subs:
                    subs.append(sub)

        if i > 0 and i < num -1:
            for each in sequence[i]:
                copied = copy.copy(sequence[i])
                copied.remove(each)
                sub = sequence[:i] + [copied] + sequence[(i + 1):]
                if sub not in subs:
                    subs.append(sub)

        if i == num -1 and len(sequence[i]) > 1:
            for each in sequence[i][:-1]:
                copied = copy.copy(sequence[i])
                copied.remove(each)
                sub = sequence[:i] + [copied]
                if sub not in subs:
                    subs.append(sub)

    return subs


# main func
if __name__ == '__main__':
    # option parser
    parser = argparse.ArgumentParser(description='description: '
        'Apriori-like algorithm to find most popular sequence(s)')
    parser.add_argument('--s', dest='support', type=int, default=50, 
        help="support value, default value is 20 (20 percent)")
    parser.add_argument('infile', type=argparse.FileType('r'), 
        help='path of input file')
    parser.add_argument('outfile', type=argparse.FileType('w'), 
        help='path of output file')
    parser.add_argument('--ctoken', type=str, default=' ', 
        help="string used for splitting each course, e.g. ',', "
        "default value is space")
    parser.add_argument('--ttoken', type=str, default=', ', 
        help="string used for splitting each course, e.g. ',', "
        "default value is ', '")
    parser.add_argument('--minsize', type=int, default=2, help="minimal size "
        "of frequent itemsets")
    parser.add_argument('--maxsize', type=int, default=0, help="max size of "
        "frequent itemsets, 0 means no limitation")
    
    args = parser.parse_args()
    
    if args.minsize < 1:
        print "error: minsize should be larger than 1"
        sys.exit(1)

    # pre-process the input data
    minsup = args.support / 100.0
    minsize = args.minsize
    if args.maxsize <= 0:
        maxsize = 0
    elif args.maxsize < minsize:
        print "error: minsize should not be larger than maxsize"
        sys.exit(1)
    else:
        maxsize = args.maxsize

    sequences = []
    k1_items = []
    frequent_sequences = {}
    for line in args.infile:
        sequence = []
        term = line.strip().split(args.ttoken)
        for each in term:
            str_list = each.split(args.ctoken)
            sequence.append([int(c) for c in str_list])
        sequences.append(sequence)
        
        for each_term in sequence:
            for each_course in each_term:
                if each_course not in k1_items:
                    k1_items.append(each_course)

    # generate the 1-size frequent sequence
    print "%s sequence(s)" % len(sequences)
    print "generating sequence(s) ..."
    start_time = time.time()
    count = len(sequences) + 0.0
    frequent_sequences[1] = []
    for each in k1_items:
        sup = support_counting(each, sequences) / count
        if sup > minsup:
            frequent_sequences[1].append([[[each]], sup])

    if not frequent_sequences[1]:
        print "no sequence generated"
        sys.exit(0)

    # generate all frequent sequences
    n = 1
    while minsize > 1 and ((maxsize != 0 and n < maxsize) or maxsize == 0):
        frequent_sequences[n + 1] = []
        k_freq_sequences = []
        for each in frequent_sequences[n]:
            k_freq_sequences.append(each[0])

        candidates = gen_candidate(k_freq_sequences)

        for each in candidates:
            sup = support_counting(each, sequences) / count
            if sup > minsup:
                frequent_sequences[n + 1].append([each, sup])

        if frequent_sequences[n + 1] == []:
            frequent_sequences.pop(n + 1)
            break

        n += 1

    end_time = time.time()
    print "generating sequence(s) done [%.4fs]" % (end_time - start_time)

    # write the result
    output = {}
    length = len(frequent_sequences) + 1
    end = maxsize if (maxsize != 0 and maxsize < length) else length

    for i in range(minsize, length):
        if frequent_sequences[i]:
            for each in frequent_sequences[i]:
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

