console.log('123123');

$( document ).ready(function() {
    /**
     * AJAX Requests settings
     */

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    window.makeApiRequest = function (url, data, callback) {
        $.ajax({
            url: window.location.origin + url,
            type: 'POST',
            data: data,
            success: callback,
            error: function (err) {
                console.dir(err);
            }
        });
    };


    $("#like-btn").on('click', function(){
        console.log('CLICK!');
        var data = {
            article_id: 1,
            user_id: 2
        };
        makeApiRequest ('/blog/like-article-rest/', data, function(response) {
            console.log(response);
        });
    });
});