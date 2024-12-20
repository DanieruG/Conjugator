// event is an event object, which has attributes and methods, like a class
// In this case, it is handling the button press.
// How to adapt this to both the registration, and login pages?
// 1. Match element IDs.
// 2. Confirm password should be added.
// 3. Post method should be different.
import { emailValidate, passwordValidate } from "./reusableStack.js";

$(document).ready(function(){ // Prevents anything from happening on the page until its fully loaded.



    var formData = { // A JS object; stores multiple pieces of data in a compact format. useful for AJAX
        emailField: $('#emailField').val(),
        passField: $('#inputPassword').val() // #passField is the element ID in the JS code.
        // .val() fetches the value in that element.
     };


     // Actively checking for valid inputs, and adherance to formats.
     $('#emailField').on('input', function(){
        formData.emailField = $(this).val() // 'This' refers to the element with the ID that triggered the listening
        if (emailValidate(formData)){ // Toggles between valid and invalid messages.
            $('#emailField').removeClass('is-invalid')
            $('#emailField').addClass('is-valid')
        } else {
            $('#emailField').addClass('is-invalid')
            $('#emailField').removeClass('is-valid')
        }
     })

     $('#inputPassword').on('input', function(){
        formData.passField = $(this).val() // This ensures that the variable is being updated dynamically.
        if (passwordValidate(formData)){ // Toggles between valid and invalid messages.
            $('#inputPassword').removeClass('is-invalid')
            $('#inputPassword').addClass('is-valid')
        } else {
            $('#inputPassword').addClass('is-invalid')
            $('#inputPassword').removeClass('is-valid')
        }
     })

    
    $('#loginForm').submit(function(event){ // This looks out for a button with type submit to be pressed...
        event.preventDefault(); // This will prevent the page from reloading when the submit button is clicked...
        event.stopPropagation();

         var element = $('#loginForm') // To manipulate form div

         // Maybe the div should be disabled, then shown for each of them? it should keep looping? and go green
         if (emailValidate(formData) && passwordValidate(formData)) { // Text should only go red if wrong...


            $.post('/auth/login', formData, // Takes path, data, and function for status as parameters.
                function(status, textStatus, jqXHR) { // status is the response sent by the server, textStatus is a simple message stating what the request's outcome was.
                    if (jqXHR.status == 200) { // Looks out for the status code returned by flask.
                        $('#alertBox').html(
                            `<div class="alert alert-success" role="alert">
                                ${status}
                            </div>`
                        ); // This alert should be green, to indicate that the details have been received successfully.
                        setTimeout(() => {
                            window.location.href = "/user/dashboard";
                        }, 5000)
                    }
                }).fail(function(jqXHR) {
                    if (jqXHR.status == 401) {
                        $('#alertBox').html(
                            `<div class="alert alert-warning" role="alert">
                                ${jqXHR.responseText}
                            </div>`
                        )
                    }
                })}
    });
});


