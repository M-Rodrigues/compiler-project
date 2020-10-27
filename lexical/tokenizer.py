from .token import Token, keyWords

class Tokenizer:
  def __init__(self, s):
    # posicao do proximo char a ser lido da string de codigo
    self.charIdCodeString = None

    # string do codigo a ser avaliada
    self.codeString = None

    # proximo caracter a ser lido do string de codigo
    self.nextChar = None

    # tabela de nomes dos ID - tokensecundario
    self.idNames = {}

    # tabela com valor das constantes
    self.vConst = {}

    # Token Secundario do token atual
    self.secondaryToken = None

    self.setCodeString(s)
  
  def getIdName(self, ts):
    for key in self.idNames:
      if self.idNames[key] == ts:
        return key
    return None

  def setCodeString(self, s):
    self.codeString = s
    self.charIdCodeString = 0
    self.nextChar = ' '
    self.idNames = {}
    self.vConst = {}

  def searchKeyWord(self, name):
    if name in keyWords: 
      return keyWords[name]
    return None

  def readChar(self):
    # EOF
    if self.charIdCodeString == len(self.codeString):
      return None

    self.nextChar = c = self.codeString[self.charIdCodeString]
    self.charIdCodeString += 1
    return c

  def getTokenSecundario(self, text):
    if text not in self.idNames:
      self.idNames[text] = len(self.idNames)
    self.secondaryToken = self.idNames[text]
    
    print(self.vConst)
    return self.secondaryToken
  
  def addIntConst(self, text):
    tokenSecundario = self.getTokenSecundario(text)
    self.vConst[tokenSecundario] = int(text)
    return tokenSecundario
  
  def getIntConst(self, text):
    return self.getConst(text)
  
  def getStrConst(self, text):
    return self.getConst(text)
  
  def getChrConst(self, text):
    return self.getConst(text)
  
  def getConst(self, text):
    return self.vConst[text]
  
  def addFloatConst(self, text):
    tokenSecundario = self.getTokenSecundario(text)
    self.vConst[tokenSecundario] = float(text)
    return tokenSecundario

  def addStringConst(self, text):
    tokenSecundario = self.getTokenSecundario(text)
    self.vConst[tokenSecundario] = str(text)
    return tokenSecundario
  
  def doubleCharKeyword(self, c, cc):
    self.readChar()
    if self.nextChar == cc[1]:
      self.readChar()
      return self.searchKeyWord(cc), self.getTokenSecundario(cc), cc
    return self.searchKeyWord(c), self.getTokenSecundario(c), c

  def nextToken(self):
    while self.nextChar.isspace():
      self.readChar()

    # palavras reservadas e IDs
    if self.nextChar.isalpha():

      text = ""
      while self.nextChar.isalnum() or self.nextChar == '_':
        text += self.nextChar
        self.readChar()
      
      if text in keyWords:
        return self.searchKeyWord(text), self.getTokenSecundario(text), text
      else:        
        return Token.ID, self.getTokenSecundario(text), text
    
    # constantes numerais
    elif self.nextChar.isdigit():

      # parte inteira
      text = ""
      while self.nextChar.isdigit():
        text += self.nextChar
        self.readChar()

      if self.nextChar != '.':
        # return Token.INT_NUMERAL, self.addIntConst(text), text
        return Token.NUMERAL, self.addIntConst(text), text
      
      text += self.nextChar
      self.readChar()

      # parte decimal
      while self.nextChar.isdigit():
        text += self.nextChar
        self.readChar()
      
      if not self.nextChar.isdigit():
        # return Token.FLOAT_NUMERAL, self.addFloatConst(text), text
        return Token.NUMERAL, self.addFloatConst(text), text

    # constantes strings
    elif self.nextChar == '"':

      text = '"'
      self.readChar()
      while self.nextChar != '"':
        text += self.nextChar
        self.readChar()
      text += '"'
      self.readChar()

      return Token.STRINGVAL, self.addStringConst(text), text
    
    # demais lexemas
    else:
      # unico caracter
      if self.nextChar == "'":
        self.readChar()
        c = self.nextChar
        self.readChar()
        self.readChar()
        return Token.CHARACTER, self.addStringConst(c), c

      # characteres reservados
      elif self.nextChar in ':;,[](){}*/.':
        c = self.nextChar
        self.readChar()
        return self.searchKeyWord(c), self.getTokenSecundario(c), c

      # = e ==
      elif self.nextChar == '=':
        return self.doubleCharKeyword('=', '==')

      # < e <=
      elif self.nextChar == '<':
        return self.doubleCharKeyword('<', '<=')

      # > e >=
      elif self.nextChar == '>':
        return self.doubleCharKeyword('>', '>=')
      
      # ! e !=
      elif self.nextChar == '!':
        return self.doubleCharKeyword('!', '!=')
      
      # + e ++
      elif self.nextChar == '+':
        return self.doubleCharKeyword('+', '++')

      # - e --
      elif self.nextChar == '-':
        return self.doubleCharKeyword('-', '--')

      # EOF
      elif self.nextChar == '\x03':
        return Token.EOF, self.getTokenSecundario(self.nextChar), 'EOF'
      
      # UNKNOW
      else:
        c = self.nextChar
        self.readChar()
        return Token.UNKNOWN, self.getTokenSecundario(self.nextChar), c

  def getTokens(self, s):
    self.setCodeString(s)
    
    token, tokenSecundario, identificador = self.nextToken()
    while token is not Token.EOF:
      print(token, tokenSecundario, identificador)
      token, tokenSecundario, identificador = self.nextToken()