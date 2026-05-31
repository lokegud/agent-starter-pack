"""
Forgix calculator skill — safe math evaluation.

Uses Python's ast module to parse and evaluate ONLY arithmetic expressions.
NO eval(), NO exec(), NO __builtins__ access. Whitelist of operators and functions only.
"""
from __future__ import annotations

import ast
import math
import operator

from forgix.modules.base import tool_schema

_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARYOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}
_FUNCTIONS = {
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "log": math.log, "log2": math.log2, "log10": math.log10, "exp": math.exp,
    "floor": math.floor, "ceil": math.ceil, "abs": abs, "round": round,
    "factorial": math.factorial, "gcd": math.gcd, "pow": pow,
    "min": min, "max": max,
}
_CONSTANTS = {"pi": math.pi, "e": math.e, "tau": math.tau, "inf": math.inf}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants allowed")
    if isinstance(node, ast.BinOp):
        op = _BINOPS.get(type(node.op))
        if not op:
            raise ValueError(f"Operator not allowed: {type(node.op).__name__}")
        return op(_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp):
        op = _UNARYOPS.get(type(node.op))
        if not op:
            raise ValueError(f"Unary operator not allowed: {type(node.op).__name__}")
        return op(_eval_node(node.operand))
    if isinstance(node, ast.Name):
        if node.id in _CONSTANTS:
            return _CONSTANTS[node.id]
        raise ValueError(f"Unknown name: {node.id}")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name) or node.func.id not in _FUNCTIONS:
            raise ValueError("Function not allowed")
        args = [_eval_node(a) for a in node.args]
        return _FUNCTIONS[node.func.id](*args)
    raise ValueError(f"Expression element not allowed: {type(node).__name__}")


@tool_schema(
    "skill.calculate",
    "Safely evaluate a mathematical expression. Supports +, -, *, /, **, sqrt, sin, cos, log, pi, e, etc.",
    {"expression": {"type": "string", "description": "Math expression, e.g. 'sqrt(2) * pi + 3**2'"}},
    required=["expression"],
)
async def calculate(expression: str) -> str:
    """Evaluate a math expression safely (no eval/exec)."""
    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval_node(tree.body)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "[Error: division by zero]"
    except (ValueError, SyntaxError, TypeError, OverflowError) as e:
        return f"[Calculation error: {e}]"
