var _aliTracker = (function(){
    let spinner = $("#results_spinner");
    let trackerForm = $("#form_request");
    window.onload = function(){
        spinner.removeClass("d-none");
        trackerForm.submit();
    }

    trackerForm.submit(function(e){
        e.preventDefault();
        e.stopPropagation();
        spinner.removeClass("d-none");

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

        }).fail(function(jqXHR, textStatus, errorThrown){

        }).always(function(data){
            spinner.addClass("d-none");
        });
    });
})();