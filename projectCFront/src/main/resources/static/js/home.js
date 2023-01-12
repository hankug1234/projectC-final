let navUnderLine = document.getElementById("nav-underline");
let navMenus = document.querySelectorAll(".nav a");

navMenus.forEach(menu=>menu.addEventListener("mouseover",(e)=>horizontalIndicator(e)))

function horizontalIndicator(e){
    navUnderLine.style.left = e.currentTarget.offsetLeft + "px";
    navUnderLine.style.width = e.currentTarget.offsetWidth + "px";
    navUnderLine.style.top =
        e.currentTarget.offsetTop + e.currentTarget.offsetHeight + "px";
}