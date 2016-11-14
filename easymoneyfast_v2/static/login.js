$(document).ready(function(){



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
				} else {
					$('#rightcredentials').show();
					setTimeout(function(){window.location.href='/'}, 500)
				}
			}
		})
	})
}


var registration = function(){
	$('#registerform').on('submit', function(event){
		event.preventDefault();
		newusername = $('#newusername').val();
		newpassword = $('#newpassword').val();
		newpassword2 = $('#newpassword2').val();
		$('#usertaken').hide();
		$('#diffpass').hide();
		$('#registerok').hide();
		$.ajax({
			method:'POST',
			url:'/register',
			data:{'username':newusername, 'password':newpassword, 'password2':newpassword2},
			success: function(result){
				console.log(result);
				if (result.username==='taken'){
					$('#usertaken').show();
				} else if (result.username==='diffpass'){
					$('#diffpass').show();
				} else if (result.username==='ok'){
					$('#registerok').show();
					setTimeout(function(){window.location.href='/'}, 500)		
				}
			}
		})
	})
}



	showhide('#register', '#login', '#registerform', '#loginform', '#register');
	showhide('#login', '#loginform', '#register', '#login', '#registerform');
	loginCheck();
	registration();


})