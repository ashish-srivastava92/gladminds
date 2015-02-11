(function() {

	$(".modal-footer .download-member-detail").click(function(e) {
		var choice = $( "#download-option option:selected" ).val();
		    downloadModal = $('.modal.download-modal'),
		    downloadChoice = {'choice':choice};
		console.log(choice);
		url = '/kit/download/'+choice
		downloadModal.modal('hide');
		location.replace(url);
	});
})();