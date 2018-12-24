var _ali = (function(){
    // HTML elements
    let spinner = $("#results_spinner");
    let searchForm = $("#form_request");
    let resultsWrapper = $("#resultsWrapper");

    // results object
    var aliResults = (function(){
        var empty = true;
        var data = {};
        var insertData = function(receivedData){
            data = receivedData;
            empty = false;
        }
        var clearData = function(){
            data = {};
            empty = true;
            return true;
        }
        var getData = function(){
            return $.extend(true,{},data);
        }
        var isEmpty = function(){
            return empty == true;
        }
        return {
            insertData: insertData,
            isEmpty: isEmpty,
            getData: getData,
            clearData: clearData
        }
    }());

    // form submition
    searchForm.submit(function(e){
        e.preventDefault();
        if (resultsWrapper.hasClass("d-none")){
            resultsWrapper.removeClass("d-none");
        }
        aliResults.clearData();
        let formData = {
            'text': $('input[name=text]').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        }                
        spinner.removeClass("d-none");

        $.ajax({
            type: 'POST',
            url: searchForm.attr("action"),
            data: formData,
            dataType: 'json',
            encode: true
        }).done(function(data, textStatus, jqXHR){
            console.log(data);
        }).fail(function(jqXHR, textStatus, errorThrown){

        }).always(function(data){
            spinner.addClass("d-none");
        });
    });
})();