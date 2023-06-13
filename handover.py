# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2/13/2023 13:56
# @Author : Xiaosheng Jin
# @Email : xiaosheng7@126.com
# @File : ft.py
# @Software: PyCharm

import time

from ccnbase import Ccn


def changCCN(valuelist, p=0, q=0):
    for i in valuelist[0]:
        valuelist[0][i] += p

    for i in valuelist[1]:
        valuelist[1][i] += q

    return valuelist


fdd_1_1 = {5: 35, 14: 35}
fdd_1_2 = {21: 35, 30: 35}
fdd_2 = {37: 35, 46: 35}
tdd_1 = {5: 28, 14: 21, 23: 22, 32: 30}
tdd_2 = {37: 27, 46: 31, 55: 28, 64: 30}

host1 = '10.164.147.74'
host2 = '10.164.147.75'


def mobilityHO(source, target):
    ccn1 = Ccn(host1)
    ccn2 = Ccn(host2)
    def setv(valuelist):
        if valuelist[0] != {}:
            ccn1.set_values(valuelist[0])
        if valuelist[1] != {}:
            ccn2.set_values(valuelist[1])

    setv(source)
    setv(changCCN(target, 30, 30))

    time.sleep(5)

    print('\nUE start to handover from source to target\n')

    for i in range(6):
        print('\nThis is the %d cycle!\n' % (i + 1))
        setv(changCCN(source, 5, 5))
        setv(changCCN(target, -5, -5))

        time.sleep(1)

    print('\n' + '=' * 20 + '  wait 60s  ' + '=' * 20 + '\n')

    time.sleep(30)

    print('\nUE start to handover from target to source\n')

    for i in range(6):
        print('\nThis is the %d cycle!\n' % (i + 1))
        setv(changCCN(source, -5, -5))
        setv(changCCN(target, 5, 5))

        time.sleep(1)

    print('\nHandover success...\n')



    del ccn1
    del ccn2


if __name__ == '__main__':
    mobilityHO([{}, tdd_2], [{}, tdd_1])
