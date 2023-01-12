package projectC.controller;

import java.util.LinkedList;
import java.util.List;

import org.json.simple.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import DTO.Video;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import projectC.service.BusinessModel;

@Controller
public class MainController {
	
private BusinessModel bmodel;
	
	@Autowired
	public MainController(BusinessModel bmodel) {
		this.bmodel = bmodel;
	}
	
	@GetMapping("/")
	public String home() {
		return "/home";
	}
	
	@GetMapping("/signin")
	public String signin() {
		return "/signin";
	}
	
	@GetMapping("/signup")
	public String signup() {
		return "/signup";
	}
	
	
	@GetMapping("/repository")
	public String repogitory(Model model,HttpServletRequest request) {
		HttpSession session = request.getSession(false);
		String clientId = (String) session.getAttribute("clientId");
		List<Video> list = bmodel.getVideos(clientId);
		model.addAttribute("videos", list);
		model.addAttribute("file", "/file");
		model.addAttribute("delete","/delete");
		model.addAttribute("analysis", "/analysis");
		model.addAttribute("information", "/file/show");
		model.addAttribute("progress","/progress");
		return "/repository";
	}
	
	@PostMapping("/file")
	public void file(HttpServletResponse response,@RequestParam(value = "clientId")String clientId, @RequestParam MultipartFile file) {
		
		JSONObject result = bmodel.postFile(clientId, file);
		try {
			response.getWriter().print(result);
		}catch(Exception e) {
			e.printStackTrace();
		}
		
	}
	
	@GetMapping("/progress")
	public void progress(HttpServletResponse response ,@RequestParam(value = "clientId")String clientId,@RequestParam(value = "videoId")int videoId) {
		JSONObject result = bmodel.getProgress(clientId, videoId);
		try {
			response.getWriter().print(result);
		}catch(Exception e) {
			e.printStackTrace();
		}
		
	}
	
	@GetMapping("/analysis")
	public void analysis(HttpServletResponse response ,@RequestParam(value = "clientId")String clientId,@RequestParam(value = "videoId")int videoId) {
		JSONObject result = bmodel.doAnalysis(clientId, videoId);
		try {
			response.getWriter().print(result);
		}catch(Exception e) {
			e.printStackTrace();
		}
		
	}
	
	
	@PostMapping("/delete")
	public void delete(HttpServletResponse response ,@RequestParam(value = "clientId")String clientId,@RequestParam(value = "videoId")int videoId) {
		JSONObject result = bmodel.deleteVideo(clientId, videoId);
		try {
			response.getWriter().print(result);
		}catch(Exception e) {
			e.printStackTrace();
		}
		
	}
	
	
	@GetMapping("/infomation")
	public String infomation() {
		return "/infomation";
	}
	

}
