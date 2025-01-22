def remove_unreachable_code(input_filename, output_filename):
    # Open and read the content of the input file
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # List to store the processed code without unreachable code
    reachable_code = []
    is_reachable = True  # Boolean flag to indicate if the current line is reachable

    # Iterate through each line in the code
    for line in lines:
        stripped_line = line.strip()  # Remove leading and trailing whitespace

        # Detect the start of a new method or block
        if stripped_line.endswith("{") and ("class " not in stripped_line):
            is_reachable = True  # Reset reachability at the start of each method

        # Check if the line contains an unconditional return statement
        if "return" in stripped_line and ";" in stripped_line:
            reachable_code.append(line)  # Add the return statement to reachable code
            is_reachable = False  # Mark subsequent lines as unreachable
            continue

        # If the line is a closing brace, always add it (even if it's after unreachable code)
        if stripped_line == "}":
            reachable_code.append(line)
            continue

        # If the line is reachable, add it to the reachable code list
        if is_reachable:
            reachable_code.append(line)

    # Write the modified code without unreachable sections to the output file
    with open(output_filename, 'w') as out_file:
        out_file.writelines(reachable_code)

    print(f"Unreachable code removed and saved to {output_filename}")

# Example usage
input_filename = "C:/Code Cleaner/Cleaned_ShowEg.java"  
output_filename = "C:/Code Cleaner/Unreachable.java"  # The file where modified code will be saved
remove_unreachable_code(input_filename, output_filename)