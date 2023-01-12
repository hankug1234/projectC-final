package DTO;


public class ObjFrame {
	private int objectId;
	private int objectFrame;
	private int videoId;
	private int x1;
	private int x2;
	private int y1;
	private int y2;
	
	public ObjFrame() {}
	
	public ObjFrame(int objectId,int objectFrame,int videoId,int x1,int y1, int x2, int y2) {
		this.objectId = objectId;
		this.objectFrame = objectFrame;
		this.videoId = videoId;
		this.x1 = x1;
		this.y1 = y1;
		this.x2 = x2;
		this.y2 = y2;
	}
	
	public int getObjectId() {return this.objectId;}
	public int getObjectFrame() {return this.objectFrame;}
	public int getVideoId() {return this.videoId;}
	public int getX1() {return this.x1;}
	public int getX2() {return this.x2;}
	public int getY1() {return this.y1;}
	public int getY2() {return this.y2;}
	
	public void setObjectId(int objectId) {this.objectId = objectId;}
	public void setObjectFrame(int objectFrame) {this.objectFrame = objectFrame;}
	public void setVideoId(int videoId) {this.videoId = videoId;}
	public void setX1(int x1) {this.x1 = x1;}
	public void setX2(int x2) {this.x2 = x2;}
	public void setY1(int y1) {this.y1 = y1;}
	public void setY2(int y2) {this.y2 = y2;}

}
