#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator
import sys

class Token:
    def __init__(self, tokentype, tokenvalue):
        self.tokentype = tokentype
        self.tokenvalue = tokenvalue

class PrePro:
    @staticmethod
    def removeComments(origin):
        flag = False
        procorigin = ''
        for i in origin:
            if (i == "'"):
                flag = not flag
                continue
            if (i == '\n'):
                flag = False
            if (flag):
                continue
            procorigin += i
        return procorigin

class Node:
    def __init__(self, value=False, nodes=[]):
        self.value = value
        self.children = nodes
    def Evaluate(self, st):
        pass

class BinOp (Node):
    def Evaluate(self, st):
        # https://stackoverflow.com/questions/18591778/how-to-pass-an-operator-to-a-python-function
        allowed_operators={
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "//": operator.floordiv,
            "=": operator.eq,
            ">": operator.gt,
            "<": operator.lt
        }
        child1 = self.children[0]
        child1 = child1.Evaluate(st)

        child2 = self.children[1]
        child2 = child2.Evaluate(st)
        return allowed_operators[self.value](child1, child2)

class UnOp(Node):
    def Evaluate(self, st):
        child = self.children[0]
        child = child.Evaluate(st)
        if (self.value == '-'):
            return -child
        elif (self.value == '+'):
            return +child

class IntVal(Node):
    def Evaluate(self, st):
        return int(self.value)

class Identifier(Node):
    def Evaluate(self, st):
        return st.getter(self.value)

class NoOp(Node):
    pass

class Statements(Node):
    def Evaluate(self, st):
        for i in self.children:
            i.Evaluate(st)

class Assignment(Node):
    def Evaluate(self, st):
        st.setter(self.children[0], self.children[1].Evaluate(st))

class Print(Node):
    def Evaluate(self, st):
        print(self.children[0].Evaluate(st))

class While(Node):
    def Evaluate(self, st):
        while (self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)

class If(Node):
    def Evaluate(self, st):
        if (self.children[0].Evaluate(st)):
            self.children[1].Evaluate(st)
        elif (len(self.children) == 3):
            self.children[2].Evaluate(st)

class Input(Node):
    def Evaluate(self, st):
        print('Input:')
        return int(input())

class Tokenizer:
    def __init__(self, origin):
        self.origin = PrePro.removeComments(origin)
        self.position = 0
        self.actual = Token('EOF', 'EOF')
        self.reservedwords = ['PRINT', 'IF', 'WHILE', 'THEN', 'ELSE', 'WEND', 'INPUT', 'END']
        self.selectNext()

    def selectNext(self):
        while (self.position < len(self.origin) and self.origin[self.position] == ' '):
            self.position += 1

        if (self.position >= (len(self.origin))):
            self.actual = Token('EOF', 'EOF')
            return

        token = ''

        if (self.origin[self.position].isdigit()):
            while (self.position < (len(self.origin)) and self.origin[self.position].isdigit()):
                token += self.origin[self.position]
                self.position += 1
            self.actual = Token('INT', token)

        elif (self.origin[self.position].isalpha()):
            while (self.position < (len(self.origin)) and self.origin[self.position].isalpha()):
                token += self.origin[self.position]
                self.position += 1
            token = token.upper()

            if (token in self.reservedwords):
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
            elif (token == '\n'):
                self.actual = Token('ENDL', token)
            elif (token == '<'):
                self.actual = Token('LESS', token)
            elif (token == '>'):
                self.actual = Token('GREATER', token)
            else:
                raise ValueError('Unexpected token %s' %(token))



class SymbolTable:
    def __init__(self):
        self.symtabledict = {}

    def getter(self, identifier):
        return self.symtabledict[identifier]
    def setter(self, identifier, value):
        self.symtabledict[identifier] = value

