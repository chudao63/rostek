$(document).ready(function() {
    for (let i=1;i<10;i++) {
        $("#ct-menu-"+i).click(function() {
            $(".ct-menu").removeClass("active")
            $(this).addClass("active")
            $(".ct-body").hide()
            $("#ct-body-"+i).show()
        });
    }    
})
function send_message(url) {
    console.log(url)
    $.ajax({
        url: url,
        type: 'GET',
        data: "",
        success: function(response) {
            // alert(response)
            $("#home").text(response)
        },
        error: function(response) {
            alert(response);
        }
    })
}