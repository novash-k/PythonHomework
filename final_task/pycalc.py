import argparse
import math
from math import *
import operator
from operator import *
import importlib
import importlib.util

split = ('^', '/', '*', '%', '-', '+', '=', '<', '>', '!',  '(', ')', ',')
# Good style
#funclst = [attr in dir(math) if callable(getattr(math, attr))]
# fundic = dict([(attr, getattr(math, attr)) for attr in dir(math) if callable(getattr(math, attr))])
# callable false pi, e, tau
funclst = dir(math) + ['abs', 'round', 'sum']
funcdic = math.__dict__
operdic = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
        '//': floordiv,
        '%': mod,
        '^': pow,
        '==': eq,
        '<=': le,
        '>=': ge,
        '<': lt,
        '>': gt,
        '!=': ne,
        'abs': abs,
        'round': round,
        'sum': sum
        }
funcdic.update(operdic)
oper = ['^', '//', '/', '*', '%', '-', '+', '==', '<=', '>=', '<', '>', '!=']


def parsecmd():
    """парсинг командной строки"""
    ap = argparse.ArgumentParser(description='Pure-python command-line calculator.')
    ap.add_argument('EXPRESSION', type=str, help='expression string to evalute')
    ap.add_argument('-m', '--MODULE', type=str, help='use modules MODULE [MODULE...] additional modules to use')
    args = ap.parse_args()
    xprstr = args.EXPRESSION
    module = args.MODULE
    return xprstr, module


def addfunc(module):
    """добавление новой функцию из модуля (module)"""
    if module is not None:  # если введено имя модуля
        try:
            spec = importlib.util.find_spec(module)
        except ImportError:
            raise ValueError('ERROR: module ', module, 'not found, or unknown symbol')
        if spec is None:  # проверка возможности импорта модуля
            raise ValueError('ERROR: unknown function or module ', module, 'not found')
        else:
            newfunc = importlib.import_module(module)  # импортирование нового модуля
            funcdic[module] = newfunc.main
            funclst.append(module)
    return


def unaryexp(xprstr):
    """добавление в строку выражения скобок для возведение в степень типа pi^-pi >>> pi^(-pi)"""
    right = len(xprstr)
    for i in range(xprstr.count('^')):
        right = xprstr.rindex('^', 0, right)  # поиск справа первого ^
        if xprstr[right] == '^' and xprstr[right+1] == '-':  # если возведение в степень типа ^-pi добавить скобки
            xprstr = xprstr[:right+1]+'('+xprstr[right+1:]  # добавляем левую (
            right = right + 3
            # поиск строки справа от ^
            brkt = 0
            j = 0
            while j < len(xprstr[right:]) or (brkt == 0 and xprstr[j] == ')'):
                if xprstr[j] == '(':
                    brkt = brkt + 1
                if xprstr[j] == ')':
                    brkt = brkt - 1
                if brkt == 0 and xprstr[j] in oper:
                    j = j - 1
                    break
                j = j + 1
            xprstr = xprstr[:right + 1 + j] + ')' + xprstr[right + 1 + j:]
    return(xprstr)


def brackets4exp(xprstr):
    """добавление в строку выражения скобок для возведение в степень типа 2^3^4 >>> 2^(3^4)"""
    right = len(xprstr)
    for i in range(xprstr.count('^')):
        right = xprstr.rindex('^', 0, right)  # находим позицию самого правого знака ^
        if xprstr[:right].count('^') == 0:
            break
        left = xprstr.rindex('^', 0, right)+1  # находим позицию следущего правого знака ^
        tmp = xprstr[left:right]  # строка между ^ ... ^
        tmpset = set(tmp)
        if (tmp[0] == '(' and tmp[-1] == ')') or (tmpset.isdisjoint(set(split))):  # надо скобки
            xprstr = xprstr[:left]+'('+xprstr[left:]  # вставляем левую скобку
            right = right + 1
            # поиск строки справа от ^
            brkt = 0
            for j, data in enumerate(xprstr[right:]):
                if data == '(':
                    brkt = brkt + 1
                if data == ')':
                    brkt = brkt - 1
                if brkt == 0 and data in ['+', '-', '*', '/']:
                    j = j-1
                    break
                if brkt == 0 and data == ')':
                    break
            xprstr = xprstr[:right+1+j]+')'+xprstr[right + 1 + j:]
        else:  # НЕ надо скобки
            right = left
    return(xprstr)


