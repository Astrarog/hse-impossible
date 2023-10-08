def dot(x, y):
    if len(x) != len(y):
        raise IndexError("Dot operators should have the same size")

    n = len(x)
    ans = 0
    for i in range(n):
        ans += x[i] * y[i]

    return ans


def get_bits(n, digits=8):
    return [1 if n & (1 << (digits-1-i)) else 0 for i in range(digits) ]


def max_transformation(x, f, condition):
    i = 0
    y = f(x)
    while condition(y):
        x = y
        y = f(x)
        i += 1
    return i, x


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def represents_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
