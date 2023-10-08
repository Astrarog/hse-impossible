from ..useful_functions import dot, get_bits
from .constants import *


def dot_operation(x, L):
    if len(L) != len(L[0]):
        raise ValueError("L should be matrix")

    if len(x) != len(L):
        raise ValueError("Size of x and L doesn't match")

    y = [int(dot(row, x) != 0) for row in L]
    return y


def kb_forward(x):
    return dot_operation(x, L_forward)


def kb_backward(y):
    return dot_operation(y, L_backward)
