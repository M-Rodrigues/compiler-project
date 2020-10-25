from lexical.token import Token
from lexical.tokenizer import Tokenizer 

from syntatical.analyzer import Analyzer

code = """
function fibonacci(n : integer) : integer {
  var ret : integer;
  if (n >= 2)
    ret = fibonacci(n-1) + fibonacci(n-2);
}
"""

code += '\x03'

tokenizer = Tokenizer(code)
# token, tokenSecundario, identificador = tokenizer.nextToken()
# while token is not Token.EOF:
#   print(token, tokenSecundario, identificador)
#   token, tokenSecundario, identificador = tokenizer.nextToken()

synt_analyzer = Analyzer()
synt_analyzer.run_analysis(tokenizer)


# function fat(n : integer) : integer {
#   var ret : integer;
#   if (n >= 2)
#     ret = n * fat(n-1);
# }
