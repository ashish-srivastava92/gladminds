(function() {
	$('.tasksER').click(function(e) {
		var messageBlock = $('.user-message .message');
		var sqsTasks = {'task' : e.currentTarget.parentNode.className};
		var triggerTask = $.ajax({
			type : 'POST',
			url : '/trigger-tasks',
			data : sqsTasks,
			beforeSend : function() {
				messageBlock.stop().fadeOut(0);
				$('.query-submit').prop('disabled', true);
			},
			success : function() {
				messageBlock.text('Query has been submitted');
				messageBlock.fadeIn(1000).fadeOut(5000);
				$('.query-submit').prop('disabled', false);
			},
			error : function() {
				messageBlock.text('Error');
				messageBlock.fadeIn(1000).fadeOut(5000);
				$('.query-submit').prop('disabled', false);
			}
		});
	});
	
	

})();

