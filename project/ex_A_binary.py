from delta import Compiler, Phase

source = '''
#o321342
'''

c = Compiler('program')
c.realize(source, Phase.CODE_GENERATION)
print()
print(c.parse_tree_str)
# print()
# print(c.symbol_table)
print()
print(c.wat_code)
# print()
# print(c.result)
