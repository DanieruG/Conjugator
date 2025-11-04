function getParams() {
    let params = new URLSearchParams(window.location.search)
    return {
        name: params.get('name')
    }
}

$(document).ready(function(){
    let data = getParams()
    let exerciseName = data.name

    $.getJSON("/user/fetch_details", function(exerciseData){
        let exercise = exerciseData["rightTable"][exerciseName]
        let questions = JSON.parse(exerciseData["rightTable"][exerciseName]["question_data"])
        let count = Number(questions["details"]["total"])

        $('#correct').html("<b>" + questions["details"]["correct"] + "</b>")
        $('#incorrect').html("<b>" + questions["details"]["wrong"] + "</b>")
        $('#totalQuestions').html(questions["details"]["total"])
        $('#minutes').html(questions["details"]["minutes"] + " minute(s)")
        $('#seconds').html(questions["details"]["seconds"] + " seconds")



        for (i = 1; i <= count; i++) {
            var row = '<tr>' + // This is for displaying the questions.
                        '<th scope="row">' + i + '</th>' +
                        '<td>' + questions[String(i)]["question"] + '</td>' +
                        '<td>' + questions[String(i)]["user_ans"] + '</td>' +
                        '<td>' + questions[String(i)]["answer"] + '</td>' +
                        '<td>' + "<b>" + questions[String(i)]["result"] + "</b>" + '</td>' +
                        '</tr>';
                $('#summaryTable').append(row);
        }
    })
})