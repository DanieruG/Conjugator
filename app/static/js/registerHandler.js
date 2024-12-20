import { emailValidate, passwordValidate } from "./reusableStack.js";

$(document).ready(function(){

    var formData = { // A JS object; stores multiple pieces of data in a compact format. useful for AJAX
        emailField: $('#emailField').val(),
        passField: $('#inputPassword').val(), // #passField is the element ID in the JS code.
        confirmPass: $('#confirmPassword').val()
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
        $('#confirmPassword').trigger('input'); // This is to check the confirm password field matches everytime.
     })

     $('#confirmPassword').on('input', function(){ // Checks matching password fields.
        formData.confirmPass = $(this).val()
        if (formData.confirmPass && formData.confirmPass ===  formData.passField){ // Checks whether confirmPass is actually filled...
            $('#confirmPassword').removeClass('is-invalid')
            $('#confirmPassword').addClass('is-valid')
        } else {
            $('#confirmPassword').addClass('is-invalid')
            $('#confirmPassword').removeClass('is-valid')
        }
     }) // this needs to block the submit from happening, if the condition is not met.

     $('#registerForm').submit(function(event){ // This looks out for a button with type submit to be pressed...
        event.preventDefault(); // This will prevent the page from reloading when the submit button is clicked...
        event.stopPropagation();

         var element = $('#registerForm') // To manipulate form div


         if (emailValidate(formData) && passwordValidate(formData)) { // Final check
            if(formData.confirmPass == formData.passField){
                $.post('/auth/register', formData, // Takes path, data, and function for status as parameters.
                    function(status, textStatus, jqXHR) { // status is the response sent by the server, textStatus is a simple message stating what the request's outcome was.
                        if (jqXHR.status == 200) { // Looks out for the status code returned by flask.
                            $('#alertBox').html(
                                `<div class="alert alert-success alert-dismissible fade show" role="alert">
                                    ${status}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>`
                            ); // This alert should be green, to indicate that the details have been received successfully.
                            setTimeout(() => { // Using an arrow function here...
                                window.location.href = "/auth/login";
                            }, 5000) // Redirect automatically to login page after 5 seconds.
                        }
                    }).fail(function(jqXHR) {
                        if (jqXHR.status == 400) {
                            $('#alertBox').html(
                                `<div class="alert alert-danger alert-dismissible fade show" role="alert">
                                    ${jqXHR.responseText}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                </div>`
                            )
                        }
                    })} else {
                        $('#alertBox').html(`
<div class="alert alert-danger alert-dismissible fade show" role="alert">
                              Passwords do not match.
  <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
  </button>
</div>`)
                    }} else {
                         $('#alertBox').html(`
<div class="alert alert-danger alert-dismissible fade show" role="alert">
                        Invalid email and/or password.
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
    </button>
</div>`)
                    }
    });
});