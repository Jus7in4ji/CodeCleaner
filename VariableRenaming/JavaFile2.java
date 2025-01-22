public class ShowEg {
    public static void repeatedBlock1() {
        for (int i = 1; i <= n; i++) {
            System.out.println("Number: " + i+x);
        }
    }

    public static void func1(int n) {
        int x = 0;
        System.out.println("Displaying numbers from 1 to " + n + ":");
        repeatedBlock1();
        System.out.println("Counting down from " + n + " using a while loop:");
        while (n > 0) {
            System.out.println("Number: " + n);
            n--;
        }
        repeatedBlock1();
        return;
    }
}

