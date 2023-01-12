function analysis(Aurl,Purl,clientId,videoId){
	$.ajax ({
	  url	: Aurl, // 요청이 전송될 URL 주소
	  type	: "GET", // http 요청 방식 (default: ‘GET’)
	  async : true,  // 요청 시 동기화 여부. 기본은 비동기(asynchronous) 요청 (default: true)
	  cache : false,  // 캐시 여부
	  timeout : 30000, // 요청 제한 시간 안에 완료되지 않으면 요청을 취소하거나 error 콜백을 호출.(단위: ms)
	  data  : {"clientId" : clientId,"videoId":videoId}, // 요청 시 포함되어질 데이터
	  processData : true, // 데이터를 컨텐트 타입에 맞게 변환 여부
	  beforeSend  : function () {
	    // XHR Header를 포함해서 HTTP Request를 하기전에 호출됩니다.
	  },
	  success : function(data, status, xhr) {
		  $('#videos').load(location.href+' #videos');
		  getProgress(Purl,clientId,videoId);
	  },
	  error	: function(xhr, status, error) {
		  alert("analysis error occure");
	  },
	  complete : function(xhr, status) {
	  
	  }
	});
}



function getProgress(url,clientId,videoId){
	$.ajax ({
	  url	: url, // 요청이 전송될 URL 주소
	  type	: "GET", // http 요청 방식 (default: ‘GET’)
	  async : true,  // 요청 시 동기화 여부. 기본은 비동기(asynchronous) 요청 (default: true)
	  cache : false,  // 캐시 여부
	  timeout : 30000, // 요청 제한 시간 안에 완료되지 않으면 요청을 취소하거나 error 콜백을 호출.(단위: ms)
	  data  : {"clientId" : clientId,"videoId":videoId}, // 요청 시 포함되어질 데이터
	  processData : true, // 데이터를 컨텐트 타입에 맞게 변환 여부
	  contentType : "application/json", // 요청 컨텐트 타입 
	  dataType    : "json", // 응답 데이터 형식 (명시하지 않을 경우 자동으로 추측)
	  beforeSend  : function () {
	    // XHR Header를 포함해서 HTTP Request를 하기전에 호출됩니다.
	  },
	  success : function(data, status, xhr) {
		  type = data["type"];
		  if(type === "tracking-progress"){
			  document.getElementById(videoId).getElementsByClassName("tracking")[0].value=data["progress"]*100;
			  getProgress(url,clientId,videoId);
			  
			  
		  }else if(type === "labeling-progress"){
			   document.getElementById(videoId).getElementsByClassName("labeling")[0].value=data["progress"]*100;
			   getProgress(url,clientId,videoId);
			  
		  }else if(type === "done"){
			  $('#videos').load(location.href+' #videos');
		  }
	    
	  },
	  error	: function(xhr, status, error) {
		  alert("error occure "+status);
	        
	  },
	  complete : function(xhr, status) {
	  
	  }
	});
}

 
function uploadFile(url){
    
    var form = $('#upload')[0];
    var formData = new FormData(form);
 	
 	var header = $("meta[name='_csrf_header']").attr('content');
	var token = $("meta[name='_csrf']").attr('content');
 	
    $.ajax({
        url : url,
        type : 'POST',
        data : formData,
        contentType : false,
        processData : false,
        beforeSend: function(xhr){
        xhr.setRequestHeader(header, token);
    	},
        success : function(data, status, xhr) {
		$('#videos').load(location.href+' #videos');
		},
        error	: function(xhr, status, error) {alert("error occure "+error);}        
    });
}

function deleteFile(url,clientId,videoId){
    
    var header = $("meta[name='_csrf_header']").attr('content');
	var token = $("meta[name='_csrf']").attr('content');
    
    $.ajax({
        url : url,
        type : 'POST',
        data : {"clientId":clientId,"videoId":videoId},
        processData : true, // 데이터를 컨텐트 타입에 맞게 변환 여부
        beforeSend: function(xhr){
        xhr.setRequestHeader(header, token);
    	},
        success : function(data, status, xhr) {
		$('#videos').load(location.href+' #videos');
			
		},
        error	: function(xhr, status, error) {alert("error occure ");}        
    });
}
