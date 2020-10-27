from errorModule import ErrorHandler, ErrorTypes

from semantics import types as SemTypes
from semantics.rule import SemRule

from scope.analyzer import ScopeAnalyzer
from scope.types import ScopeKind, ScopeObject, IntObj, CharObj, BoolObj, StringObj, UniversalObj, isTypeKind
from scope.types import Function, Param, Var, Struct, Field, Array, Alias, Type

from nonterminals.tokens import Nonterminal

class SemanticAnalyzer():
  def __init__(self, lexical):
    self.lexical = lexical
    self.stack = []
    self.scope = ScopeAnalyzer()

    self.nFuncs = 0
    self.t = ScopeObject()
    self.f = ScopeObject()
    self.curFunction = ScopeObject()
    self.n = ""
    self.rLabel = ""
    self.name = ""
    self.constPool = 0

  def check(self, rule):
    # print('Verificando regra semantica', rule, SemRule(rule).name, 'tokenSecundario', self.lexical.secondaryToken, '~{}~'.format(self.lexical.getIdName(self.lexical.secondaryToken)))
    print("ST: {}\tRule: {} {}\t{}".format(self.lexical.secondaryToken, SemRule(rule).name, rule, self.stringify_stack()))

    # Identificadores
    if rule == SemRule.IDD0.value: # IDD -> Id
      name = self.lexical.secondaryToken
      p = self.scope.search(name)
      if p is not None:
        ErrorHandler(ErrorTypes.ERR_REDCL)
      p = self.scope.define(name)
      p.eKind = ScopeKind.UNDEFINED_
      SemTypes.IDD_.t_nont=Nonterminal.ID
      SemTypes.IDD_._=SemTypes.ID(p,name)
      self.push(SemTypes.IDD_)
    elif rule == SemRule.IDU0.value: # IDU -> Id
        name = self.lexical.secondaryToken
        p=self.scope.find(name)
        if (p==None):
            ErrorHandler(ErrorTypes.ERR_NO_DECL)
            p=self.scope.define(name)
        SemTypes.IDU_.t_nont=Nonterminal.IDU
        SemTypes.IDU_._=SemTypes.ID(p,name)
        self.push(SemTypes.IDU_)

    elif rule == SemRule.NF0.value: # NF -> ''
      IDD_ = self.top()
      self.f = SemTypes.IDD_._.objeto
      self.f.eKind = ScopeKind.FUNCTION_
      self.f._ = Function(None,None,self.nFuncs,0,0) #E SE F JÁ TIVER VALORES NOS 3 PRIMEIROS CAMPOS?
      self.nFuncs += 1
      self.scope.new_block()
    
    # Uso de tipos
    elif rule == SemRule.T0.value: # T -> 'integer'
      SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,1,SemTypes.T(IntObj))
      self.push(SemTypes.T_)
    elif rule == SemRule.T1.value:
      SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,1,SemTypes.T(CharObj)) # T -> 'char'
      self.push(SemTypes.T_)
    elif rule==SemRule.T2.value:
      SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,1,SemTypes.T(BoolObj)) # T -> 'boolean'
      self.push(SemTypes.T_)
    elif rule==SemRule.T3.value: # T -> 'string'
      SemTypes.T_=SemTypes.T_Attrib(T,1,SemTypes.T(StringObj))
      self.push(SemTypes.T_)
    elif rule == SemRule.T4.value: # T -> IDU
      SemTypes.IDU_=self.pop()
      p=SemTypes.IDU_._.objeto
      if isTypeKind(p.eKind) or p.eKind==ScopeKind.UNIVERSAL_:
        SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,p._.nSize,SemTypes.T(p))
      else:
        SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,0,SemTypes.T(UniversalObj))
        Error(ERR_TYPE_EXPECTED)
      self.push(SemTypes.T_)
    
    # Uso de parametros
    elif rule==SemRule.LP1.value: # LP -> LP ',' IDD ':' T
        SemTypes.T_=self.pop()
        SemTypes.IDD_=self.pop()
        p=SemTypes.IDD_._.objeto
        p.eKind=ScopeKind.PARAM_
        p._=Param(self.t,0,SemTypes.T_.nSize)
        SemTypes.LP_=SemTypes.T_Attrib(Nonterminal.LP,SemTypes.T_.nSize,SemTypes.LP(p))
        self.push(SemTypes.LP_)
    elif rule==SemRule.LP0.value: # LP -> IDD ':' T
        SemTypes.T_=self.pop()
        SemTypes.IDD_=self.pop()
        SemTypes.LP1_=self.pop()
        p=SemTypes.IDD_._.objeto
        self.t=SemTypes.T_._.type
        self.n=SemTypes.LP1_.nSize
        p.eKind=PARAM_
        p._=Param(t,n,SemTypes.T_.nSize)
        SemTypes.LP0_=SemTypes.T_Attrib(Nonterminal.LP,n+SemTypes.T_.nSize,SemTypes.LP(SemTypes.LP1_._.list))

    # Funcoes
    elif rule==SemRule.MF0.value: # MF -> ''
        SemTypes.T_=self.pop()
        SemTypes.LP_=self.pop()
        SemTypes.IDD_=self.pop() #TA DANDO VAZIO, É NORMAL?
        self.f=SemTypes.IDD_._.objeto
        self.f.eKind=ScopeKind.FUNCTION_
        self.f._=Function(SemTypes.T_._.type,SemTypes.LP_._.list,self.f._.nIndex,SemTypes.LP_.nSize,SemTypes.LP_.nSize) #E se F n for function
        self.curFunction=self.f
    
    # Variaveis
    elif rule==SemRule.LI1.value: # LI -> IDD
      SemTypes.IDD_=self.pop()
      SemTypes.LI_=SemTypes.T_Attrib(Nonterminal.LI,None,SemTypes.LI(SemTypes.IDD_._.objeto))
      self.push(SemTypes.LI_)
    elif rule==SemRule.LI0.value: # LI -> LI ',' IDD
      SemTypes.IDD_=self.pop()
      SemTypes.LI1_=self.pop()
      SemTypes.LI0_=SemTypes.T_Attrib(Nonterminal.LI,None,SemTypes.LI(SemTypes.LI1_._.list))
      self.push(SemTypes.LI0_)
    elif rule == SemRule.DV0.value: # DV -> 'var' LI ':' T ';'
      SemTypes.T_=self.pop()
      self.t=SemTypes.T_._.type
      SemTypes.LI_=self.pop()
      p=SemTypes.LI_._.list
      self.n=self.curFunction._.nVars
      while p!=None and p.eKind==ScopeKind.UNDEFINED_:
        p.eKind=ScopeKind.VAR_
        p._=Var(self.t,self.n,SemTypes.T_.nSize)
        self.n+=SemTypes.T_.nSize
        p=p.pNext
      self.curFunction._.nVars=self.n

    # Declaracao de Variaveis
    elif rule == SemRule.LDV0.value: pass # LDV -> LDV DV
    elif rule == SemRule.LDV1.value: pass # LDV -> DV
    
    # Atribuicao de valroes
    elif rule == SemRule.LV0.value: # LV -> LV '.' IDU
      SemTypes.ID_=StackSem.pop()
      SemTypes.LV1_=StackSem.pop()
      self.t=SemTypes.LV1_._.type
      if self.t.eKind!=ScopeKind.STRUCT_TYPE_:
        if self.t.eKind!=ScopeKind.UNIVERSAL_:
          ErrorHandler(ErrorTypes.ERR_KIND_NOT_STRUCT)
        SemTypes.LV0_=SemTypes.T_Attrib(Nonterminal.LV,None,SemTypes.LV(UniversalObj))
      else:
        p=self.t._.campos
        while p!=None :
          if p.aName==SemTypes.ID_._.name:
            break
          p=p.pNext
        if p==None:
          ErrorHandler(ErrorTypes.ERR_FIELD_NOT_DECL)
          SemTypes.LV0_=SemTypes.T_Attrib(Nonterminal.LV,None,SemTypes.LV(UniversalObj))
        else:
          SemTypes.LV0_=SemTypes.T_Attrib(Nonterminal.LV,None,SemTypes.LV(p._.tipo))
          SemTypes.LV0._.type._=Type(None,p._.nSize)
      self.push(SemTypes.LV0_)
    elif rule == SemRule.LV1.value: # LV -> LV '[' E ']'
      SemTypes.E_=self.pop()
      SemTypes.LV1=self.pop()
      self.t=SemTypes.LV1_._.type
      if self.scope.check_types(self.t,StringObj):
        SemTypes.LV0_=SemTypes.T_Attrib(Nonterminal.LV,None,SemTypes.LV(CharObj))
      elif t.eKind!=ScopeKind.ARRAY_TYPE_:
        if t.eKind!=ScopeKind.UNIVERSAL_:
          ErrorHandler(ErrorTypes.ERR_KIND_NOT_ARRAY)
        SemTypes.LV0_=SemTypes.T_Attrib(Nonterminal.LV,None,SemTypes.LV(UniversalObj))
      else:
        SemTypes.LV0_=SemTypes.T_Attrib(Nonterminal.LV,None,SemTypes.LV(t._.tipoElemento))
        self.n=self.t._tipoElemento._.nSize
      if not self.scope.check_types(SemTypes.E_._.type,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_INDEX_TYPE)
      self.push(SemTypes.LV0_)
    elif rule == SemRule.LV2.value: # LV -> IDU
      SemTypes.IDU_=self.pop()
      p=SemTypes.IDU_._.objeto
      if p.eKind!=ScopeKind.VAR_ and p.eKind!=ScopeKind.PARAM_:
        if p.eKind != ScopeKind.UNIVERSAL_:
          pass
          # ErrorHandler(ErrorTypes.ERR_KIND_NOT_VAR)
        SemTypes.LV_=SemTypes.T_Attrib(Nonterminal.LV,None,SemTypes.LV(UniversalObj))
      else:
        SemTypes.LV_=SemTypes.T_Attrib(Nonterminal.LV,None,SemTypes.LV(p._.tipo))
        SemTypes.LV_._.type._=Type(None,p._.nSize)
      self.push(SemTypes.LV_)
    
    # Expressoes elementares
    elif rule==SemRule.F0.value: # F -> LV
      SemTypes.LV_=self.pop()
      self.n=SemTypes.LV_._.type._.nSize 
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(SemTypes.LV_._.type))
      self.push(SemTypes.F_)
    elif rule==SemRule.F1.value: # F -> '++' LV
      SemTypes.LV_=self.pop()
      self.t=SemTypes.LV_._.type
      if not self.scope.check_types(self.t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(IntObj))
    elif rule==SemRule.F2.value: # F -> '--' LV
      SemTypes.LV_=self.pop()
      self.t=SemTypes.LV_._.type
      if not self.scope.check_types(self.t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(SemTypes.LV_._.type))
      self.push(SemTypes.F_)
    elif rule==SemRule.F3.value: # F -> LV '++'
      SemTypes.LV_=self.pop()
      self.t=SemTypes.LV_._.type
      if not self.scope.check_types(t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypesF(SemTypes.LV_._.type))
      self.push(SemTypes.F_)
    elif rule==SemRule.F4.value: # F -> LV '--'
      SemTypes.LV_=self.pop()
      self.t=SemTypes.LV_._.type
      if not self.scope.check_types(t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypesF(self.t))
      self.push(SemTypes.F_)
    elif rule==SemRule.F5.value: # F -> '(' E ')'
      SemTypes.E_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypesF(SemTypesE_._.type))
      self.push(SemTypes.F_)
    elif rule==SemRule.F7.value: # F -> '-' F
      SemTypes.F1_=self.pop()
      self.t=SemTypes.F1_._.type
      if not self.scope.check_types(self.t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F0_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(t))
      self.push(SemTypes.F0_)
    elif rule==SemRule.F8.value: # F -> '!' F
      SemTypes.F1_=self.pop()
      t=SemTypes.F1_._.type
      if not self.scope.check_types(self.t,BoolObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F0_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(self.t))
      self.push(SemTypes.F0_)
    elif rule==SemRule.F9.value: # F -> TRUE
      SemTypes.TRU_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(BoolObj))
      self.push(SemTypes.F_)
    elif rule==SemRule.F10.value: # F -> FALSE
      SemTypes.FALS_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(BoolObj))
      self.push(SemTypes.F_)
    elif rule==SemRule.F11.value: # F -> CHR
      SemTypes.CHR_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(CharObj))
      self.push(SemTypes.F_)
      self.n = self.lexical.secondaryToken
      self.constPool+=1
    elif rule==SemRule.F12.value: # F -> STR
      SemTypes.STR_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(StringObj))
      self.push(SemTypes.F_)
      self.n = self.lexical.secondaryToken
      self.constPool+=1
    elif rule==SemRule.F13.value: # F -> NUM
      SemTypes.NUM_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(IntObj))
      self.push(SemTypes.F_)
      self.n = self.lexical.secondaryToken
      self.constPool+=1

    # Expressoes Aritimeticas
    elif rule == SemRule.R0.value:
      SemTypes.Y_=self.pop()
      SemTypes.R1_=self.pop()
      if not self.scope.check_types(SemTypes.R1_._.type,SemTypes.Y_._.type):
          ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      if not self.scope.check_types(SemTypes.R1_._.type,int_) and (not self.scope.check_types(SemTypes.R1_._.type,string_)):
          ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.R0_=SemTypes.T_Attrib(Nonterminal.R,None,SemTypes.R(SemTypes.R1_._.type))
      self.push(SemTypes.R0_)
    elif rule == SemRule.R1.value:
      SemTypes.Y_=self.pop()
      SemTypes.R1_=self.pop()
      if not self.scope.check_types(SemTypes.R1_._.type,SemTypes.Y_._.type):
          ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      if not self.scope.check_types(SemTypes.R1_._.type,int_):
          ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.R0_=SemTypes.T_Attrib(Nonterminal.R,None,SemTypes.R(SemTypes.R1_._.type))
      self.push(SemTypes.R0_)
    elif rule == SemRule.R2.value:
      SemTypes.Y_=self.pop()
      SemTypes.R_=SemTypes.T_Attrib(Nonterminal.R,None,SemTypes.R(SemTypes.Y_._.type))
      self.push(SemTypes.R_)
    elif rule == SemRule.Y0.value:
      SemTypes.F_=self.pop()
      SemTypes.Y1_=self.pop()
      if not self.scope.check_types(SemTypes.Y1_._.type,SemTypes.F_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      if not self.scope.check_types(SemTypes.Y1_._.type,int_):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.Y0_=SemTypes.T_Attrib(Nonterminal.Y,None,SemTypes.Y(SemTypes.Y1_._.type))
      self(SemTypes.Y0_)
    elif rule == SemRule.Y1.value:
      SemTypes.F_=self.pop()
      SemTypes.Y1_=self.pop()
      if not self.scope.check_types(SemTypes.Y1_._.type,SemTypes.F_._.type):
          ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      if not self.scope.check_types(SemTypes.Y1_._.type,int_):
          ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.Y0_=SemTypes.T_Attrib(Nonterminal.Y,None,SemTypes.Y(SemTypes.Y1_._.type))
      self(SemTypes.Y0_)
    elif rule == SemRule.Y2.value:
      SemTypes.F_=self.pop()
      SemTypes.Y_=SemTypes.T_Attrib(Nonterminal.Y,None,SemTypes.Y(SemTypes.F_._.type))
      self.push(SemTypes.Y_)

    # Expressoes Logicas
    elif rule == SemRule.E0.value:
      SemTypes.L_=self.pop()
      SemTypes.E1_=self.pop()
      if not self.scope.check_types(SemTypes.E1_._.type,BoolObj):
        ErrorHandler(ErrorTypes.ERR_BOOL_TYPE_EXPECTED)
      if not self.scope.check_types(SemTypes.L_._.type,BoolObj):
        ErrorHandler(ErrorTypes.ERR_BOOL_TYPE_EXPECTED)
      SemTypes.E0_=SemTypes.T_Attrib(Nonterminal.E,None,SemTypes.SemTypes.E(BoolObj))
      self.push(SemTypes.E0_)
    elif rule == SemRule.E1.value:
      SemTypes.L_=self.pop()
      SemTypes.E1_=self.pop()
      if not self.scope.check_types(SemTypes.E1_._.type,BoolObj):
        ErrorHandler(ErrorTypes.ERR_BOOL_TYPE_EXPECTED)
      if not self.scope.check_types(L_._.type,BoolObj):
        ErrorHandler(ErrorTypes.ERR_BOOL_TYPE_EXPECTED)
      SemTypes.E0_=SemTypes.T_Attrib(Nonterminal.E,None,SemTypes.E(BoolObj))
      self.push(SemTypes.E0_)
    elif rule == SemRule.E2.value:
      SemTypes.L_=self.pop()
      SemTypes.E_=SemTypes.T_Attrib(Nonterminal.E,None,SemTypes.E(SemTypes.L_._.type))

    # Expressoes Relacionais
    elif rule == SemRule.L0.value:
      SemTypes.R_=self.pop()
      SemTypes.L1_=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,SemTypes.L(BoolObj))
      self.push(SemTypes.L0_)
    elif rule == SemRule.L1.value:
      SemTypes.R_=self.pop()
      SemTypes.L1_=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
    elif rule == SemRule.L2.value:
      SemTypes.R_=self.pop()
      SemTypes.L1=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
    elif rule == SemRule.L3.value:
      SemTypes.R_=self.pop()
      SemTypes.L1=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
    elif rule == SemRule.L4.value:
      SemTypes.R_=self.pop()
      L1=self.pop()
      if not self.scope.check_types(L1_._.type,SemTypes.R_._.type):
          ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
    elif rule == SemRule.L5.value:
      SemTypes.R_=self.pop()
      SemTypes.L1=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
    elif rule == SemRule.L6.value:
      SemTypes.R_=self.pop()
      SemTypes.L_=SemTypes.T_Attrib(Nonterminal.L,None,SemTypes.L(SemTypes.R_._.type))
      self.push(SemTypes.L_)

    # Atributos para os Literais
    elif rule == SemRule.TRUE0.value:
        SemTypes.TRU_=t_attrib(Nonterminal.TRU,None,SemTypes.TRU(BoolObj,True)) #tem problema ter o None?
        self.push(SemTypes.TRU_)
    elif rule == SemRule.FALSE0.value:
        SemTypes.FALS_=SemTypes.T_Attrib(Nonterminal.FALS,None,SemTypes.FALS(BoolObj,False))
        self.push(SemTypes.FALS_)
    elif rule == SemRule.CHR0.value:
        SemTypes.CHR_=SemTypes.T_Attrib(Nonterminal.CHR,None,SemTypes.CHR(CharObj,self.lexical.secondaryToken,self.lexical.getChrConst(self.lexical.secondaryToken)))
        self.push(SemTypes.CHR_)
    elif rule == SemRule.STR0.value:
        SemTypes.STR_=SemTypes.T_Attrib(Nonterminal.STR,None,SemTypes.STR(StringObj,self.lexical.getStrConst(self.lexical.secondaryToken),self.lexical.secondaryToken))
        self.push(SemTypes.STR_)
    elif rule == SemRule.NUM0.value:
      # Verificar erro do token secundario
      SemTypes.NUM_=SemTypes.T_Attrib(Nonterminal.NUM,None,SemTypes.NUM(IntObj,2,self.lexical.secondaryToken))
      # SemTypes.NUM_=SemTypes.T_Attrib(Nonterminal.NUM,None,SemTypes.NUM(IntObj,self.lexical.secondaryToken,self.lexical.secondaryToken))
      self.push(SemTypes.NUM_)
    
    
    else:
      pass
      # print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tSem regra semantica para {} {} :('.format(rule, SemRule(rule).name))

  def push(self, attribute):
    self.stack.append(attribute)

  def pop(self):
    return self.stack.pop()

  def top(self):
    if (len(self.stack) == 0):
      return None # Atributo vazio
    return self.stack[-1]

  def stringify_stack(self):
    s = ''
    for v in self.stack:
      s += '{}, '.format(Nonterminal(v.t_nont).name)
    return 'SemStack: [{}]'.format(s)