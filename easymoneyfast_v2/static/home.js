$(document).ready(function(){

var cd10 = '';
var cd50 = '';
var cd100 = '';
var cd500 = '';

var initinfo = function(username){
	var now_mil = new Date().getTime()/1000;
	var now = Math.ceil(now_mil)
	// console.log(now);
	$.ajax({
		method:'POST',
		url:'/initinfo',
		data:{'username':username},
		success: function(result){
			// console.log(result['cd10']);
			$('#balance').html(result['balance']);
			$('#creationdate10').html('<h6>Created&nbsp;&nbsp;'+(now-result.cd10).toString().toHHMMSS()+'</h6>');
			$('#creationdate50').html('<h6>Created&nbsp;&nbsp;'+(now-result.cd50).toString().toHHMMSS()+'</h6>');
			$('#creationdate100').html('<h6>Created&nbsp;&nbsp;'+(now-result.cd100).toString().toHHMMSS()+'</h6>');
			$('#creationdate500').html('<h6>Created&nbsp;&nbsp;'+(now-result.cd500).toString().toHHMMSS()+'</h6>');
			cd10 = result.cd10;
			cd50 = result.cd50;
			cd100 = result.cd100;
			cd500 = result.cd500;

		}
	});
}


var bid = function(total, username){
	$('#bid'+total).on('click', function(event){
		$('#bid'+total).hide();
		event.preventDefault();
		$.ajax({
			method: 'POST',
			url: '/bid'+total,
			data: {'username':username},
			success: function(result){
				console.log(result);
				$('#balance').empty();
				$('#balance').html(result['balance']);
				$('#message'+total).empty();
				if (result['status']==='open'){
					$('#message'+total).html('Better luck next time!').fadeIn(2000);
					setTimeout(function(){$('#message'+total).hide(); $('#bid'+total).fadeIn(1000) }, 2000);
					initinfo(username);
				} else if (result['status']==='waslast'){
					$('#message'+total).html('You were the last person to bid.').fadeIn(2000);
					setTimeout(function(){$('#message'+total).hide(); $('#bid'+total).fadeIn(1000) }, 2000);
					initinfo(username);
				} else if (result['status']==='nomoney'){
					$('#message'+total).html('Insufficient funds.').fadeIn(2000);
					setTimeout(function(){$('#message'+total).hide(); $('#bid'+total).fadeIn(1000) }, 2000);
					initinfo(username);
				} else if (result['status']==='done'){
					$('#message'+total).html('YOU WIN!').fadeIn(2000);
					setTimeout(function(){$('#message'+total).hide(); $('#bid'+total).fadeIn(1000) }, 2000);
					initinfo(username);
				}

			} 
		})
	});
};

var roulette = function(){
	$('#roulette').on('click', function(event){
		event.preventDefault();
		console.log('HOLA')
		$.ajax({
			method: 'GET',
			url: '/roulette/'+username,
			success: function(result){
				console.log(result);
				if (result['status']==='forbidden'){
					var time = 86164-result['interval'];
					$('#roulette-message').html('You still need to wait '+time.toString().toHHMMSS()+' (h/m/s) to play the roulette again.');
					// console.log($('#roulette-message').html());
					// console.log($('.modal-trigger'));
					$('#modal1').openModal();
				} else {
					var prize = result['prize']
					$('#roulette-message').html('Congratulations! You have been credited with USD '+prize+'.');
					$('#modal1').openModal();
					setTimeout(function(){window.location.reload()}, 3000);
				}
			}

		})
	})
};

	
String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
};







initinfo(username);
bid('10', username);
bid('50', username);
bid('100', username);
bid('500', username);
roulette();
window.setInterval(function(){
	var now_mil = new Date().getTime()/1000;
	var now = Math.ceil(now_mil);
	$('#creationdate10').html('<h6>Created&nbsp;&nbsp;'+(now-cd10).toString().toHHMMSS()+'</h6>');
	$('#creationdate50').html('<h6>Created&nbsp;&nbsp;'+(now-cd50).toString().toHHMMSS()+'</h6>');
	$('#creationdate100').html('<h6>Created&nbsp;&nbsp;'+(now-cd100).toString().toHHMMSS()+'</h6>');
	$('#creationdate500').html('<h6>Created&nbsp;&nbsp;'+(now-cd500).toString().toHHMMSS()+'</h6>');
}, 1000);
window.setInterval(function(){window.location.reload()}, 60000);




})