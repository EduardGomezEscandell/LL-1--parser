class Token:
    @classmethod
    def test(self, str) -> bool:
        raise NotImplementedError("Calling base class Group.test()")

    def value(self):
        return self._value

    def __eq__(self, other):
        if isinstance(other, Token):
            return type(other) == type(self) and self._value == other._value
        else:
            return self.test(other) and self._value == other


# TOKEN TYPES
class ValuedToken(Token):
    def __init__(self, value: str):
        self._value = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return type(other) == type(self) and self._value == other._value
        return self.test(other) and self._value == other

    def __str__(self):
        return type(self).__name__ + f"[{self.value()}]"

class UniqueToken(Token):
    def __init__(self, *_):
        pass

    @classmethod
    def test(cls, other) -> bool:
        return isinstance(other, cls)

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __str__(self):
        return type(self).__name__

class UniquelyValuedToken(Token):
    def __init__(self, *_):
        pass

    @classmethod
    def test(cls, other) -> bool:
        if isinstance(other, cls):
            return True
        return other == cls.value

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __str__(self):
        return str(self.value)


# Token end results
class TAny(ValuedToken):
    def test(self, _):
        return True

class TDigits(ValuedToken):
    @classmethod
    def test(self, str) -> bool:
        return str.isdigit()

class TLetter(ValuedToken):
    @classmethod
    def test(self, str) -> bool:
        return str.isalpha()

class TAlNum(ValuedToken):
    @classmethod
    def test(self, str) -> bool:
        return str.isalnum()

class TMathOp(ValuedToken):
    @classmethod
    def test(self, str) -> bool:
        return str in "+-*/^"

class TWhitespace(ValuedToken):
    @classmethod
    def test(self, str) -> bool:
        return str.isspace()

class TBegin(UniqueToken):
    def __str__(self):
        return "BEGIN"

class TEnd(UniqueToken):
    def __str__(self):
        return "END"
