public class Counter {
	private int instanceCount;
	
	public Counter() {
		instanceCount = 0;
	}
	
	public void increment() {
		instanceCount++;
	}
	
	public int getCount() {
		return instanceCount;
	}
}
