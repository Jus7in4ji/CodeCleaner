import re

def read_replacement_table(txt_file_path):
    replacements = {}
    with open(txt_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                old_name, new_name = parts
                replacements[old_name] = new_name
    return replacements

def replace_variables_in_code(java_code, replacements):
    """Replaces variable """
    for old_name, new_name in sorted(replacements.items(), key=lambda x: -len(x[0])):
        java_code = re.sub(r'\b' + re.escape(old_name) + r'\b', new_name, java_code)
    return java_code

def process_java_file(java_file_path, txt_file_path, output_file_path):

    replacements = read_replacement_table(txt_file_path)
    
    with open(java_file_path, 'r') as java_file:
        java_code = java_file.read()
    
    updated_java_code = replace_variables_in_code(java_code, replacements)
    
    with open(output_file_path, 'w') as output_file:
        output_file.write(updated_java_code)

    print(f"Updated Java code has been saved to {output_file_path}")

java_file_path = 'JavaFile2.java'   
txt_file_path = 'input2.txt'  
output_file_path = 'OpFile.java'  

process_java_file(java_file_path, txt_file_path, output_file_path)
