# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 4/7/2023 15:54
# @Author : Xiaosheng Jin
# @Email : xiaosheng7@126.com
# @File : linkcurve.py
# @Software: PyCharm

import time

from ccnbase import Ccn


def changCCN(valuelist, p=0):
    for i in valuelist:
        valuelist[i] += p
    return valuelist


fdd_1_1 = {5: 35, 14: 35}
fdd_1_2 = {21: 35, 30: 35}
fdd_2 = {37: 35, 46: 35}
tdd_1 = {5: 28, 14: 21, 23: 22, 32: 30}
tdd_2 = {37: 28, 46: 21, 55: 22, 64: 30}

host1 = '10.164.147.74'
host2 = '10.164.147.75'


def link_curve(fddccn, tddccn, t, v1, v2):
    ccn1 = Ccn(host1)
    ccn2 = Ccn(host2)

    def setv(fddccn, tddccn):
        if fddccn != {}:
            ccn1.set_values(fddccn)
        if tddccn != {}:
            ccn2.set_values(tddccn)

    setv(fddccn, tddccn)
    time.sleep(5)

    print('\n start to test link curve \n')

    for i in range(t):
        print('\nThis is the %d cycle!\n' % (i + 1))
        setv(changCCN(fddccn, v1), changCCN(tddccn, v2))
        time.sleep(5)

    del ccn1
    del ccn2


if __name__ == '__main__':
    link_curve(fdd_1_1, tdd_1, 18, 3, 3)
