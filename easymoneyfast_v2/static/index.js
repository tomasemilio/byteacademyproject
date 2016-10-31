var initinfo = function(username){
	$.ajax({
		method:'POST',
		url:'/initinfo',
		data:{'username':username},
		success: function(result){
			$('#balance').html(result['balance']);
			$('#creationdate10').html(result['cd10']);
			$('#creationdate50').html(result['cd50']);
			$('#creationdate100').html(result['cd100']);
			$('#creationdate500').html(result['cd500']);
		}
	})
}


var bid = function(total, username){
	$('#bid'+total).on('click', function(event){
		event.preventDefault();
		$.ajax({
			method: 'POST',
			url: '/bid'+total,
			data: {'username':username},
			success: function(result){
				console.log(result);
				$('#balance').empty();
				$('#balance').html(result['balance']);
				$('#message'+bid).empty();
				if (result['status']==='open'){
					$('#message'+bid).html('Better luck next time!')
				} else if (result['status']==='waslast'){
					$('#message'+bid).html('You were the last person to bid.')
				} else if (result['status']==='nomoney'){
					$('#message'+bid).html('Insufficient funds.')
				} else if (result['status']==='done'){
					$('#message'+bid).html('YOU WIN!')
				}

			} 
		})
	});
}


$(document).ready(function(){
	initinfo(username);
	bid('10', username);
	bid('50', username);
	bid('100', username);
	bid('500', username);

})