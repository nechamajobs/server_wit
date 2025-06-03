import ast

def check_function_length(tree):
    warnings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            end = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')], default=start)
            length = end - start + 1
            if length > 20:
                warnings.append(f"Function '{node.name}' is too long: {length} lines")
    return warnings

def check_file_length(source_code):
    lines = source_code.splitlines()
    if len(lines) > 200:
        return [f"File is too long: {len(lines)} lines"]
    return []


def check_unused_variables(tree):
    assigned = set()
    used = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)

    unused = assigned - used
    return [f"Variable '{var}' assigned but never used" for var in unused]

def check_missing_docstrings(tree):
    warnings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node) is None:
                warnings.append(f"Function '{node.name}' has no docstring")
    return warnings


def analyze_code(source_code):
    tree = ast.parse(source_code)

    warnings = []
    warnings += check_function_length(tree)
    warnings += check_file_length(source_code)
    warnings += check_unused_variables(tree)
    warnings += check_missing_docstrings(tree)

    return warnings
