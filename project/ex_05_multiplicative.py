from delta import Compiler, Phase

source = '1 + 2 * 3'

c = Compiler('program')
c.realize(source, Phase.EVALUATION)
print()
print(c.wat_code)
print()
print(c.result)