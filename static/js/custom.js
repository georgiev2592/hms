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