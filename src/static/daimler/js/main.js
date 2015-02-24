(function() {
	'use strict';
    $('.help-desk-form').on('submit', function() {
        var formData = new FormData($(this).get(0)),
            messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            messageHeader = $('.modal-title', messageModal),
            waitingModal = $('.modal.waiting-dialog'),
      jqXHR = $.ajax({
            type: 'POST',
            url: '/aftersell/servicedesk/helpdesk',
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
                messageHeader.text('Thanks');
                waitingModal.modal('hide');
                messageModal.modal('show');
                $('.summary').val('');
                $('.type').val('');
                $('.description').val('');
                $('.advisorMobile').val('');
                $('.priority').val('')
                setTimeout(function() {
                    parent.window.location='/aftersell/servicedesk/helpdesk';
                }, 2000);
            },
            error: function() {
                messageBlock.text('Invalid Data');
                messageHeader.text('Invalid');
                waitingModal.modal('hide');
                messageModal.modal('show');
                
            }
        });
        return false;
    });
    
    $('.service-desk-form').on('submit', function() {
        var formData = new FormData($(this).get(0)),
            messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            messageHeader = $('.modal-title', messageModal),
            waitingModal = $('.modal.waiting-dialog'),
      jqXHR = $.ajax({
            type: 'POST',
            url: '/aftersell/servicedesk/save-feedback/',
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
                messageHeader.text('Thanks');
                waitingModal.modal('hide');
                messageModal.modal('show');
                $('.summary').val('');
                $('.type').val('');
                $('.description').val('');
                $('.advisorMobile').val('');
                $('.priority').val('');
                $('.department').val('');
                $('.sub-department').val('');
                setTimeout(function() {
                    parent.window.location='/aftersell/servicedesk/';
                }, 2000);
                
            },
            error: function() {
                messageBlock.text('Invalid Data');
                messageHeader.text('Invalid');
                waitingModal.modal('hide');
                messageModal.modal('show');
                
            }
        });
        return false;
    });
    
    $('.department').on('change', function(){
    	var department = $('.department'),
    		jqXHR = $.ajax({
            type: 'POST',
            url : '/aftersell/servicedesk/get-subcategories/',
            data: department,
            success : function(data){
            	console.log(data);
            	console.log(data.length);
            	$('.sub-department').empty()
            	for (var i=0;i< data.length;i++){
            		console.log(data[i]);
            		console.log(data[i]);
            		$('.sub-department')
            		.append($('<option>', {
            			value: data[i].id,
            			text : data[i].name
            		}));
            	}
            }
        });
    });
    $('.sd_file').on('change', function() {
        var fileInput = $(this),
            ext = fileInput.val().split('.').pop().toLowerCase();
        if($.inArray(ext, ['pdf','jpg','jpeg','png','ppt','pptx','doc','docx','xls','xlsx']) === -1) {
            alert('Invalid file type!');
            fileInput.replaceWith(fileInput=fileInput.clone(true));
        }
    });
    
   $('.sd-file').on('click', function() {
	   var time = 5;
	   setTimeout(function(){
		   $('.sd-file').prop('disabled',false);
	    }, time*1000);
	   $('.sd-file').prop('disabled',true);
    });

    

    $('.comment-form').on('submit', function(e) {
        var data = Utils.getFormData('.servicedesk'),
            formData = new FormData($(this).get(0)),
            comment_data = Utils.getFormData('.comment-form'),
            url = '/aftersell/feedbackdetails/'+data.ticketId+'/comments/'+comment_data.commentId+'/',
            messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            messageHeader = $('.modal-title', messageModal),
            waitingModal = $('.modal.waiting-dialog');

        var jqXHR = $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function(){
                $(this).find('input[type="text"]').val('');
                waitingModal.modal('show');
            },
            success: function(data){
            	var data = Utils.getFormData('.servicedesk');
                messageBlock.text('Updated Successfully');
                messageHeader.text('Save');
                waitingModal.modal('hide');
                messageModal.modal('show');
	            $('.comment-id').val('');
	            $('.comment-user').val('');
	            $('.comment-description').val('');
	            $('.comment-date').val('');
                setTimeout(function() {
                	parent.window.location='/aftersell/feedbackdetails/'+data.ticketId+'/';
                }, 2000);
                
            },
            error: function() {
                messageBlock.text('Invalid Data');
                messageHeader.text('Invalid');
                waitingModal.modal('hide');
                messageModal.modal('show');
            }
        });
        return false;
    });

    
    $('.servicedesk').on('submit', function(e) {
        var data = Utils.getFormData('.servicedesk'),
            formData = new FormData($(this).get(0)),
            url = '/aftersell/feedbackdetails/'+data.ticketId+'/',
            messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            messageHeader = $('.modal-title', messageModal),
            waitingModal = $('.modal.waiting-dialog');
        if (data.assign_to === 'Assign to reporter'){
            formData.append('reporter_status',true);
        }
        else{
            formData.append('reporter_status',false);
        }

        var jqXHR = $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function(){
                $(this).find('input[type="text"]').val('');
                waitingModal.modal('show');
            },
            success: function(data){
                messageBlock.text('Updated Successfully');
                messageHeader.text('Save');
                waitingModal.modal('hide');
                messageModal.modal('show');
                setTimeout(function() {
                	var parts = document.referrer.split('://')[1].split('/');
                	var pathName = parts.slice(1).join('/');
                	parent.window.location='/'+pathName;
                }, 3000);
                
            },
            error: function() {
                messageBlock.text('Invalid Data');
                messageHeader.text('Invalid');
                waitingModal.modal('hide');
                messageModal.modal('show');
            }
        });
        return false;
    });

    $('.due-datetime-picker').datetimepicker({
    	dayOfWeekStart : 1,
    	lang:'en',
    	format:'Y-m-d H:i:s',
	});
    
    $(".feedback-free-text-search").click(function(){
    	window.location.href = change_url_by_filter();
    })
    
    $('.feedback-filters-options').change(function() {
    	window.location.href = change_url_by_filter();
    })
    
})();

