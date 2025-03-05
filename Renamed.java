Here is the refactored Java code with meaningful names based on the context provided:

```java
public class PrimeNumberFinder {
    public static void main(String[] args) {
        int primeCount = 0;
        for (int currentNumber = 2; currentNumber <= 50; currentNumber++) {
            boolean isCurrentNumberPrime = true;
            for (int divisor = 2; divisor <= Math.sqrt(currentNumber); divisor++) {
                if (currentNumber % divisor == 0) {
                    isCurrentNumberPrime = false;
                    break;
                }
            }
            
            if (isCurrentNumberPrime) {
                System.out.print(currentNumber + " ");
                primeCount++;
            }
        }
        System.out.println("\nTotal primes: " + primeCount);
    }
}
```

### Changes made:
1. **Class Name**: `PrimeNumbers` changed to `PrimeNumberFinder` to better reflect its functionality.
2. **Variable Names**:
   - `count` changed to `primeCount` for clarity on what it counts.
   - `num` changed to `currentNumber` to specify its role in the iteration.
   - `isPrime` changed to `isCurrentNumberPrime` for clarity on which number it refers to.
   - `i` changed to `divisor` to indicate its purpose as a divisor in prime checking.
3. **Function Names**: In this case, the functionality is within the `main` method, which maintains its standard naming for simplicity.

The structure and indentation of the original code have been preserved.