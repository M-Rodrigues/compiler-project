from enum import Enum

ErrorTypes = Enum('ErrorTypes', [
  'ERR_REDCL',
  'ERR_NO_DECL',
  'ERR_TYPE_EXPECTED',
  'ERR_BOOL_TYPE_EXPECTED'
  'ERR_TYPE_MISMATCH',
  'ERR_INVALID_TYPE',
  'ERR_KIND_NOT_STRUCT',
  'ERR_FIELD_NOT_DECL',
  'ERR_KIND_NOT_ARRAY',
  'ERR_INVALID_INDEX_TYPE',
  'ERR_KIND_NOT_VAR',
  'ERR_KIND_NOT_FUNCTION',
  'ERR_TOO_MANY_ARG',
  'ERR_PARAM_TYPE',
  'ERR_TOO_FEW_ARGS',
  'ERR_RETURN_TYPE_MISMATCH'
], start=0)

def ErrorHandler(code):
  hasErr = True
  # print("Linha: "+str(lxc.linha)+" - ")
  if (code==ErrorTypes.ERR_NO_DECL):
    print("Variável não previamente declarada")
  elif (code==ErrorTypes.ERR_REDCL):
    print("Variável já declarada")
  elif (code==ErrorTypes.ERR_TYPE_EXPECTED):
    print("Tipo não declarado previamente")
  elif (code==ErrorTypes.ERR_BOOL_TYPE_EXPECTED):
    print("Tipo boolean é esperado")
  elif (code==ErrorTypes.ERR_INVALID_TYPE):
    print("Tipo é invalido para a operação realizada")
  elif (code==ErrorTypes.ERR_TYPE_MISMATCH):
    print("Tipo é invalido para a operação realizada")
  elif (code==ErrorTypes.ERR_KIND_NOT_STRUCT):
    print("A operação pode ser realizada somente em tipos Struct")
  elif (code==ErrorTypes.ERR_FIELD_NOT_DECL):
    print("Campo não foi declarado")
  elif (code==ErrorTypes.ERR_KIND_NOT_ARRAY):
    print("A operação é destinada somente para Array")
  elif (code==ErrorTypes.ERR_INVALID_INDEX_TYPE):
    print("O índice é inválido para o Array")
  elif(code==ErrorTypes.ERR_KIND_NOT_VAR):
    print("A operação somente válida para tipo Var")
  elif(code==ErrorTypes.ERR_KIND_NOT_FUNCTION):
    print("A operação somente válida para tipo Function")
  elif (code==ErrorTypes.ERR_TOO_FEW_ARGS):
    print("O número de parâmetros é menor do que o especificado")
  elif (code==ErrorTypes.ERR_TOO_MANY_ARG):
    print("O número de parametros é maior do que o especificado")
  elif (code==ErrorTypes.ERR_PARAM_TYPE):
    print("O tipo especificado não é válido")
  elif (code==ErrorTypes.ERR_RETURN_TYPE_MISMATCH):
    print("O tipo de retorno não é compatível com o tipo especificado na função")