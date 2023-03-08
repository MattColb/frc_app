public class CounterTester {
	public static void main(String[] args) {
		Counter x = new Counter();
		Counter y = new Counter();
		
		x.increment();
		y.increment();
		y.increment();
		y.increment();
		
		System.out.println("The count for x is: " + x.getCount());
		System.out.println("The count for y is: " + y.getCount());
	}
}