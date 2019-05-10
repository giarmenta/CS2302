# -*- coding: utf-8 -*-
"""
Created on Tue May 7 10:45:10 2019
@author: Gerardo Armenta
Instructor: Dr. Olac Fuentes
TA: Anindita Nath, Maliheh Zargaran, Erik Macik, Eduardo Lara
Purpose: part1: To write a program that discovers trigonometric identities using a randomized
                algorithm to detect equalities using random numbers in range of -pi to pi. 
         part2: To write a program that determines if there is a way to partition a set of
                integers into two substes using backtracking.
"""

import random
import math
import mpmath
import time

'''  
###############################################################################
                                 PART 1
###############################################################################
'''

# Checks equality for all trig functions in main with different t values
def are_equal(f1, f2, n):
    # There are n (length of trig functions list) number of times trig functions
    # are checked for equalities.
    for i in range(n):
        t = random.uniform(-math.pi,math.pi)  # t varies per each test
        # The following functions aren't recognized by the math libary used
        # so they are changed to be recognized by math and mpmath (for sec(t)).
        if f1 == 'sin^2(t)':  # sin(t) to the power of 2
            f1 = 'math.pow(math.sin(t),2)'
        if f1 == '1-cos^2(t)':  # 1 - cos(t) to the power of 2
            f1 = '1-math.pow(math.cos(t),2)'
        if f1 == 'sec(t)':  # sec not recognized by math, used mpmath
            f1 = 'mpmath.sec(t)'
        if f2 == 'sin^2(t)':  # sin(t) to the power of 2
            f2 = 'math.pow(math.sin(t),2)'
        if f2 == '1-cos^2(t)':  # 1 - cos(t) to the power of 2
            f2 = '1-math.pow(math.cos(t),2)'
        if f2 == 'sec(t)':  # sec not recognized by math, used mpmath
            f2 = 'mpmath.sec(t)'
        # Values are rounded to the 7th decimal point to avoid any float issues.
        y1 = round(eval(f1), 7)
        y2 = round(eval(f2), 7)
        if y1 != y2:  # if results after evaluation are different, returns false
            return False
    return True  # returns true if comparisons of trig identities are equal

# Sets the comparisons for the trig identities and shows equalities to the user.
def comparisons(trig, n):
    start = time.time()*1000
    count = 0  # Counter used to show total of equalities found to user.
    while len(trig) > 0:  # gets the first element of the list for f1
        f1 = trig[0]
        trig.pop(0)  # removing element 0 keeps while loop moving and assures f1 and f2 aren't the same
        for function in trig:  # loop used to set f2 and check for equality
            f2 = function
            if are_equal(f1,f2,n) is True:  # if equality found lets user know
                count += 1  # counter adds 1 every time equality is found
                print('\n',f1, ' is equal to ', f2)
    stop = time.time()*1000
    print('\n There are a total of ', count, ' equalities from ', n, ' trigonometric funtions. Time elapsed = ', stop-start, 'milliseconds')

'''  
###############################################################################
                                 PART 2
###############################################################################
'''

# adds the sum of a given subset
def subset(s):
    if len(s) == 0:  # used to return 0 if list is empty
        return 0
    a = sum(s)
    return a
    
    
def partition(S1,S2,last):
    if last < 0:  # once last is less than 0 there are no more subsets to be compared
        return False,S1,S2
    if subset(S1) == subset(S2):  # if two subsets are equal, a partition exists
        return True,S1,S2   
    if subset(S1) < subset(S2):  # if S1 is less than S2, the last value added to S2 is returned to S1 and removed from S2
        S1.append(S2[-1])
        S2.remove(S2[-1])
    else:
        S2.append(S1[last])  # if sum of S1 is more than sum of S2, last value is removed from S1 and added to S2
        S1.remove(S1[last])
    return partition(S1,S2,last-1)  # New comparisons are made with changes to subsets S1 and S2 making last subtrated by one to traverse lists

# list of trig identities          
trig_id = ['sin(t)', 'cos(t)', 'tan(t)', 'sec(t)', '-sin(t)', '-cos(t)', '-tan(t)', 'sin(-t)', 'cos(-t)', 'tan(-t)', 'sin(t)/cos(t)', '2*sin(t/2)*cos(t/2)', 'sin^2(t)', '1-cos^2(t)', '(1-cos(2*t))/2', '1/cos(t)']
comparisons(trig_id, len(trig_id))  # will check for equalities in trig_id list

# asks user to select S list
selection = (int(input('Select 1 for S = [2, 4, 5, 9, 12] or select 2 for S = [2, 3, 5, 8, 13]: ')))
if selection == 1:
    S = [2, 4, 5, 9, 12]
else:
    S = [2, 3, 5, 8, 13]
start = time.time()*1000
is_set,s1,s2 = partition(S, [], len(S)-1)
set_list = sorted(s1+s2)  # s1 + s2 will create original S list in ascending order
stop = time.time()*1000
if is_set is True:  # if a partition is found
    print('\n This set: S =', set_list, ' has a partition ', s1, ' ', s2, '. Time elapsed = ', stop-start, 'milliseconds')
else:  # if no partition is found
    print('\n No partition exists for: S =', set_list, '. Time elapsed = ', stop-start, 'milliseconds')
