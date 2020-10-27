from enum import Enum

ScopeKind = Enum('ScopeKind', [
  'UNDEFINED_',
  'VAR_',
  'PARAM_',
  'FUNCTION_',
  'FIELD_',
  'ARRAY_TYPE_',
  'STRUCT_TYPE_',
  'ALIAS_TYPE_',
  'SCALAR_TYPE_',
  'UNIVERSAL_',
], start=-1)

def isTypeKind(kind):
  return kind in [ScopeKind.ARRAY_TYPE_, ScopeKind.STRUCT_TYPE_, ScopeKind.ALIAS_TYPE_, ScopeKind.SCALAR_TYPE]

# Tipos de objetos
class Var:
  def __init__(self,tipo=None,nIndex=None, nSize=None):
    self.tipo=tipo
    self.nIndex=nIndex
    self.nSize=nSize
class Param:
  def __init__(self,tipo=None,nIndex=None, nSize=None):
    self.tipo=tipo
    self.nIndex=nIndex
    self.nSize=nSize
class Field:
  def __init__(self,tipo=None,nIndex=None, nSize=None):
    self.tipo=tipo
    self.nIndex=nIndex
    self.nSize=nSize
class Function:
  def __init__(self,pRetType=None,pParams=None, nIndex=None, nParams=None,nVars=None):
    self.pRetType=pRetType
    self.pParams=nParams
    self.nIndex=nIndex
    self.nParams=nParams
    self.nVars=nVars       
class Array:
  def __init__(self,tipoElemento=None,nNumElems=None, nSize=None):
    self.tipoElemento=tipoElemento
    self.nNumElems=nNumElems
    self.nSize=nSize
class Struct:
  def __init__(self,campos=None, nSize=None):
    self.campos=campos
    self.nSize=nSize
class Alias:
  def __init__(self,tipoBase=None, nSize=None):
    self.tipoBase=tipoBase
    self.nSize=nSize
class Type:
  def __init__(self,tipoBase=None, nSize=None):
    self.tipoBase=tipoBase
    self.nSize=None

# Estrutura de dados do objeto
class ScopeObject:
  def __init__(self, nName=None, pNext=None,eKind=None, under=None):
    self.nName=nName
    self.pNext=pNext
    self.eKind=eKind
    self._=under


IntObj = ScopeObject(-1, None, ScopeKind.SCALAR_TYPE_, Type(None, 1))
CharObj = ScopeObject(-1, None, ScopeKind.SCALAR_TYPE_, Type(None, 1))
BoolObj = ScopeObject(-1, None, ScopeKind.SCALAR_TYPE_, Type(None, 1))
StringObj = ScopeObject(-1, None, ScopeKind.SCALAR_TYPE_, Type(None, 1))
UniversalObj = ScopeObject(-1, None, ScopeKind.SCALAR_TYPE_, Type(None, 1))
