#!/usr/bin/python

import re

def is_cond_in(cond, rule, index):
    if cond == rule[index]:
        return True
    else:
        return False

def is_continuous_cond_in(interval, rule, index):
    if isinstance(rule[index], str) and rule[index].find('%') != -1:
        value = float(rule[index].replace('%', ''))
    else:
        value = float(rule[index]) * 100

    if value >= interval[0] and value < interval[1]:
        return True
    else:
        return False

def find_dist_region(dataset, inlist, target, minsup, index, num, namestr):

    result = []
    for each in inlist:
        sup = 0
        for rule in dataset[target]:
            if is_cond_in(each, rule, index):
                sup += 1

        sup = sup * 1.0 / num
        if sup >= minsup:
            result.append(["%s=%s" % (namestr, each), sup])

    return result

def find_continuous(dataset, inlist, target, minsup, index, num, namestr):
    cond = []
    for each in inlist:
        sup = 0
        for rule in dataset[target]:
            if is_continuous_cond_in(each, rule, index):
                sup += 1

        sup = sup * 1.0 / num
        if sup >= minsup:
            cond.append(["%d<=%s<%d" % (each[0], namestr, each[1]), sup])
            
    return cond

def support_counting(condition, dataset):
    
    sup_count = 0.0
    for each in dataset:
        for cond in condition:
            if not is_cond_true(cond, each):
                break
        else:
            sup_count += 1

    return sup_count            


def is_cond_true(cond, rule):
    global district_index, region_index, frl_index
    global pct_asian_index, pct_black_index, pct_hisp_index, pct_white_index

    flag = False
    try:
        mstr = re.match('(\w+)=(.*)', cond)
        if mstr:
            m = mstr.groups()
            if m[0] == 'district' and int(m[1]) == rule[district_index]:
                flag = True
            elif m[0] == 'region' and m[1] == rule[region_index]:
                flag = True
        else:
            m = re.match('([\d|\.]+)[<|=]+(\w+)<([\d|\.]+)', cond).groups()
            if m[1] == 'frl':
                pct = float(rule[frl_index].replace('%', ''))
                if float(m[0]) <= pct and float(m[2]) > pct:
                    flag = True
            elif m[1] == 'pct_asian':
                # print m
                if (float(m[0]) <= float(rule[pct_asian_index]) * 100 
                    and float(m[2]) > float(rule[pct_asian_index]) * 100):
                    flag = True
            elif m[1] == 'pct_black':
                if (float(m[0]) <= float(rule[pct_black_index]) * 100 
                    and float(m[2]) > float(rule[pct_black_index]) * 100):
                    flag = True
            elif m[1] == 'pct_hisp':
                if (float(m[0]) <= float(rule[pct_hisp_index]) * 100 
                    and float(m[2]) > float(rule[pct_hisp_index]) * 100):
                    flag = True
            elif m[1] == 'pct_white':
                if (float(m[0]) <= float(rule[pct_white_index]) * 100 
                    and float(m[2]) > float(rule[pct_white_index]) * 100):
                    flag = True
    except Exception:
        pass

    return flag

