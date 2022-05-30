import parser_LL

filename = "data/wikipedia.txt"

# Defining valid tokens in the grammar
class F(parser_LL.UniqueToken): pass

class A(parser_LL.UniquelyValuedToken): value = "a"
class BOpen(parser_LL.UniquelyValuedToken): value = "("
class BClose(parser_LL.UniquelyValuedToken): value = ")"
class Plus(parser_LL.UniquelyValuedToken): value = "+"

S = parser_LL.TBegin
End = parser_LL.TEnd

# Defining the grammar
grammar = parser_LL.Grammar(nonterminals=[S, F], terminals=[BOpen, BClose, A, Plus, End])
grammar[S, BOpen] = lambda _: [BOpen(), S(), Plus(), F(), BClose()]
grammar[S, A] = lambda _: F()
grammar[F, A] = lambda a: a

parser = parser_LL.Parser(grammar)
parser.push(End())
parser.push(S())

print(f"{'Input':>10} | Stack")
with open (filename, "r") as f:
    for line in f:
        parser.parse(line)
        parser.parse([End()])
        assert parser.finished()
