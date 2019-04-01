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


class Node:
    def __init__(self, value=False, nodes=[]):
        self.value = value
        self.children = nodes
    def Evaluate(self):
        pass

class BinOp (Node):
    def Evaluate(self):
        # https://stackoverflow.com/questions/18591778/how-to-pass-an-operator-to-a-python-function
        allowed_operators={
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "//": operator.floordiv
        }
        child1 = self.children[0]
        child1 = child1.Evaluate()

        child2 = self.children[1]
        child2 = child2.Evaluate()
        return allowed_operators[self.value](child1, child2)

class UnOp(Node):
    def Evaluate(self):
        child = self.children[0]
        child = child.Evaluate()
        if (self.value == '-'):
            return -child
        elif (self.value == '+'):
            return +child

class IntVal(Node):
    def Evaluate(self):
        return self.value

class NoOp(Node):
    pass

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

        elif (self.origin[self.position].isalpha()):
            while (self.origin[self.position].isalpha()):
                token += self.origin[self.position]
                self.position += 1
                if (self.position == (len(self.origin))):
                    break
            if (token == 'print'):
                self.actual = Token('COMM', token)
            else:
                self.actual = Token('IDENT', token)

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
            elif (token == '/'):
                self.actual = Token('DIV', '//')
            elif (token == '//'):
                self.actual = Token('DIV', token)
            elif (token == '('):
                self.actual = Token('PAR', token)
            elif (token == ')'):
                self.actual = Token('PAR', token)
            elif (token == '='):
                self.actual = Token('ASSIG', token)
            elif (token == 'BEGIN'):
                self.actual = Token('COMM', token)
            elif (token == 'END'):
                self.actual = Token('COMM', token)
            else:
                raise ValueError('Unexpected token %s' %(token))


class Parser:

    def factorExpression():
        try:
            token1 = Parser.tokens.actual
        except:
            raise ValueError('Token not found')
        if (token1.tokentype == 'INT'):
            Parser.tokens.selectNext()
            return IntVal(int(token1.tokenvalue))

        elif (token1.tokentype == 'PLUS' or token1.tokentype == 'MINUS'):
            if (token1.tokentype == 'PLUS'):
                Parser.tokens.selectNext()
                unop = UnOp('+', [Parser.factorExpression()])
                return unop
            elif (token1.tokentype == 'MINUS'):
                Parser.tokens.selectNext()
                unop = UnOp('-', [Parser.factorExpression()])
                return unop
            else:
                raise SyntaxError('Unexpected unary operation %s' %(token1.tokenvalue))
        elif (token1.tokenvalue == '('):
            Parser.tokens.selectNext()
            expr = Parser.parserExpression()
            if (Parser.tokens.actual.tokenvalue == ')'):
                Parser.tokens.selectNext()
                return expr
            else:
                raise SyntaxError('Unexpected token  %s, expected ")"' %(Parser.tokens.actual.tokenvalue))

        else:
            raise SyntaxError('Invalid token, element %s is not INT' %(token1.tokentype))


    def termExpression():
        factor1 = Parser.factorExpression()
        op = Parser.tokens.actual
        termop = factor1

        while (op.tokentype == 'DIV' or op.tokentype == 'MULT'):
            termop = BinOp(op.tokenvalue, [termop])
            Parser.tokens.selectNext()
            factor2 = Parser.factorExpression()
            termop.children.append(factor2)
            op = Parser.tokens.actual
        return termop

    @staticmethod
    def parserExpression():
        term1 = Parser.termExpression()
        op = Parser.tokens.actual
        parserop = term1

        while (op.tokentype == 'PLUS' or op.tokentype == 'MINUS'):
            parserop = BinOp(op.tokenvalue, [parserop])
            Parser.tokens.selectNext()
            term2 = Parser.termExpression()
            parserop.children.append(term2)
            op = Parser.tokens.actual
        return parserop

    def statement():
        Parser.tokens.selectNext()
        actualtoken = Parser.tokens.actual

        if (actualtoken.tokentype == 'COMM' and actualtoken.tokenvalue == 'print'):
            result = Parser.parserExpression()
            printtree = UnOp('print', [result])
        elif (actualtoken.tokentype == 'IDENT'):
            ident = actualtoken
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokentype == 'ASSIG'):
                result = Parser.parserExpression()
                assigtree = UnOp('assig', [ident, result])
            else:
                raise ValueError('Expected assignment symbol "=", got %s', %(Parser.tokens.actual.tokenvalue))
        elif (actualtoken.tokentype == 'COMM' and actualtoken.tokenvalue == 'BEGIN'):
            Parser.statements()
        else:
            pass

    def statements():
        if (Parser.tokens.actual.tokenvalue == 'BEGIN'):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokenvalue == '\n'):
                while (Parser.tokens.actual.tokenvalue != 'END'):
                    Parser.statement()
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.tokenvalue != '\n'):
                        raise SyntaxError('End line after statement token not found')
            else:
                raise SyntaxError('End line after BEGIN token not found')

    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.parserExpression()
        if (Parser.tokens.actual.tokentype == 'EOF'):
            return result
        else:
            raise EOFError('Program ended before EOF')



'''Rotina de Testes'''

with open('test.vbs', 'r', encoding='utf-8') as infile:
    lines = []
    for line in infile:
        lines.append(line)
print('\nResult:', (Parser.run(lines[0]).Evaluate()))