def preparse(xprstr):
    """очистка строки выражения от мусора, повторных знаков и пробелов"""
    xprset = set(xprstr)
    operset = set(oper)
    operset.add(' ')
    if xprset.issubset(operset):  # проверка если выражение сосотоит только из операторов или пробелов
        raise ValueError('ERROR: no digits or functions in expression')
    if xprstr.count('(') != xprstr.count(')') or len(xprstr) == 0:  # проверка скобок в строке
        raise ValueError('ERROR: brackets are not balanced')
    # устранение пробелов с операторами и повторов операторов
    while xprstr.count('  ') > 0 or \
            xprstr.count('++') > 0 or \
            xprstr.count('-+') > 0 or \
            xprstr.count(' *') > 0 or \
            xprstr.count('* ') > 0 or \
            xprstr.count(' +') > 0 or \
            xprstr.count('+ ') > 0 or \
            xprstr.count(' -') > 0 or \
            xprstr.count('- ') > 0 or \
            xprstr.count(', ') > 0:
        xprstr = xprstr.replace('  ', ' ')
        xprstr = xprstr.replace('++', '+')
        xprstr = xprstr.replace('-+', '-')
        xprstr = xprstr.replace(' *', '*')
        xprstr = xprstr.replace('* ', '*')
        xprstr = xprstr.replace(' +', '+')
        xprstr = xprstr.replace('+ ', '+')
        xprstr = xprstr.replace(' -', '-')
        xprstr = xprstr.replace('- ', '-')
        xprstr = xprstr.replace(', ', ',')
    if xprstr[0] == '+':
        xprstr = xprstr[1:]
    if xprstr.count(' ') > 0:  # проверка лишних пробелов
        raise ValueError('ERROR: useles spaces')
    # print('PREPARSE', xprstr)
    return(xprstr)


def afterparse(xprlst):
    """поиск операторов типа <= >= == !=, замена унарнонго - на -1*"""
    i = 0
    while i < len(xprlst):
        if i < len(xprlst)-1:
            if type(xprlst[i]) == float and xprlst[i+1] == '(':  # елсли перед скобкой цифра без оператора 5(
                raise ValueError('ERROR: digit & ( wihout operator')
            if xprlst[i] == ')' and type(xprlst[i+1]) == float:  # елсли после скобки цифра без оператора (5
                raise ValueError('ERROR: ) & digit wihout operator')
        if i == len(xprlst) - 1:
            break
        if str(xprlst[i]) + str(xprlst[i+1]) in oper:  # '>' + '='
            xprlst[i+1] = str(xprlst[i]) + str(xprlst[i+1])  # '>='
            xprlst.pop(i)
        # унарный минус (-( +-( +-5 +-sin
        # print('i=', i, '[i]=', xprlst[i])
        if xprlst[i] == '-' and xprlst[i-1] in oper+['('] and (type(xprlst[i + 1]) == float
                                                               or xprlst[i + 1] in funclst
                                                               or xprlst[i + 1] == '-'
                                                               or xprlst[i + 1] == '('):
            xprlst[i] = -1
            xprlst = xprlst[:i + 1] + ['*'] + xprlst[i + 1:]
        i = i + 1
    if xprlst[0] == '-':
        xprlst[0] = -1
        xprlst.insert(1, '*')
    # print('AFTERPARSE', *xprlst, sep=' ')
    return(xprlst)


def parse(xprstr):
    """парсинг строки математического выражения. на выходе список в инфиксной нотации"""
    word = ''
    xprlst = []
    xprstr = preparse(xprstr)  # подготовка к парсингу
    xprstr = unaryexp(xprstr)  # добавление скобок для e^-e >>> e^(-e)
    xprstr = brackets4exp(xprstr)  # добавление скобок для 2^3^4 >>> 2^(3^4)
    # print(xprstr)
    # разбор строки
    for i, sym in enumerate(xprstr + ' '):  # добавлен дополнительный пробел
        if sym in split or i == len(xprstr):
            if word in funclst:  # если функция
                xprlst.append(word)
            elif word.replace('.', '').isdigit() and word.count('.') < 2:  # если цифра
                xprlst.append(float(word))
            elif word != '':  # если не пусто и непонятно что, возможно это внешняя функция
                addfunc(word)  # попытка импортировать неизвестную функцию
                xprlst.append(word)
            xprlst.append(sym)
            word = ''
        else:
            word = word + sym
    xprlst.pop()  # удаляется добавленный пробел
    # print('PARSE', *xprlst, sep=' ')
    return xprlst


def prior(op1, op2):
    """сравнивает приоритеты математических опрераторов и функций op1 <= op2, возвращает bool"""
    operhiest = ['^'] + funclst                                         # 4
    operhi = ['*']                                                      # 3
    opermid = ['/', '%', '//']                                          # 2
    operlow = ['+', '-']                                                # 1
    operlowest = ['(', ')', '==', '<=', '>=', '<', '>', '!=', ',']      # 0
    priorset = [operlowest, operlow, opermid, operhi, operhiest]
    for i, data in enumerate(priorset):
        if op1 in data:
            pr1 = i
        if op2 in data:
            pr2 = i
    return pr1 <= pr2


