import parser_LL

filename = "data/sums.txt"

# Defining valid tokens in the grammar
class EndExpr(parser_LL.UniqueToken): pass
class Number(parser_LL.UniqueToken): pass

class BOpen(parser_LL.UniquelyValuedToken): value = "("
class BClose(parser_LL.UniquelyValuedToken): value = ")"
class Dot(parser_LL.UniquelyValuedToken): value = "."

BeginExpr = parser_LL.TBegin
EOT = parser_LL.TEnd
Digit = parser_LL.TDigits
Op = parser_LL.TMathOp
WS = parser_LL.TWhitespace

# Defining the grammar
grammar = parser_LL.Grammar(nonterminals=[BeginExpr, Number, EndExpr], terminals=[BOpen, BClose, Digit, Op, EOT, WS])

grammar[BeginExpr, BOpen] = lambda _: [BOpen(), BeginExpr(), BClose(), EndExpr()]
grammar[BeginExpr, Digit] = lambda x: Number()

grammar[Number, Digit] = lambda x: [x, Number()]
grammar[Number, Op] = lambda x: [EndExpr()]
grammar[Number, BClose] = lambda x: []
grammar[Number, WS] = lambda x: [EndExpr()]
grammar[Number, EOT] = lambda x: []

grammar[EndExpr, Op] = lambda x: [x, BeginExpr()]
grammar[EndExpr, EOT] = lambda x: []

grammar[BeginExpr, WS] = lambda x: [x, BeginExpr()]
grammar[EndExpr, WS] = lambda x: [x, EndExpr()]

# Initialize the parser
parser = parser_LL.Parser(grammar)
parser.push(EOT())
parser.push(BeginExpr())

# Parse
with open (filename, "r") as f:
    line = f.readline()

print(f"{'Input':>10} | Stack")
parser.parse(line)
parser.parse([EOT()])
assert parser.finished()
