#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Token:
    def __init__(self, tokentype, tokenvalue):
        self.tokentype = tokentype
        self.tokenvalue = tokenvalue

class PrePro:
    def removeComments(origin):
        flag = False
        procorigin = ''
        for i in origin:
            if (i == "'"):
                flag = not flag
                continue
            if (flag):
                continue
            procorigin += i
        return procorigin

class Tokenizer:
    def __init__(self, origin):
        self.origin = PrePro.removeComments(origin)
        self.position = 0
        self.actual = Token('EOF', 'EOF')
        self.selectNext()

    def selectNext(self):
        while (self.position < len(self.origin) and self.origin[self.position] == ' '):
            self.position += 1

        token = ''
        if (self.position >= (len(self.origin))):
            self.actual = Token('EOF', 'EOF')
            return

        elif (self.origin[self.position].isdigit()):
            while (self.origin[self.position].isdigit()):
                token += self.origin[self.position]
                self.position += 1
                if (self.position == (len(self.origin))):
                    break
            self.actual = Token('INT', token)

        else:
            while (not self.origin[self.position].isdigit()):
                token += self.origin[self.position]
                self.position += 1
                if (self.position == (len(self.origin))):
                    break
            if (token == '+'):
                self.actual = Token('PLUS', token)
            elif (token == '-'):
                self.actual = Token('MINUS', token)
            elif (token == '*'):
                self.actual = Token('MULT', token)
            else:
                self.actual = Token('DIV', token)
        
        if (self.position > (len(self.origin))):
            self.actual = Token('EOF', 'EOF')
            return


class Parser:
    @staticmethod
    def parserExpression():
        try:
            num1 = Parser.tokens.actual
            num2 = False
        except:
            raise ValueError('Token not found')

        if (num1.tokentype != 'INT'):
            raise SyntaxError('Invalid start, first element %s is not int' % num1.tokentype)

        op = 'f'
        while (Parser.tokens.actual.tokenvalue != 'EOF'):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokentype == 'PLUS' or Parser.tokens.actual.tokentype == 'MINUS' or Parser.tokens.actual.tokentype == 'DIV' or Parser.tokens.actual.tokentype == 'MULT'):
                op = Parser.tokens.actual

            elif (Parser.tokens.actual.tokentype == 'INT'):
                if (op == 'f'):
                    raise SyntaxError('Unexpected token after %s' % num1.tokenvalue)
                num2 = Parser.tokens.actual

            elif (Parser.tokens.actual.tokentype == 'EOF'):
                break

            if (op.tokentype == 'PLUS' and num2):
                res = int(num1.tokenvalue) + int(num2.tokenvalue)
                num2 = False
                op = 'f'

            elif (op.tokentype == 'MINUS' and num2):
                res = int(num1.tokenvalue) - int(num2.tokenvalue)
                num2 = False
                op = 'f'

            elif (op.tokentype == 'DIV' and num2):
                res = int(num1.tokenvalue) // int(num2.tokenvalue)
                num2 = False
                op = 'f'

            elif (op.tokentype == 'MULT' and num2):
                res = int(num1.tokenvalue) * int(num2.tokenvalue)
                num2 = False
                op = 'f'
            elif (Parser.tokens.position == len(Parser.tokens.origin)):
                raise SyntaxError('Invalid operation %s%s' %(num1.tokenvalue, op.tokenvalue))

        return res

    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.parserExpression()
        if (Parser.tokens.actual.tokentype == 'EOF'):
            return result
        else:
            raise EOFError('Program ended befor EOF')



# Testes
while True:
    print('\nType a math operation (+, -, * and / allowed):')
    test = input()
    print('Result:', Parser.run(test))
