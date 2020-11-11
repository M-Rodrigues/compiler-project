from lexical.token import Token
from lexical.tokenizer import Tokenizer 

from syntatical.analyzer import SyntaticalAnalyzer

code = """
function fibonacci(n : integer) : integer {
  var ret : integer;
  if (n >= 2)
    ret = fibonacci(n-1) + fibonacci(n-2);
}
}
""" + '\x03'

tokenizer = Tokenizer(code)

synt_analyzer = SyntaticalAnalyzer()
synt_analyzer.run_analysis(tokenizer)