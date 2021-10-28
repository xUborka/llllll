function worker() {
    var str_input = $("#parsed_url").text();
    console.log(str_input);
    $.get('/progress/' + str_input, function(data) {
        console.log(data["status"]);
        if (data["status_message"] != 'Done!') {
            $("#bar").attr("aria-valuenow", data["status"]);
            $("#bar").css("width", data["status"] + "%");
            $("#currently_parsing").text(data["message"]);
            setTimeout(worker, 1500)
        }
    })
}

function loading() {
    $("#loading").show();
    $("#loading_text").show();
    $("#form").hide();
    $("#loading_url").text($("#exampleInputEmail").val());
}

function runPageAnalysis(){
    $("#page_content").hide();
    $("#loading").hide();
    $("#loading_text").hide();
    $("#loading_bar").show();
    $("#loading_text_bar").show();
    setTimeout(worker, 1500);
}

function rerunLoading(){
    $("#loading_url").text($("#parsed_url").text())
    $("#page_content").hide();
    $("#loading").show();
    $("#loading_text").show();
}
