package projectC.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import projectC.service.BusinessModel;

@Controller
@RequestMapping("/video")
public class VideoController {
	
private BusinessModel bmodel;
	
	@Autowired
	public VideoController(BusinessModel bmodel) {
		this.bmodel = bmodel;
	}

}
