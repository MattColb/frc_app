public class RecTest {
	public static void main(String[] args) {
		Rectangle r1 = new Rectangle(10, 2);
		Rectangle r2 = new Rectangle(70, 200);
		
		Rectangle rect = combineRectangles(r1, r2);
		System.out.println("The area of rect is: " + rect.getArea());
	}
	
	public static Rectangle combineRectangles(Rectangle rect1, Rectangle rect2) {
		double newLength = rect1.getLength() + rect2.getLength();
		double newWidth = rect1.getWidth() + rect2.getWidth();
		
		Rectangle rect = new Rectangle(newLength, newWidth);
		return rect;
	}
}
