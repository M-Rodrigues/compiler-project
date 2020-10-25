import time
from .action_table import action_table

from nonterminals.tokens import rule_number_of_tokens, rule_left_token

class Analyzer:
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
    curr_token, _, _ = lexical.nextToken()
    action = self.action_table[state][curr_token.value]

    while not self.final(action):
      time.sleep(0.1)
      print('state: {}\tcurrToken: {} {}\taction: {}\t stack: {}'.format(state, curr_token.value, curr_token, action, self.stack))
      state, is_shift = self.shift(action)
      if is_shift:
        # print(action, 'is shift')

        self.stack.append(state)
        curr_token, _, _ = lexical.nextToken()
        action = self.action_table[state][curr_token.value]
        continue

      rule, is_reduction = self.reduction(action)
      if is_reduction:
        # print(action, 'is reduction')

        r = rule_number_of_tokens[rule-1]
        print('rule:', r)
        self.stack = self.stack[:len(self.stack)-r]
        print('stack: {}'.format(self.stack))
  
        tmp_state = self.stack[-1]
        left_token = rule_left_token[rule-1]
        
        # print(type(tmp_state), type(left_token))
        new_state = self.action_table[tmp_state][left_token]
        print('tmp_state: {}\tleft_token: {}\t new_state {}'.format(tmp_state, left_token, new_state))
        state = int(new_state)
        self.stack.append(state)
        action = self.action_table[state][curr_token.value]
        continue

    
