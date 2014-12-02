//This gets the CSRF token; Django doesn't let you post unless you give it the CSRF token
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
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var swap_icon = function(item) {
	if ($(item).hasClass("glyphicon-ok-sign")) {
		$(item).removeClass("glyphicon-ok-sign");
		$(item).removeClass("green");
		$(item).addClass("glyphicon-minus-sign");
		$(item).addClass("red");
	} else {
		$(item).removeClass("glyphicon-minus-sign");
		$(item).removeClass("red");
		$(item).addClass("glyphicon-ok-sign");
		$(item).addClass("green");
	}
}

$(document).ready(function(){
	$(".attendance_icon").click(function(){
		elem = this
		data = $(this).attr("data").split(" ");
		u = data[0];
		c = data[1];

  		$.ajax(
  			{
  				type:"POST",
  				url:"/attendance/change/",
  				data:{
  					user: u,
  					course: c
  				},

  				success:function(response){
  					if (response == "True") {
    					swap_icon(elem);
  					}
  					console.log(response);
  				}
  			}
  		);
	});
});