if __name__ == '__main__':

    minsup = 0.05
    minconf = 0.7
    target = 'C'
    # conf+, conf-, qg, wra
    method = 'qg'
    g = 1
    k = 10
    district_index = 1
    region_index = 2
    grade_index = 3
    frl_index = 12
    pct_asian_index = 15
    pct_black_index = 16
    pct_hisp_index = 17
    pct_white_index = 18

    infile = open('dataset.csv', 'rU')

    dataset = {'A': [], 'B': [], 'C': [], 'DF': []}
    district = []
    region = []

    # frl = []
    # frl_step = 10
    # for i in range(0, 100, frl_step):
    #     frl.append((i, i + frl_step))
    frl = [(0, 20), (20, 50), (50, 100)]
    pct_asian = [(0, 1.5), (1.5, 3), (3, 100)]
    pct_black = [(0, 2), (2, 4), (4, 100)]
    pct_hisp = [(0, 20), (20, 40), (40, 100)]
    pct_white = [(0, 30), (30, 60), (60, 100)]

    total_num = 0
    for line in infile:
        school = line.strip().split(',')
        if not school[0].isdigit():
            continue

        total_num += 1
        for i in range(len(school)):
            if school[i].isdigit() and i < frl_index:
                school[i] = int(school[i])

        if school[1] not in district:
            district.append(school[1])
        if school[2] not in region:
            region.append(school[2])

        if school[grade_index] >= 11: 
            dataset['A'].append(school)
        elif school[grade_index] >= 8 and school[grade_index] < 11:
            dataset['B'].append(school)
        elif school[grade_index] < 8 and school[grade_index] >= 5:
            dataset['C'].append(school)
        else:
            dataset['DF'].append(school)

    dist_cond = find_dist_region(dataset, district, target, minsup, 1, 
        total_num, 'district')
    reg_cond = find_dist_region(dataset, region, target, minsup, 2, total_num, 
        'region')
    
    frl_cond = find_continuous(dataset, frl, target, minsup, frl_index, 
        total_num, 'frl')
    pct_asian_cond = find_continuous(dataset, pct_asian, target, minsup,
        pct_asian_index, total_num, 'pct_asian')
    pct_black_cond = find_continuous(dataset, pct_black, target, minsup, 
        pct_black_index, total_num, 'pct_black')
    pct_hisp_cond = find_continuous(dataset, pct_hisp, target, minsup, 
        pct_hisp_index, total_num, 'pct_hisp')
    pct_white_cond = find_continuous(dataset, pct_white, target, minsup, 
        pct_white_index, total_num, 'pct_white')

    conditions = [dist_cond, reg_cond, frl_cond, pct_asian_cond, 
        pct_black_cond, pct_hisp_cond, pct_white_cond]

    # print conditions
    
    # 2-size conditions
    freq_conds = {}
    size = len(conditions)
    for i in range(size):
        for cond1 in conditions[i]:
            for j in range(i + 1, size):
                for cond2 in conditions[j]:
                    cond = [cond1[0], cond2[0]]
                    sup_count = support_counting(cond, dataset[target])
                    sup = sup_count / total_num

                    if sup >= minsup:
                        if freq_conds.has_key(2):
                            freq_conds[2].append([cond, sup])
                        else:
                            freq_conds[2] = [[cond, sup]]

    # size >= 3
    n = 2
    size = len(freq_conds[n])
    while size > 1:
        n += 1
        for i in range(size):
            for j in range(i + 1, size):
                if freq_conds[n - 1][i][0][1:] == freq_conds[n - 1][j][0][:-1]:
                    cond = (freq_conds[n - 1][i][0] 
                        + [freq_conds[n - 1][j][0][-1]])
                    sup_count = support_counting(cond, dataset[target])
                    sup = sup_count / total_num

                    if sup >= minsup:
                        if freq_conds.has_key(n):
                            freq_conds[n].append([cond, sup])
                        else:
                            freq_conds[n] = [[cond, sup]]

        if freq_conds.has_key(n):
            size = len(freq_conds[n])
        else:
            size = 0

    if method == 'conf+':
        result = {}
        for catagory in conditions:
            for cond in catagory:
                sup_count = 0
                for key in dataset:
                    sup_count += support_counting([cond[0]], dataset[key])

                conf = cond[-1] * total_num / sup_count
                if conf > minconf:
                    if result.has_key(conf):
                        result[conf].append(cond)
                    else:
                        result[conf] = [cond]
        for key in freq_conds:
            for each in freq_conds[key]:
                sup_count = 0
                for eachkey in dataset:
                    sup_count += support_counting(each[0], dataset[eachkey])
                
                conf = each[-1] * total_num / sup_count
                if conf > minconf:
                    if result.has_key(conf):
                        result[conf].append(each)
                    else:
                        result[conf] = [each]
        
        for key in sorted(result.keys(), reverse=True):
            print "conf=%.4f, %s" % (key, result[key])
    elif method == 'conf-':
        result = {}
        for catagory in conditions:
            for cond in catagory:
                conf = cond[-1] * total_num / len(dataset[target])
                if conf > minconf:
                    if result.has_key(conf):
                        result[conf].append(cond)
                    else:
                        result[conf] = [cond]
        for key in freq_conds:
            for each in freq_conds[key]: 
                conf = each[-1] * total_num / len(dataset[target])
                if conf > minconf:
                    if result.has_key(conf):
                        result[conf].append(each)
                    else:
                        result[conf] = [each]
        for key in sorted(result.keys(), reverse=True):
            print "conf=%.4f, %s" % (key, result[key])
    elif method == 'qg':
        beam = {}
        for catagory in conditions:
            for cond in catagory:
                sup_count = 0
                for key in dataset:
                    if key == target:
                        continue

                    sup_count += support_counting([cond[0]], dataset[key])

                qg = (cond[-1] * total_num) / (sup_count + g)
                if beam.has_key(qg):
                    beam[qg].append(cond)
                else:
                    beam[qg] = [cond]

        for key in freq_conds:
            for each in freq_conds[key]:
                sup_count = 0
                for eachkey in dataset:
                    if eachkey == target:
                        continue
                    
                    sup_count += support_counting(each[0], dataset[eachkey])
                
                qg = (each[-1] * total_num) / (sup_count + g)
                if beam.has_key(qg):
                    beam[qg].append(each)
                else:
                    beam[qg] = [each]

        for key in sorted(beam.keys(), reverse=True):
            if k < 0:
                break

            print "qg=%.4f, %s" % (key, beam[key])
            k -= 1

    elif method == 'wra':
        beam = {}
        for catagory in conditions:
            for cond in catagory:
                sup_count = 0
                for key in dataset:
                    sup_count += support_counting([cond[0]], dataset[key])

                wra = (cond[-1] - (sup_count / total_num) 
                    * (len(dataset[target]) / total_num))
                
                if beam.has_key(wra):
                    beam[wra].append(cond)
                else:
                    beam[wra] = [cond]

        for key in freq_conds:
            for each in freq_conds[key]:
                sup_count = 0
                for eachkey in dataset:
                    sup_count += support_counting(each[0], dataset[eachkey])

                wra = (each[-1] - (sup_count / total_num) 
                    * (len(dataset[target]) / total_num))
                
                if beam.has_key(wra):
                    beam[wra].append(each)
                else:
                    beam[wra] = [each]

        for key in sorted(beam.keys(), reverse=True):
            if k < 0:
                break

            print "wra=%.4f, %s" % (key, beam[key])
            k -= 1
    else:
        pass

