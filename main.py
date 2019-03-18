#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator

class Token:
    def __init__(self, tokentype, tokenvalue):
        self.tokentype = tokentype
        self.tokenvalue = tokenvalue

class PrePro:
    def removeComments(origin):
        flag = False
        procorigin = ''
        for i in origin:
            if (i == "'" or i == '\n'):
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
            if (not self.origin[self.position].isdigit()):
                token += self.origin[self.position]
                self.position += 1
            if (token == '+'):
                self.actual = Token('PLUS', token)
            elif (token == '-'):
                self.actual = Token('MINUS', token)
            elif (token == '*'):
                self.actual = Token('MULT', token)
            else:
                self.actual = Token('DIV', token)


class Parser:
    def termExpression():
        try:
            num1 = Parser.tokens.actual
        except:
            raise ValueError('Token not found')

        if (num1.tokentype == 'INT'):
            res = int(num1.tokenvalue)
            Parser.tokens.selectNext()
            op = Parser.tokens.actual

            while (op.tokentype == 'DIV' or op.tokentype == 'MULT'):
                if (op.tokentype == 'DIV'):
                    Parser.tokens.selectNext()
                    num2 = Parser.tokens.actual
                    if (num2.tokentype == 'INT'):
                        res = res // int(num2.tokenvalue)
                    else:
                        raise ValueError('Unespected token type %s' %(num2.tokentype))
                elif (op.tokentype == 'MULT'):
                    Parser.tokens.selectNext()
                    num2 = Parser.tokens.actual
                    if (num2.tokentype == 'INT'):
                        res *= int(num2.tokenvalue)
                    else:
                        raise ValueError('Unespected token type %s' %(num2.tokentype))
                Parser.tokens.selectNext()
                op = Parser.tokens.actual
        else:
            raise SyntaxError('Invalid token, element %s is not INT' %(num1.tokentype))

        return res

    @staticmethod
    def parserExpression():
        allowed_operators={
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "//": operator.floordiv
        }
        res = Parser.termExpression()
        op = Parser.tokens.actual
        while (op.tokentype == 'PLUS' or op.tokentype == 'MINUS'):
            Parser.tokens.selectNext()
            num2 = Parser.termExpression()
            res = allowed_operators[op.tokenvalue](res, num2)
            op = Parser.tokens.actual
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
    print('\nType a math operation (+, -, * and // allowed):')
    test = input()
    print('\nResult:', Parser.run(test))
