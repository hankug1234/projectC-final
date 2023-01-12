package projectC.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import DTO.Client;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import projectC.service.BusinessModel;

@Controller
@RequestMapping("/log")
public class SignInController {
	
private BusinessModel bmodel;
private PasswordEncoder passwordEncoder;
	
	@Autowired
	public SignInController(BusinessModel bmodel,PasswordEncoder passwordEncoder) {
		this.bmodel = bmodel;
		this.passwordEncoder = passwordEncoder;
	}
	
	@GetMapping("/in")
	public String logIn2(HttpServletRequest request) {
		Object principal = SecurityContextHolder.getContext().getAuthentication().getPrincipal(); 
		Client userDetails = (Client)principal; 
		String username = userDetails.getUsername(); 
		bmodel.getSession(username, request);
		System.out.println(userDetails.getAuthorities());
		return "/home";
	}
	
	@PostMapping("/in")
	public String logIn(HttpServletRequest request,HttpServletResponse response,Client client) {
		String id = client.getUsername();
		String pw = client.getPassword();
		
		
		Client info = bmodel.getClientInfo(id);
		
		
		if(bmodel.isLogined(request)) {
			return "/home";
		}
		else if((info != null) && (passwordEncoder.matches(pw, info.getPassword()))) {
			bmodel.getSession(id, request);
			return "/home";
		}else {
			return "/signin";
		}
	}
	
	@GetMapping("/out")
	public String logOut(HttpServletRequest request,HttpServletResponse response) {
		bmodel.logOut(request);
		return "/home";
	}

}
