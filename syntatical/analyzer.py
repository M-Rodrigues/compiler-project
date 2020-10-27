import time
from .action_table import action_table

from nonterminals.tokens import rule_number_of_tokens, rule_left_token

from semantics.analyzer import SemanticAnalyzer

class SyntaticalAnalyzer:
  def __init__(self):
    self.action_table = action_table
    self.stack = [0]

  def final(self, q):
    return q == "acc"

  def shift(self, q):
    if len(q) == 0 or q[0] != 's':
      return -1, False
    return int(q[1:]), True
  
  def reduction(self, q):
    if len(q) == 0 or q[0] != 'r':
      return -1, False
    return int(q[1:]), True

  def run_analysis(self, lexical):
    state = 0
    curr_token, st, _ = lexical.nextToken()
    action = self.action_table[state][curr_token.value]

    sematics_analyzer = SemanticAnalyzer(lexical)

    while not self.final(action):
      print('state: {}\tcurrToken: {} {}\taction: {}\t SyntaticalStack: {}'.format(state, curr_token.value, curr_token, action, self.stack))
      
      state, is_shift = self.shift(action)
      if is_shift:
        self.stack.append(state)
        curr_token, st, _ = lexical.nextToken()

      rule, is_reduction = self.reduction(action)
      if is_reduction:
        r = rule_number_of_tokens[rule-1]
        self.stack = self.stack[:len(self.stack)-r]
        tmp_state = self.stack[-1]
        left_token = rule_left_token[rule-1]
        new_state = self.action_table[tmp_state][left_token]
        state = int(new_state)
        self.stack.append(state)
        sematics_analyzer.check(rule)

      action = self.action_table[state][curr_token.value]