function getUrl(current_page_num, no_of_link_in_page, flage){
	var url = change_url_by_filter() + 'page=';
		if (flage == 'true'){
			url = url +  current_page_num
		}else{
			var diff = current_page_num - no_of_link_in_page;
				if (diff > 1){
					url = url + diff 
				}else{
					url = url + 1
				}
		}
		
		window.location.href = url;
}

function change_url_by_filter(){
	var url = window.location.pathname + '?',
		serch_text = $(".feedback-search-text").val(),
    	selectedOptions = $('.feedback-filters-options'),
    	filters = ['priority', 'type', 'status', 'count'];
    	$.each(filters, function(index, val){
    		url = url + val + '=' + selectedOptions[index].options[selectedOptions[index].selectedIndex].value + '&'
    	});
    	
    	if(serch_text){
    		url = url + "search=" + serch_text
    	}
    	return url;
}

function rootCause(status){
	'use strict';
	var rootCauseClass = $('.rootcause'),
        resolution = $('.resolution'),
        reason = $('.root-cause'),
        ticketResolution = $('.ticket-resolution'),
        assignee = $('.assignee'),
        comments = $('.comments');
	assignee.attr('required', false);
	rootCauseClass.addClass('hide');
	resolution.addClass('hide');
	reason.attr('required', false);
	ticketResolution.attr('required', false);
	comments.attr('required', false);
	
	if (status === 'Resolved'){
		rootCauseClass.removeClass('hide');
        resolution.removeClass('hide');
        reason.attr('required', true);
        ticketResolution.attr('required', true);
        comments.attr('required', true);
	}
	if (status !== 'Open'){
		assignee.attr('required', true);
	}
	
	if (status === 'Pending'){
		document.getElementById('assignee').value='Assign to reporter';
		comments.attr('required', true);
	}
	if (status === 'In Progress'){
		document.getElementById('assignee').value=document.getElementById('assignee').options[1].value;
		comments.attr('required', true);
	}
	
}
function disable_func(group){
	if (group === 'Manager'){
		$("#type").prop("disabled", true);
	}else{
		$("#type").prop("disabled", true);
		$("#priority").prop("disabled", true);
		$("#assignee").prop("disabled", true);
		$("#status").prop("disabled", true);
	}
}

function showMessage(id){
	'use strict';
	$('#'+id).popover();
}

function change_status(){
	var status = window.location.search.split('?status=')[1];
    $('.status').val(status);
    $('.status').change(function() {
    	status = $('.status').val();
    	window.location.href = window.location.pathname + '?status='+status;
    });
	
}

function getDataByDate(){
    var month = $('#month').val(),
        year =  $('#year').val();
    if(month=='' || year==''){
    	window.location.href = window.location.pathname
    	
    }
    else{
    window.location.href = window.location.pathname + '?month='+month+'&'+'year='+year;
    }
   
}

$(document).on("click", ".open-add-comment-dialog", function (e) {

	e.preventDefault();
	
	var _self = $(this);
	var commentId = _self.data('id'),
		commentUser = _self.data('user'),
	    commentDescription = _self.data('comment'),
	    commentDate = _self.data('date'),
	    comment = $('.comment-description'),
	    loginUser = _self.data('owner');
	$(".comment-id").val(commentId);
	$(".comment-user").val(commentUser);
	$(".comment-description").val(commentDescription);
	$(".comment-date").val(commentDate);
	comment.attr('readonly', false);
	if (loginUser != commentUser){
		comment.attr('readonly', true);
	}
	
	$(_self.attr('href')).modal('show');
	
});