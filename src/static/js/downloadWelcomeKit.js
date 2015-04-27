(function() {

	$(".modal-footer .download-member-detail").click(function(e) {
		$('.download-fail').addClass('hide');
		var choice = $( "#download-option option:selected" ).val();
		    downloadModal = $('.modal.download-modal'),
		    downloadChoice = {'choice':choice};
		check_url = '/check-form/'+choice
		url = '/kit-download/'+choice
		downloadModal.modal('hide');
		e.preventDefault();
    	$.ajax({
            type: 'POST',
            url: check_url,
            success: function(data){
            	e.preventDefault()
            	if (data.status) {
            		window.location.replace(url)
            	}
            	else{
            		$('.download-fail').removeClass('hide');
            	}
            },
    		error: function(data){
    			e.preventDefault();
    		}
    	});
	});
})();