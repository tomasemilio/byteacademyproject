var showhide = function(tag, show1, show2, hide1, hide2){
	$(tag).on('click', function(event){
		event.preventDefault();
		$(show1).show();
		$(show2).show();
		$(hide1).hide();
		$(hide2).hide();
	})
};

var loginCheck = function(){
	$('#loginform').on('submit', function(event){
		event.preventDefault();
		$('#wronguser').hide();
		$('#wrongpass').hide();
		$('#rightcredentials').hide();
		username = $('#username').val();
		password = $('#password').val();
		$.ajax({
			method: 'POST',
			url: '/login',
			data: {'username':username, 'password': password},
			success: function(result){
				if (result['status'] ==='wusername'){
					$('#wronguser').show();
				} else if (result['status'] ==='wpass'){
					$('#wrongpass').show();	
				} else if (result['status'] ==='success'){
					$('#rightcredentials').show();
					window.location.href='/home'
				}
			}
		})
	})
}

$(document).ready(function(){
	showhide('#register', '#login', '#registerform', '#loginform', '#register');
	showhide('#login', '#loginform', '#register', '#login', '#registerform');
	loginCheck();


})