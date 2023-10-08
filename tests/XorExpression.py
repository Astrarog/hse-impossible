import unittest
from kb_anlysis.expressions.XorExpression import XorExpression


class TestXorInit(unittest.TestCase):
    def test_xor_iterator(self):
        data = [1, "a", "b", "c", "b", 13]

        xor = XorExpression(data)

        result = set()
        for e in xor:
            result.add(e)

        self.assertEqual(result, {1^13, "a", "c"})

    def test_number_xor(self):
        data = 2**31

        xor = XorExpression(data)
        xor.add(data)

        self.assertEqual(xor.number, 0)

    def test_simple_xor(self):
        data = [1, "a", "b", "c", "b", 13]

        xor = XorExpression(data)

        number = xor.number
        lhs = xor.lhs

        self.assertEqual(number, 1^13)
        self.assertEqual(lhs, {'a', 'c'})

    def test_xor_other_expression(self):
        data1 = XorExpression([1, "a", "c", "b"])
        data2 = XorExpression([13, "b"])

        xor = data1.add(data2)

        number = xor.number
        lhs = xor.lhs

        self.assertEqual(number, 1^13)
        self.assertEqual(lhs, {'a', 'c'})

    def test_xor_to_str(self):
        data = XorExpression()
        self.assertEqual(str(data), "0")

        data.add(1)
        self.assertEqual(str(data), "1")

        values = {"a"}
        other_data = XorExpression(values)

        expected = ' ^ '.join(values)
        self.assertEqual(str(other_data), expected)

        data.add(other_data)
        expected = '1 ^ ' + expected
        self.assertEqual(str(data), expected)

    def test_equal(self):
        data = [1, "a", "b", "c", "b", 1, "c", "a"]

        xor = XorExpression(data)

        self.assertEqual(XorExpression(), xor)


if __name__ == '__main__':
    unittest.main()
