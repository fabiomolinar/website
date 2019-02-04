var _aliSearch = (function(toast){
    toast.options = {
        "positionClass": "toast-bottom-center",
        "showDuration": "600"
    }
    // HTML elements
    let spinner = $("#results_spinner");
    let searchForm = $("#form_request");
    let resultsWrapper = $("#resultsWrapper");
    let plotWrapper = $('#plotWrapper');
    let usernameSpan = $('#plotWrapper h3 span');

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
        plotWrapper.addClass("d-none");
        let formData = {
            'text': $('input[name=text]').val(),
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        }
        gtag('event', 'mentions', {
            'event_category': 'twitter',
            'event_label': formData.text
        });

        var timeBeginning = new Date();
        $.ajax({
            type: 'POST',
            url: searchForm.attr("action"),
            data: formData,
            dataType: 'json',
            encode: true
        }).done(function(data, textStatus, jqXHR){
            paintPlot(data.data, formData.text);
            plotWrapper.removeClass("d-none");
            searchForm.removeClass("was-validated");
        }).fail(function(jqXHR, textStatus, errorThrown){
            plotWrapper.addClass("d-none");
            let msg = "";
            if (typeof jqXHR.responseText == "string" && jqXHR.responseText != "" && jqXHR.responseText.length < 70){
                toast.warning(jqXHR.responseText,"Something went wrong...");
            } else {
                toast.warning(errorThrown + " Try again in a few minutes. You may also try to check your internet connection.","Something went wrong...");
            }
        }).always(function(data){
            spinner.addClass("d-none");
            var timeEnd = new Date();
            gtag('event', 'timing_complete', {
                'name' : 'mentions',
                'value' : timeEnd.getTime() - timeBeginning.getTime(),
                'event_category' : 'twitter'
            });
        });
    });

    var noMentions = function(){
        resultsWrapper.addClass("d-none");
        toast.info("This user didn't mention anybody on its tweets.","No mentions found");
    };

    var paintPlot = function(data, AccountName){
        // A tweet object can be a original tweet, an answer to a tweet, a quoted tweet or a retweet
        // Don't count retweets
        let mentions = {};
        for (let i = 0; i < data.length; i++) {
            const e = data[i];
            if (e.retweeted){
                continue;
            }
            if (e.in_reply_to_user_id == null){
                for (let i2 = 0; i2 < e.entities.user_mentions.length; i2++) {
                    const e2 = e.entities.user_mentions[i2];
                    let name = e2.screen_name;
                    if (name == AccountName){continue;}
                    if (mentions[name] == undefined) {
                        mentions[name] = {"main": 1, "total": 1};
                    } else if (mentions[name]["main"] == undefined){
                        mentions[name]["main"] = 1;
                        mentions[name]["total"] = mentions[name]["total"] + 1;
                    } else {
                        mentions[name]["main"] = mentions[name]["main"] + 1;  
                        mentions[name]["total"] = mentions[name]["total"] + 1;                      
                    } 
                }
            } else {
                for (let i2 = 0; i2 < e.entities.user_mentions.length; i2++) {
                    const e2 = e.entities.user_mentions[i2];
                    let name = e2.screen_name;
                    if (name == AccountName){continue;}
                    if (mentions[name] == undefined) {
                        mentions[name] = {"answers": 1, "total": 1};
                    } else if (mentions[name]["answers"] == undefined){
                        mentions[name]["answers"] = 1;
                        mentions[name]["total"] = mentions[name]["total"] + 1;
                    } else {
                        mentions[name]["answers"] = mentions[name]["answers"] + 1;
                        mentions[name]["total"] = mentions[name]["total"] + 1;
                    }                    
                }
            }
        }
        let results = Object.keys(mentions).map(function(key){
            let xM = mentions[key]["main"] == undefined ? 0 : mentions[key]["main"]
            let xA = mentions[key]["answers"] == undefined ? 0 : mentions[key]["answers"]
            let xT = mentions[key]["total"]
            let y = key
            return [key,xM, xA, xT]
        });
        if (results.length == 0){
            noMentions();
            return
        }
        usernameSpan.text(AccountName);
        results.sort(function(a,b){
            return (a[3] < b[3]) ? 1 : -1;
        });
        top10Results = results.slice(0,10);
        otherResults = results.slice(10,results.length).reduce((a,c) => ["others",a[1] + c[1], a[2] + c[2], a[3] + c[3]]);
        top10Results.push(otherResults);
        var trace1 = {
            x: top10Results.map(x => x[1]).reverse(),
            y: top10Results.map(x => x[0]).reverse(),
            name: 'Main',
            orientation: 'h',
            marker: {
                color: 'rgba(55,128,191,0.6)',
                width: 1
            },
            type: 'bar'
        };
        var trace2 = {
            x: top10Results.map(x => x[2]).reverse(),
            y: top10Results.map(x => x[0]).reverse(),
            name: 'Answers',
            orientation: 'h',
            marker: {
                color: 'rgba(255,153,51,0.6)',
                width: 1
            },
            type: 'bar'
        };
        var data = [trace1, trace2];
        var layout = {
            barmode: 'stack'
        };
        Plotly.react('plot', data, layout);
    }
})(toastr);