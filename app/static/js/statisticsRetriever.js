$(document).ready(function(){ 

    $.getJSON("/user/fetch_details", function(data){

        // LEFT TABLE //
        $("#totalExercises").text(data["leftTable"]["exerciseCount"])
        $("#totalCorrect").text(data["leftTable"]["totalCorrect"])
        $("#totalIncorrect").text(data["leftTable"]["totalIncorrect"])

        time_spent = data["leftTable"]["totalTime"]
        let minutes = Math.floor(time_spent / 60);
        let seconds = time_spent % 60
        $("#totalTime").text(minutes + "m " + seconds + "s");
        console.log(data)

        $("#Correctness").text(Math.round(data["leftTable"]["rateCorrect"]) + "%")
        $("#Incorrectness").text(Math.round(data["leftTable"]["rateIncorrect"]) + "%")
        $("#bestExercise").html(`<a href="/user/exercise_recall?name=${encodeURIComponent(data["leftTable"]["bestExercise"])}">${data["leftTable"]["bestExercise"]}</a>`)
        $("#worstExercise").html(`<a href="/user/exercise_recall?name=${encodeURIComponent(data["leftTable"]["worstExercise"])}">${data["leftTable"]["worstExercise"]}</a>`)

        // RIGHT TABLE //
        tableBody = $("#exercisesTable")
        for (let key in data["rightTable"]) {
            let exerciseLink = `<a href="/user/exercise_recall?name=${encodeURIComponent(key)}">${key}</a>`;
            row = `
            <tr>
                <td scope="row">${exerciseLink}</td>
                <td>${data["rightTable"][key]["timestamp"]}</td>
            </tr>
            `
            tableBody.append(row)
        }







    })

})