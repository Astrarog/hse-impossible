from kb_anlysis.expressions.KB256 import KB256

x_start  = ('a', 'a', 0, 0, 0, 0, 0, 'a')
y_finish = ('a', 'a', 'a', 0, 0, 0, 0, 0)

kb = KB256()
kb.encrypt_n(x_start, 9)
kb.creator.save('enc_9.tex')
kb.decrypt_n(y_finish, 9)
kb.creator.save('dec_9.tex')
