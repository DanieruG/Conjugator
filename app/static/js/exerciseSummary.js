$(document).ready(function(){
    
    $.getJSON("/user/summary", function(data){
        $('#correct').html("<b>" + data["details"]["correct"] + "</b>")
        $('#incorrect').html("<b>" + data["details"]["wrong"] + "</b>")
        $('#totalQuestions').html(data["details"]["total"])
        $('#minutes').html(data["details"]["minutes"] + " minute(s)")
        $('#seconds').html(data["details"]["seconds"] + " seconds")

        var count = Number(data["details"]["total"]) // This is the total number of questions.
        for (var i = 1; i <= count; i++) {
            var row = '<tr>' +
                      '<th scope="row">' + i + '</th>' +
                      '<td>' + data[String(i)]["question"] + '</td>' +
                      '<td>' + data[String(i)]["user_ans"] + '</td>' +
                      '<td>' + data[String(i)]["answer"] + '</td>' +
                      '<td>' + "<b>" + data[String(i)]["result"] + "</b>" + '</td>' +
                      '</tr>';
            $('#summaryTable').append(row);
        }

    })
})