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
    self.labelNo = 0
    self.name = ""
    self.constPool = 0
    
    # with open('output.file', 'w') as arq:
    #   arq.close()
    self.output_file = open('output.file', 'w')
      
  def close_file(self):
    self.output_file.close()
  
  def write_to_output_file(self, line):
    self.output_file.write(line)
  
  def new_label(self):
    self.labelNo += 1
    return self.labelNo

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
      # print(SemTypes.IDD_._.__dict__)
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
      self.f._ = Function(None,None,self.nFuncs,0,0)
      self.nFuncs += 1
      self.scope.new_block()
    
    # Uso de tipos
    elif rule == SemRule.T0.value: # T -> 'integer'
      SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,1,SemTypes.T(IntObj))
      self.push(SemTypes.T_)
    elif rule == SemRule.T1.value: # T -> 'char'
      SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,1,SemTypes.T(CharObj))
      self.push(SemTypes.T_)
    elif rule==SemRule.T2.value: # T -> 'boolean'
      SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,1,SemTypes.T(BoolObj))
      self.push(SemTypes.T_)
    elif rule==SemRule.T3.value: # T -> 'string'
      SemTypes.T_=SemTypes.T_Attrib(Nonterminal.T,1,SemTypes.T(StringObj))
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
        SemTypes.IDD_=self.pop() 
        self.f=SemTypes.IDD_._.objeto
        self.f.eKind=ScopeKind.FUNCTION_
        self.f._=Function(SemTypes.T_._.type,SemTypes.LP_._.list,self.f._.nIndex,SemTypes.LP_.nSize,SemTypes.LP_.nSize) 
        self.curFunction=self.f
        
        self.write_to_output_file("BEGIN_FUNC {} {}\n".format(self.f._.nIndex, self.f._.nParams))    
    
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
    
    # Atribuicao de valores
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
        self.write_to_output_file("\tADD {}".format(p._.nIndex))

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
        
        self.write_to_output_file('\tMUL {}\n'.format(self.n))
        self.write_to_output_file('\tADD\n')
        
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
        
        self.write_to_output_file('\tLOAD_REF {}\n'.format(p._.nIndex))
      self.push(SemTypes.LV_)
    
    # Expressoes elementares
    elif rule==SemRule.F0.value: # F -> LV
      SemTypes.LV_=self.pop()
      self.n=SemTypes.LV_._.type._.nSize 
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(SemTypes.LV_._.type))
      self.push(SemTypes.F_)
      
      self.write_to_output_file('\tDE_REF\n')
    elif rule==SemRule.F1.value: # F -> '++' LV
      SemTypes.LV_=self.pop()
      self.t=SemTypes.LV_._.type
      if not self.scope.check_types(self.t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(IntObj))
      
      self.write_to_output_file('\tDUP\n\tDUP\n\tDE_REF 1\n')
      self.write_to_output_file('\tINC\n\tSTORE_REF 1\n\tDE_REF 1\n')
    elif rule==SemRule.F2.value: # F -> '--' LV
      SemTypes.LV_=self.pop()
      self.t=SemTypes.LV_._.type
      if not self.scope.check_types(self.t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(SemTypes.LV_._.type))
      self.push(SemTypes.F_)
      
      self.write_to_output_file('\tDUP\n\tDUP\n\tDE_REF 1\n')
      self.write_to_output_file('\tDEC\n\tSTORE_REF 1\n\tDE_REF 1\n')
    elif rule==SemRule.F3.value: # F -> LV '++'
      SemTypes.LV_=self.pop()
      self.t=SemTypes.LV_._.type
      if not self.scope.check_types(t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypesF(SemTypes.LV_._.type))
      self.push(SemTypes.F_)
      
      self.write_to_output_file('\tDUP\n\tDUP\n\tDE_REF 1\n')
      self.write_to_output_file('\tINC\n\tSTORE_REF 1\n\tDE_REF 1\n')
      self.write_to_output_file('\tDEC\n')
    elif rule==SemRule.F4.value: # F -> LV '--'
      SemTypes.LV_=self.pop()
      self.t=SemTypes.LV_._.type
      if not self.scope.check_types(t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypesF(self.t))
      self.push(SemTypes.F_)
      
      self.write_to_output_file('\tDUP\n\tDUP\n\tDE_REF 1\n')
      self.write_to_output_file('\tDEC\n\tSTORE_REF 1\n\tDE_REF 1\n')
      self.write_to_output_file('\tINC\n')
    elif rule==SemRule.F5.value: # F -> '(' E ')'
      SemTypes.E_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypesF(SemTypesE_._.type))
      self.push(SemTypes.F_) 
    elif rule==SemRule.F6.value: # F -> IDU MC '(' LE ')'
        SemTypes.LE_=self.pop()
        SemTypes.MC_=self.pop()
        SemTypes.IDU_=self.pop()
        self.f=SemTypes.IDU_._.objeto
        SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(SemTypes.MC_._.type))
        if not SemTypes.LE_._.err:
          if SemTypes.LE_._.n-1 < self.f._nParams and SemTypes.LE_._.n != 0:
            ErrorHandler(ErrorTypes.ERR_TOO_FEW_ARGS)
          elif SemTypes.LE_._.n-1 > self.f._.nParams:
            ErrorHandler(ErrorTypes.ERR_TOO_MANY_ARG)
        self.append(SemTypes.F_)
    elif rule==SemRule.F7.value: # F -> '-' F
      SemTypes.F1_=self.pop()
      self.t=SemTypes.F1_._.type
      if not self.scope.check_types(self.t,IntObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F0_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(t))
      self.push(SemTypes.F0_)

      self.write_to_output_file('\tNEG\n')
    elif rule==SemRule.F8.value: # F -> '!' F
      SemTypes.F1_=self.pop()
      t=SemTypes.F1_._.type
      if not self.scope.check_types(self.t,BoolObj):
        ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.F0_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(self.t))
      self.push(SemTypes.F0_)
      
      self.write_to_output_file('\tNOT\n')
    elif rule==SemRule.F9.value: # F -> TRUE
      SemTypes.TRU_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(BoolObj))
      self.push(SemTypes.F_)
      
      self.write_to_output_file('\tLOAD_TRUE\n')
    elif rule==SemRule.F10.value: # F -> FALSE
      SemTypes.FALS_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(BoolObj))
      self.push(SemTypes.F_)
      
      self.write_to_output_file('\tLOAD_FALSE\n')
    elif rule==SemRule.F11.value: # F -> CHR
      SemTypes.CHR_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(CharObj))
      self.push(SemTypes.F_)
      self.n = self.lexical.secondaryToken
      self.constPool+=1
      
      self.write_to_output_file('\tLOAD_CONST {}\n'.format(self.constPool))
    elif rule==SemRule.F12.value: # F -> STR
      SemTypes.STR_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(StringObj))
      self.push(SemTypes.F_)
      self.n = self.lexical.secondaryToken
      self.constPool+=1
      
      self.write_to_output_file('\tLOAD_CONST {}\n'.format(self.constPool))
    elif rule==SemRule.F13.value: # F -> NUM
      SemTypes.NUM_=self.pop()
      SemTypes.F_=SemTypes.T_Attrib(Nonterminal.F,None,SemTypes.F(IntObj))
      self.push(SemTypes.F_)
      self.n = self.lexical.secondaryToken
      self.constPool+=1
      
      self.write_to_output_file('\tLOAD_CONST {}\n'.format(self.constPool))

    # Expressoes Aritimeticas
    elif rule == SemRule.R0.value:
      SemTypes.Y_=self.pop()
      SemTypes.R1_=self.pop()
      if not self.scope.check_types(SemTypes.R1_._.type,SemTypes.Y_._.type):
          ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      print(SemTypes.R1_._.__dict__)
      print(IntObj)
      if not self.scope.check_types(SemTypes.R1_._.type,IntObj) and (not self.scope.check_types(SemTypes.R1_._.type, StringObj)):
          ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.R0_=SemTypes.T_Attrib(Nonterminal.R,None,SemTypes.R(SemTypes.R1_._.type))
      self.push(SemTypes.R0_)
      
      self.write_to_output_file("\tADD\n")
    elif rule == SemRule.R1.value:
      SemTypes.Y_=self.pop()
      SemTypes.R1_=self.pop()
      if not self.scope.check_types(SemTypes.R1_._.type,SemTypes.Y_._.type):
          ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      if not self.scope.check_types(SemTypes.R1_._.type,IntObj):
          ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.R0_=SemTypes.T_Attrib(Nonterminal.R,None,SemTypes.R(SemTypes.R1_._.type))
      self.push(SemTypes.R0_)
      
      self.write_to_output_file("\tSUB\n")
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
      
      self.write_to_output_file("\tMUL\n")
    elif rule == SemRule.Y1.value:
      SemTypes.F_=self.pop()
      SemTypes.Y1_=self.pop()
      if not self.scope.check_types(SemTypes.Y1_._.type,SemTypes.F_._.type):
          ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      if not self.scope.check_types(SemTypes.Y1_._.type,int_):
          ErrorHandler(ErrorTypes.ERR_INVALID_TYPE)
      SemTypes.Y0_=SemTypes.T_Attrib(Nonterminal.Y,None,SemTypes.Y(SemTypes.Y1_._.type))
      self(SemTypes.Y0_)
      
      self.write_to_output_file("\tDIV\n")
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
      
      self.write_to_output_file("\tAND\n")
    elif rule == SemRule.E1.value:
      SemTypes.L_=self.pop()
      SemTypes.E1_=self.pop()
      if not self.scope.check_types(SemTypes.E1_._.type,BoolObj):
        ErrorHandler(ErrorTypes.ERR_BOOL_TYPE_EXPECTED)
      if not self.scope.check_types(L_._.type,BoolObj):
        ErrorHandler(ErrorTypes.ERR_BOOL_TYPE_EXPECTED)
      SemTypes.E0_=SemTypes.T_Attrib(Nonterminal.E,None,SemTypes.E(BoolObj))
      self.push(SemTypes.E0_)
      
      self.write_to_output_file("\tOR\n")
    elif rule == SemRule.E2.value:
      SemTypes.L_=self.pop()
      SemTypes.E_=SemTypes.T_Attrib(Nonterminal.E,None,SemTypes.E(SemTypes.L_._.type))
      self.push(SemTypes.E_)

    # Expressoes Relacionais
    elif rule == SemRule.L0.value:
      SemTypes.R_=self.pop()
      SemTypes.L1_=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,SemTypes.L(BoolObj))
      self.push(SemTypes.L0_)
      
      self.write_to_output_file("\tLT\n")
    elif rule == SemRule.L1.value:
      SemTypes.R_=self.pop()
      SemTypes.L1_=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
      
      self.write_to_output_file("\tGT\n")
    elif rule == SemRule.L2.value:
      SemTypes.R_=self.pop()
      SemTypes.L1=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
      
      self.write_to_output_file("\tLE\n")
    elif rule == SemRule.L3.value:
      SemTypes.R_=self.pop()
      SemTypes.L1_=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,SemTypes.L(BoolObj))
      self.push(SemTypes.L0_)
      self.write_to_output_file("\tGE\n")
    elif rule == SemRule.L4.value:
      SemTypes.R_=self.pop()
      L1=self.pop()
      if not self.scope.check_types(L1_._.type,SemTypes.R_._.type):
          ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
      self.write_to_output_file("\tEQ\n")
    elif rule == SemRule.L5.value:
      SemTypes.R_=self.pop()
      SemTypes.L1=self.pop()
      if not self.scope.check_types(SemTypes.L1_._.type,SemTypes.R_._.type):
        ErrorHandler(ErrorTypes.ERR_TYPE_MISMATCH)
      SemTypes.L0_=SemTypes.T_Attrib(Nonterminal.L,None,BoolObj)
      self.push(SemTypes.L0_)
      
      self.write_to_output_file("\tNE\n")
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
    
    # Comandos de selecao
    elif rule == SemRule.MT0.value: # MT -> ''
      rLabel=self.new_label()
      SemTypes.MT_=SemTypes.T_Attrib(Nonterminal.MT,None,SemTypes.MT(rLabel))
      self.push(SemTypes.MT_)
      
      self.write_to_output_file("TJMP_FW L{}".format(rLabel))

    elif rule == SemRule.MC0.value: # MC -> ''
      SemTypes.IDU_=self.pop()
      self.f=SemTypes.IDU_._.objeto
      if(self.f.eKind!=ScopeKind.FUNCTION_):
        SemTypes.MC_=SemTypes.T_Attrib(Nonterminal.MC,None,SemTypes.MC(UniversalObj,None,True))
      else:
        SemTypes.MC_=SemTypes.T_Attrib(Nonterminal.MC,None,SemTypes.MC(self.f._.pRetType,self.f._.pParams,False))
      self.push(SemTypes.MC_)
    elif rule == SemRule.LE1.value: # LE -> E
      SemTypes.E_=self.pop()
      SemTypes.MC_=self.pop()
      SemTypes.LE_=SemTypes.T_Attrib(Nonterminal.LE,None,SemTypes.LE(None,None,SemTypes.MC_._.err,1))
      if not SemTypes.MC_._.err:
        p=SemTypes.MC_._.param 
        print(p)
        if p==None:
          ErrorHandler(ErrorTypes.ERR_TOO_MANY_ARG)
          SemTypes.LE_._.err=True
        else:
          # if not self.scope.check_types(p._.tipo,SemTypes.E_._.type):
          #   ErrorHandler(ErrorTypes.ERR_PARAM_TYPE)
          SemTypes.LE_._.param=p.pNext
          SemTypes.LE_._.n=n+1
      self.push(SemTypes.LE_)
    elif rule == SemRule.LE0.value:  # LE -> LE ',' E
      SemTypes.E_=self.pop()
      SemTypes.LE1_=self.pop()
      SemTypes.LE0_=t_attrib(Nonterminal.LE,None,SemTypes.LE(None,None,SemTypes.L1_._.err,SemTypes.LE1_._.n))
      if not SemTypes.LE1_._.err:
        p=SemTypes.LE1_._.param
        if p==None:
          ErrorHandler(ErrorTypes.ERR_TOO_MANY_ARG)
          SemTypes.LE0_._.err=True
        else:
          if not self.scope.check_types(p._.tipo,SemTypes.E_._.type):
            ErrorHandler(ErrorTypes.ERR_PARAM_TYPE)
          SemTypes.LE0._.param=p.pNext
          SemTypes.LE0._.n=n+1
      self.push(SemTypes.LE0_)
    
    else:
      pass
      print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tSem regra semantica para {} {} :('.format(rule, SemRule(rule).name))

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