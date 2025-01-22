def find_and_refactor_repeated_blocks(code, function_prefix="repeatedBlock"):
    """
    Identifies and refactors repeated blocks of any size in Java code by replacing them
    with a function that encapsulates the repeated code block, using the line-by-line comparison logic.
    A repeated block is only refactored if the number of open and closed curly braces are equal.
    
    :param code: The input Java code as a string.
    :param function_prefix: The prefix used for naming new functions.
    :return: The refactored Java code with duplicate blocks replaced by function calls.
    """
    # Split code into lines and clean up whitespace, ignore blank lines
    lines = [line.strip() for line in code.split('\n') if line.strip()]
    
    # Initialize structures to track repeated blocks and their locations
    repeated_blocks = {}
    visited_lines = set()
    refactored_code = []
    function_definitions = []
    
    function_counter = 1
    
    # Helper function to check if a block has balanced braces
    def has_balanced_braces(block):
        open_braces = 0
        close_braces = 0
        for line in block:
            open_braces += line.count("{")
            close_braces += line.count("}")
        return open_braces == close_braces
    
    # Iterate over each line to find repeated blocks
    for i in range(len(lines)):
        if i in visited_lines:
            continue

        for j in range(i + 1, len(lines)):
            # Check if we already visited line j
            if j in visited_lines:
                continue
            
            block = []
            k = 0
            block_lines = set()  # Tracks which lines are in the current block

            # Keep checking consecutive lines until they don't match
            while (i + k < len(lines)) and (j + k < len(lines)) and (lines[i + k] == lines[j + k]):
                block.append(lines[i + k])
                block_lines.add(i + k)
                block_lines.add(j + k)
                k += 1

            # If a repeated block is found, check for balanced braces and add it to repeated_blocks
            block_tuple = tuple(block)
            if len(block) > 1 and block_tuple not in repeated_blocks:
                if has_balanced_braces(block):
                    function_name = f"{function_prefix}{function_counter}"
                    repeated_blocks[block_tuple] = function_name
                    
                    # Define the new function only for relevant repeated blocks
                    function_definitions.append(
                        f"public void {function_name}(int limit) {{\n" +
                        "\n".join([f"    {line}" for line in block]) +
                        "\n}\n"
                    )
                    
                    # Mark lines as visited
                    visited_lines.update(block_lines)
                    function_counter += 1

            # Exit the inner loop if a repeated block was identified
            if block:
                break

    # Generate the refactored code with function calls
    i = 0
    while i < len(lines):
        replaced = False
        for block_tuple, function_name in repeated_blocks.items():
            block_size = len(block_tuple)

            # If the current set of lines matches a block, replace it with a function call
            if tuple(lines[i:i + block_size]) == block_tuple:
                refactored_code.append(f"{function_name}(limit);")
                i += block_size
                replaced = True
                break
        
        if not replaced:
            refactored_code.append(lines[i])
            i += 1

    # Combine the refactored code with function definitions
    refactored_code_text = "\n".join(refactored_code) + "\n\n" + "\n".join(function_definitions)
    return refactored_code_text


# Example Java code (as a string)
java_code = """
import java.util.Scanner;

public class ClassExample {
public static void main(String[] args) {
int n1 , n2;
int unusedVar;
Scanner scanner = new Scanner(System.in);

System.out.print("Enter the limit: ");
int val = scanner.nextInt();

n1 = 0;
n2 = 0;
n1 = 0;
n2 = 0;
for (int i = 1; i <= val; i++) {
if (i % 2 == 0) {
n2 += i; 
} else {
n1 += i; 
}
}
System.out.println("Sum of even numbers up to " + val + ": " + n2);
System.out.println("Sum of odd numbers up to " + val + ": " + n1);
scanner.close();
}
}



"""

# Refactor the Java code
refactored_code = find_and_refactor_repeated_blocks(java_code)
print("Refactored Java Code:\n")
print(refactored_code)
