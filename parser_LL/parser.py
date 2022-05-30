from collections.abc import Iterable
from parser_LL import Grammar, Token


class Parser:

    def __init__(self, gramar: Grammar):
        self.grammar = gramar
        self.stack = []

    def pop(self) -> str:
        return self.stack.pop()

    def push(self, tk: Token) -> None:
        if isinstance(tk, Iterable):
            self.stack.extend(tk[::-1])
        else:
            self.stack.append(tk)

    def parse(self, line: str) -> None:
        i = 0
        while i < len(line):
            print(self.status(line, i))
            if self.next(line[i]):
                i += 1
        print(self.status(line, i))

    def next(self, input: str) -> bool:
        input = self.grammar.tokenize(input)
        stacktop = self.pop()

        if input == stacktop:
            return True

        try:
            rule = self.grammar[stacktop, input]
        except KeyError as ke:
            raise Exception("No rule found for [{}, {}]".format(stacktop, input)) from ke

        self.push(rule(input))
        return False

    def finished(self) -> bool:
        return len(self.stack) == 0

    def status(self, line, ptr) -> str:
        stackstr = " ".join(map(str, self.stack[::-1]))
        if ptr < len(line):
            return f"{str(line[ptr]):>10} | {stackstr}"
        return f"{' ':>10} | {stackstr}"



