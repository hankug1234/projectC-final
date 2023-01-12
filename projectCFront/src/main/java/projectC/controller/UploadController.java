package projectC.controller;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import org.json.simple.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import DTO.Obj;
import DTO.Video;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import projectC.service.BusinessModel;

@Controller
@RequestMapping("file")
public class UploadController {
	
	
private BusinessModel bmodel;
private String host = "http://127.0.0.1:8085/";

	@Autowired
	public UploadController(BusinessModel bmodel) {
		this.bmodel = bmodel;
	}
	
	@GetMapping("/stream")
	public String stream(@RequestParam(value = "clientId")String clientId ,@RequestParam(value = "videoId")String videoId) {
		return"redirect:"+host+"videoPlay/video?clientId="+clientId+"&videoId="+videoId;
	}
	
	@GetMapping("/show")
	public String showVideo(@RequestParam(value = "videoId")int videoId,@RequestParam(value = "fps")int fps
			,@RequestParam(value = "totalFrame")int totalFrame,@RequestParam(value = "width")int width
			,@RequestParam(value = "height")int height,Model model,HttpServletRequest request){
		HttpSession session = request.getSession(false);
		String clientId = (String) session.getAttribute("clientId");
		
		model.addAttribute("videoInfo", new Video(fps,totalFrame,width,height));
		model.addAttribute("datas", new JSONObject());
		model.addAttribute("objectList", new LinkedList<Obj>());
		model.addAttribute("clientId", clientId);
		model.addAttribute("videoId", videoId);
		model.addAttribute("source","/file/stream");
		model.addAttribute("info","/file/info");
		return  "/infomation";
	}
	
	@PostMapping("/info")
	public String info(@RequestParam(value = "videoId")int videoId,@RequestParam(value = "types")LinkedList<String> types,@RequestParam(value = "colors")LinkedList<String> colors,Model model,HttpServletRequest request) {
		HttpSession session = request.getSession(false);
		String clientId = (String) session.getAttribute("clientId");
		StringBuffer stypes = new StringBuffer();
		StringBuffer scolors = new StringBuffer();
		
		for(String type : types) {
			stypes.append(type).append(",");
		}
		for(String color : colors) {
			scolors.append(color).append(",");
		}
		
		
		JSONObject obj = bmodel.getObjectList(clientId, videoId,stypes.toString(),scolors.toString());
		
		List<Obj> objectList = new LinkedList<>();
		
		try {
		JSONObject datas = (JSONObject)obj.get("datas");
		JSONObject videoInfo = (JSONObject)obj.get("info");
		int fps = (int) Math.round((double) videoInfo.get("fps"));
		int totalFrame = (int) Math.round((double) videoInfo.get("totalFrame"));
		int width = (int) Math.round((double) videoInfo.get("width"));
		int height = (int) Math.round((double) videoInfo.get("height"));
		
		Iterator iter = datas.keySet().iterator();
		while(iter.hasNext()) {
			String skey = (String)iter.next();
			int key = Integer.parseInt(skey);
			JSONObject target = (JSONObject)datas.get(skey);
			String className = (String)target.get("className");
			String classColor = (String)target.get("classColor");
			int startFrame = ((Long)target.get("startFrame")).intValue();
			int endFrame = ((Long)target.get("endFrame")).intValue();
			String image = (String)target.get("image");
			objectList.add(new Obj(key,className,classColor,startFrame,endFrame,image));
		}
		
		model.addAttribute("videoInfo", new Video(fps,totalFrame,width,height));
		model.addAttribute("datas", datas);
		model.addAttribute("objectList", objectList);
		model.addAttribute("clientId", clientId);
		model.addAttribute("videoId", videoId);
		model.addAttribute("info","/file/info");
		model.addAttribute("source","/file/stream");
		}catch(NullPointerException e) {
			JSONObject videoInfo = (JSONObject)obj.get("info");
			int fps = (int) Math.round((double) videoInfo.get("fps"));
			int totalFrame = (int) Math.round((double) videoInfo.get("totalFrame"));
			int width = (int) Math.round((double) videoInfo.get("width"));
			int height = (int) Math.round((double) videoInfo.get("height"));
			
			List<Obj> failList = new LinkedList<>();
			failList.add(new Obj(0,"please select condition!","please select condition!",0,0,""));
			
			model.addAttribute("videoInfo", new Video(fps,totalFrame,width,height));
			model.addAttribute("datas", "");
			model.addAttribute("objectList", failList);
			model.addAttribute("clientId", clientId);
			model.addAttribute("videoId", videoId);
			model.addAttribute("info","/file/info");
			model.addAttribute("source","/file/stream");
		}
		return "/infomation";
	}
	

}
