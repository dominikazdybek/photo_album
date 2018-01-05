function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
console.log(csrftoken);

//Ajax call
function csrfSafeMethod(method) {
// these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


var likeTextButton ='Polub zdjęcie'
$('.likes').click(function () {
    var button = $(this);
    var buttonText = button.children('.button_text');
    console.log(buttonText.text());
    if (buttonText.text() === likeTextButton) {
        buttonText.text('Lubisz to zdjęcie')
    } else {
        buttonText.text('Polub zdjęcie')
    }
    var count = button.siblings('.like_count');
    var currentLikeCount = count.text();
    var id = $(this).attr("data-photo");

    $.ajax({
        url: '/photo/like/' + id + '/',
        type: 'POST',
        success: function (data) {
            console.log(data, count);
            if (data === "False") {
                count.text(+currentLikeCount - 1)
            } else {
                count.text(+currentLikeCount + 1)
            }
        }
    });

});

