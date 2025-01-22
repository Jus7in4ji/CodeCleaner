from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI()

def refactor_java_code(java_code):
    """
    Refactor Java code to rename non-meaningful variables, class names,
    and function names to meaningful ones based on context.
    """
    prompt = f"""
You are a code refactoring tool. Your task is to analyze the provided Java code and rename:
1. Variables to meaningful names based on their purpose.
2. Class names to something relevant to the program's functionality.
3. Function names to describe their behavior.

Do not hardcode specific names in the response; instead, infer meaningful names from the code's context.

Here is the Java code:
{java_code}

Return the updated code, and preserve the structure and indentation.
    """

    # Call the GPT model
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert in analyzing and refactoring Java code."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the content of the first choice
    return completion.choices[0].message.content

# Example Java code (replace this with any Java snippet you want to test)
java_code = """
class something {
    public static void main(String[] args) {
        System.out.println("Factorial of 5: " + func1(5));
        System.out.println("Concatenation of 'Hello' and 'World': " + func2("Hello", "World"));
    }

    public static int func1(int x) {
        // x represents a number for which factorial is calculated
        int result = 1;
        for (int i = 1; i <= x; i++) {
            result *= i;
        }
        return result;
    }

    public static String func2(String x, String y) {
        // x and y represent two strings to concatenate
        return x + " " + y;
    }
}

"""

# Call the refactor function
refactored_code = refactor_java_code(java_code)

# Print the updated code
print("Refactored Java Code:\n")
print(refactored_code)
