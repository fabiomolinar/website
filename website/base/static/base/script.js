var _website = (function(){
    window.onload = function(){
        paintHeader(getSubDirectory(window.location.pathname), "my-top-nav-list")
    }
    var getSubDirectory = function(path){
        path = path.split("/")[1];
        typeof path == "undefined" ? "/" : path;
        path == "" ? "/" : path;
        if(path != "/"){
            path = "/" + path;
        }
        return path;
    }
    var paintHeader = function(subDirectory, htmlTagId){
        let list = document.getElementById(htmlTagId);
        let item = list.querySelector("a[href='" + subDirectory + "']");
        if (item){
            let parent = item.parentElement;
            parent.className = parent.className + " active";
        }        
    }
})();