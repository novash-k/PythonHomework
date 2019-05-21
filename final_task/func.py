
def brexp(xprstr):
    print(xprstr, ' ---------')
    right = xprstr.rindex('^')
    print(right)
    brkt = 0
    for j, data in enumerate(xprstr[right:]):
        if data == '(':
            brkt = brkt + 1
        if data == ')':
            brkt = brkt - 1
        print(j, data, brkt)
        if brkt == 0 and data in ['+', '-', '*', '/']:
            j=j-1
            break
        if brkt == 0 and data == ')':
            break
    print(j)
    print('==== ', xprstr[right+1:right+j+1])
    return

brexp('2^(3*2)^4+2')
brexp('2^333^(3/34+443)+3432')
brexp('2^333^4+2')
brexp('2^333^4/2')
brexp('2^(333-3)^4+(2-2)')
brexp('2^(-333)^(4)+2')
brexp('2^(-333)^e/2')
brexp('2^(-333)^(e+(3))/2')
brexp('2^(-333)^(e+(3))--2')
