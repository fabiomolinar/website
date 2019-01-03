var _aliTracker = (function(toast){
    toast.options = {
        "positionClass": "toast-bottom-center",
        "showDuration": "600"
    }
    let spinner = $("#results_spinner");
    let trackerForm = $("#form_request");
    let retryButton = $('#retry_button');
    let plotWrapper = $('#plotWrapper');
    window.onload = function(){
        spinner.removeClass("d-none");
        retryButton.addClass("d-none");
        plotWrapper.addClass("d-none");
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
        var tracesStandard = {
            x: x,
            mode: "lines",
            type: "scatter"
        }
        var markerStandard = {
            ...tracesStandard,
            marker: {color: "444"}
        }
        var markerLineStandard = {
            shape: "spline",
            dash: "dash"
        }
        var markerCStandard = {
            ...markerStandard,
            legendgroup: "Corrected",
            line: {
                ...markerLineStandard,
                color: "rgba(0,100,80,0.2)"
            }
        }
        var markerNcStandard = {
            ...markerStandard,
            legendgroup: "Non-corrected",
            line: {
                ...markerLineStandard,
                color: "rgba(0,176,246,0.2)"
            }
        }

        var trace1 = {
            ...markerCStandard,
            y: max,
            name: "Maximum price"
        };
        var trace2 = {
            ...tracesStandard,
            legendgroup: "Corrected",
            y: avr,
            line: {color: "rgb(0,100,80)"},
            name: "Corrected Median"
          };          
          var trace3 = {
            ...markerCStandard,
            y: min,
            name: "Minimum price"
          };
          var trace4 = {
            ...markerNcStandard,
            y: max_nc,
            name: "Maximum price"
        };
        var trace5 = {
            ...tracesStandard,
            legendgroup: "Non-corrected",
            y: avr_nc,
            line: {color: "rgb(0,176,246)"},
            name: "Non-corrected Median"
          };          
          var trace6 = {
            ...markerNcStandard,
            y: min_nc,
            name: "Minimum price"
          };
          var layout = {
            showlegend: true, 
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
            if (!data.data.count > 1){
                retryButton.removeClass("d-none");
                plotWrapper.addClass("d-none");
                toast.info("Our tracker returned zero results. Try again tomorrow.", "Ooops...");
            } else {
                retryButton.addClass("d-none");
                plotWrapper.removeClass("d-none");
                paintPlot(data);
            }            
        }).fail(function(jqXHR, textStatus, errorThrown){
            retryButton.removeClass("d-none");
            plotWrapper.addClass("d-none");
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