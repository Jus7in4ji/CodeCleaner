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
public class PrimeNumbers {
    public static void main(String[] args) {
        int count = 0;
        for (int num = 2; num <= 50; num++) {
            boolean isPrime = true;
            for (int i = 2; i <= Math.sqrt(num); i++) {
                if (num % i == 0) {
                    isPrime = false;
                    break;
                }
            }
            
            if (isPrime) {
                System.out.print(num + " ");
                count++;
            }
        }
        System.out.println("\nTotal primes: " + count);
    }
}
"""

# Call the refactor function
refactored_code = refactor_java_code(java_code)

# Print the updated code
print("Refactored Java Code:\n")
print(refactored_code)

# Save the output to Rename.java
with open("Renamed.java", "w", encoding="utf-8") as file:
    file.write(refactored_code)

print("\nRefactored code has been saved to Rename.java")
