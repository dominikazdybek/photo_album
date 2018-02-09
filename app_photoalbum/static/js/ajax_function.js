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


$('#comment').click(function(event) {

    event.preventDefault();
    // pobierz text komentarza
    console.log(this);
    var id = $(this).attr("data-prod");
    var comment = $('#comment-input').val();
    // wyczysc input
    // $('#comment-input').val('');
    // umiec comentarz w nowym divie

    // wyslij komentarz do bazy danych
    $.post(
        '/photo/' + id + '/comments/',
        comment
    ).done(function (response) {
        console.log(response);
        var parsedDate = new Date(response.date);
        var date = parsedDate.getUTCDate() + '/' + (parsedDate.getMonth() + 1) + '/' + parsedDate.getFullYear();
        var time = parsedDate.getHours() + ':' + parsedDate.getMinutes();
        newCommentDiv = $('.new');
        $('<div><hr>' +
            '<div class="editing-comment">' +
            response.comment +
            '</div>' +
            '<button class="delete-button btn btn-default custom" type="button" style="float: right" data-comment="' +
            response.id +
            '"><span class="glyphicon glyphicon-trash"></span><small>delete</small>' +
            '</button>' +
            '<button class="edit-button btn btn-default custom" type="button" style="float: right" data-comment="' +
            response.id +
            '"><span class="glyphicon glyphicon-edit"></span><small class="edit-button-text">edit</small>' +
            '</button><p>' +
            response.author +
            ', <small>' +
            date + ' ' + time +
            '</small></p></div>').insertBefore(newCommentDiv)
    });
});


$('#comments').on('click', '.delete-button',function () {
// $('.delete-button').click(function () {
    console.log("click", this);
    var button = $(this);
    var id = $(this).attr("data-comment");
    var div = button.parent()
    $.ajax({
        url: '/comments/' + id,
        type: 'DELETE',
        success: function() {
            div.remove();
            }
        });
    });


$('#comments').on("click", '.edit-button', function(){
    // console.log("click", this.parent());
    var button = $(this);
    var currentTextElement = button.children('.edit-button-text');
    var iconElement = currentTextElement.siblings('.glyphicon');
    var id = $(this).attr("data-comment");
    var commentElement =  $(this).siblings('.editing-comment')
    if (currentTextElement.text() === "edit") {
        currentTextElement.text('save');
        iconElement.removeClass('glyphicon-edit').addClass('glyphicon-send');
        commentElement.prop('contentEditable',true).addClass('rounded');
    } else {
        currentTextElement.text('edit');
        iconElement.removeClass('glyphicon-send').addClass('glyphicon-edit');
        commentElement.prop('contentEditable',false).removeClass('rounded');
        var editedComment = commentElement.text();
        $.ajax({
            url: '/comments/' + id,
            type: 'PUT',
            data:editedComment,
        });
    }
});


$(".navbar a, footer a[href='#myPage']").on('click', function (event) {
// Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
        // Prevent default anchor click behavior
        event.preventDefault();

        // Store hash
        var hash = this.hash;

        // Using jQuery's animate() method to add smooth page scroll
        // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
        $('html, body').animate({
            scrollTop: $(hash).offset().top
        }, 900, function () {

            // Add hash (#) to URL when done scrolling (default click behavior)
            window.location.hash = hash;
        });
    } // End if
});
