$(document).ready(function(){
    $('#nucleotideTableR').DataTable();
});

function loading(){
            $("#loading").show();
            $("#data").addClass("disabledbutton");
        }

//
//$(document).ready(function() {
//   $('li a').click(function(e) {
////        e.preventDefault();
////        $(this).closest('li').addClass('active').siblings('.active').removeClass('active');
//        var url = window.location.href;
//        $('a[href="'+url+'"]').addClass('active');
//
//
//    });
//    var pageTitle = window.location.pathname.replace( /^.*\/([^/]*)/ , "$1");
//
//            ///// Apply active class to selected page link
//            $('.link a').each(function () {
//
//                if ($(this).attr('href').toLowerCase() == pageTitle.toLocaleLowerCase())
//                    $(this).closest('li').addClass('active');
//            });

//});



