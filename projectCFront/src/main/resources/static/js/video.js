var video = document.getElementById("video");
var seekBar = document.getElementById("seekslider");
function setVideo(event){
    var start = event.target.getElementsByClassName("start")[0].value;
    var end = event.target.getElementsByClassName("end")[0].value;
    var id = event.target.getElementsByClassName("id")[0].value;
    var video = document.getElementById("video");
    var time =  start*(1/fps);
    video.currentTime = time;

    function renderRect(){
    currentFrame = videoElem.currentTime*fps;
    ctx.drawImage(videoElem, 0, 0, 720, 400);
    if(currentFrame <= end && currentFrame >= start){
		try{
			loca = datas[id]["frameData"][parseInt(currentFrame)];
    drawRect(parseInt(loca["x1"]),parseInt(loca["y1"]),parseInt(loca["x2"]),parseInt(loca["y2"]),width,height,720,400);
    }catch(e){
		console.log(e);
	}
    }
    requestAnimationFrame(renderRect);
    }

    video.addEventListener('canplaythrough', renderRect);
}

function seekTimeUpdate(){
    var nt = (video.currentTime * seekBar.max)/video.duration;
    seekBar.value = nt;
}

function vidSeek(){
    var seekto = video.duration *(seekBar.value/seekBar.max);
    video.currentTime = seekto;

}


function playPause(btn,vid){
var vid = document.getElementById(vid);
    if(vid.paused){
        vid.play();
        btn.innerHTML = "Pause";
    }else{
        vid.pause();
        btn.innerHTML = "Play";
    }
}

var items = document.getElementsByName("item");
for(var i=0; i<items.length; i++){
    items[i].onclick = setVideo;
}
seekBar.addEventListener("change",vidSeek,false);
video.addEventListener("timeupdate",seekTimeUpdate,false);


