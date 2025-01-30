import re

# --- Optimization: Remove Unreachable Code ---
def remove_unreachable_code(input_filename, temp_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    reachable_code = []
    scope_stack = []  # Stack to track nested scopes
    is_reachable = [True]  # Stack-based reachability tracking

    for line in lines:
        stripped_line = line.strip()

        if "{" in stripped_line:
            scope_stack.append("{")
            is_reachable.append(is_reachable[-1])

        if "return" in stripped_line and ";" in stripped_line and is_reachable[-1]:
            reachable_code.append(line)
            is_reachable[-1] = False
            continue

        if "}" in stripped_line and scope_stack:
            scope_stack.pop()
            is_reachable.pop()

        if is_reachable[-1]:
            reachable_code.append(line)

    with open(temp_filename, 'w') as out_file:
        out_file.writelines(reachable_code)

    print(f"Unreachable code removed and saved to {temp_filename}")

# --- Optimization: Remove Unused Variable Declarations ---
def count_variable_references(code):
    variable_pattern = r"\b(int|double|String|boolean|char|float|long|short|byte|int\[\]|double\[\]|String\[\]|boolean\[\]|char\[\]|float\[\]|long\[\]|short\[\]|byte\[\])\s+(\w+)(\s*=\s*[^;]*)?;"
    
    declaration_pattern = re.compile(variable_pattern)
    variable_names = []
    reference_counts = {}
    
    for match in declaration_pattern.finditer(code):
        variable_name = match.group(2)
        variable_names.append(variable_name)
        reference_counts[variable_name] = 0
    
    for variable in variable_names:
        reference_pattern = rf"\b{variable}\b"
        count = len(re.findall(reference_pattern, code)) - 1
        reference_counts[variable] = max(0, count)
    
    return reference_counts

def remove_unused_declarations(code, reference_counts):
    lines = code.split("\n")
    modified_code = []
    
    variable_pattern = r"\b(int|double|String|boolean|char|float|long|short|byte|int\[\]|double\[\]|String\[\]|boolean\[\]|char\[\]|float\[\]|long\[\]|short\[\]|byte\[\])\s+(\w+)(\s*=\s*[^;]*)?;"
    declaration_pattern = re.compile(variable_pattern)
    
    for line in lines:
        match = declaration_pattern.match(line.strip())
        if match:
            variable_name = match.group(2)
            if reference_counts.get(variable_name, 1) == 0:
                continue
        modified_code.append(line)
    
    return "\n".join(modified_code)

# --- Refactoring: Find and Refactor Repeated Blocks ---
def find_and_refactor_repeated_blocks(input_file, output_file, function_prefix="repeatedBlock"):
    with open(input_file, "r") as file:
        code = file.read()
    
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    repeated_blocks = {}
    visited_lines = set()
    refactored_code = []
    function_definitions = []
    function_counter = 1
    variable_types = {}  # Stores {variable_name: data_type}

    def has_balanced_braces(block):
        open_braces = sum(line.count("{") for line in block)
        close_braces = sum(line.count("}") for line in block)
        return open_braces == close_braces
    
    def extract_variables(block):
        variable_pattern = re.compile(r"\b(\w+)\b(?!\s*\()")  # Exclude words followed by '(' (function calls)
        variables = set()
        keywords = {"if", "else", "for", "while", "return", "public", "private", "static", "void"}

        for line in block:
            for match in variable_pattern.findall(line):
                if not match.isnumeric() and match not in keywords:
                    variables.add(match)

        return list(variables)

    # Track Variable Declarations
    declaration_pattern = re.compile(r"\b(int|double|String|boolean|char|float|long|short|byte)\s+(\w+)")
    for line in lines:
        matches = declaration_pattern.findall(line)
        for data_type, var_name in matches:
            variable_types[var_name] = data_type  # Store variable and its type

    for i in range(len(lines)):
        if i in visited_lines:
            continue
        
        for j in range(i + 1, len(lines)):
            if j in visited_lines:
                continue
            
            block = []
            k = 0
            block_lines = set()
            
            while (i + k < len(lines)) and (j + k < len(lines)) and (lines[i + k] == lines[j + k]):
                block.append(lines[i + k])
                block_lines.add(i + k)
                block_lines.add(j + k)
                k += 1
            
            block_tuple = tuple(block)
            if len(block) > 1 and block_tuple not in repeated_blocks:
                if has_balanced_braces(block):
                    function_name = f"{function_prefix}{function_counter}"
                    variables = extract_variables(block)

                    # Add Data Types to Function Parameters
                    typed_params = []
                    for var in variables:
                        data_type = variable_types.get(var, "int")  # Default to int if type not found
                        typed_params.append(f"{data_type} {var}")

                    param_list = ", ".join(typed_params)
                    repeated_blocks[block_tuple] = (function_name, param_list)

                    # Add static keyword to the function definition
                    function_definitions.append(
                        f"    public static void {function_name}({param_list}) {{\n" +
                        "\n".join([f"        {line}" for line in block]) +
                        "\n    }\n"
                    )
                    visited_lines.update(block_lines)
                    function_counter += 1
            
            if block:
                break
    
    # Refactor the code and insert function calls
    i = 0
    while i < len(lines):
        replaced = False
        for block_tuple, (function_name, param_list) in repeated_blocks.items():
            block_size = len(block_tuple)
            if tuple(lines[i:i + block_size]) == block_tuple:
                # Function call with only variable names, no data types
                refactored_code.append(f"        {function_name}({', '.join(extract_variables(block_tuple))});")
                i += block_size
                replaced = True
                break
        
        if not replaced:
            refactored_code.append(lines[i])
            i += 1

    # Find the location of the main function and insert the repeated functions before it
    class_code = "\n".join(refactored_code)
    main_start = class_code.find("public static void main")
    refactored_class_code = class_code[:main_start] + "\n\n" + "\n".join(function_definitions) + "\n\n" + class_code[main_start:]
    
    # Write the refactored code to the output file
    with open(output_file, "w") as file:
        file.write(refactored_class_code)
    
    print(f"Refactored Java Code saved to {output_file}")

# --- Formatting: Clean Indentation ---
def clean_indentation(code: str, indent_size: int = 4) -> str:
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

# --- Process Flow ---
def process_and_optimize_code(input_filename, output_filename):
    temp_file_1 = "temp_unreachable.java"
    temp_file_2 = "temp_optimized.java"
    temp_file_3 = "temp_refactored.java"
    
    # Step 1: Remove unreachable code
    remove_unreachable_code(input_filename, temp_file_1)
    
    with open(temp_file_1, "r") as file:
        java_code = file.read()
    
    # Step 2: Remove unused variable declarations
    reference_counts = count_variable_references(java_code)
    optimized_code = remove_unused_declarations(java_code, reference_counts)
    
    with open(temp_file_2, "w") as file:
        file.write(optimized_code)
    
    # Step 3: Refactor repeated blocks
    find_and_refactor_repeated_blocks(temp_file_2, temp_file_3)
    
    # Step 4: Clean indentation
    format_code(temp_file_3, output_filename)

    print(f"Final cleaned and formatted Java code saved to {output_filename}")

# Example usage
input_filename = "C:/Code Cleaner/ShowEg.java"
output_filename = "C:/Code Cleaner/RefactorAndCleaned_ShowEg.java"
process_and_optimize_code(input_filename, output_filename)
