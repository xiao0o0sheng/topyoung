# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2/11/2023 16:32
# @Author : Xiaosheng Jin
# @Email : xiaosheng7@126.com
# @File : ccnbase.py
# @Software: PyCharm
import ast
import sys
import time

import pandas as pd
import parsel
import requests


class Ccn:

    def __init__(self, host):
        self.host = host
        self.url = 'http://{}/cgi-bin/welcome.cgi'.format(self.host)
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                print('Initial connect to server {} success...\n'.format(
                    self.host))
                selector = parsel.Selector(response.text)
                tmp = selector.xpath('//input[1]/@onclick').get()
                res = tmp.split('/')[-1][:-1]
                self.conf = 'http://10.164.132.28/' + res
            else:
                print('status_code:\t', response.status_code)
        except Exception as e:
            print(e)

    def __tmp(self):
        values_response = requests.get(
            'http://{}/cgi-bin/Set_Display.cgi'.format(self.host))
        selector = parsel.Selector(values_response.text)
        values = selector.xpath('//table[1]/tbody[1]/tr/td/text()').getall()
        values = pd.array(values)
        print('\nThe real time values of {}\n'.format(self.host))
        tmp = values.reshape(9, 9)
        return tmp

    def now(self):
        tmp = self.__tmp()
        tmp[0][0] = ''
        df = pd.DataFrame(data=tmp[1:], columns=tmp[0])
        print(df.to_string(index=False))
        print()

    def search(self, k):
        """
        search and print the specified port's value
        :param k: <class 'int'>
        :return: None
        """
        print('\n%s port %d value is:\t' % (self.host, k),
              self.__tmp()[(k - 1) % 8 + 1, (k - 1) // 8 + 1])

    def set_values(self, ccnValues):
        """
        Set specified value
        :param ccnValues: <class 'dict'>, port:value
        :return: None
        """
        for i, j in ccnValues.items():
            cmd = 'http://{}/cgi-bin/setting_id.cgi?ID={}&VALUE={}'.format(
                self.host, str(i), str(j))
            print('%s SET %d:\t%d' % (self.host, i, j))
            response = requests.get(cmd)
            time.sleep(0.1)

    def dynamic_modify(self, ccnValues, k, t):
        """
        Dynamic adjust the CCN's values
        :param ccnValues: ccnValues: <class 'dict'>, {port:value,...}, port: <class 'int'>, value: <class 'int'>
        :param k: <class 'int'>, added value in every cycle
        :param t: <class 'int'>, cycle times
        :return:None
        """
        print('\nStart to dynamic modify {}\'s values!'.format(self.host))
        for i in range(1, t + 1):
            print('\nThis is the {} cycle!\n'.format(i))
            for j in ccnValues:
                ccnValues[j] += k
            self.set_values(ccnValues)
            time.sleep(3)
        print('\nDynamic modify {}\'s values has done!\n'.format(self.host))

    def reset(self):
        """
        Factory reset
        :return: None
        """
        default = {i: 90 for i in range(1, 65)}
        self.set_values(default)
        print('CCN {} has been reset!'.format(self.host))

    def reboot(self):
        """
        Reboot machine
        :return: None
        """
        url = 'http://{}/cgi-bin/reboot.cgi'.format(self.host)
        print('\nreboot %s\n' % self.host)
        requests.get(url)
        time.sleep(5)

    def __del__(self):
        tmp = self.host
        try:
            del self
            print('\nDisconnect to server {} success...'.format(tmp))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ccn = Ccn(sys.argv[1])
    ccn.set_values(ast.literal_eval(sys.argv[2]))
    ccn.now()
    del ccn
