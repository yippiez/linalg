#!/usr/bin/env python3

import re
from typing import List, Dict, Any, Union, Tuple
from enum import Enum, auto


class NodeType(Enum):
    """Enum representing the types of nodes in the AST."""
    PLACEHOLDER = auto()
    BINARY_OP = auto()
    UNARY_OP = auto()
    FUNCTION = auto()
    CONSTANT = auto()


class Node:
    """Base class for AST nodes."""
    def __init__(self, node_type: NodeType):
        self.node_type = node_type


class PlaceholderNode(Node):
    """Node representing a matrix placeholder (A, B, C, etc.)."""
    def __init__(self, name: str):
        super().__init__(NodeType.PLACEHOLDER)
        self.name = name
    
    def __repr__(self):
        return f"Placeholder({self.name})"


class BinaryOpNode(Node):
    """Node representing a binary operation (+, -, *, @, etc.)."""
    def __init__(self, op: str, left: Node, right: Node):
        super().__init__(NodeType.BINARY_OP)
        self.op = op
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.op}, {self.left}, {self.right})"


class UnaryOpNode(Node):
    """Node representing a unary operation (transpose, etc.)."""
    def __init__(self, op: str, operand: Node):
        super().__init__(NodeType.UNARY_OP)
        self.op = op
        self.operand = operand
    
    def __repr__(self):
        return f"UnaryOp({self.op}, {self.operand})"


class FunctionNode(Node):
    """Node representing a function call (det, inv, svd, etc.)."""
    def __init__(self, name: str, args: List[Node]):
        super().__init__(NodeType.FUNCTION)
        self.name = name
        self.args = args
    
    def __repr__(self):
        return f"Function({self.name}, {self.args})"


class ConstantNode(Node):
    """Node representing a numeric constant."""
    def __init__(self, value: Union[int, float]):
        super().__init__(NodeType.CONSTANT)
        self.value = value
    
    def __repr__(self):
        return f"Constant({self.value})"


class ExpressionParser:
    """Parser for linear algebra expressions."""
    
    def __init__(self, expression: str):
        self.expression = expression
        self.tokens = self._tokenize(expression)
        self.current = 0
    
    def _tokenize(self, expression: str) -> List[str]:
        """Convert the expression string into tokens."""
        # Replace special PIPE placeholder with a single letter token
        expression = expression.replace("{PIPE}", "{P}")
        
        # Replace placeholder syntax with simple tokens
        pattern = r'\{([A-Z])\}'
        expression = re.sub(pattern, r'\1', expression)
        
        # Add spaces around special characters
        special_chars = ['+', '-', '*', '@', '^', '(', ')', ',', '.']
        for char in special_chars:
            expression = expression.replace(char, f" {char} ")
        
        # Split by whitespace and filter out empty tokens
        tokens = expression.split()
        return tokens
    
    def _peek(self) -> str:
        """Return the current token without advancing."""
        if self.current >= len(self.tokens):
            return None
        return self.tokens[self.current]
    
    def _advance(self) -> str:
        """Return the current token and advance to the next one."""
        token = self._peek()
        self.current += 1
        return token
    
    def _match(self, expected: str) -> bool:
        """Check if the current token matches the expected token."""
        if self._peek() == expected:
            self._advance()
            return True
        return False
    
    def _is_placeholder(self, token: str) -> bool:
        """Check if the token is a placeholder (A, B, C, etc.)."""
        return token and token.isalpha() and token.isupper() and len(token) == 1
    
    def _is_function(self, token: str) -> bool:
        """Check if the token is a function name."""
        functions = [
            'inv', 'pinv', 'matrix_power', 'exp', 'sin', 'cos',
            'det', 'trace', 'tr', 'norm', 'rank', 'cond', 'sum', 'prod', 'mean', 'std',
            'svd', 'eig', 'qr', 'lu', 'cholesky', 'solve', 'lstsq',
            'eye', 'diag', 'rand', 'zeros', 'ones'
        ]
        return token and token in functions
    
    def _is_numeric(self, token: str) -> bool:
        """Check if the token is a numeric value."""
        try:
            float(token)
            return True
        except (ValueError, TypeError):
            return False
    
    def parse(self) -> Node:
        """Parse the tokens and build an AST."""
        return self._expression()
    
    def _expression(self) -> Node:
        """Parse an expression (lowest precedence: + and -)."""
        left = self._term()
        
        while self._peek() in ['+', '-']:
            op = self._advance()
            right = self._term()
            left = BinaryOpNode(op, left, right)
        
        return left
    
    def _term(self) -> Node:
        """Parse a term (medium precedence: * and @)."""
        left = self._power()
        
        while self._peek() in ['*', '@']:
            op = self._advance()
            right = self._power()
            left = BinaryOpNode(op, left, right)
        
        return left
    
    def _power(self) -> Node:
        """Parse a power expression (high precedence: ^)."""
        left = self._factor()
        
        if self._match('^'):
            right = self._factor()
            return BinaryOpNode('^', left, right)
        
        return left
    
    def _factor(self) -> Node:
        """Parse a factor (highest precedence: parentheses, functions, placeholders)."""
        token = self._peek()
        
        # Parentheses
        if token == '(':
            self._advance()  # Consume '('
            expr = self._expression()
            if not self._match(')'):
                raise ValueError("Expected closing parenthesis")
            return expr
        
        # Function call
        elif self._is_function(token):
            return self._function_call()
        
        # Placeholder
        elif self._is_placeholder(token):
            self._advance()  # Consume placeholder
            node = PlaceholderNode(token)
            
            # Check for transpose or property access
            if self._match('.'):
                prop = self._advance()
                if prop == 'T':
                    return UnaryOpNode('transpose', node)
                else:
                    raise ValueError(f"Unknown property: {prop}")
            
            return node
        
        # Numeric constant
        elif self._is_numeric(token):
            self._advance()  # Consume number
            return ConstantNode(float(token))
        
        # Unary minus
        elif token == '-':
            self._advance()  # Consume '-'
            operand = self._factor()
            return UnaryOpNode('negate', operand)
        
        else:
            raise ValueError(f"Unexpected token: {token}")
    
    def _function_call(self) -> Node:
        """Parse a function call."""
        func_name = self._advance()  # Consume function name
        
        if not self._match('('):
            raise ValueError(f"Expected opening parenthesis after function {func_name}")
        
        # Parse arguments
        args = []
        if self._peek() != ')':
            args.append(self._expression())
            
            while self._match(','):
                args.append(self._expression())
        
        if not self._match(')'):
            raise ValueError("Expected closing parenthesis")
        
        return FunctionNode(func_name, args)


def parse_expression(expression: str) -> Node:
    """Parse a linear algebra expression into an AST.
    
    Args:
        expression: The expression string to parse
        
    Returns:
        The root node of the AST
    """
    parser = ExpressionParser(expression)
    return parser.parse()