package DTO;

public class Obj {
	private int id;
	private String className;
	private String classColor;
	private int startFrame;
	private int endFrame;
	private double prob;
	private int videoId;
	private String image;
	
	public Obj() {}
	
	public Obj(int id,String className,String classColor,int startFrame,int endFrame, double prob, int videoId) {
		this.id = id;
		this.className = className;
		this.classColor = classColor;
		this.startFrame = startFrame;
		this.endFrame = endFrame;
		this.prob = prob;
		this.videoId = videoId;
				
	}
	
	public Obj(int id,String className,String classColor,int startFrame,int endFrame,String image) {
		this.id = id;
		this.className = className;
		this.classColor = classColor;
		this.startFrame = startFrame;
		this.endFrame = endFrame;
		this.image = image;
	}
	
	public int getId() {
		return this.id;
	}
	public String getClassName()
	{
		return this.className;
	}
	public String getClassColor() {
		return this.classColor;
	}
	public int getStartFrame() {
		return this.startFrame;
	}
	public int getEndFrame() {
		return this.endFrame;
	}
	public double getProb()
	{
		return this.prob;
	}
	public int getVideoId() {
		return this.videoId;
	}
	
	public String getImage() {
		return this.image;
	}
	
	public void setImage(String image) {
		this.image = image;
	}
	
	public void setId(int id) {
		this.id = id;
	}
	public void setClassName(String className)
	{
		this.className = className;
	}
	public void setClassColor(String classColor) {
		this.classColor = classColor;
	}
	public void setStartFrame(int startFrame) {
		this.startFrame = startFrame;
	}
	public void setEndFrame(int endFrame) {
		this.endFrame = endFrame;
	}
	public void setProb(double prob)
	{
		this.prob = prob;
	}
	public void setVideoId(int videoId) {
		this.videoId = videoId;
	}


}
