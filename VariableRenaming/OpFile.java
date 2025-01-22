public class ShowEg {
    public static void repeatedBlock1() {
        for (int i = 1; i <= Limit; i++) {
            System.out.println("Number: " + i+x);
        }
    }

    public static void DisplayNumberLimit(int Limit) {
        int x = 0;
        System.out.println("Displaying numbers from 1 to " + Limit + ":");
        repeatedBlock1();
        System.out.println("Counting down from " + Limit + " using a while loop:");
        while (Limit > 0) {
            System.out.println("Number: " + Limit);
            Limit--;
        }
        repeatedBlock1();
        return;
    }
}

