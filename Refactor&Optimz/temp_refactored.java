import java.util.Scanner;
public class ShowEg{
public static int main(String[] args) {
int n1 , n2;
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
repeatedBlock1(limit);
repeatedBlock1(limit);
scanner.close();
return 0;
}
}

public void repeatedBlock1(int limit) {
    System.out.println("Sum of even numbers up to " + val + ": " + n2);
    System.out.println("Sum of odd numbers up to " + val + ": " + n1);
}
