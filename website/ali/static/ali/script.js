var _ali = (function(toast){
    toast.options = {
        "positionClass": "toast-bottom-center",
        "showDuration": "600"
    }
    // HTML elements
    let spinner = $("#results_spinner");
    let searchForm = $("#form_request");
    let resultsWrapper = $("#resultsWrapper");
    let dataTable = $("#search-data-table");

    // results object
    var aliResults = (function(){
        var empty = true;
        var data = {};
        var tableComponents = {
            'min': dataTable.find("#min td"),
            'mean': dataTable.find("#mean td"),
            'avg': dataTable.find("#avg td"),
            'max': dataTable.find("#max td"),
            'std': dataTable.find("#std td"),
            'points': dataTable.find("#points td"),
            'results': dataTable.find("#results td")
        }
        var insertData = function(receivedData){
            data = receivedData;
            empty = false;
            let currency = data.currency;
            tableComponents.min[0].textContent = currency + " " + data.min_price.toFixed(2);
            tableComponents.min[1].textContent = currency + " " + data.min_price_nc.toFixed(2);
            tableComponents.min[2].textContent = currency + " " + (data.min_price_nc - data.min_price).toFixed(2);
            tableComponents.mean[0].textContent = currency + " " + data.median.toFixed(2);
            tableComponents.mean[1].textContent = currency + " " + data.median_nc.toFixed(2);
            tableComponents.mean[2].textContent = currency + " " + (data.median_nc - data.median).toFixed(2);
            tableComponents.avg[0].textContent = currency + " " + data.average.toFixed(2);
            tableComponents.avg[1].textContent = currency + " " + data.average_nc.toFixed(2);
            tableComponents.avg[2].textContent = currency + " " + (data.average_nc - data.average).toFixed(2);
            tableComponents.max[0].textContent = currency + " " + data.max_price.toFixed(2);
            tableComponents.max[1].textContent = currency + " " + data.max_price_nc.toFixed(2);
            tableComponents.max[2].textContent = currency + " " + (data.max_price_nc - data.max_price).toFixed(2);
            tableComponents.std[0].textContent = currency + " " + data.stddev.toFixed(2);
            tableComponents.std[1].textContent = currency + " " + data.stddev_nc.toFixed(2);
            tableComponents.std[2].textContent = currency + " " + (data.stddev_nc - data.stddev).toFixed(2);
            tableComponents.points[0].textContent = data.number_points;
            tableComponents.points[1].textContent = data.number_points_nc;
            tableComponents.points[2].textContent = data.number_points_nc - data.number_points;
            tableComponents.results[0].textContent = data.results;
            tableComponents.results[1].textContent = data.results;
            tableComponents.results[2].textContent = data.results - data.results;
        }
        var getData = function(){
            // copying array as value
            return $.extend(true,{},data);
        }
        var isEmpty = function(){
            return empty == true;
        }
        return {
            insertData: insertData,
            isEmpty: isEmpty,
            getData: getData
        }
    }());

    // form submition
    searchForm.submit(function(e){
        e.preventDefault();
        e.stopPropagation();
        searchForm.addClass("was-validated");
        if (!searchForm[0].checkValidity()){
            return;    
        }

        if (resultsWrapper.hasClass("d-none")){
            resultsWrapper.removeClass("d-none");
        }
        spinner.removeClass("d-none");
        dataTable.addClass("d-none");
        let formData = {
            'text': $('input[name=text]').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        }                

        $.ajax({
            type: 'POST',
            url: searchForm.attr("action"),
            data: formData,
            dataType: 'json',
            encode: true
        }).done(function(data, textStatus, jqXHR){
            if (typeof data.returned_empty == "boolean" && data.returned_empty == true){
                toast.info("Your search request returned no results. Check your spelling or try searching for something different.", "Ooops...");
            } else {
                aliResults.insertData(data);
                dataTable.removeClass("d-none");
            }
        }).fail(function(jqXHR, textStatus, errorThrown){
            let msg = "";
            if (typeof jqXHR.responseText == "string" && jqXHR.responseText != "" && jqXHR.responseText.length < 70){
                msg = jqXHR.responseText;
            } else {
                msg = errorThrown;
            }
            toast.warning(msg + " Try again in a few minutes. You may also try to check your internet connection.","Something went wrong...");
        }).always(function(data){
            spinner.addClass("d-none");
        });
    });
})(toastr);