(function() {
	var notiOvelay = $('notification-overlay');
	var notiIcon = $('.notification-icon');
	var notiCount = $(notiIcon).data('notification-count');
	var notiPopup = $('.notification-popup');

	$(notiPopup).hide();

	$('.noti-no, .noti-yes').bind('click', function() {
		$(notiPopup).hide();
	});

	if(notiCount <= '0') {
		$('.notification-overlay').hide();
	}

	$('.notification-overlay').bind('click', function() {
		$("#notification_message").html("Do you want to review <br> notifications?");
		$(".notification-popup .noti-yes a").attr("href","#notification-page");
		$(".notification-popup .noti-no a").attr("href","#profile-page");
		$(notiPopup).show();
	});

})();
