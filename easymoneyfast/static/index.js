// var success = function(){}




$(document).ready(function(){
	$('#login_id').on('submit', function(event){
		event.preventDefault();
		var username = $('#username').val();
		var password = $('#password').val();
		$.ajax({
			method:'POST',
			url: 'http://127.0.0.1:8000/login',
			data:{'username': username, 'password':password},
			success: function(result){
				if (result['status']==='success'){
					alert('SUCCESS');

				} else if (result['status']==='wpass') {
					alert('Wrong Password.')
				} else {
					alert('Username does not exit.')
				}
			}
		})
	})
})