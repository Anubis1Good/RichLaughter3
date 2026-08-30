from itertools import *

s = '256 159 468 367 127 134 45 39 28'.split()
v = 'АБ АД АЖ ДЖ ЕК ВГ ГЕ ГК БВ ДЕ ЖИ ИК'.split()
print(*range(1,10))

for p in permutations('АБВГДЕЖИК'):
    if all(str(p.index(y)+1) in s[p.index(x)] for x,y in v):
        print(*p)

