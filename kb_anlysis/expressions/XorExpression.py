from ..useful_functions import represents_int, represents_float


class XorExpression:

    class XorExpressionIterator:
        def __init__(self, expr):
            self.number = expr.number
            self.is_number_shown = (expr.number == 0)
            self.lhs_iter = iter(expr.lhs)

        def __next__(self):
            if not self.is_number_shown:
                self.is_number_shown = True
                return self.number

            result = next(self.lhs_iter)
            return result

    def __init__(self, exp=None):
        self.lhs = set()
        self.number = 0
        self.add(exp)

    def __add_elem(self, e):
        if e is None:
            return self

        e = str(e)
        if represents_int(e):
            e = int(e)
            self.number ^= (e % 2**32)
            return self

        if represents_float(e):
            raise ValueError("Float numbers not supported")

        if e in self.lhs:
            self.lhs.remove(e)
        else:
            self.lhs.add(e)

        return self

    def add(self, e):
        if type(e) in [list, set, XorExpression]:
            for elem in e:
                self.add(elem)
            return self

        return self.__add_elem(e)

    def __iter__(self):
        return XorExpression.XorExpressionIterator(self)

    def __str__(self):
        if len(self.lhs) == 0:
            return str(self.number)

        prefix = str(self.number) if self.number != 0 else ''
        join = ' ^ ' if self.number != 0 else ''
        expression = ' ^ '.join(self.lhs)

        return prefix + join + expression

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if type(other) == XorExpression:
            return self.number == other.number and self.lhs == other.lhs
        if type(other) == int:
            return self.number == other
        if type(other) == str:
            return other in self.lhs

        return False
