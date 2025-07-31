#!/usr/bin/env python3
"""
Script to generate a dynamic checklist for README.md from the check functions
in the operators/checks folder by extracting their docstrings.
"""

import os
import re
import ast


def get_check_function_docstring(file_path):
    """
    Extract the docstring from the 'check' function by parsing the file as text.

    Args:
        file_path (str): Path to the Python file

    Returns:
        str: The docstring of the check function, or None if not found
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Look for the check function definition and its docstring
        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "check":
                if (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    return node.body[0].value.value
                # For older Python versions, check for ast.Str
                elif node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                    return node.body[0].value.s

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return None


def generate_checklist():
    """
    Generate the markdown checklist from all check files.

    Returns:
        str: Markdown formatted checklist
    """
    checks_dir = os.path.join(os.path.dirname(__file__), "operators", "checks")
    check_files = []

    # Get all Python files in the checks directory and subdirectories
    for root, dirs, files in os.walk(checks_dir):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                file_path = os.path.join(root, filename)
                # Get relative path from checks directory for better organization
                rel_path = os.path.relpath(file_path, checks_dir)
                check_files.append((rel_path, file_path))

    # Sort files alphabetically by their relative path
    check_files.sort(key=lambda x: x[0])

    checklist_lines = ["Checks:", ""]

    for rel_path, file_path in check_files:
        docstring = get_check_function_docstring(file_path)

        if docstring:
            # Clean up the docstring - take first line and remove extra whitespace
            description = docstring.strip().split("\n")[0].strip()
            checklist_lines.append(f"* [x] {description}")

    return "\n".join(checklist_lines)


def cleanup_excessive_linebreaks(content):
    """
    Remove sequences of more than two consecutive line breaks.

    Args:
        content (str): The content to clean up

    Returns:
        str: Content with excessive line breaks removed
    """
    # Replace 3 or more consecutive newlines with just 2
    return re.sub(r"\n{3,}", "\n\n", content)


def update_readme():
    """
    Update the README.md file with the generated checklist.
    """
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")

    # Read the current README
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Generate the new checklist
    new_checklist = generate_checklist()

    # Find the existing checklist section and replace it
    # Look for "Checks:" followed by any content until we hit "To do:" or another section
    pattern = r"(Checks:\s*\n(?:<!--.*?-->\s*\n)?)(.*?)(\n\nTo do:)"

    def replacement(match):
        prefix = match.group(1)
        suffix = match.group(3)
        # Add a blank line after the comment/header and before the checks
        return prefix + new_checklist[8:] + suffix  # Skip "Checks:\n\n" from new_checklist

    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # Clean up excessive line breaks
    updated_content = cleanup_excessive_linebreaks(updated_content)

    # Write the updated README
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    checklist_items = [l for l in new_checklist.split("\n") if l.startswith("* [x]")]
    print(f"README.md updated with {len(checklist_items)} checks")


if __name__ == "__main__":
    update_readme()
