import operator
import typing as t

# TODO
# proper testing of things
# mb fast zig impl for fun, comptiming things could be fun (?)
# maybe comment more things?

ParserP = t.Callable[[str], t.Tuple[t.Any, str]]

class ParseError(Exception): 
    def __init__(self, msg, content):
        super().__init__(f'{msg}: {content}')

def parse(p:ParserP, s:str) -> t.Tuple[t.Any, str]:
    (a, s) = p(s)
    return (a,s)

def satisfy(predicate:t.Callable[['char'], bool]):
    def func(s):
        if not s:
            raise ParseError("empty string")
        if predicate(s[0]):
            return (s[0], s[1:])
        raise ParseError(f'Unexpected condition {s}', s)
    return func

#def oneChar(c) -> ParserP:
#    def func(st):
#        if st[0] == c:
#            return (st[0], s[1:])
#        else:
#            raise ParseError(f'unexpected {st[0]}, expected {c}')
#    return func

def oneChar(c) -> ParserP:
    return satisfy(lambda i: i==c)

def anyChar() -> ParserP:
    def func(st):
        return (st[0], st[1:])
    return func

def anyDigit() -> ParserP:
    return satisfy(lambda i: i.isdigit())

#def anyDigit() -> ParserP:
#    def func(st):
#        if st[0].isDigit() :
#            return (st[0], s[1:])
#        else:
#            raise ParseError(f'unexpected {st[0]}, expected a digit')
#    return func


def oneDigit(d) -> ParserP:
    d = str(d)
    def func(st):
        if st[0] == d:
            return (st[0], st[1:])
        else:
            raise ParseError(f'unexpected {st[0]}, expected a digit', st)
    return func

def compose(p1:ParserP, p2:ParserP) -> ParserP:
    def func(i):
        (st1, s1) = p1(i)
        (st2, s2) = p2(s1)
        return ((st1, st2), s2)
    return func

def choice(p1:ParserP, p2:ParserP):
    def func(i):
        try:
            return p1(i)
        except ParseError as pe:
            return p2(i)
    return func

ParserF = t.Callable[[t.Any], ParserP]
# while ParserP is a static function/parser, 
# parserF is a function that produces a parser. 

def bind(p1:ParserP, pf:ParserF) -> ParserP:
    'We have a parser, and whatever is its output gets passed onto pf, which then decides on the next parser to be used on the resulting text'
    def func(s):
        (a,s1) = parse(p1,s)
        p2 = pf(a) 
        (b, s2) = parse(p2, s1)
        return (b, s2)

def main():
    # mostly for testing and dev, this file is made to be used as a module, but for now it is what it is.
    print('hello', parse(anyChar(), 'hello'))
    print('any digit ', parse(anyDigit(), '123'))
    print('specific digit ', parse(oneDigit('1'), '123'))
    print('composition', parse(compose(oneDigit('1'),oneChar('b')), '1bcd'))  
    try:
        parse(oneDigit('2'), '123')
    except:
        print('caught exception')
    print('choice 1', parse(choice(oneDigit('1'), oneChar('b')), '1bcd'))  
    print('choice 2', parse(choice(oneDigit('3'), oneDigit('1')), '1bcd'))  
    try:
        parse(choice(oneDigit('3'), oneDigit('7')), '1bcd')
    except:
        print('negative check for choice')
    
if __name__ == '__main__':
    main()

