window.onload = function(){
    let path = window.location.pathname.replace(/\/$/, "")
    let list = document.getElementById("my-top-nav-list")
    for(i = 0; i < list.childElementCount; i++){
        if(list.children[i].getElementsByTagName("a")[0].pathname.startsWith(path)){
            list.children[i].className = list.children[i].className + " active"
        }
    }
}