var _website = (function(){
    /** List of languages I expect to support */
    let langs = ['en','pt','en_US','pt_BR','pl','it'];
    /**
     * Checks if there is a language sub-directory in the URL path
     * @param {string} path - the URL path
     */
    let isLangActive = function(path){
       let pathComponents = path.split('/');
       if (langs.includes(pathComponents[1])){
           return true;
       }
       return false;
    }
    /**
     * Gets the first sub-directory of an URL path including the language sub-directory
     * @example
     * // returns "/pt/contact/"
     * getSubDirectory("/pt/contact/author/1");
     * @example
     * // returns "/contact/"
     * getSubDirectory("/contact/author/1");
     * @param {string} path - the URL path
     */
    let getSubDirectory = function(path){
        langActive = isLangActive(path)
        if (langActive){ 
            var lang = path.split("/")[1];
        }
        let subDir;
        subDir = langActive ? path.split("/")[2] : path.split("/")[1];
        subDir = typeof subDir == "undefined" ? "/" : subDir;
        subDir = subDir == "" ? "/" : subDir;
        if (subDir == "/"){
            return langActive == true ? "/" + lang + "/" : "/";
        }
        return langActive ? "/" + lang + "/" + subDir + "/" : "/" + subDir + "/";
    }
    /**
     * Marks the element of a menu list with the 'active' tag
     * @param {string} subDirectory - first sub-directory (including the language sub-directory) of an URL path
     * @param {string} htmlTagId - id of the HTML element where the list of items is contained
     */
    let paintHeader = function(subDirectory, htmlTagId){
        let list = document.getElementById(htmlTagId);
        let item = list.querySelector("a[href='" + subDirectory + "']");
        if (item){
            let parent = item.parentElement;
            parent.className = parent.className + " active";
        }        
    }
    return {
        paintHeader: paintHeader,
        getSubDirectory: getSubDirectory
    }
})();