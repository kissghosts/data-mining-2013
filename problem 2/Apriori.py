#!/usr/bin/python
import argparse
import sys
import copy
import time

def support_counting(itemset, itemsets):
    """calc support for a given itemset
    """

    support_count = 0
    for each_set in itemsets:
        if isinstance(itemset, list):
            for each_item in itemset:
                if each_item not in each_set:
                    break
            else:
                support_count += 1
        else:
            if itemset in each_set:
                support_count += 1

    return support_count

def gen_candidate(itemsets):
    """generate candidates by using Fk-1 * Fk-1
    """

    candidates = []
    num = len(itemsets)

    # the combination method used for k = 1 is different 
    if len(itemsets[0]) == 1:
        for n in range(num - 1):
            for m in range(n + 1, num):
                    candidates.append([itemsets[n][0], itemsets[m][0]])
    else:
        for n in range(num - 1):
            for m in range(n + 1, num):
                if (itemsets[n][:-1] == itemsets[m][:-1] 
                    and itemsets[n][1:] + [itemsets[m][-1]] in itemsets):
                    candidates.append(itemsets[n] + [itemsets[m][-1]])

    return candidates

def is_subset(set1, set2):
    """check whether set1 is subset of set2, returen True or False
    """

    for item in set1:
        if item not in set2:
            return False
    else:
        return True

def max_frequent(frequent_itemsets):
    """use specific-to-general method to prune all subsets of maximal 
    frequent itemsets
    1. start from the max-k level of frequent itemsets, 
    where all sets are maximal
    2. prune all the subsets of the maximal frequent itemsets 
    in step 1 recursively
    3. move to another maximal frequent itemset and repeat
    """

    size = len(frequent_itemsets)
    for i in range(size, 0, -1):
        if frequent_itemsets[1]:
            for each in frequent_itemsets[i]:
                for j in range(i - 1, 0, -1):
                    # the loop will modify the frequent_itemsets, 
                    # so use deepcopy
                    iter_itemsets = copy.deepcopy(frequent_itemsets[j])
                    for itemset in iter_itemsets:
                        if is_subset(itemset[0], each[0]):
                            frequent_itemsets[j].remove(itemset)    
    return frequent_itemsets

def closed_frequent(frequent_itemsets):
    """chech all the frequent itemsets to find the closed ones
    """

    closed_freq_itemsets = {}
    size = len(frequent_itemsets)
    closed_freq_itemsets[size] = frequent_itemsets[size]
    
    for i in range(1, size):
        closed_freq_itemsets[i] = []
        for each in frequent_itemsets[i]:
            for itemset in frequent_itemsets[i + 1]:
                if is_subset(itemset[0], each[0]) and itemset[1] == each[1]:
                    break
            else:
                closed_freq_itemsets[i].append(each)

    return closed_freq_itemsets

def sub(set1, set2):
    """return = set2 - set1
    """

    result = []
    for each in set2:
        if not each[0] in set1:
            result.append(each[0])
    return result

def gen_rules(minconf, frequent_itemsets):
    """rule generation
    """
    
    result = {}

    for n in range(2, len(frequent_itemsets) + 1):
        for itemset in frequent_itemsets[n]:
            h = []
            for each in itemset[0]:
                h.append([each])

            k_itemset = copy.deepcopy(h)
            count = len(k_itemset)
            for i in range(count - 1):
                for each in k_itemset:
                    div = sub(each, k_itemset)
                    for l in frequent_itemsets[len(div)]:
                        if sorted(div) == sorted(l[0]):
                            sup = l[1]
                            break
                          
                    conf = itemset[1] / sup
                    if conf < minconf:
                        if each in h:
                            h.remove(each)
                    elif (result.has_key(conf) 
                        and [div, each] not in result[conf]):
                        result[conf].append([div, each])
                    else:
                        result[conf] = [[div, each]]

                if h:
                    h = gen_candidate(h)
                else:
                    break

    return result


