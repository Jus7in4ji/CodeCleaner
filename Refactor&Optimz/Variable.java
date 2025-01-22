import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.HashMap;
import java.util.ArrayList;
import java.util.List;

public class Variable {
    public static void main(String[] args) {
        // Sample Java code to analyze
        String code = """
public class ShowEg {
public static void func1(int n) {
int x = 0;
System.out.println("Displaying numbers from 1 to " + n + ":");
for (int i = 1; i <= n; i++) {
System.out.println("Number: " + i);
}
System.out.println("Counting down from " + n + " using a while loop:");
while (n > 0) {
System.out.println("Number: " + n);
n--;
}
for (int i = 1; i <= n; i++) {
System.out.println("Number: " + i);
}
return;
System.out.println(n);
}
}

        """;

        // Get the variable reference counts
        HashMap<String, Integer> referenceCounts = countVariableReferences(code);

        // Remove declarations with zero references and print modified code
        String modifiedCode = removeUnusedDeclarations(code, referenceCounts);
        System.out.println("Modified Code:");
        System.out.println(modifiedCode);
    }

    public static HashMap<String, Integer> countVariableReferences(String code) {
        // Define regex pattern for variable declarations
        String variablePattern = "\\b(int|double|String|boolean|char|float|long|short|byte|int\\[\\]|double\\[\\]|String\\[\\]|boolean\\[\\]|char\\[\\]|float\\[\\]|long\\[\\]|short\\[\\]|byte\\[\\])\\s+(\\w+)(\\s*=\\s*[^;]*)?;";
        
        Pattern declarationPattern = Pattern.compile(variablePattern);
        Matcher declarationMatcher = declarationPattern.matcher(code);

        ArrayList<String> variableNames = new ArrayList<>();
        HashMap<String, Integer> referenceCounts = new HashMap<>();

        // Find all variable declarations and initialize reference count
        while (declarationMatcher.find()) {
            String variableName = declarationMatcher.group(2); // Get variable name
            variableNames.add(variableName);
            referenceCounts.put(variableName, 0); // Initialize reference count to 0
        }

        // For each variable, count occurrences in the code after its declaration
        for (String variable : variableNames) {
            // Regex to match variable by name
            String referencePattern = "\\b" + variable + "\\b";
            Pattern usagePattern = Pattern.compile(referencePattern);
            Matcher usageMatcher = usagePattern.matcher(code);

            int count = 0;
            int firstOccurrence = -1;

            // Count each occurrence, excluding the first match (declaration itself)
            while (usageMatcher.find()) {
                if (firstOccurrence == -1) {
                    firstOccurrence = usageMatcher.start();
                } else {
                    count++;
                }
            }
            referenceCounts.put(variable, count);
        }

        return referenceCounts;
    }

    public static String removeUnusedDeclarations(String code, HashMap<String, Integer> referenceCounts) {
        // Split code into lines for easier manipulation
        String[] lines = code.split("\n");
        StringBuilder modifiedCode = new StringBuilder();

        // Define regex pattern for variable declarations
        String variablePattern = "\\b(int|double|String|boolean|char|float|long|short|byte|int\\[\\]|double\\[\\]|String\\[\\]|boolean\\[\\]|char\\[\\]|float\\[\\]|long\\[\\]|short\\[\\]|byte\\[\\])\\s+(\\w+)(\\s*=\\s*[^;]*)?;";
        Pattern declarationPattern = Pattern.compile(variablePattern);

        // Process each line and remove unused variable declarations
        for (String line : lines) {
            Matcher matcher = declarationPattern.matcher(line.trim());
            
            if (matcher.find()) {
                String variableName = matcher.group(2);

                // Check if the variable has zero references
                if (referenceCounts.get(variableName) != null && referenceCounts.get(variableName) == 0) {
                    continue; // Skip this line if it's an unused declaration
                }
            }
            
            // Append the line if it's not an unused declaration
            modifiedCode.append(line).append("\n");
        }

        return modifiedCode.toString();
    }
}
