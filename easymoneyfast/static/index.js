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
					$.ajax({
						method: 'POST',
						url: 'http://127.0.0.1:8000/balance',
						data: {'username': username},
						success: function(result){
							$('#balance').html('User: '+result.user+' | Balance: '+result.balance);
							$('#register').empty();
							$('#loginform').empty();
							$('#loginform').append('<a class="col s3 " href="/">LOGOUT</a>');
							$('#button100').on('click', function(event){
								$.ajax({
									method:'POST',
									url: 'http://127.0.0.1:8000/bid100',
									data: {'username': username},
									success: function(result){
										console.log(result);
										if (result['lastuser']==='forbidden'){
											alert('You cannot bid twice in a row.')
										} else {
											console.log(result);
											$('#balance').html('User: '+result.user+' | Balance: '+result.balance);
											if (result['status']==='done'){
											alert('CONGRATULATIONS!')
											}
										}
									}
								})
							})

						}
					})

				} else if (result['status']==='wpass') {
					alert('Wrong Password.')
				} else {
					alert('Username does not exit.')
				}
			}
		})
	})
})