# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import time
import re
import traceback


def st_col(num, st, right=False):
    l = len(st)
    res = u""
    if right: 
        part = (num - l)
        res = st + (u' ' * part)
        
    else:
        part = (num - l)
        res = str(u' ' * part) + st

    return res
    
# удаление лишних нулей справа и слева от числа (для формы создания, редактирование товара)
def empty_nl_temp(nstr):
    if nstr != '0':
        nstr = str(nstr)
        
        isPoint = False
        if re.search(r'\.$', nstr):
            isPoint = True
        
        nlist = nstr.split('.')
        nstr = ''
        
        ns_left = re.sub(r"^[0]{0,}", "", nlist[0])
        
        try:
            ns_right = nlist[1]
        except IndexError:
            ns_right = ''
        
        if ns_left == '':
            nstr += '0'
        else:
            nstr += ns_left
            
        if (ns_left == '' and ns_right == '') or ns_right == '':
            nstr += ''
        else:
            nstr += '.'

        nstr += ns_right
        
        if isPoint:
            nstr += '.'

    return nstr
    
# удаление лишних нулей справа и слева от числа
def empty_nl(nstr):
    if nstr != '0':
        nstr = str(nstr)
        nlist = nstr.split('.')
        nstr = ''
        
        ns_left = re.sub(r"^[0]{0,}", "", nlist[0])
        
        try:
            ns_right = re.sub(r"[0]{0,}$", "", nlist[1])
        except IndexError:
            ns_right = ''
        
        if ns_left == '':
            nstr += '0'
        else:
            nstr += ns_left
            
        if (ns_left == '' and ns_right == '') or ns_right == '':
            nstr += ''
        else:
            nstr += '.'

        nstr += ns_right

    return nstr