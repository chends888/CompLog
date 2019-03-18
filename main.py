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
        i = 0
        while i < len(origin):
            if (i < len(origin)-1):
                if (origin[i] == "'"):
                    flag = not flag
                    i += 1
                    continue
                if (origin[i] + origin[i+1] == '\\n'):
                    flag = not flag
                    i += 2
                    continue
                if (flag):
                    i += 1
                    continue
                procorigin += origin[i]
                i += 1
            else:
                if (origin[i] == "'"):
                    flag = not flag
                    i += 1
                    continue
                if (flag):
                    i += 1
                    continue
                procorigin += origin[i]
                i += 1
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
            elif (token == '//'):
                self.actual = Token('DIV', token)
            elif (token == '('):
                self.actual = Token('(', token)
            elif (token == ')'):
                self.actual = Token(')', token)
            else:
                raise ValueError('Unexpected operation %s' %(token))


class Parser:

    def factorExpression():
        try:
            token1 = Parser.tokens.actual
        except:
            raise ValueError('Token not found')
        if (token1.tokentype == 'INT'):
            Parser.tokens.selectNext()
            return int(token1.tokenvalue)

        elif (token1.tokentype == 'PLUS' or token1.tokentype == 'MINUS'):
            if (token1.tokentype == 'PLUS'):
                Parser.tokens.selectNext()
                return +Parser.factorExpression()
            elif (token1.tokentype == 'MINUS'):
                Parser.tokens.selectNext()
                return -Parser.factorExpression()
            else:
                raise SyntaxError('Unexpected unary operation %s' %(token1.tokenvalue))
        elif (token1.tokentype == '('):
            Parser.tokens.selectNext()
            expr = Parser.parserExpression()
            if (Parser.tokens.actual.tokentype == ')'):
                Parser.tokens.selectNext()
                return expr
            else:
                raise SyntaxError('Unexpected token  %s, expected ")"' %(Parser.tokens.actual.tokenvalue))

        else:
            raise SyntaxError('Invalid token, element %s is not INT' %(token1.tokentype))


    def termExpression():
        allowed_operators={
            "*": operator.mul,
            "//": operator.floordiv
        }
        factor1 = Parser.factorExpression()
        op = Parser.tokens.actual

        while (op.tokentype == 'DIV' or op.tokentype == 'MULT'):
            Parser.tokens.selectNext()
            factor2 = Parser.factorExpression()
            factor1 = allowed_operators[op.tokenvalue](factor1, factor2)
            op = Parser.tokens.actual
        return factor1

    @staticmethod
    def parserExpression():
        allowed_operators={
            "+": operator.add,
            "-": operator.sub
        }
        term1 = Parser.termExpression()
        op = Parser.tokens.actual
        while (op.tokentype == 'PLUS' or op.tokentype == 'MINUS'):
            Parser.tokens.selectNext()
            term2 = Parser.termExpression()
            term1 = allowed_operators[op.tokenvalue](term1, term2)
            op = Parser.tokens.actual
        return term1

    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.parserExpression()
        if (Parser.tokens.actual.tokentype == 'EOF'):
            return result
        else:
            raise EOFError('Program ended before EOF')



# Testes
while True:
    print('\nType a math operation (+, -, * and // allowed):')
    test = input()
    print('\nResult:', Parser.run(test))
