# Author: A01752785 David Damian Galan

from delta import Compiler, Phase

source = '''
var i;
i = 10;
do {
    i = i - 1;
} while i;
i
'''


c = Compiler('program')
c.realize(source, Phase.EVALUATION)
print()
print(c.parse_tree_str)
# print()
# print(c.symbol_table)
print()
print(c.wat_code)
print()
print(c.result)