if __name__ == '__main__':
    # option parser
    parser = argparse.ArgumentParser(description='description: '
        'Apriori algorithm')
    parser.add_argument('--t', dest='type', choices=['f', 'c', 'm', 'r'], 
        default='f', help="choose func type. f: frequent, c: closed, m: "
        "maximal, r: rule, default value is f")
    parser.add_argument('--s', dest='support', type=int, default=10, 
        help="support value, default value is 10 (10 percent)")
    parser.add_argument('infile', type=argparse.FileType('r'), 
        help='path of input file')
    parser.add_argument('outfile', type=argparse.FileType('w'), 
        help='path of output file')
    parser.add_argument('--token', type=str, default=' ', 
        help="string used for splitting each transaction, e.g. ',', "
        "default value is space")
    parser.add_argument('--minsize', type=int, default=1, help="minimal size "
        "of frequent itemsets")
    parser.add_argument('--maxsize', type=int, default=30, help="max size of "
        "frequent itemsets")
    parser.add_argument('--c', dest='conf', type=int, default=80, 
        help="confidence value, default value is 80 (80 percent)")
    
    args = parser.parse_args()
    
    if args.minsize < 1:
        print "error: minsize should be larger than 1"
        sys.exit(1)

    # pre-process the input data
    minsup = args.support / 100.0
    maxsize = args.maxsize
    minsize = args.minsize
    if maxsize < 1:
        print "error: maxsize should be equal to or larger than 1"
        sys.exit(1)
    
    items = []
    itemsets = []
    frequent_itemsets = {}
    for line in args.infile:
        itemset = line.strip().split(args.token)
        if itemset:
            itemsets.append(sorted(itemset))
            for item in itemset:
                if item not in items:
                    items.append(item)

    items.sort()
    itemset_count = float(len(itemsets))
    print "%s item(s), %s transaction(s)" % (len(items), len(itemsets))
    print "generating set(s) ..."
    start_time = time.time()

    # generate the 1-size itemsets
    frequent_itemsets[1] = []
    for each in items:
        sup = support_counting(each, itemsets) / itemset_count
        if sup > minsup:
            frequent_itemsets[1].append([[each], sup])

    # generate frequent itemset
    if not frequent_itemsets:
        print "no set generated"
        sys.exit(0)

    n = 1
    while n < maxsize:
        frequent_itemsets[n + 1] = []
        k_freq_itemsets = []
        for each in frequent_itemsets[n]:
            k_freq_itemsets.append(each[0])

        candidates = gen_candidate(k_freq_itemsets)

        for each in candidates:
            sup = support_counting(each, itemsets) / itemset_count
            if sup > minsup:
                frequent_itemsets[n + 1].append([each, sup])

        if frequent_itemsets[n + 1] == []:
            frequent_itemsets.pop(n + 1)
            break

        n += 1

    # maximal, closed or rule generation
    if args.type == 'm':
        frequent_itemsets = max_frequent(frequent_itemsets)
    elif args.type == 'c':
        frequent_itemsets = closed_frequent(frequent_itemsets)
    elif args.type == 'r':
        minconf = args.conf / 100.0
        rules = gen_rules(minconf, frequent_itemsets)
        end_time = time.time()
        print ("generating set(s) done [%.4fs]" % (end_time - start_time))

        print "writing outfile ..."
        num = 0
        for each in sorted(rules.keys(), reverse=True):
            if int(each) < minsize:
                continue 

            if len(rules[each]) > 1:
                for rule in rules[each]:
                    args.outfile.write("%s => %s (%s)\n" % (rule[0], 
                        rule[1], each))
                    num += 1
            else:
                args.outfile.write("%s => %s (%s)\n" % (rules[each][0][0], 
                    rules[each][0][1], each))
                num += 1

        print "%s set(s) generated" % num
        sys.exit(0)

    # write the result
    end_time = time.time()
    print "generating set(s) done [%.4fs]" % (end_time - start_time)
    output = {}
    for i in range(minsize, len(frequent_itemsets) + 1):
        if frequent_itemsets[i]:
            for each in frequent_itemsets[i]:
                if not output.has_key(each[1]):
                    output[each[1]] = [each[0]]
                else:
                    output[each[1]].append(each[0]) 

    print "writing outfile ..."
    num = 0
    for each in sorted(output.keys(), reverse=True):
        if each:
            if len(output[each]) > 1:
                for itemset in output[each]:
                    args.outfile.write("%s, %s\n" % (itemset, each))
                    num += 1
            else:
                args.outfile.write("%s, %s\n" % (output[each][0], each))
                num += 1

    print "%s set(s) generated" % num