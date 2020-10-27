from lexical.token import Token
from lexical.tokenizer import Tokenizer 

from syntatical.analyzer import SyntaticalAnalyzer

code = """
function fib(n : integer) : integer {
  var result : integer;
  result = 1;
  if (n >= 2)
    ret = fib(n-1) + fib(n-2);
}
""" + '\x03'

tokenizer = Tokenizer(code)

synt_analyzer = SyntaticalAnalyzer()
synt_analyzer.run_analysis(tokenizer)