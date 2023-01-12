package projectC.service;

import java.net.URI;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.util.UriComponentsBuilder;

import DTO.Client;
import DTO.Video;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

@Service
public class BusinessModel {
	
	private String host = "http://127.0.0.1:8085";
	
	public boolean isLogined(HttpServletRequest request) {
		HttpSession session = request.getSession(false);
		if(session.getAttribute("clientId") == null) {
			return false;
		}
		return true;
		
	}
	
	public void getSession(String clientId,HttpServletRequest request) {
		HttpSession session = request.getSession();
		session.setAttribute("clientId", clientId);
	}
	
	public void logOut(HttpServletRequest request) {
		HttpSession session = request.getSession(false);
		if(session != null) {
			session.invalidate();
		}
	}
	
	
	public JSONObject postApi(URI uri,MultiValueMap body) throws ParseException {
		JSONObject json = null;
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
		RestTemplate restTemplete = new RestTemplate();
		
		HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(body, headers);
		
		ResponseEntity<String> result = restTemplete.postForEntity(uri, request, String.class);
		System.out.println(result.getStatusCode());
        
        JSONParser jsonParser = new JSONParser();
        Object obj = jsonParser.parse(result.getBody());
        json = (JSONObject) obj;
        return json;

	}
	
	
	public JSONObject postMultipartApi(URI uri,MultiValueMap body) throws ParseException {
		JSONObject json = null;
		HttpHeaders headers = new HttpHeaders();
		headers.setContentType(MediaType.MULTIPART_FORM_DATA);
		RestTemplate restTemplete = new RestTemplate();
		
		HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(body, headers);
		
		ResponseEntity<String> result = restTemplete.postForEntity(uri, request, String.class);
		System.out.println(result.getStatusCode());
        
        JSONParser jsonParser = new JSONParser();
        Object obj = jsonParser.parse(result.getBody());
        json = (JSONObject) obj;
        return json;

	}
	
	
	public JSONObject getApi(URI uri) throws ParseException {
		JSONObject json = null;
		RestTemplate restTemplete = new RestTemplate();

        ResponseEntity<String> result = restTemplete.getForEntity(uri, String.class);
        System.out.println(result.getStatusCode());
        
        JSONParser jsonParser = new JSONParser();
        Object obj = jsonParser.parse(result.getBody());
        json = (JSONObject) obj;
        return json;
	}
	
	public JSONObject doAnalysis(String clientId,int videoId) {
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/analysis/execute/"+clientId+"/"+videoId)
                .encode()
                .build()
                .toUri();
		JSONObject jsonObj = new JSONObject();
		try {
			jsonObj =this.getApi(uri);
		}catch(ParseException e){
			
			e.printStackTrace();
		}
		return jsonObj;
		
	}
	
	public JSONObject deleteVideo(String clientId,int videoId) {
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/video/delete/"+clientId+"/"+videoId)
                .encode()
                .build()
                .toUri();
		JSONObject jsonObj = new JSONObject();
		try {
			jsonObj =this.getApi(uri);
		}catch(ParseException e){
			
			e.printStackTrace();
		}
		return jsonObj;
	}
	
	public JSONObject getProgress(String clientId, int videoId) {
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/analysis/progress/"+clientId+"/"+videoId)
                .encode()
                .build()
                .toUri();
		JSONObject jsonObj = new JSONObject();
		try {
			jsonObj =this.getApi(uri);
		}catch(ParseException e){
			
			e.printStackTrace();
		}
		return jsonObj;
	}
	
	public Client getClientInfo(String id) {
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/client/info/"+id)
                .encode()
                .build()
                .toUri();
		Client client = null;
		 try {
		        JSONObject jsonObj = this.getApi(uri);
		        boolean result = (boolean) jsonObj.get("result");
		        if(result) {
		        	String clientId = (String)jsonObj.get("clientId");
		        	String clientpw = (String)jsonObj.get("clientpw");
		        	client = new Client(clientId,clientpw);
		        }
		        
		        
		     }
		     catch(ParseException e) {
		        e.printStackTrace();
		     }
		     return client;
		
		
	}
	
	public boolean postClientInfo(String id,String pw) {
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/client/signUp")
                .encode()
                .build()
                .toUri();
		
		MultiValueMap<String,String> body = new LinkedMultiValueMap<>();
		body.add("clientId", id);
		body.add("clientPw", pw);
		
		try {
			JSONObject jsonObj =this.postApi(uri, body);
			return true;
		}catch(ParseException e){
			e.printStackTrace();
		}
		return false;
		
	}
	
