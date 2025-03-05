import re

def remove_unreachable_code(code: str) -> str:
    lines = code.splitlines()
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

    return "\n".join(reachable_code)

def count_variable_references(code: str) -> dict:
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

def remove_unused_declarations(code: str, reference_counts: dict) -> str:
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

def clean_indentation(code: str, indent_size: int = 4) -> str:
    lines = code.splitlines()
    clean_lines = []
    indent_level = 0
    indent_space = ' ' * indent_size

    for line in lines:
        stripped_line = line.strip()
        
        if not stripped_line:
            clean_lines.append('')
            continue

        if stripped_line.startswith('}') or stripped_line.startswith(']'):
            indent_level -= 1

        clean_lines.append(indent_space * indent_level + stripped_line)

        if stripped_line.endswith('{') or stripped_line.endswith('['):
            indent_level += 1
    
    return "\n".join(clean_lines)

def process_and_format_code(java_code: str) -> str:
    cleaned_code = remove_unreachable_code(java_code)
    reference_counts = count_variable_references(cleaned_code)
    optimized_code = remove_unused_declarations(cleaned_code, reference_counts)
    formatted_code = clean_indentation(optimized_code)
    return formatted_code

# Example usage:
input_code = """
// SimpleCode3: Factorial calculation with inefficiencies
import java.util.Scanner;
class factorialcalc {
public static void main(String args[]) {
Scanner sc=new Scanner(System.in);
System.out.println("Enter a number:");
int num=sc.nextInt();
int fact=1;
// Unoptimized loop
for(int i=num;i>0;i--) fact*=i;
System.out.println("Factorial: "+fact);
// Dead Code
if(false) { System.out.println("This code never runs"); }
}
}
"""

output_code = process_and_format_code(input_code)
print("Cleaned Code:")
print(output_code)
