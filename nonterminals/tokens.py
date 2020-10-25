from lexical.token import Token
from enum import Enum

Nonterminal = Enum('Nonterminal', [
  'PLINE',
  'P',
  'LDE',
  'DE',
  'T',
  'DT',
  'DC',
  'DF',
  'LP',
  'B',
  'LDV',
  'LS',
  'DV',
  'LI',
  'S',
  'U',
  'M',
  'E',
  'L',
  'R',
  'Y',
  'F',
  'LE',
  'LV',
  'IDD',
  'IDU',
  'ID',
  'TRUE',
  'FALSE',
  'CHR',
  'STR',
  'NUM',
  'NB',
  'MF',
  'MC',
  'NF',
  'MT',
  'ME',
  'MW'
], start=Token.EOF.value + 1)

rule_left_token = [
  Nonterminal.P.value, Nonterminal.LDE.value, Nonterminal.LDE.value, Nonterminal.DE.value, Nonterminal.DE.value, Nonterminal.T.value, Nonterminal.T.value, Nonterminal.T.value, Nonterminal.T.value, Nonterminal.T.value, Nonterminal.DT.value, Nonterminal.DT.value, Nonterminal.DT.value, Nonterminal.DC.value, Nonterminal.DC.value, Nonterminal.DF.value, Nonterminal.LP.value, Nonterminal.LP.value, Nonterminal.B.value, Nonterminal.LDV.value, Nonterminal.LDV.value, Nonterminal.LS.value, Nonterminal.LS.value, Nonterminal.DV.value, Nonterminal.LI.value, Nonterminal.LI.value, Nonterminal.S.value, Nonterminal.S.value, Nonterminal.U.value, Nonterminal.U.value, Nonterminal.M.value, Nonterminal.M.value, Nonterminal.M.value, Nonterminal.M.value, Nonterminal.M.value, Nonterminal.M.value, Nonterminal.M.value, Nonterminal.E.value, Nonterminal.E.value, Nonterminal.E.value, Nonterminal.L.value, Nonterminal.L.value, Nonterminal.L.value, Nonterminal.L.value, Nonterminal.L.value, Nonterminal.L.value, Nonterminal.L.value, Nonterminal.R.value, Nonterminal.R.value, Nonterminal.R.value, Nonterminal.Y.value, Nonterminal.Y.value, Nonterminal.Y.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.F.value, Nonterminal.LE.value, Nonterminal.LE.value, Nonterminal.LV.value, Nonterminal.LV.value, Nonterminal.LV.value, Nonterminal.IDD.value, Nonterminal.IDU.value, Nonterminal.ID.value, Nonterminal.TRUE.value, Nonterminal.FALSE.value, Nonterminal.CHR.value, Nonterminal.STR.value, Nonterminal.NUM.value, Nonterminal.NB.value, Nonterminal.MF.value, Nonterminal.MC.value, Nonterminal.NF.value, Nonterminal.MT.value, Nonterminal.ME.value, Nonterminal.MW.value
]

rule_number_of_tokens = [
  1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 9, 8, 4, 5, 3, 10, 5, 3, 4, 2, 1, 2, 1, 5, 3, 1, 1, 1, 6, 9, 9, 7, 8, 2, 4, 2, 2, 3, 3, 1, 3, 3, 3, 3, 3, 3, 1, 3, 3, 1, 3, 3, 1, 1, 2, 2, 2, 2, 3, 5, 2, 2, 1, 1, 1, 1, 1, 3, 1, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0
]