import { emailValidate, passwordValidate } from "./reusableStack.js";

$(document).ready(function(){
    var formData = {
        emailField: '',
        newPasswordField: '',
        currentPasswordField: ''
    }

    $('#showPassword').on('change', function(){
        if ($(this).prop("checked")){
            $('#newPassword').attr("type", "text")
            $('#inputPassword').attr("type", "text")
        } else {
            $('#newPassword').attr("type", "password")
            $('#inputPassword').attr("type", "password")
        }
    })

    // Dynamic valdiation for the new email field.
    $('#emailField').on('input', function(){
        formData.emailField = $(this).val() // 'This' refers to the element with the ID that triggered the event
        if (emailValidate(formData.emailField)){ // Toggles between valid and invalid messages.
            $('#emailField').removeClass('is-invalid')
            $('#emailField').addClass('is-valid')
        } else {
            $('#emailField').addClass('is-invalid')
            $('#emailField').removeClass('is-valid')
        }
    })

    // Dynamic valdiation for the new password field.
    $('#newPassword').on('input', function(){
        formData.newPasswordField = $(this).val() // This ensures that the variable is being updated dynamically.
        if (passwordValidate(formData.newPasswordField)){ // Toggles between valid and invalid messages.
            $('#newPassword').removeClass('is-invalid')
            $('#newPassword').addClass('is-valid')
        } else {
            $('#newPassword').addClass('is-invalid')
            $('#newPassword').removeClass('is-valid')
        }
    })    

    $('#inputPassword').on('input', function(){
        formData.currentPasswordField = $(this).val()
    })

    $('#changeDetails').on('submit', function(event){
        event.preventDefault(); // This will prevent the page from reloading when the submit button is clicked...

        if (!formData.emailField.trim() && !formData.newPasswordField.trim()) { // Check that at least one field is filled.
            alert("You must fill in at least one of the email or password fields.")
            return
        }

        if (formData.currentPasswordField == ""){
            alert("The current password field cannot be left blank!")
            return
        }

        if (formData.emailField.trim() !== "") { // Trim removes extra whitespace that may be present
            // If email field is not empty, it is validated.
            if (!emailValidate(formData.emailField)) {
                delete formData.emailField // Delete emailField if validation fails
            }
        }
        
        if (formData.newPasswordField.trim() !== "") {
            // If password field is not empty, it is validated.
            if (!passwordValidate(formData.newPasswordField)) {
                delete formData.newPasswordField; // Delete newPasswordField if validation fails
            }
        }


        $.ajax({
            type: 'POST',
            url: '/user/update_details',
            data: JSON.stringify(formData),
            contentType: 'application/json',
            success: function(status){
                alert(`${status.emailStatus}`)
                alert(`${status.passwordStatus}`)
                location.reload()
            },
            error: function(){
                alert("An error occurred. The page will be refreshed.")
                location.reload()
            }


        })
    })

})