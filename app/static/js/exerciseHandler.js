$(document).ready(function(){
    var totalQuestions = 1
    var currentQuestion = 1 // Keeps track of the current question.
    var timer = new easytimer.Timer()
    var duration = 0
    var time_taken = {
        "minutes": 0,
        "seconds": 0
    }


    function answerTracker(num){ // Takes the number of questions as parameter.
        obj = {}
        for (let i = 1; i <= num; i++){
            obj[i] = "" // Creates a key-value pair for each question, with the key being the question number and the value being an empty string.
        }
        return obj
    }
 
    $.getJSON("/user/initialise", function(data){ 
        $('#verbText').html('<b>' + data.infinitive + '</b> - ' + data.translation)
        $('#pronounText').text("The pronoun is " + data.pronoun)
        $('#tenseText').text(data.mood + ' , ' + data.tense + ' tense')

        totalQuestions = data.count
        answers = answerTracker(totalQuestions)
        $('#questionCount').html('<b>Question ' + currentQuestion + '/' + totalQuestions + '</b>')

        duration = Number(data.duration) * 60
        timer.start({precision: 'seconds', startValues: {seconds: 0}, target: {seconds: duration}})

        $('#timer').html("<b>" + "Time remaining: " + timer.getTimeValues().toString() + "/" + duration / 60 + ":00" +  "</b>")
    
        timer.addEventListener('secondsUpdated', function(e){ 
            $('#timer').html("<b>" + "Time remaining: " + timer.getTimeValues().toString() + "/" + duration / 60 + ":00" +  "</b>")
            time_taken["minutes"] = timer.getTimeValues().minutes
            time_taken["seconds"] = timer.getTimeValues().seconds
        })

        timer.addEventListener('targetAchieved', function(e){ 
            alert("Time's up!")
            var merged_data = {...answers, ...time_taken}
            $.ajax({
                url: '/user/marking',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(merged_data),
                success: function(){
                    window.location.href = "/user/exercise_summary"
                }
            })
        })
    })


    $('#next').on("click", function(){ // Needs to become a POST
        answers[currentQuestion] = $('#textAnswer').val() // Saves the current input.
        $.getJSON("/user/next", function(data){
            $('#verbText').html('<b>' + data.infinitive + '</b> - ' + data.translation)
            $('#pronounText').text("The pronoun is " + data.pronoun)
            $('#tenseText').text(data.mood + ' , ' + data.tense + ' tense')
            currentQuestion = currentQuestion + 1
            $('#textAnswer').val(answers[currentQuestion]) // This will set the input field to the user's answer, if it exists.
            $('#questionCount').html('<b>Question ' + currentQuestion + '/' + totalQuestions + '</b>')
        }).fail(function(jqXHR){
            if (confirm("Would you like to submit the exercise?") == true){
                var merged_data = {...answers, ...time_taken}
                $.ajax({
                    url: '/user/marking',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(merged_data),
                    success: function(){
                        window.location.href = "/user/exercise_summary"
                    }
                })
                alert("Submitted!")
            } else {
                return
            }
        })
    })

    $('#previous').on("click", function(){
        answers[currentQuestion] = $('#textAnswer').val() // Saves the current input
        $.getJSON("/user/previous", function(data){
            $('#verbText').html('<b>' + data.infinitive + '</b> - ' + data.translation)
            $('#pronounText').text("The pronoun is " + data.pronoun)
            $('#tenseText').text(data.mood + ' , ' + data.tense + ' tense')
            currentQuestion = currentQuestion - 1
            $('#textAnswer').val(answers[currentQuestion]) // Sets the previous's current question to what the user inputted, if anything
            $('#questionCount').html('<b>Question ' + currentQuestion + '/' + totalQuestions + '</b>')
        }).fail(function(jqXHR){
            alert(jqXHR.responseText)
        })
    })

})