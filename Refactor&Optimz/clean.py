import re

def clean_indentation(code: str, indent_size: int = 4) -> str:
    """
    This function takes a code string and restructures its indentation.
    It removes extra spaces and makes the indentation consistent.

    :param code: The code content in string form (C/Java).
    :param indent_size: Number of spaces for indentation (default is 4).
    :return: Re-indented code string.
    """
    lines = code.splitlines()
    clean_lines = []
    indent_level = 0
    indent_space = ' ' * indent_size

    for line in lines:
        stripped_line = line.strip()

        # Skip empty lines
        if not stripped_line:
            clean_lines.append('')
            continue

        # Decrease indent level if line starts with a closing brace
        if stripped_line.startswith('}') or stripped_line.startswith(']'):
            indent_level -= 1

        # Apply the current indent level
        clean_lines.append(indent_space * indent_level + stripped_line)

        # Increase indent level if line ends with an opening brace
        if stripped_line.endswith('{') or stripped_line.endswith('['):
            indent_level += 1

    return "\n".join(clean_lines)


def format_code(file_path: str, output_path: str = None) -> None:
    """
    Reads the file, formats its indentation, and saves the output.

    :param file_path: Path to the C/Java code file.
    :param output_path: Where to save the formatted code. If not provided, overwrites the original file.
    """
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        formatted_code = clean_indentation(code)

        if output_path is None:
            output_path = file_path

        with open(output_path, 'w') as file:
            file.write(formatted_code)

        print(f"Formatted code saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")


# Usage example
file_path = 'C:\Code Cleaner\Refactor.java'  # or 'example.java'
format_code(file_path, output_path='C:\Code Cleaner\Cleaned_ShowEg.java')
