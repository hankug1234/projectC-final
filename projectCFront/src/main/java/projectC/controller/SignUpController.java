package projectC.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import DTO.Client;
import projectC.service.BusinessModel;




@Controller
@RequestMapping("/register")
public class SignUpController {
	
	private BusinessModel bmodel;
	private PasswordEncoder passwordEncoder;
	
	@Autowired
	public SignUpController(BusinessModel bmodel,PasswordEncoder passwordEncoder) {
		this.bmodel = bmodel;
		this.passwordEncoder = passwordEncoder;
	}
	

	@PostMapping
	public String processRegistration(Client client) {
		String id = client.getUsername();
		String pw = client.getPassword();
		String repw = client.getRepw();
		
		if((pw != null )&&(pw.equals(repw))) {
			if(bmodel.getDuplicatedResult(id)) {
				return "/signup";
			}else {
				pw = passwordEncoder.encode(pw);
				bmodel.postClientInfo(id,pw);
				return "/home";
			}
		}
				
		return "/signup";
	}
}