class Parser:
    @staticmethod
    def factorExpression():
        try:
            token1 = Parser.tokens.actual
        except:
            raise ValueError('Token not found')
        if (token1.tokentype == 'INT'):
            Parser.tokens.selectNext()
            return IntVal(token1.tokenvalue)

        elif (token1.tokentype == 'PLUS' or token1.tokentype == 'MINUS'):
            if (token1.tokentype == 'PLUS'):
                Parser.tokens.selectNext()
                return UnOp('+', [Parser.factorExpression()])
            elif (token1.tokentype == 'MINUS'):
                Parser.tokens.selectNext()
                return UnOp('-', [Parser.factorExpression()])

            else:
                raise SyntaxError('Unexpected unary operation %s' %(token1.tokenvalue))

        elif (token1.tokentype == 'IDENT'):
            Parser.tokens.selectNext()
            return Identifier(token1.tokenvalue)

        elif (token1.tokenvalue == '('):
            Parser.tokens.selectNext()
            parexpr = Parser.parserExpression()

            if (Parser.tokens.actual.tokenvalue == ')'):
                Parser.tokens.selectNext()
                return parexpr
            else:
                raise SyntaxError('Unexpected token  %s, expected ")"' %(Parser.tokens.actual.tokenvalue))
        elif (token1.tokenvalue == 'INPUT'):
            Parser.tokens.selectNext()
            return Input()
        else:
            raise SyntaxError('Invalid token, element %s is not INT' %(token1.tokenvalue))

    @staticmethod
    def termExpression():
        termop = Parser.factorExpression()
        while (Parser.tokens.actual.tokentype == 'DIV' or Parser.tokens.actual.tokentype == 'MULT'):
            termop = BinOp(Parser.tokens.actual.tokenvalue, [termop])
            Parser.tokens.selectNext()
            factor2 = Parser.factorExpression()
            termop.children.append(factor2)
        return termop

    @staticmethod
    def parserExpression():
        parserop = Parser.termExpression()
        while (Parser.tokens.actual.tokentype == 'PLUS' or Parser.tokens.actual.tokentype == 'MINUS'):
            parserop = BinOp(Parser.tokens.actual.tokenvalue, [parserop])
            Parser.tokens.selectNext()
            parserop.children.append(Parser.termExpression())
        return parserop

    @staticmethod
    def statement():
        if (Parser.tokens.actual.tokentype == 'COMM'):
            if (Parser.tokens.actual.tokenvalue == 'PRINT'):
                Parser.tokens.selectNext()
                printtree = Print('PRINT', [Parser.parserExpression()])
                return printtree
            elif (Parser.tokens.actual.tokenvalue == 'IF'):
                Parser.tokens.selectNext()
                iftree = If('IF',[])
                iftree.children.append(Parser.relExpression())
                if (Parser.tokens.actual.tokenvalue == 'THEN'):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.tokenvalue == '\n'):
                        Parser.tokens.selectNext()
                        iftree.children.append(Parser.statements())
                        if (Parser.tokens.actual.tokenvalue == 'ELSE'):
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.tokenvalue == '\n'):
                                Parser.tokens.selectNext()
                                iftree.children.append(Parser.statements())
                            else:
                                raise SyntaxError('Expected endline token, got %s' %(Parser.tokens.actual.tokenvalue))
                        if (Parser.tokens.actual.tokenvalue == 'END'):
                            Parser.tokens.selectNext()
                            if (Parser.tokens.actual.tokenvalue == 'IF'):
                                Parser.tokens.selectNext()
                                return iftree
                            else:
                                raise SyntaxError('Expected "IF" token, got %s' %(Parser.tokens.actual.tokenvalue))
                        else:
                            raise SyntaxError('Expected "END" token, got %s' %(Parser.tokens.actual.tokenvalue))
                    else:
                        raise SyntaxError('Expected endline token, got %s' %(Parser.tokens.actual.tokenvalue))
                else:
                    raise SyntaxError('Expected "THEN" token, got %s' %(Parser.tokens.actual.tokenvalue))
            elif (Parser.tokens.actual.tokenvalue == 'WHILE'):
                Parser.tokens.selectNext()
                whiletree = While('WHILE', [])
                whiletree.children.append(Parser.relExpression())
                if (Parser.tokens.actual.tokenvalue == '\n'):
                    Parser.tokens.selectNext()
                    whiletree.children.append(Parser.statements())
                    if (Parser.tokens.actual.tokenvalue == 'WEND'):
                        Parser.tokens.selectNext()
                        return whiletree
        elif (Parser.tokens.actual.tokentype == 'IDENT'):
            ident = Parser.tokens.actual
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokentype == 'ASSIG'):
                Parser.tokens.selectNext()
                assigtree = Assignment('ASSIG', [ident.tokenvalue, Parser.parserExpression()])
                return assigtree
            else:
                raise ValueError('Expected assignment token "=", got %s' %(Parser.tokens.actual.tokenvalue))
        else:
            return NoOp()

    @staticmethod
    def statements():
        statements = []
        statements.append(Parser.statement())
        while (Parser.tokens.actual.tokenvalue == '\n'):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.tokenvalue not in ["END", "ELSE", "WEND"]):
                statements.append(Parser.statement())
        return Statements('STATEMENTS', statements)

    @staticmethod
    def relExpression():
        var1 = Parser.parserExpression()
        op = Parser.tokens.actual
        relop = BinOp(op.tokenvalue, [var1])
        Parser.tokens.selectNext()
        var2 = Parser.parserExpression()
        relop.children.append(var2)
        return relop

    def run(code):
        Parser.tokens = Tokenizer(code)
        result = Parser.statements()
        if (Parser.tokens.actual.tokentype == 'EOF'):
            return result
        else:
            raise EOFError('Program ended before EOF')

'''Rotina de Testes'''
file = sys.argv[1]
# file = './test.vbs'
with open(file, 'r', encoding='utf-8') as infile:
    lines = infile.read()

st = SymbolTable()
Parser.run(lines).Evaluate(st)