def postfix(xprlst):
    """преобразование инфиксной нотации в постфиксную
    на входе список элементов выражения инфиксной нотации, на выходе список элементов постфиксной нотации"""
    output = []
    stack = []
    for i in xprlst:
        if type(i) == float or type(i) == int:  # если цифра то положить на выход
            output.append(i)
        elif i == ',':  # если , то положить на выход
            if stack != []:
                while stack != [] and stack[-1] in oper+funclst and prior(i, stack[-1]):
                    # пока наверху стека оператор с большим или равным приоритетом
                    output.append(stack.pop())  # переложить оператор из стека на выход
            output.append(i)
        elif i in oper:  # если оператор то положить в стек
            if stack == []:  # если стек пуст, оператор добавить в стек
                stack.append(i)
            elif stack[-1] == '(':  # если стек содержит ( положить в стек (
                stack.append(i)
            else:
                while stack != [] and stack[-1] in oper+funclst and prior(i, stack[-1]):
                    # пока наверху стека оператор с большим или равным приоритетом
                    output.append(stack.pop())  # переложить оператор из стека на выход
                stack.append(i)  # иначе положить оператор в стек
        elif i in funclst or i == '(':  # если функция или ( то помещаем в стек
            stack.append(i)
        elif i == ')':
            while stack[-1] != '(':  # пока верх стека не равен (
                output.append(stack.pop())  # выталкиваем элемент из стека на выход. удаляя последний элемент в стеке
            stack.pop()  # удаление из стека (
    stack.reverse()
    # print('POSTFIX', output, stack )
    return output + stack


def operate(operator, args):
    """выполняет математическое действие или функцию (operator) со списком аргументов (args)"""
    global stack  # используется в функции evalpostfix
    # print('OPERATE', operator, 'ARGS', args, 'STACK', stack)
    try:
        result = funcdic[operator](*args)  # если функция с одним или двумя аргументами типа sin(x), pow(x,y)
        stack.pop()
    except TypeError:
        try:
            result = funcdic[operator](args)  # если функция с аргументом типа список sum(x,y,z,...)
            stack.pop()
        except TypeError:
            try:
                result = funcdic[operator]()  # если функция без аргументов типа pi, e, tau
            except TypeError:
                try:
                    result = funcdic[operator]  # если внешняя функция без аргументов типа myfunc()
                    if type(result) != float:
                        raise ValueError('ERROR: not float argument for ', operator)
                except TypeError:
                    raise ValueError('ERROR: invalid argument for ', operator)
    except ValueError:
        raise ValueError('ERROR: invalid argument for ', operator)
    # print('RESULT', result)
    return result


def evalpostfix(xprpstfx):
    """вычисление выражения в постфиксной нотации (список)"""
    global stack  # используется в функции operate для удаления аргументов из стека
    stack = []
    args = []
    for i in xprpstfx:
        if i in funclst:  # если функция типа sin, pow, sum, tau
            if len(stack) == 0:
                args = 0  # функция без аргументов типа pi, e, tau
            if len(stack) == 1:
                args = stack[0]  # один аргумент функции типа sin(x)
            if len(stack) > 1:
                j = len(stack)-2
                args.append(stack[-1])  # один аргумент функции типа sin(x)
                while stack[j] == ',':  # если в стэке список аргументов разделенных запятой ,
                    args.append(stack[j-1])  # добавить в список агрументов функции типа pow(x,y), sum(x,y,z,...)
                    stack.pop()  # удалить из стэка ,
                    stack.pop()  # удалить из стэка аргумент
                    j = j - 2
                args.reverse()
            # print('OPERATEf', i, 'ARGS', args, 'STACK', stack)
            stack.append(operate(i, args))  # удаление аргумента из стэка произойдет в функции operate
            args = []

        elif i in oper:  # если оператор типа a + b
            # print('OPERATEo', i, 'ARGS', *stack[-2:], 'STACK', stack)
            # print(*stack[-2:])
            # print(funcdic[i])
            tmp = funcdic[i](*stack[-2:])
            stack.pop()  # удалить из стэка аргумент a
            stack.pop()  # удалить из стэка аргумент b
            stack.append(tmp)
            # print('RESULT', tmp)
        else:
            stack.append(i)  # если число то добавить его в стэк
        # print('STACK',stack)
    return stack[0]


def calc(xprstr):
    """вычисление строки (xprstr) математического выражения"""
    xprlst = parse(xprstr)  # разбор строки вырыжения в список
    xprlst = afterparse(xprlst)
    xprlst = postfix(xprlst)  # преобразование инфиксного списка в постфиксных список
    result = evalpostfix(xprlst)  # вычисление постфиксного списка
    print(result)
    return result


def main():
    try:
        xprstr, module = parsecmd()  # парсинг аргументов командной строки xprstr выражение и module модуль функции
        addfunc(module)  # попытка добавления внешней функции если указана -m module
        calc(xprstr)  # калькулятор. вычисление выражения в строке xprstr
    except Exception as error:
        print('ERROR:', error)
    return


if __name__ == '__main__':
    main()
