//$(document).ready(function(){
//    $('#nucleotideTable').DataTable();
//});

function loading(){
            $("#loading").show();
            $("#data").addClass("disabledbutton");
        }

$(function() {
    $('#submitSearch').click(function() {
        var user = $('#term').val();
        $.ajax({
            url: '/searchFasta',
            data: $('#data').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