	public JSONObject postFile(String clientId, MultipartFile file) {
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/video/file/"+clientId)
                .encode()
                .build()
                .toUri();
		JSONObject jsonObj = new JSONObject();
		MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
		body.add("file",file.getResource());
		
		try {
			jsonObj =this.postMultipartApi(uri, body);
			return jsonObj;
		}catch(ParseException e){
			e.printStackTrace();
		}
		return jsonObj;
		
	}
	
	public boolean canLogin(String id,String pw) {
		
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/client/signIn")
                .encode()
                .build()
                .toUri();
		
		MultiValueMap<String,String> body = new LinkedMultiValueMap<>();
		body.add("clientId", id);
		body.add("clientPw", pw);
		
		try {
			JSONObject jsonObj =this.postApi(uri, body);
			return Boolean.parseBoolean(jsonObj.get("result").toString());
		}catch(ParseException e){
			e.printStackTrace();
		}
		return false;
		
	}
	
	public JSONObject getObjectList(String clientId,int videoId,String types,String colors) {
		URI uri = UriComponentsBuilder
        .fromUriString(host)
        .path("/analysis/info/"+clientId+"/"+videoId)
        .encode()
        .build()
        .toUri();
		
		MultiValueMap<String,String> body = new LinkedMultiValueMap<>();
		body.add("types",types);
		body.add("colors", colors);
		JSONObject jsonObj = new JSONObject();
		try {
			jsonObj =this.postApi(uri, body);
	
		}catch(ParseException e){
			e.printStackTrace();
		}
		return jsonObj;
		
	}
	
	
	
	public List<Integer> getProgressList(String clientId){
		List<Integer> list = new LinkedList<>();
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/analysis/progress/"+clientId)
                .encode()
                .build()
                .toUri();
		
		 try {
		        JSONObject jsonObj = this.getApi(uri);
		        JSONArray progressList = (JSONArray) jsonObj.get("result");
		        for(int i=0;i<progressList.size();i++) {
		        	
		        	Long progress = (Long)progressList.get(i);
		        	list.add((Integer)progress.intValue());
		        }
		        
		     }
		     catch(ParseException e) {
		        e.printStackTrace();
		     }
		     return list;
	}
	
	public List<Video> getVideoList(String clientId) {
		List<Video> list = new LinkedList<>();
		URI uri = UriComponentsBuilder
                .fromUriString(host) //http://localhost에 호출
                .path("/video/list/"+clientId)
                .encode()
                .build()
                .toUri();
		
		 try {
		        JSONObject jsonObj = this.getApi(uri);
		        Iterator iter = jsonObj.keySet().iterator();
		        while(iter.hasNext()) {
		        	String key = (String)iter.next();
		        	JSONObject obj = (JSONObject)jsonObj.get(key);
		        	
		        	Double totalFrame = (Double) obj.get("totalFrame");
		        	int num = (int) totalFrame.doubleValue(); 
		        	
		        	Long state = (Long) obj.get("state");
		        	int num2 = state.intValue();
		        	
		        	
		        	list.add(new Video(Integer.parseInt(key),(String)obj.get("videoName"),(String)obj.get("image"),num,num2));
		        }
		        
		     }
		     catch(ParseException e) {
		        e.printStackTrace();
		     }
		     return list;
		
	}
	
	public List<Video> getVideos(String clientId){
		List<Video> videos = getVideoList(clientId);
		List<Integer> progressVideos = getProgressList(clientId);
		for(int progress : progressVideos) {
			for(Video video:videos) {
				if(video.getId() == progress) {
					video.setState(1);
				}
			}
		}
		return videos;
	}
	
	
	public boolean getDuplicatedResult(String clientId) {
		
		URI uri = UriComponentsBuilder
                .fromUriString(host) 
                .path("/client/signUp")
                .queryParam("clientId", clientId) 
                .encode()
                .build()
                .toUri();
		
        try {
        JSONObject jsonObj = this.getApi(uri);
        
        return Boolean.parseBoolean(jsonObj.get("result").toString());
        }
        catch(ParseException e) {
        	e.printStackTrace();
        }
        return false;

		
	}
	
}
