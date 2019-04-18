# 18.04.2019 00:20

import argparse
import math
from math import *

ap = argparse.ArgumentParser(description='Pure-python command-line calculator.')
ap.add_argument('EXPRESSION', type=str, help='expression string to evalute')
ap.add_argument('-p', '--PRINT', default='n', choices=['y', 'n'], type=str, help='print evaluation process')
ap.add_argument('-m', '--MODULE', type=str, help='use modules MODULE [MODULE...] additional modules to use')
args = ap.parse_args()
# print(args.EXPRESSION)
# print(args.PRINT)
# print(args.MODULE)
xpr = args.EXPRESSION
show = args.PRINT
# show = 'y'

# xpr = modstr = args.MODULE
# xpr=
# xpr=mod=__import__(modstr)
# xpr=print (modstr, '=',mod.myfunc(3))


# EVAL TEST
# test = xpr
# test = test.replace('^', '**')
# test = test.replace(' ', '')
# test = test.replace(', ', '.')
# print ('EVAL:',test, '=',eval(test))
# print(xpr)

oper = ('!', '^', '//', '/', '*', '%', '-', '+', '(', ')', '==', '<=', '>=', '<', '>', '!=', '=')

# func = ('sin', 'cos', 'tan', 'log10', 'log', 'exp', 'abs', 'round', 'sqrt')

funclist = dir(math)+['abs']      # list of math functions names
funcdict = math.__dict__          # dict of math functions
funcdict['abs'] = abs


#print(func)
xprstr = ''
# word = ''
operator = ''
xprlst = []
a = 0.
b = 0.
result = 0.


# разбор строки на элементы списка
def parse(xprstr):
    word = ''
    # исправление неверно введенных знаков
    xprstr = xprstr.replace(' ', '')
    xprstr = xprstr.replace(', ', '.')
    xprstr = xprstr.replace('--', '+')
    xprstr = xprstr.replace('++', '+')
    xprstr = xprstr.replace('+-', '-')
    xprstr = xprstr.replace('-+', '-')
    xprstr = xprstr.replace('<+', '<')
    xprstr = xprstr.replace('>+', '>')
    xprstr = xprstr.replace('=<', '<=')
    xprstr = xprstr.replace('=>', '>=')
    xprstr = xprstr.replace('==+', '+')
    if xprstr[0] == '+': xprstr = xprstr[1:]
    print('parse:',xprstr)

    # разбор строки
    for i,sym in enumerate(xprstr + ' '):     # добавлен дополнительный пробел
        if sym in oper or i == len(xprstr):
            if word == 'pi':
                xprlst.append(pi)
            elif word == 'e':
                xprlst.append(e)
            elif word in funclist:
                print(word,' in math')
                xprlst.append(word)
            elif word.replace('.', '').isdigit() and word.count('.')<2:
                xprlst.append(float(word))
            #elif word != '':
            #else:
            #    print('ERROR: wrong symbol "',word,sym, '"')
            #    exit(0)
            xprlst.append(sym)
            word = ''
        else:
            word = word + sym

    xprlst.pop()    # удаляется добавленный пробел      

    print(xprlst)

    
    for i,data in enumerate(xprlst):
        if xprlst[i] == '/' and xprlst[i + 1] == '/':
            xprlst[i] = '//'
            xprlst.pop(i + 1)
        if xprlst[i] == '>' and xprlst[i + 1] == '=':
            xprlst[i] = '>='
            xprlst.pop(i + 1)
        if xprlst[i] == '<' and xprlst[i + 1] == '=':
            xprlst[i] = '<='
            xprlst.pop(i + 1)
        if xprlst[i] == '=' and xprlst[i + 1] == '=' or xprlst[i] =='=':
            xprlst[i] = '=='
            xprlst.pop(i + 1)
        if xprlst[i] == '!' and xprlst[i + 1] == '=':
            xprlst[i] = '!='
            xprlst.pop(i + 1)
        if xprlst[i] == '-' and xprlst[i - 1] in ('^', '//', '/', '*', '%', '-', '+', '==', '<=', '>=', '<', '>', '!=', '=') and type(xprlst[i + 1]) == float:
            xprlst[i + 1] = xprlst[i + 1]* - 1
            xprlst.pop(i)
        if (xprlst[i] == '-' and i == 0) or(xprlst[i] == '-' and xprlst[i - 1] in('*', '^', '+', '-', '(', '<', '>', '=') ):
            xprlst[i] = -1
            xprlst.insert(i + 1, '*')
        if xprlst[i] == '-' and xprlst[i - 1] == '/':
            xprlst[i - 1] = '*'
            xprlst[i]=-1
            xprlst.insert(i + 1, '/')
    # print(xprlst)        
    return(xprlst)


