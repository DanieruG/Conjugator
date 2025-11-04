$(document).ready(function(){
    $(".js-example-basic-multiple").select2();

    function validateForm(){
        var flag = false;
        $('.js-example-basic-multiple').each(function(){
            if ($(this).val().length > 0){
                flag = true
            } else {
                flag = false
            }
        })
        return flag
    }

    $('#exerciseDuration').on('input', function(){
        var duration = Number($(this).val())
        if (isNaN(duration) || duration > 20 || duration < 0 ) {
            $(this).addClass('is-invalid')
            $(this).removeClass('is-valid')
            $(this).val(20)
        } else {
            $(this).addClass('is-valid')
            $(this).removeClass('is-invalid')
        }
})

    $('#exerciseCustomisation').submit(function(event){
        event.preventDefault(); // Stops reload and default submit action.

        if (validateForm()){

            var tensesGrouped = {
                'indicatif': [],
                'subjonctif': [],
                'conditionnel': [],
            }

            $('#tenseSelector option:selected').each(function(){
                var optgroupLabel = $(this).closest('optgroup').attr('label')
                tensesGrouped[optgroupLabel].push($(this).attr('value'))
            })

            var formData = {
                selected_verbs: $('#verbSelector').val(),
                selected_pronouns: $('#pronounSelector').val(),
                selected_tenses: tensesGrouped,
                duration: $('#exerciseDuration').val()
            }

            $.ajax({
                url: '/user/begin_exercise',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(formData),
                success: function(status){
                    $('#alertBox').html(
                        `<div class="alert alert-success" role="alert">
                            ${status.success}
                        </div>`
                    );
                    window.location.href = "/user/main_exercise"
                },
                error: function(jqXHR){
                    $('#alertBox').html(
                        `<div class="alert alert-danger" role="alert">
                            ${jqXHR.responseText}
                        </div>`
                    );
                }
            })
    }else{
        alert('Please fill in all fields.')
        return
    }}
    )
}
)
