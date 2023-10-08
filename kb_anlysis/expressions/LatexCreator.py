kb_latex_prefix = r'''
\documentclass[tikz, border=2mm]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T2A]{fontenc}
\usepackage{titlesec}
\usepackage{amsmath}
\usepackage{amsthm}
\usepackage{amsfonts}
\usepackage{mathrsfs}
\usepackage{amssymb,stmaryrd}


\usepackage{geometry}
\usepackage{tikz}
\usetikzlibrary{
	calc,
	positioning,
	backgrounds,
	arrows.meta
}

% define the XOR node
\tikzset{XOR/.style={draw,circle,append after command={
			[shorten >=\pgflinewidth, shorten <=\pgflinewidth,]
			(\tikzlastnode.north) edge (\tikzlastnode.south)
			(\tikzlastnode.east) edge (\tikzlastnode.west)
		}
	}
}

\geometry{left=2.5cm}
\geometry{right=2.5cm}
\geometry{top=2.5cm}
\geometry{bottom=2.5cm}

\begin{document}
	\begin{tikzpicture}	

'''

kb_latex_suffix = r'''
	\end{tikzpicture}
\end{document}
'''


class LatexCreator:
    def __init__(self):
        self.tex_prefix = kb_latex_prefix
        self.tex_body = ''
        self.tex_suffix = kb_latex_suffix
        self.Xcrt = 0
        self.Scrt = 0
        self.XORcrt = 0
        self.FQcrt = 0
        self.baseYCoord = 0
        self.encrypt=True
        
    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(self.tex_prefix + self.tex_body + self.tex_suffix)
        
    def flush(self):
        self.tex_body = ''
        self.Xcrt = 0
        self.Scrt = 0
        self.XORcrt = 0
        self.FQcrt = 0
        self.baseYCoord = 0
    
    def draw_xor_arrows_and_step(self):
        self.draw_xor_boxes()
        self.draw_arrows()
        self.step()
    
    def step(self):
        self.baseYCoord -= 6
        
    def draw_x_boxes(self, x, top=False):
        string = ''
        first = True
        y_cord = self.baseYCoord 
        y_cord -= (6 if not top else 0)
        
        for e in x:
            e = '' if str(e) == '0' else str(e).replace('^', r'\oplus')
            
            x_idx = self.Xcrt
            self.Xcrt += 1

            relative_pos = f', right=0mm of X{x_idx-1}'
            absolute_pos = f''
            if first:
                relative_pos = f''
                absolute_pos = f'at (0, {y_cord}) '
                first = False

            prefix = r'\node [rectangle, draw=black, fill=white, minimum width=2cm, minimum height=1cm' + relative_pos + '] '
            position = f'(X{x_idx}) {absolute_pos} {{${e}$}};'
            string += prefix + position + '\n'

        self.tex_body += string
        return

    def draw_s_box(self, s):
        s = '' if str(s) == '0' else str(s).replace('^', r'\oplus')

        x_cord = 9 if self.encrypt else 6
        
        s_idx = self.Scrt
        self.Scrt += 1

        absolute_pos = f'at ({x_cord}, {self.baseYCoord - 1.75})'

        prefix = r'\node [rectangle, draw=black, fill=white, minimum width=2cm, minimum height=0.8cm] '
        position = f'(S{s_idx}) {absolute_pos} {{${s}$}};'
        string = prefix + position + '\n'
        
        self.tex_body += string
        return

    def draw_f_boxes(self, f):
        x_cords = [2, 8, 12] if self.encrypt else [0, 4, 10]

        string = ''
        for e, x in zip(f, x_cords):
            e = '' if str(e) == '0' else str(e).replace('^', r'\oplus')
            
            f_idx = self.FQcrt
            self.FQcrt += 1

            absolute_pos = f'at ({x + 1.5}, {self.baseYCoord - 3.25}) '

            prefix = r'\node [rectangle, draw=black, fill=white, minimum width=2cm, minimum height=0.8cm] '
            position = f'(FQ{f_idx}) {absolute_pos} {{${e}$}};'
            string += prefix + position + '\n'

        self.tex_body += string
        return
    
    def draw_xor_boxes(self):
        x_cords = [2, 8, 14] if self.encrypt else [0, 4, 10]

        string = ''
        for x in x_cords:
            xor_idx = self.XORcrt
            self.XORcrt += 1

            absolute_pos = f'at ({x}, {self.baseYCoord - 4.5}) '

            prefix = r'\node [XOR, draw=black, fill=white, scale=2] '
            position = f'(XOR{xor_idx}) {absolute_pos} {{}};'
            string += prefix + position + '\n'

        self.tex_body += string
        return
    
    def draw_arrows(self):
        
        # draw arrows on backgroud nodes
        string = r'\begin{scope}[on background layer]' + '\n'
        
        x_base = self.Xcrt - 16
        s_idx = self.Scrt - 1
        fq_base = self.FQcrt - 3
        xor_base = self.XORcrt - 3

        # draw line to S summ box
        # and from direct top to bottom lines
        x_idxs = [1, 3, 4, 6, 7] if self.encrypt else [0, 2, 3, 5, 6] 
        for i in x_idxs:
            x_top = x_base + i
            x_bot = x_top + 8
            x_bot += (-1 if self.encrypt else +1)
            
            prefix = r'\draw [draw = red, thick, fill = red] '
            position = f'(X{x_top}.south) edge [-{{Latex}}] (S{s_idx});'
            string += prefix + position + '\n'
            
            prefix = r'\draw [draw = blue, thick, fill = blue] '
            position = f'(X{x_top}.south) edge [-{{Latex}}] (X{x_bot}.north);'
            string += prefix + position + '\n'
            
            
        
        # draw line form S summ box to F boxes
        # and from F boxes to XOR boxes
        for i in range(3):
            fq_idx = fq_base + i
            xor_idx = xor_base + i

            prefix = r'\draw [draw = red, thick, fill = red] '
            position = f'(S{s_idx}) edge [-{{Latex}}]  (FQ{fq_idx});'
            string += prefix + position + '\n'

            prefix = r'\draw [draw = red, thick, fill = red] '
            position = f'(FQ{fq_idx}) edge [-{{Latex}}]  (XOR{xor_idx});'
            string += prefix + position + '\n'

        # draw line form top boxes to XOR operators
        # and from XOR operators to bottom boxes
        shift_encrypt = {0:(2, 8 + 7), 
                         2:(0, 8 + 2 - 1), 
                         5:(1, 8 + 5 - 1)}
        shift_decrypt = {1:(1, 8 + 1 + 1), 
                         4:(2, 8 + 4 + 1), 
                         7:(0, 8)}
        
        shift = shift_encrypt if self.encrypt else shift_decrypt
        for i in shift.keys():
            xor_shift, x_bot_shift = shift[i]
            
            x_top = x_base + i
            xor_idx = xor_base + xor_shift
            x_bot = x_base + x_bot_shift


            prefix = r'\draw [draw = blue, thick, fill = blue] '
            position = f'(X{x_top}.south) edge [-{{Latex}}] (XOR{xor_idx});'
            string += prefix + position + '\n'

            prefix = r'\draw [thick, draw = {rgb:red,119;green,0;blue,200}, fill = {rgb:red,119;green,0;blue,200}] '
            position = f'(XOR{xor_idx}) edge [-{{Latex}}]  (X{x_bot}.north);'
            string += prefix + position + '\n'

        string += r'\end{scope}' + '\n'
        self.tex_body += string
        return

