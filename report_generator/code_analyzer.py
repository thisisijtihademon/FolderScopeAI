import re
from pathlib import Path
import subprocess
import os
import ast
import math
from collections import Counter

def analyze_code_file(file_path):
    summary = {"language": None, "line_count": 0, "function_count": 0, "class_count": 0}
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            summary["line_count"] = len(content.splitlines())

            if file_path.endswith('.py'):
                summary["language"] = "Python"
                summary["function_count"] = len(re.findall(r"def\\s+\w+\\s*\\(", content))
                summary["class_count"] = len(re.findall(r"class\\s+\w+", content))
            elif file_path.endswith('.js'):
                summary["language"] = "JavaScript"
                summary["function_count"] = len(re.findall(r"function\\s+\w+\\s*\\(", content))
            elif file_path.endswith('.java'):
                summary["language"] = "Java"
                summary["class_count"] = len(re.findall(r"class\\s+\w+", content))
            elif file_path.endswith('.cpp'):
                summary["language"] = "C++"
                summary["function_count"] = len(re.findall(r"\w+\\s+\w+\\s*\\(", content))
            elif file_path.endswith('.c'):
                summary["language"] = "C"
                summary["function_count"] = len(re.findall(r"\w+\\s+\w+\\s*\\(", content))
            elif file_path.endswith('.html'):
                summary["language"] = "HTML"
            elif file_path.endswith('.css'):
                summary["language"] = "CSS"
    except Exception as e:
        summary["error"] = str(e)

    return summary


def deep_code_analysis(file_path):  # ✅ Accepts 1 argument
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        lines = content.splitlines()
        comment_lines = len([line for line in lines if line.strip().startswith(("#", "//", "/*", "*", "--"))])
        function_count = len([line for line in lines if "def " in line or "function " in line])
        complexity_score = sum(content.count(k) for k in ["if ", "for ", "while ", "try ", "catch", "switch"])

        flagged = any(x in content for x in ["eval(", "exec(", "import os", "subprocess"])

        return {
            "total_lines": len(lines),
            "comment_lines": comment_lines,
            "comment_density": round((comment_lines / len(lines)) * 100, 2) if lines else 0,
            "function_count": function_count,
            "complexity_score": complexity_score,
            "suspicious_patterns": flagged
        }
    except Exception as e:
        return {"error": str(e)}

def run_bandit_scan(file_path):
    """
    Run Bandit security scan on a Python file and return results.
    """
    try:
        result = subprocess.run(
            ["bandit", "-r", file_path, "-f", "json"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr.strip()}
    except Exception as e:
        return {"error": str(e)}


# -----------------------------
# 📈 Code Complexity Analyzer
# -----------------------------
def analyze_code_complexity(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        function_defs = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        class_defs = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

        total_lines = len(source_code.splitlines())
        avg_function_length = 0
        if function_defs:
            func_lengths = [len(node.body) for node in function_defs]
            avg_function_length = sum(func_lengths) / len(func_lengths)

        return {
            "total_lines": total_lines,
            "num_functions": len(function_defs),
            "num_classes": len(class_defs),
            "avg_function_length": round(avg_function_length, 2),
            "cyclomatic_complexity_estimate": round(len(function_defs) * 1.5 + len(class_defs) * 2, 2)
        }

    except Exception as e:
        return {"error": str(e)}