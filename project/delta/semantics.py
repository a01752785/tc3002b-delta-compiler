# Author: A01752785 David Damian Galan

from arpeggio import PTNodeVisitor


class SemanticMistake(Exception):

    def __init__(self, message):
        super().__init__(f'Semantic error: {message}')


class SemanticVisitor(PTNodeVisitor):

    RESERVED_WORDS = ['true', 'false', 'var', 'if', 'else', 'while', 'do']

    def __init__(self, parser, **kwargs):
        super().__init__(**kwargs)
        self.__parser = parser
        self.__symbol_table = []

    def position(self, node):
        return self.__parser.pos_to_linecol(node.position)

    @property
    def symbol_table(self):
        return self.__symbol_table

    def visit_integer(self, node, children):
        value = int(children[0])
        if value >= 2 ** 31:
            raise SemanticMistake(
                'Out of range decimal integer literal at position '
                f'{self.position(node)} => { value }'
            )
        
    def visit_decimal(self, node, children):
        return node.value
    
    def visit_binary(self, node, children):
        return str(int(node.value[2:], 2))
    
    def visit_octal(self, node, children):
        return str(int(node.value[2:], 8))
    
    def visit_hexadecimal(self, node, children):
        return str(int(node.value[2:], 16))

    def visit_decl_variable(self, node, children):
        name = node.value
        if name in SemanticVisitor.RESERVED_WORDS:
            raise SemanticMistake(
                'Reserved word not allowed as variable name at position '
                f'{self.position(node)} => {name}'
            )
        if name in self.__symbol_table:
            raise SemanticMistake(
                'Duplicate variable declaration at position'
                f'{self.position(node)} => {name}'
            )
        self.symbol_table.append(name)

    def visit_lhs_variable(self, node, children):
        name = node.value
        if name not in self.__symbol_table:
            raise SemanticMistake(
                'Assignment to undeclared variable at position'
                f'{self.position(node)} => {name}'
            )
        
    def visit_rhs_variable(self, node, children):
        name = node.value
        if name not in self.__symbol_table:
            raise SemanticMistake(
                'Undeclared variable reference at position'
                f'{self.position(node)} => {name}'
            )