def operate2(operator,a,b):
    if operator in dir(math):
        result = math.__dict__[operator](a)
    return result		



def operate(operator,a,b):
    if operator in dir(math):
        result = funcdict[operator](a)
    elif operator == "+":
       result = a + b
    elif operator == "-":
       result=a - b
    elif operator == "*":
       result = a * b

    elif operator == "//":
        if b != 0:
            result=a // b
        else:
            print('ERROR: division by zero')
            exit(0)
    elif operator == "/":
        if b != 0:
            result=a / b
        else:
            print('ERROR: division by zero')
            exit(0)
    elif operator == "%":
       result=a % b
    elif operator == "^":
       result=a**b
    elif operator == "<=":
        result=a <= b
    elif operator == ">=":
        result=a >= b
    elif operator == "<":
        result=a < b
    elif operator == ">":
        result=a > b
    elif operator == "==":
        result=a == b
    elif operator == "!=":
        result=a != b
    else:
        print('ERROR: unknown math operator',operator)
        result=0
    if show == 'y':
        if operator in oper:
            print('Operate:',a,operator,b, '=',result)
        elif operator in func:
            print('Operate:',operator,a, '=',result)
    return result

# вычисление выражения без скобок
def calculate(xprlst):
    if show == 'y': print('Calculate:',xprlst)
    # перебор списка функций 
    for f in funclist:
        for i in range(xprlst.count(f)):
           # print(f,xprlst.count(f))
            s = xprlst.index(f)
            xprlst[s] = (operate(f,xprlst[s + 1],0))
            xprlst[s + 1] = ''
            wipe(xprlst)
            # print(*xprlst,sep = '')
            
    # вычисление возведение в степень с реверсом списка
    # print('^ count:',xprlst.count('^'))
    if '^' in xprlst:
        xprlst.reverse()
        # print('reverse: ',xprlst)
        while '^' in xprlst:
            i = xprlst.index('^')
            # print('i=',i)
            xprlst[i] = xprlst[i + 1]**xprlst[i - 1]
            # print(xprlst[i + 1], '^',xprlst[i - 1], '=',xprlst[i])
            xprlst[i - 1] = ''
            xprlst[i + 1] = ''
            # print(xprlst)
            wipe(xprlst)
            # print(xprlst)
        xprlst.reverse()
        
    # перебор списка математических операций
    for j in oper:
        # print('operation=',j)
        # print(xprlst)
        i = 1
        while i < len(xprlst):
            if xprlst[i] == j:
                # print('calculate: ',*xprlst,sep='')
                xprlst[i] = operate(xprlst[i],xprlst[i - 1],xprlst[i + 1])
                xprlst[i - 1] = ''
                xprlst[i + 1] = ''
                # print(xprlst)
                wipe(xprlst)
                i = i - 1
            i = i + 1
    # print('Stop calculate:',float(xprlst[0]))
    wipe(xprlst)
    # print(xprlst)
    result = xprlst[0]
    if len(xprlst) > 1:
        print('ERROR: missed operator')
        # exit(0)
    return(result)

# очистка списка от пустых значений ''
def wipe(xprlst):
    # print('WIPE:\n',xprlst)
    while '' in xprlst:
        i = xprlst.index('')
        xprlst.pop(i)
    # print('WIPED:\n',xprlst)
    return(xprlst)

# поиск начала и конца выражения в скобках()
def brktindx(xprlst):
    bl = xprlst.index('(')
    br = xprlst.index(')')
    s = xprlst[bl + 1:br]
    # print('BL BR ',bl + 1, ' ',br, ' ',*s,sep='')
    while '(' in s:
        if s.count('(') == s.count(')'):
            bl = xprlst.index('(',bl + 1)
            br = xprlst.index(')',bl + 1)
            s = xprlst[bl + 1:br]
            # print('BL BR ',bl + 1, ' ',br, ' ', *s,sep='')
        else:
            br = xprlst.index(')',br + 1)
            s = xprlst[bl:br + 1]
    return(bl + 1,br)


# основная функция
def main(xpr):
    # проверка скобок в строке
    if xpr.count('(') != xpr.count(')'):
        print('ERROR: brackets are not balanced')
        exit(0)

    # разбор строики в список
    xprlst = parse(xpr)
    # print(*xprlst,sep=', ')





    # поиск скобок и вычисление в скобках
    while '(' in xprlst:
        a,b = brktindx(xprlst)
        # print('in brackets: ',*xprlst[a:b],sep='')
        xprlst[a - 1] = calculate(xprlst[a:b])
        while a < b + 1:
            xprlst[a] = ''
            a = a + 1
        wipe(xprlst)
        # print(*xprlst,sep='')

    # вычисление без скобок
    result = calculate(xprlst)
    # print(result)
    return (result)

print (main(xpr))

