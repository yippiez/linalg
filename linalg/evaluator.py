#!/usr/bin/env python3

import numpy as np
from typing import Dict, Any, Union, List, Tuple, Optional
from .parser import Node, NodeType, PlaceholderNode, BinaryOpNode, UnaryOpNode, FunctionNode, ConstantNode

# Type for results of evaluation
Result = Union[np.ndarray, float, Tuple[Any, ...]]


class Evaluator:
    """Evaluator for AST nodes."""
    
    def __init__(self, matrices: Dict[str, np.ndarray]):
        self.matrices = matrices
    
    def evaluate(self, node: Node) -> Result:
        """Evaluate an AST node."""
        match node.node_type:
            case NodeType.PLACEHOLDER:
                return self._evaluate_placeholder(node)
            case NodeType.BINARY_OP:
                return self._evaluate_binary_op(node)
            case NodeType.UNARY_OP:
                return self._evaluate_unary_op(node)
            case NodeType.FUNCTION:
                return self._evaluate_function(node)
            case NodeType.CONSTANT:
                return self._evaluate_constant(node)
            case _:
                raise ValueError(f"Unknown node type: {node.node_type}")
    
    def _evaluate_placeholder(self, node: PlaceholderNode) -> np.ndarray:
        """Evaluate a placeholder node."""
        # Special handling for P placeholder (represents PIPE)
        if node.name == 'P' and 'PIPE' in self.matrices:
            return self.matrices['PIPE']
        
        if node.name not in self.matrices:
            raise ValueError(f"Unknown placeholder: {node.name}")
        return self.matrices[node.name]
    
    def _evaluate_binary_op(self, node: BinaryOpNode) -> Result:
        """Evaluate a binary operation node."""
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        
        match node.op:
            case '+':
                return left + right
            case '-':
                return left - right
            case '*':
                return left * right
            case '@':
                return left @ right
            case '^':
                if isinstance(right, (int, float, np.number)):
                    from numpy.linalg import matrix_power
                    return matrix_power(left, int(right))
                else:
                    raise ValueError("Power must be a scalar")
            case _:
                raise ValueError(f"Unknown binary operator: {node.op}")
    
    def _evaluate_unary_op(self, node: UnaryOpNode) -> Result:
        """Evaluate a unary operation node."""
        operand = self.evaluate(node.operand)
        
        match node.op:
            case 'transpose':
                return operand.T
            case 'negate':
                return -operand
            case _:
                raise ValueError(f"Unknown unary operator: {node.op}")
    
    def _evaluate_function(self, node: FunctionNode) -> Result:
        """Evaluate a function node."""
        args = [self.evaluate(arg) for arg in node.args]
        
        match node.name:
            # Matrix operations that return a matrix
            case 'inv':
                from numpy.linalg import inv
                return inv(args[0])
            case 'pinv':
                from numpy.linalg import pinv
                return pinv(args[0])
            case 'matrix_power':
                from numpy.linalg import matrix_power
                return matrix_power(args[0], int(args[1]))
            
            # Element-wise math functions
            case 'exp':
                return np.exp(args[0])
            case 'sin':
                return np.sin(args[0])
            case 'cos':
                return np.cos(args[0])
            
            # Scalar output functions
            case 'det':
                from numpy.linalg import det
                return det(args[0])
            case 'trace' | 'tr':
                return np.trace(args[0])
            case 'norm':
                from numpy.linalg import norm
                return norm(args[0])
            case 'rank':
                from numpy.linalg import matrix_rank
                return matrix_rank(args[0])
            case 'cond':
                from numpy.linalg import cond
                return cond(args[0])
            case 'sum':
                return np.sum(args[0])
            case 'prod':
                return np.prod(args[0])
            case 'mean':
                return np.mean(args[0])
            case 'std':
                return np.std(args[0])
            
            # Decomposition functions (returning tuples)
            case 'svd':
                from numpy.linalg import svd
                return svd(args[0], full_matrices=True)
            case 'eig':
                from numpy.linalg import eig
                return eig(args[0])
            case 'qr':
                from numpy.linalg import qr
                return qr(args[0])
            case 'lu':
                from scipy.linalg import lu
                return lu(args[0])
            case 'cholesky':
                from numpy.linalg import cholesky
                return cholesky(args[0])
            
            # Equation solving
            case 'solve':
                from numpy.linalg import solve
                return solve(args[0], args[1])
            case 'lstsq':
                from numpy.linalg import lstsq
                return lstsq(args[0], args[1], rcond=None)[0]  # Return just the solution
            
            # Matrix creation functions
            case 'eye':
                return np.eye(int(args[0]))
            case 'diag':
                return np.diag(args[0])
            case 'rand':
                if len(args) == 1:
                    return np.random.rand(int(args[0]))
                elif len(args) == 2:
                    return np.random.rand(int(args[0]), int(args[1]))
                else:
                    raise ValueError("rand() takes 1 or 2 arguments")
            case 'zeros':
                if len(args) == 1:
                    return np.zeros(int(args[0]))
                elif len(args) == 2:
                    return np.zeros((int(args[0]), int(args[1])))
                else:
                    raise ValueError("zeros() takes 1 or 2 arguments")
            case 'ones':
                if len(args) == 1:
                    return np.ones(int(args[0]))
                elif len(args) == 2:
                    return np.ones((int(args[0]), int(args[1])))
                else:
                    raise ValueError("ones() takes 1 or 2 arguments")
            case _:
                raise ValueError(f"Unknown function: {node.name}")
    
    def _evaluate_constant(self, node: ConstantNode) -> float:
        """Evaluate a constant node."""
        return node.value


def evaluate_expression(ast: Node, matrices: Dict[str, np.ndarray]) -> Result:
    """Evaluate a parsed expression AST.
    
    Args:
        ast: The AST root node to evaluate
        matrices: Dictionary mapping placeholder names to NumPy arrays
        
    Returns:
        The result of evaluating the expression
    """
    evaluator = Evaluator(matrices)
    return evaluator.evaluate(ast)