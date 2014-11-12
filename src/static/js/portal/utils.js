'use strict';
var Utils = {
	getFormData : function(className) {
		var data = $(className).serializeArray();
		$.map(data, function(x) {
			data[x.name] = x.value;
		});
		return data;
	},
	
	showErrorMessage : function(message, fadeIn, fadeOut){
		var messageBlock = $(".user-message .message");
	      	messageBlock.text(message);
	      	messageBlock.stop().fadeOut(0);
	      	messageBlock.fadeIn(fadeIn).fadeOut(fadeOut);
	},

	submitForm : function(event, data, url) {
		// Items are hidden
		var messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            waitingModal = $('.modal.waiting-dialog');
		if (data['password'] && (data['password'] !== data['re-password'])) {
			messageBlock.text('Re-typed password does not match');
			messageModal.modal('show');
			return;
		}
		var jqXHR = $.ajax({
			type : 'POST',
			data : data,
			url : url,
			beforeSend : function() {
				waitingModal.modal('show');
			},
			success : function(data) {
				waitingModal.modal('hide');
				messageBlock.text(data.message);
				messageModal.modal('show');
				event.preventDefault();
			},
			error : function() {
				waitingModal.modal("hide");
				messageBlock.text("Some error occurred. Please contact customer support: +91-9741775128");
				messageModal.modal("show");
			}
		});
	}
};
