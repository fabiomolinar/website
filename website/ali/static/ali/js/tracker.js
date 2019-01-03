var _aliTracker = (function(toast){
    toast.options = {
        "positionClass": "toast-bottom-center",
        "showDuration": "600"
    }
    let spinner = $("#results_spinner");
    let trackerForm = $("#form_request");
    let retryButton = $('#retry_button');
    let plot = $('#plot');
    window.onload = function(){
        spinner.removeClass("d-none");
        retryButton.addClass("d-none");
        trackerForm.submit();
    }

    var paintPlot = function(data){
        var points = data.data.data
        var avr = [];
        var max = [];
        var min = [];
        var avr_nc = [];
        var max_nc = [];
        var min_nc = [];
        var x = [];
        for (let i = 0; i < points.length; i++){
            date = new Date(points[i].date_created);
            x.push(date);
            avr.push(points[i].median);
            min.push(points[i].min_price);
            max.push(points[i].max_price);
            avr_nc.push(points[i].median_nc);
            min_nc.push(points[i].min_price_nc);
            max_nc.push(points[i].max_price_nc);
        }
        var trace1 = {
            x: x,
            y: min,
            line: {width: 0}, 
            marker: {color: "444"}, 
            mode: "lines", 
            name: "Minimum price", 
            type: "scatter"
        };
        var trace2 = {
            x: x, 
            y: avr,
            fill: "tonexty", 
            fillcolor: "rgba(0,100,80,0.2)", 
            line: {color: "rgb(0,100,80)"}, 
            mode: "lines", 
            name: "Median", 
            type: "scatter"
          };          
          var trace3 = {
            x: x,
            y: max,
            fill: "tonexty", 
            fillcolor: "rgba(0,100,80,0.2)", 
            line: {width: 0}, 
            marker: {color: "444"}, 
            mode: "lines", 
            name: "Maximum price", 
            type: "scatter"
          };
          var trace4 = {
            x: x,
            y: min_nc,
            line: {width: 0}, 
            marker: {color: "444"}, 
            mode: "lines", 
            name: "Minimum price", 
            type: "scatter"
        };
        var trace5 = {
            x: x, 
            y: avr_nc,
            fill: "tonexty", 
            fillcolor: "rgba(0,100,80,0.2)", 
            line: {color: "rgb(0,176,246)"}, 
            mode: "lines", 
            name: "Median", 
            type: "scatter"
          };          
          var trace6 = {
            x: x,
            y: max_nc,
            fill: "tonexty", 
            fillcolor: "rgba(0,100,80,0.2)", 
            line: {width: 0}, 
            marker: {color: "444"}, 
            mode: "lines", 
            name: "Maximum price", 
            type: "scatter"
          };
          var layout = {
            showlegend: false, 
            title: "Tracker", 
            yaxis: {title: "Price"}
          };
          var config = {
              responsive: true
          }
          var traces = [trace1, trace2, trace3, trace4, trace5, trace6];
          Plotly.plot('plot', traces, layout, config);
    }

    trackerForm.submit(function(e){
        e.preventDefault();
        e.stopPropagation();
        spinner.removeClass("d-none");
        retryButton.addClass("d-none");

        let formData = {
            'search_text': $('input[name=search_text]').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        }

        $.ajax({
            type: 'POST',
            url: trackerForm.attr("action"),
            data: formData,
            dataType: 'json',
            encode: true
        }).done(function(data, textStatus, jqXHR){
            if (!data.data.count > 0){
                retryButton.removeClass("d-none");
                toast.info("Our tracker returned zero results. Try again tomorrow.", "Ooops...");
            } else {
                retryButton.addClass("d-none");
                paintPlot(data);
            }            
        }).fail(function(jqXHR, textStatus, errorThrown){
            retryButton.removeClass("d-none");
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

    retryButton.click(function(e){
        trackerForm.submit();
    });
})(toastr);