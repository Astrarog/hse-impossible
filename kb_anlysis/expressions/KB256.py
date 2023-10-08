from .XorExpression import XorExpression
from .LatexCreator import LatexCreator


class KB256:
    def __init__(self):
        self.equations = dict()
        self.f_idx = 1
        self.creator = LatexCreator()
        self.inner_call = False
        

    def clear(self, encrypt):
        self.equations = dict()
        self.f_idx = 1
        self.creator.flush()
        self.creator.encrypt = encrypt
    
    def encrypt(self, x):
        if not self.inner_call:
            self.clear(encrypt=True)
            self.creator.draw_x_boxes(x, top=True)

        s = XorExpression([x[1], x[3], x[4], x[6], x[7]])

        f1 = XorExpression()
        f2 = XorExpression()
        f3 = XorExpression()

        if s != XorExpression():
            i = self.f_idx
            self.f_idx += 3

            f1 = f1.add(f'f{i}')
            f2 = f2.add(f'f{i+1}')
            f3 = f3.add(f'f{i+2}')

            self.equations[str(f1)] = s
            self.equations[str(f2)] = s
            self.equations[str(f3)] = s

        
        self.creator.draw_s_box(s)
        self.creator.draw_f_boxes([f1, f2, f3])
        
        y = [x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[0]]
        y[1] = f1.add(y[1])
        y[4] = f2.add(y[4])
        y[7] = f3.add(y[7])
        
        
        if not self.inner_call:
            self.creator.draw_x_boxes(y, top=False)
            self.creator.draw_xor_boxes()
            self.creator.draw_arrows()

        return y

    def encrypt_n(self, x, n):
        self.clear(encrypt=True)
        self.inner_call = True

        if n > 0:
            self.creator.draw_x_boxes(x, top=True)
        for i in range(n):
            y = self.encrypt(x)
            x = y
            
            self.creator.draw_x_boxes(y, top=False)
            self.creator.draw_xor_arrows_and_step()
        return x

    def decrypt(self, y):
        if not self.inner_call:
            self.clear(encrypt=False)
            self.creator.draw_x_boxes(y, top=True)

        s = XorExpression([y[0], y[2], y[3], y[5], y[6]])

        g1 = XorExpression()
        g2 = XorExpression()
        g3 = XorExpression()

        if s != XorExpression():
            i = self.f_idx
            self.f_idx += 3

            g1 = g1.add(f'g{i}')
            g2 = g2.add(f'g{i+1}')
            g3 = g3.add(f'g{i+2}')

            self.equations[str(g1)] = s
            self.equations[str(g2)] = s
            self.equations[str(g3)] = s

        
        self.creator.draw_s_box(s)
        self.creator.draw_f_boxes([g1, g2, g3])
        
        x = [y[7], y[0], y[1], y[2], y[3], y[4], y[5], y[6]]
        x[0] = g1.add(x[0])
        x[2] = g2.add(x[2])
        x[5] = g3.add(x[5])
        
        
        if not self.inner_call:
            self.creator.draw_x_boxes(x, top=False)
            self.creator.draw_xor_boxes()
            self.creator.draw_arrows()

        return x

    def decrypt_n(self, y, n):
        self.clear(encrypt=False)
        self.inner_call = True

        if n > 0:
            self.creator.draw_x_boxes(y, top=True)
        for i in range(n):
            x = self.decrypt(y)
            y = x
            
            self.creator.draw_x_boxes(x, top=False)
            self.creator.draw_xor_arrows_and_step()
        return y

