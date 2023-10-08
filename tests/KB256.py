import unittest
from kb_anlysis.expressions.KB256 import KB256
from kb_anlysis.expressions.XorExpression import XorExpression


class TestKB256Encrypt(unittest.TestCase):
    def test_only_shift(self):
        kb = KB256()

        x = ['a', 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(x)):
            x[i] = XorExpression(x[i])

        y = kb.encrypt(x)

        expected = [0, 0, 0, 0, 0, 0, 0, 'a']
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(y, expected)

    def test_zero_sum(self):
        kb = KB256()

        x = ['a', 'b', 0, 'b', 0, 0, 0, 0]
        for i in range(len(x)):
            x[i] = XorExpression(x[i])

        y = kb.encrypt(x)

        expected = ['b', 0, 'b', 0, 0, 0, 0, 'a']
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(y, expected)

    def test_nonzero_sum(self):
        kb = KB256()

        x = [0, 'a', 0, 0, 0, 0, 0, 0]
        for i in range(len(x)):
            x[i] = XorExpression(x[i])

        y = kb.encrypt(x)

        expected = ['a', 'f1', 0, 0, 'f2', 0, 0, 'f3']
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(y, expected)
        self.assertEqual(kb.equations, {'f1': XorExpression('a'),
                                        'f2': XorExpression('a'),
                                        'f3': XorExpression('a')})

    def test_nonzero_sum_and_shift(self):
        kb = KB256()

        x = ['a', 'b', 0, 0, 0, 0, 0, 0]
        for i in range(len(x)):
            x[i] = XorExpression(x[i])

        y = kb.encrypt(x)

        expected = ['b', 'f1', 0, 0, 'f2', 0, 0, 'a ^ f3']
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(y[:-1], expected[:-1])
        self.assertEqual(set(str(y[-1]).split(' ^ ')), set(str(expected[-1]).split(' ^ ')))
        self.assertEqual(kb.equations, {'f1': XorExpression('b'),
                                        'f2': XorExpression('b'),
                                        'f3': XorExpression('b')})

    def test_two_rounds(self):
        kb = KB256()

        x = [0, 0, 0, 0, 0, 'a', 0, 0]
        for i in range(len(x)):
            x[i] = XorExpression(x[i])

        y = kb.encrypt_n(x, 2)

        expected = [0, 'f1', 0, 'a', 'f2', 0, 0, 'f3']
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(y, expected)
        self.assertEqual(kb.equations, {'f1': XorExpression('a'),
                                        'f2': XorExpression('a'),
                                        'f3': XorExpression('a')})


class TestKB256Decrypt(unittest.TestCase):
    def test_only_shift(self):
        kb = KB256()

        y = [0, 0, 0, 0, 0, 0, 0, 'a']
        for i in range(len(y)):
            y[i] = XorExpression(y[i])

        x = kb.decrypt(y)

        expected = ['a', 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(x, expected)

    def test_zero_sum(self):
        kb = KB256()

        y = ['b', 0, 'b', 0, 0, 0, 0, 'a']
        for i in range(len(y)):
            y[i] = XorExpression(y[i])

        x = kb.decrypt(y)

        expected = ['a', 'b', 0, 'b', 0, 0, 0, 0]
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(x, expected)

    def test_nonzero_sum(self):
        kb = KB256()

        y = ['a', 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(y)):
            y[i] = XorExpression(y[i])

        x = kb.decrypt(y)

        expected = ['g1', 'a', 'g2', 0, 0, 'g3', 0, 0]
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(x, expected)
        self.assertEqual(kb.equations, {'g1': XorExpression('a'),
                                        'g2': XorExpression('a'),
                                        'g3': XorExpression('a')})

    def test_nonzero_sum_and_shift(self):
        kb = KB256()

        y = ['a', 0, 0, 0, 0, 0, 0, 'b']
        for i in range(len(y)):
            y[i] = XorExpression(y[i])

        x = kb.decrypt(y)

        expected = ['b ^ g1', 'a', 'g2', 0, 0, 'g3', 0, 0]
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(x[1:], expected[1:])
        self.assertEqual(set(str(x[0]).split(' ^ ')), set(str(expected[0]).split(' ^ ')))
        self.assertEqual(kb.equations, {'g1': XorExpression('a'),
                                        'g2': XorExpression('a'),
                                        'g3': XorExpression('a')})

    def test_two_rounds(self):
        kb = KB256()

        x = [0, 0, 0, 0, 'a', 0, 0, 0]
        for i in range(len(x)):
            x[i] = XorExpression(x[i])

        y = kb.decrypt_n(x, 2)

        expected = ['g1', 0, 'g2', 0, 0, 'g3', 'a', 0]
        for i in range(len(expected)):
            expected[i] = XorExpression(expected[i])

        self.assertEqual(y, expected)
        self.assertEqual(kb.equations, {'g1': XorExpression('a'),
                                        'g2': XorExpression('a'),
                                        'g3': XorExpression('a')})


if __name__ == '__main__':
    unittest.main()
