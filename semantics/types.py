class ID:
	def __init__(self, objeto=None,name=None):
		self.objeto=objeto
		self.name=name
class T:
	def __init__(self, type=None):
		self.type=type
class E:
	def __init__(self, type=None):
		self.type=type
class L:
	def __init__(self, type=None):
		self.type=type
class R:
	def __init__(self, type=None):
		self.type=type
class Y:
	def __init__(self, type=None):
		self.type=type
class F:
	def __init__(self, type=None):
		self.type=type
class LV:
	def __init__(self, type=None):
		self.type=type
class MC:
	def __init__(self,type=None,param=None,err=None):
		self.type=type
		self.param=param
		self.err=err
class MT:
	def __init__(self,label=None):
		self.label=label   
class ME:
	def __init__(self,label=None):
		self.label=label	
class MW:
	def __init__(self,label=None):
		self.label=label  
class MA:
	def __init__(self,label=None):
		self.label=label  
class LE:
	def __init__(self, type=None,param=None,err=None,n=None):
		self.type=type
		self.param=param
		self.err=err
		self.n=n
class LI:
	def __init__(self, list=None):
		self.list=list
class DC:
	def __init__(self, list=None):
		self.list=list
class LP:
	def __init__(self, list=None):
		self.list=list
class TRU:
	def __init__(self, type=None,val=None):
		self.type=type
		self.val=val
class FALS:
	def __init__(self, type=None,val=None):
		self.type=type
		self.val=val
class CHR:
	def __init__(self, type=None,pos=None,val=None):
		self.type=type
		self.pos=pos
		self.val=val    
class STR:
	def __init__(self, type=None,val=None,pos=None):
		self.type=type
		self.val=val
		self.pos=pos
class NUM:
	def __init__(self, type=None,val=None,pos=None):
		self.type=type
		self.val=val
		self.pos=pos

# Estrutura de dados de atributos
class T_Attrib:
	def __init__(self, t_nont=None, nSize=None,under=None):
		self.t_nont=t_nont
		self.nSize=nSize
		self._=under
  
	def __str__(self):
		return '{}'.format(self.t_nont)


# Objetos da gramatica de atributos
IDD_=T_Attrib()
IDU_=T_Attrib()
ID_=T_Attrib()
T_=T_Attrib()
LI_=T_Attrib()
LI0_=T_Attrib()
LI1_=T_Attrib()
TRU_=T_Attrib()
FALS_=T_Attrib()
STR_=T_Attrib()
CHR_=T_Attrib()
NUM_=T_Attrib()
DC_=T_Attrib()
DC0_=T_Attrib()
DC1_=T_Attrib()
LP_=T_Attrib()
LP0_=T_Attrib()
LP1_=T_Attrib()
E_=T_Attrib()
E0_=T_Attrib()
E1_=T_Attrib()
L_=T_Attrib()
L0_=T_Attrib()
L1_=T_Attrib()
R_=T_Attrib()
R0_=T_Attrib()
R1_=T_Attrib()
Y_=T_Attrib()
Y0_=T_Attrib()
Y1_=T_Attrib()
F_=T_Attrib()
F0_=T_Attrib()
F1_=T_Attrib()
LV_=T_Attrib()
LV0_=T_Attrib()
LV1_=T_Attrib()
MC_=T_Attrib()
LE_=T_Attrib()
LE0_=T_Attrib()
LE1_=T_Attrib()
MT_=T_Attrib()
ME_=T_Attrib()
MW_=T_Attrib()