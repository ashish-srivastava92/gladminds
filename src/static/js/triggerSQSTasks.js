(function() {

	$("trigger-sqs-tasks btn").click(function() {
		find out the
		{
			
			
			
			
		}
	});
	
	var triggerTask = $.ajax({
		type: 'POST',
		url: '/',
		  data: formData,
		  cache: false,
		  processData: false,
		  contentType: false,
		  beforeSend: function(){
		  $(this).find('input[type="text"]').val('');
				waitingModal.modal('show');
		  },
		  success: function(data){
		    messageBlock.text(data.message);
		    waitingModal.modal('hide');
			messageModal.modal('show');
		  },
		  error: function() {
		    messageBlock.text('Invalid Data');
			waitingModal.modal('hide');
			messageModal.modal('show');
		  }
        
	}) ;
	
})();

