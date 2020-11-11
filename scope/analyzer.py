from .types import ScopeKind, ScopeObject, UniversalObj

# Analizador de escopo

class ScopeAnalyzer:
  def __init__(self):
    self.symbol_table = [None] * 64
    self.level = 0

  def new_block(self):
    self.level += 1
    self.symbol_table[self.level] = None
    return self.level
  
  def end_block(self):
    self.level -= 1
    return self.level
  
  def define(self, name):
    obj = ScopeObject(name, self.symbol_table[self.level], ScopeKind.UNDEFINED_)
    self.symbol_table[self.level] = obj
    return obj

  def search(self, name):
    obj = self.symbol_table[self.level]
    while obj != None:
      if obj.nName == name:
        return obj
      obj = obj.pNext
    return obj

  def find(self, name):
    obj = None
    i = self.level
    while i >= 0:
      obj = self.symbol_table[i]
      while obj != None:
        if obj.nName == name:
          return obj
        obj = obj.pNext
      i -= 1
    return obj

  def check_types(self, t1, t2):
    if (t1==t2):
      return True
    elif (t1==UniversalObj or t2==UniversalObj):
      return True
    elif (t1.eKind==ScopeKind.UNIVERSAL_ or t2.eKind==ScopeKind.UNIVERSAL_):
      return True
    elif (t1.eKind==ScopeKind.ALIAS_TYPE_ and t2.eKind!=ScopeKind.ALIAS_TYPE_):
      return self.check_types(t1._.tipoBase,t2)
    elif(t1.eKind!=ScopeKind.ALIAS_TYPE_ and t2.eKind==ScopeKind.ALIAS_TYPE_):
      return self.check_types(t1,t2._.tipoBase)
    elif (t1.eKind==t2.eKind):
      if (t1.eKind==ScopeKind.ALIAS_TYPE_):
        return self.check_types(t1._.tipoBase,t2._.tipoBase)
      elif (t1.eKind==ScopeKind.ARRAY_TYPE_):
        if(t1._.nNumElems==t2._.nNumElems):
          return self.check_types(t1._.tipoElemento,t2._.tipoElemento)
      elif (t1.eKind==ScopeKind.STRUCT_TYPE_):
        f1 = t1._.campos
        f2 = t2._.campos
        while (f1 != None and f2 != None):
          if (not self.check_types(f1._.tipo,f2._.tipo)):
            return False
        return (f1==None and f2==None)
      return True
    else:
      return False



# def check_types(t1, t2):
#   if t1 == t2: # ponteiro, mesmo objeto
#     return True

#   # Prevencao de erros
#   elif t1 == UniversalObj or t2 == UniversalObj:
#     return True
#   elif t1.eKind == UNIVERSAL_ or t2.eKind == UNIVERSAL_:
#     return True
  
#   # Aliases
#   elif t1.eKind == ALIAS_TYPE_ and t2.eKind != ALIAS_TYPE_:
#     return check_types(t1._.tipoBase,t2)
#   elif t1.eKind != ALIAS_TYPE_ and t2.eKind == ALIAS_TYPE_:
#     return check_types(t1,t2._.tipoBase)
#   elif t1.eKind == ALIAS_TYPE_ and t2.eKind == ALIAS_TYPE_:
#     return check_types(t1._.tipoBase,t2._.tipoBase)
  
#   # Array
#   elif t1.eKind == ARRAY_TYPE_ and t2.eKind == ARRAY_TYPE_:
#     if t1._.nNumElems == t2._.nNumElems:
#       return check_types(t1._.tipoElemento,t2._.tipoElemento)
  
#   # Struct
#   elif t1.eKind == STRUCT_TYPE_ and t2.eKind == STRUCT_TYPE_:
#     f1 = t1._.campos # lista de campos
#     f2 = t2._.campos # lista de campos
    
#     # Verififcar todos os campos
#     while f1 != None and f2 != None:
#       if not check_types(f1._.tipo,f2._.tipo):
#         return False
      
#       # Proximos campos
#       f1 = f1 + 1 # ponteiro
#       f2 = f2 + 1 # ponteiro
      
#     return f1 == None and f2 == None
  
  # else:
  #   return False