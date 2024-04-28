from delta import Compiler, Phase

source = '''
var n, r, i, x;
n = 5;
r = 1;
i = 0;
x = 2 / 2;
while n - i {
    i = i + 1;
    r = r * i;
}
r
'''

c = Compiler('program')
c.realize(source, Phase.EVALUATION)
print()
print(c.parse_tree_str)
print()
print(c.symbol_table)
print()
print(c.wat_code)
print()
print(c.result)
