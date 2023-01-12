const canvas = document.querySelector('.canvas');
const ctx = canvas.getContext('2d');
let canPlayState = false;

ctx.textAlign = 'center';
ctx.fillText('비디오 로딩 중..', 300, 200);

const videoElem = document.getElementById("video");
videoElem.addEventListener('canplaythrough', render);

function render() {
ctx.drawImage(videoElem, 0, 0, 720, 400);
requestAnimationFrame(render);
}

function drawRect(x1,y1,x2,y2,ow,oh,nw,nh){
ratioW = nw/ow;
ratioH = nh/oh
ctx.beginPath();
ctx.lineWidth = "3";
ctx.strokeStyle = "red";
ctx.rect(x1*ratioW, y1*ratioH, (x2-x1)*ratioW, (y2-y1)*ratioH);
ctx.stroke();
}
