package DTO;


public class Video {
	private int id;
	private String videoName;
	private int fps;
	private int totalFrame;
	private int width;
	private int height;
	private int state;
	private String videoImage;
	
	public Video() {}
	
	public Video(int id, String videoName, int fps, int totalFrame, int width, int height, int state,String videoImage) {
		this.id = id;
		this.videoName = videoName;
		this.fps = fps;
		this.totalFrame = totalFrame;
		this.width = width;
		this.height = height;
		this.videoImage = videoImage;
		this.state = state;
	}
	
	public Video(int fps,int totalFrame,int width,int height) {
		this.fps = fps;
		this.totalFrame = totalFrame;
		this.width = width;
		this.height = height;
	}
	
	public Video(int id,String videoName) {
		this.id = id;
		this.videoName = videoName;
	}
	
	public Video(int id,String videoName,String videoImage,int totalFrame,int state) {
		this.id = id;
		this.videoName = videoName;
		this.videoImage = videoImage;
		this.totalFrame = totalFrame;
		this.state = state;
	}
	
	public Video(int id,String videoName,String videoImage,int state) {
		this.id = id;
		this.videoName = videoName;
		this.videoImage = videoImage;
		this.state = state;
	}
	
	public int getId() {return this.id;}
	public String getVideoName() {return this.videoName;}
	public int getFps() {return this.fps;}
	public int getTotalFrame(){return this.totalFrame;}
	public int getWidth() {return this.width;}
	public int getHeight() {return this.height;}
	public String getVideoImage() {return this.videoImage;}
	public int getState() {return this.state;}
	
	public void setId(int id) {this.id = id;}
	public void setVideoName(String videoName) {this.videoName = videoName;}
	public void setFps(int fps) {this.fps=fps;}
	public void setTotalFrame(int totalFrame){this.totalFrame = totalFrame;}
	public void setWidth(int width) {this.width = width;}
	public void setHeight(int height) {this.height = height;}
	public void setVideoImage(String videoImage) {this.videoImage = videoImage;}
	public void setState(int state) {this.state = state;}

}
