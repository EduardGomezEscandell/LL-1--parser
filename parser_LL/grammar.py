import parser_LL

class _Table:
    def __init__(self, rows: list, cols: list) -> None:
        self.rows = rows
        self.cols = cols
        self.data = {}

    def __getitem__(self, idx: tuple) -> str:
        row, col = idx
        return self.data[(type(row), type(col))]

    def __setitem__(self, idx: tuple, value: str) -> None:
        (row, col) = idx
        self.data[(row, col)] = value

    def __contains__(self, idx: tuple) -> bool:
        return idx in self.data

class Grammar:
    def __init__(self, nonterminals: list, terminals: list) -> None:
        self.table = _Table(rows=nonterminals, cols=terminals)
        self.registered_tokens = set()

        for tk in terminals:
            self.register_token(tk)
        for tk in nonterminals:
            self.register_token(tk)

    def register_token(self, grouptype: type) -> None:
        assert issubclass(grouptype, parser_LL.Token)
        self.registered_tokens.add(grouptype)

    def __type_in_list(cls, inp: type, list: list) -> bool:
        return inp in list

    def __instance_in_list(cls, inp, list: list) -> bool:
        for t in list:
            if isinstance(inp, t):
                return True
        return False

    def __constructible_in_list(cls, inp, list: list) -> bool:
        for t in list:
            if t.test(inp):
                return True
        return False

    def _is_terminal(self, inp) -> bool:
        if isinstance(inp, type):
            return self.__type_in_list(inp, self.table.cols)
        elif isinstance(inp, parser_LL.Token):
            return self.__instance_in_list(inp, self.table.cols)
        return self.__constructible_in_list(inp, self.table.cols)

    def _is_nonterminal(self, inp) -> bool:
        if isinstance(inp, type):
            return self.__type_in_list(inp, self.table.rows)
        elif isinstance(inp, parser_LL.Token):
            return self.__instance_in_list(inp, self.table.rows)
        return self.__constructible_in_list(inp, self.table.rows)

    def _process_index(self, idx):
        (a, b) = idx

        a_is_nonterminal = self._is_nonterminal(a)
        a_is_terminal = self._is_terminal(a)
        b_is_nonterminal = self._is_nonterminal(b)
        b_is_terminal = self._is_terminal(b)

        if a_is_nonterminal and b_is_nonterminal:
            raise KeyError(f"Both {a} and {b} are nonterminals")

        if a_is_terminal and b_is_terminal:
            raise KeyError(f"Both {a} and {b} are terminals")

        if a_is_terminal:
            terminal = a
        elif a_is_nonterminal:
            nonterminal = a
        else:
            raise KeyError(f"{a} is not a member of this grammar")

        if b_is_terminal:
            terminal = b
        elif b_is_nonterminal:
            nonterminal = b
        else:
            raise KeyError(f"{b} is not a member of this grammar")

        return (nonterminal, terminal)

    def __getitem__(self, idx: str) -> str:
        a = self.tokenize(idx[0])
        b = self.tokenize(idx[1])
        return self.table[self._process_index((a,b))]

    def __setitem__(self, idx: str, value: str) -> None:
        self.table[self._process_index(idx)] = value

    def tokenize(self, input) -> parser_LL.Token:
        if isinstance(input, parser_LL.Token):
            return input

        for g in self.registered_tokens:
            if g.test(input):
                return g(input)

        return parser_LL.TAny(input)