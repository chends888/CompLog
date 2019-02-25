#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Token:
    def __init__(self, tokentype, tokenvalue):
        self.tokentype = tokentype
        self.tokenvalue = tokenvalue

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = self.selectNext()

    def selectNext(self):
        if (self.position == (len(self.origin))):
          self.actual = Token(None, None)
          return Token(None, None)

        token = ''
        tokentype = ''
        while self.position <= len(self.origin):
            if (self.position == (len(self.origin))):
              self.actual = Token(tokentype, int(token))
              return

            if (self.origin[self.position].isdigit()):
                if (tokentype == 'op'):
                    self.actual = Token(tokentype, token)
                    return
                token += self.origin[self.position]
                tokentype = 'int'

            elif (self.origin[self.position] == ' '):
              self.position += 1
              continue

            else:
                if (tokentype == 'int'):
                    self.actual = Token(tokentype, int(token))
                    return Token(tokentype, int(token))
                token += self.origin[self.position]
                tokentype = 'op'
            self.position += 1

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    @staticmethod
    def parserExpression(self):
        try:
            num1 = self.tokens.actual
            num2 = False
        except:
            raise ValueError('Token não encontrado')

        if (num1.tokentype != 'int'):
            raise SyntaxError('Inicio de operação inválido, primeiro elemento não é int', num1.tokentype)

        self.tokens.selectNext()
        while self.tokens.actual.tokentype:
            if (self.tokens.actual.tokentype == 'op'):
                op = self.tokens.actual.tokenvalue

            if (self.tokens.actual.tokentype == 'int'):
                num2 = self.tokens.actual

            if op == '+' and num2:
                num1.tokenvalue += num2.tokenvalue
                num2 = False

            elif op == '-' and num2:
                num1.tokenvalue -= num2.tokenvalue
                num2 = False
            self.tokens.selectNext()
        
        print('Resultado:', num1.tokenvalue)

    def run(self):
        return self.parserExpression(self)

# test = '100    +11  -  1'
# newTokenizer = Tokenizer(test)
# newParser = Parser(newTokenizer)
# newParser.run()