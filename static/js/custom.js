$(window).resize(function(){
	if ($(window).width() < 768) {
	    $('td').width('100%');
	    $('th').width('100%');
	}
	else {
		$('td').width('70%');
	    $('th').width('30%');
	}
});

$(document).ready(function() {
	$('#new-guest').click(function() {
	   	if($('#new-guest').is(':checked')) {
	   		$('#existingForm').toggle('500');
	   		$('#newForm').toggle('500');
	   	}
	});
	$('#existing-guest').click(function() {
	   	if($('#existing-guest').is(':checked')) {
	   		$('#newForm').toggle('500');
	   		$('#existingForm').toggle('500');
	   	}
	});
});

