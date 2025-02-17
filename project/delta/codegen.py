# Author: A01752785 David Damian Galan

from arpeggio import PTNodeVisitor


class CodeGenerationVisitor(PTNodeVisitor):

    WAT_TEMPLATE = ''';; Code generated by the Delta compiler
(module
  (func
    (export "_start")
    (result i32)
{}  )
)
'''

    def __init__(self, symbol_table, **kwargs):
        super().__init__(**kwargs)
        self.__symbol_table = symbol_table

    def visit_program(self, node, children):
        
        def declare_variables():
            return ''.join([f'    (local ${var_name} i32)\n'
                            for var_name in self.__symbol_table])
        
        return CodeGenerationVisitor.WAT_TEMPLATE.format(
            declare_variables()
            + ''.join(children)
        )
    
    def visit_statement(self, node, children):
        return children[0]

    def visit_declaration(self, node, children):
        return ''
    
    def visit_assignment(self, node, children):
        return children[1] + children[0]
    
    def visit_if(self, node, children):
        if_count = 1
        result = (children[0]
                  + '    if\n'
                  + children[1])
        if len(children) > 2:
            
            for i in range(2, len(children), 2):
                if children[i] == 'else':
                    result += (
                        '    else\n'
                        + children[i + 1])
                else:
                    if_count = if_count + 1
                    result += (
                        '    else\n'
                        + children[i]
                        + '    if\n'
                        + children[i + 1]
                    )

        result += '    end\n' * (if_count)
        return result
    
    def visit_dowhile(self, node, children):
        return (
            '    loop\n'
            + children[0]
            + children[1]
            + '    br_if 0\n'
            + '    end\n'
        )

    def visit_while(self, node, children):
        return (
            '    block\n'
            + '    loop\n'
            + children[0]
            + '    i32.eqz\n'
            + '    br_if 1\n'
            + children[1]
            + '    br 0\n'
            + '    end\n'
            + '    end\n')
    
    def visit_block(self, node, children):
        return ''.join(children)

    def visit_decl_variable(self, node, children):
        return 'decl_variable'
    
    def visit_lhs_variable(self, node, children):
        name = node.value
        return f'    local.set ${name}\n'
    
    def visit_rhs_variable(self, node, children):
        name = node.value
        return f'    local.get ${name}\n'

    def visit_expression(self, node, children):
        if len(children) == 1:
            return children[0]
        else:
            result = []
            for exp in children[:-1]:
                result.append(exp)
                result.append('    if (result i32)\n')
                result.append('    i32.const 1\n')
                result.append('    else')
            result.append(children[-1])
            result.append('    i32.eqz\n')
            result.append('    i32.eqz\n')
            result.append('    end\n' * (len(children) - 1))
            return ''.join(result)

    def visit_andexpression(self, node, children):
        if len(children) == 1:
            return children[0]
        result = [children[0]]
        for exp in children[1:]:
            result.append('    if (result i32)\n')
            result.append(exp)
        result.append('    i32.eqz' * 2)
        result.append(
            '    else\n'
            '    i32.const 0\n'
            '    end\n' * (len(children) - 1))
        return ''.join(result)
    
    def visit_comparison(self, node, children):
        if len(children) == 1:
            return children[0]
        result = [children[0]]
        operations = {
            "==": "    i32.eq\n",
            "!=": "    i32.ne\n",
            "<": "    i32.lt_s\n",
            "<=": "    i32.le_s\n",
            ">=": "    i32.ge_s\n",
            ">": "    i32.gt_s\n"
        }
        for i in range(1, len(children), 2):
            result.append(children[i + 1])
            result.append(operations[children[i]])
        return ''.join(result)


    def visit_additive(self, node, children):
        result = [children[0]]
        for i in range(1, len(children), 2):
            result.append(children[i + 1])
            match children[i]:
                case '+':
                    result.append('    i32.add\n')
                case '-':
                    result.append('    i32.sub\n')
        return ''.join(result)
    
    def visit_multiplicative(self, node, children):
        result = [children[0]]
        for i in range(1, len(children), 2):
            result.append(children[i + 1])
            match children[i]:
                case '*':
                    result.append('    i32.mul\n')
                case '/':
                    result.append('    i32.div_s\n')
                case '%':
                    result.append('    i32.rem_s\n')
        return ''.join(result)

    def visit_parenthesis(self, node, children):
        return children[0]
    
    def visit_unary(self, node, children):
        result = children[-1]
        for op in children[-2::-1]:
            match op:
                case '+':
                    pass
                case '-':
                    result = (
                        '    i32.const 0\n'
                        + result
                        + '    i32.sub\n'
                    )
                case '!':
                    result += '    i32.eqz\n'
        return result

    def visit_integer(self, node, children):
        return children[0]

    def visit_decimal(self, node, children):
        return f'    i32.const { node.value }\n'
    
    def visit_binary(self, node, children):
        integer = int(node.value[2:], 2)
        return f'    i32.const { integer }\n'
    
    def visit_octal(self, node, children):
        integer = int(node.value[2:], 8)
        return f'    i32.const { integer }\n'
    
    def visit_hexadecimal(self, node, children):
        integer = int(node.value[2:], 16)
        return f'    i32.const { integer }\n'

    def visit_boolean(self, node, children):
        const = 0
        if children[0] == 'true':
            const = 1
        return f'    i32.const {const} \n'
