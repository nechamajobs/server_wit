import ast
from fileinput import filename
from importlib.metadata import files

import matplotlib.pyplot as plt
from collections import Counter

from fontTools.misc.cython import returns

from anslyze import analyze_code
def collect_all_warnings(files: list[str]) -> list[str]:
    all_warnings = []
    for source_code in files:
        all_warnings.extend(analyze_code(source_code))
    return all_warnings

def get_function_lengths(tree):
    lengths = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno
            end = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')], default=start)
            length = end - start + 1
            lengths.append(length)
    return lengths

def generate_histogram(lengths, output_path="histogram.png"):
    plt.figure(figsize=(8, 6))
    plt.hist(lengths, bins=10, color='skyblue', edgecolor='black')
    plt.title("Function Length Distribution")
    plt.xlabel("Number of Lines")
    plt.ylabel("Number of Functions")
    plt.tight_layout()
    plt.savefig("static/histogram.png")

    plt.close()


def generate_pie_chart(warnings, output_path="issues_pie.png"):
    issue_types = []

    for warning in warnings:
        if "too long" in warning:
            issue_types.append("Function Too Long")
        elif "no docstring" in warning:
            issue_types.append("Missing Docstring")
        elif "assigned but never used" in warning:
            issue_types.append("Unused Variable")
        elif "File is too long" in warning:
            issue_types.append("File Too Long")
        else:
            issue_types.append("Other")

    counts = Counter(issue_types)
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Code Issues by Type")
    plt.tight_layout()
    plt.savefig("static/issues_pie.png")


    plt.close()

def generate_bar_chart(issues_per_file: dict, output_path="static/issues_bar.png"):
    print("📊 יצירת גרף עמודות:", issues_per_file)

    if not issues_per_file:
        # מציירים גרף ריק עם הודעה
        plt.figure(figsize=(6, 4))
        plt.text(0.5, 0.5, "No issues found", ha='center', va='center', fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        print("📁 נשמר גרף ריק ל:", output_path)
        return

    files = list(issues_per_file.keys())
    counts = list(issues_per_file.values())

    plt.figure(figsize=(8, 6))
    plt.bar(files, counts, color='lightcoral')
    plt.xlabel("File Name")
    plt.ylabel("Number of Issues")
    plt.title("Issues Per File")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print("📁 נשמר גרף ל:", output_path)

def count_of_problems(files: list[str], filenames: list[str]) -> dict:
    problems_per_file = {}
    for i in range(len(files)):
        source_code = files[i]
        filename = filenames[i]
        warnings = analyze_code(source_code)
        problems_per_file[filename] = len(warnings)
    return problems_per_file



