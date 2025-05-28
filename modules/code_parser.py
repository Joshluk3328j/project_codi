# project_codi/modules/code_parser.py

import ast
from typing import List, Dict

def explain_code(code: str, style: str = "concise") -> List[Dict[str, str]]:
    """Parses and explains Python code block by block."""
    explanations = []
    try:
        tree = ast.parse(code)
        for node in tree.body:
            block_type = type(node).__name__
            explanation = _explain_node(node, style)
            explanations.append({"type": block_type, "explanation": explanation})
    except Exception as e:
        explanations.append({"type": "Error", "explanation": str(e)})
    return explanations

def _explain_node(node, style: str) -> str:
    if isinstance(node, ast.FunctionDef):
        if style == "concise":
            return f"Function '{node.name}' with {len(node.args.args)} argument(s)."
        else:
            params = ", ".join([arg.arg for arg in node.args.args])
            return f"Defines a function named '{node.name}' with parameter(s): {params or 'none'}. Body contains {len(node.body)} statement(s)."
    elif isinstance(node, ast.ClassDef):
        if style == "concise":
            return f"Class '{node.name}'."
        else:
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            return f"Defines a class named '{node.name}' with {len(methods)} method(s): {', '.join(methods) or 'none'}."
    elif isinstance(node, ast.Assign):
        targets = ", ".join([ast.unparse(t) for t in node.targets])
        if style == "concise":
            return f"Assigns to: {targets}."
        else:
            return f"Assigns value to variable(s): {targets}. Value is: {ast.unparse(node.value)}."
    elif isinstance(node, ast.Import):
        names = ", ".join([alias.name for alias in node.names])
        return f"Imports module(s): {names}."
    elif isinstance(node, ast.ImportFrom):
        names = ", ".join([alias.name for alias in node.names])
        return f"From module '{node.module}', imports: {names}."
    elif isinstance(node, ast.If):
        if style == "concise":
            return f"If statement."
        else:
            return f"Conditional check with condition: {ast.unparse(node.test)}."
    elif isinstance(node, ast.For):
        if style == "concise":
            return f"For loop."
        else:
            return f"For loop iterating over: {ast.unparse(node.iter)}."
    elif isinstance(node, ast.While):
        if style == "concise":
            return f"While loop."
        else:
            return f"While loop with condition: {ast.unparse(node.test)}."
    else:
        return f"{type(node).__name__} block detected."