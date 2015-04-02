(function() {
	'use strict';
    $('input.advisor-action').click(function() {
        var actionSet = $(this).parents('.advisor-action-item'),
            postAction = $(this).val(),
            sibblingActionSet = actionSet.siblings('.advisor-action-item'),
            disabledInputs = actionSet.find('input[type="text"]'),
            activeInputs = sibblingActionSet.find('input[type="text"]');

        activeInputs.attr('disabled', 'disabled').removeAttr('required');
        disabledInputs.removeAttr('disabled').attr('required', 'required');
    });

    $('form.coupon-check-form, form.coupon-close-form').on('submit', function(e) {
        var data = $(this).serializeArray();
        Utils.submitForm(e, data, '/v1/messages');
        return false;
    });

    $('.asc-form').on('submit', function(e) {
        var data = Utils.getFormData('.asc-form');
        Utils.submitForm(e, data, '/aftersell/register/asc');
        return false;
    });
        
    $('.asc-self-form').on('submit', function(e) {
        var data = Utils.getFormData('.asc-self-form');
        Utils.submitForm(e, data, '/aftersell/asc/self-register/');
        return false;
    });
    
    $('.sa-form').on('submit', function(event) {
        var data = Utils.getFormData('.sa-form');
        Utils.submitForm(event, data, '/aftersell/register/sa');
        $('.sa-phone').val('').attr('readOnly', false);
        $('.sa-name').val('').attr('readOnly', false);
        $('.sa-id').val('').attr('readOnly', false);
        $('.sa-submit').attr('disabled', true);
        return false;
    });
    

    $('.customer-form').on('submit', function(e) {
    	var data = Utils.getFormData('.customer-form'),
    	    purchaseDate={'name':'purchase-date', 'value':$('#purchase-date').val()};
    	data.push(purchaseDate);
        Utils.submitForm(e, data, '/aftersell/register/customer');
        $('.customer-phone').val('').attr('readOnly', false);
        $('.customer-name').val('').attr('readOnly', false);
        $('.purchase-date').val('').attr('readOnly', false).attr('disabled',false);
        $('.customer-id').val('').attr('readOnly', false);
        $('.customer-submit').attr('disabled', true);
        return false;
    });
    
    $('.cutomer-reg-form').on('submit', function() {
        $('.customer-phone').val('').attr('readOnly', true);
        $('.customer-name').val('').attr('readOnly', true);
        $('.purchase-date').val('').attr('readOnly', false);
        var vin = $('#srch-vin').val(),
          user = $('#user').text().trim(),
          purchaseDate = $('#purchase-date').val(),	
          messageModal = $('.modal.message-modal'),
          messageBlock = $('.modal-body', messageModal),
          waitingModal = $('.modal.waiting-dialog');
        if(vin.trim().length!==17){
            messageBlock.text('VIN should be 17 digits. Please retry');
            messageModal.modal('show');
            return false;
        }
        $('.customer-vin').val(vin);
        var jqXHR = $.ajax({
            type: 'POST',
            url: '/aftersell/exceptions/customer',
            data: {'vin': vin},
            success: function(data){
            		if (data['phone'] && user=="d123") {
            			$('.customer-phone').val(data['phone']).attr('readOnly', false);
            		    $('.customer-name').val(data['name']).attr('readOnly', false);
            		    $('.purchase-date').val(data['purchase_date']).attr('readOnly', false);
            		    $('.customer-id').val(data['id']).attr('readOnly', true);
            		    $('.customer-submit').attr('disabled', false);
            		 	}
            	
            else if (data['phone']) {
                  $('.customer-phone').val(data['phone']).attr('readOnly', true);
            	  if (data['group']=='AuthorisedServiceCenters' || data['group']=='Dealers' || data['group']=='SdManagers'){
            		  $('.customer-phone').val(data['phone']).attr('readOnly', false);
            	}
                  $('.customer-name').val(data['name']).attr('readOnly', true);
                  $('.purchase-date').val(data['purchase_date']).attr('disabled', true);
                  $('.customer-id').val(data['id']).attr('readOnly', true);
                  $('.customer-submit').attr('disabled', false);
              }	
              else if (data['message']) {
                  $('.customer-phone').val('').attr('readOnly', false);
            	  $('.customer-name').val('').attr('readOnly', false);
            	  $('.purchase-date').val('').attr('disabled', false);
                  $('.customer-id').val('').attr('readOnly', false);
                  $('.customer-submit').attr('disabled', true);
                  messageBlock.text(data.message);
                  messageModal.modal('show');
                  if (!data['status']) {
                	  $('.modal-header .close').css("display", "block");
                	  $('.customer-id').val('').attr('readOnly', true);
                	  $('.customer-submit').attr('disabled', false);
                  }
                  else {
                      $('.modal-header .close').css("display", "none");
                      setTimeout(function(){
                      	messageModal.modal('hide');
                      }, 3000);
                	  vinSyncFeed(data);
                  }
              }
            		
            },
            error: function() {
            	messageBlock.text('Some error occurred. Please contact customer support: +91-9741775128');
                messageModal.modal('show');
            }
        });
        return false;
    });
    
function vinSyncFeed(data){
    var messageModal = $('.modal.message-modal'),
    	messageBlock = $('.modal-body', messageModal),
        waitingModal = $('.modal.waiting-dialog');
    var jqXHR = $.ajax({
        type: 'POST',
        url: '/aftersell/feeds/vin-sync/',
        data : data,
        success: function(data){
        if (data['message']) {
            $('.modal-header .close').css("display", "none");
        	waitingModal.modal('show');
            messageBlock.text(data.message);
            messageModal.modal('show');
            setTimeout(function(){
            	messageModal.modal('hide');
            	waitingModal.modal('hide');
            }, 5000);
            }
        },
        error: function() {
            messageBlock.text('Some error occurred. Please contact customer support: +91-9741775128');
            messageModal.modal('show');
        }
    });
    }

    $('.service-status-search').on('submit', function() {
    	var table = $(".status-search-results tbody .search-detail");
    		table.remove(); 
    		$('.other-details').remove();
    	var value = $('.status-search-value').val(),
	        field = $('.status-search-field').val(),
	        messageModal = $('.modal.message-modal'),
	        messageBlock = $('.modal-body', messageModal),
	        data = {};
    	data[field] =  value;
    	var jqXHR = $.ajax({
            type: 'POST',
            url: '/aftersell/exceptions/status',
            data: data,
            success: function(data){
            	var service_detail = data['search_results'],
            		other_details = data['other_details']; 
            	if (data['message']) {
                    messageBlock.text(data.message);
                    messageModal.modal('show');
            	}else{
	            	if (service_detail.length > 0) {
	            		var details_html = "<div class='other-details'><label class='control-label'>VIN:&nbsp</label>"+ other_details.vin +"<br><label class='control-label'>Customer Id:&nbsp</label>"+ other_details.customer_id +"<br><label class='control-label'>Customer Name:&nbsp</label>"+ other_details.customer_name +"</div>",
	            			table = $(".status-search-results tbody");
	            			$('.status-result-detail').append(details_html);
	            			$.each(service_detail, function(idx, elem){
	            				table.append("<tr class='search-detail'><td>"+elem.service_type+"</td><td>"+elem.status+"</td></tr>");
	            			});
	            	}
            	}
            },
            error: function() {
            	messageBlock.text('Some error occurred. Please contact customer support: +91-9741775128');
                messageModal.modal('show');
            }
          });
      return false;

    });
    
    $('.change-password-form').on('submit', function() {
        if($('.new-password').val() !== $('.retype-new-pass').val()) {
            Utils.showErrorMessage('Password does not matches.', 1000, 7000);
            return false;
        }else{
            var data = Utils.getFormData('.change-password-form');
            $.ajax({
                type: 'POST',
                url: '/aftersell/provider/change-password',
                data: data,
                success: function(data){
                        if (data.message) {
                            Utils.showErrorMessage(data.message, 10, 7000);
                        }
                        setTimeout(function(){
                            if(data.status){
                                history.back();
                            }
                        }, 2000);
                    },
                error: function(data) {
                    var messageModal = $('.modal.message-modal'),
                        messageBlock = $('.modal-body', messageModal);
                    messageBlock.text('Some error occurred. Please contact customer support: +91-9741775128');
                    messageModal.modal('show');
                }
            });
            return false;
        }
    });
    
    $('.cancel-change-pass').click(function(){
        history.back();
    });
    
    $('.vin-form').on('submit', function() {
        var table = $('#search-results tbody .search-detail');
        table.remove();
        var value = $('#search-value').val(),
            field = $('#search-field').val(),
            messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            data = {};
        data[field] =  value;
        var jqXHR = $.ajax({
            type: 'POST',
            url: '/aftersell/exceptions/search',
            data: data,
            success: function(data){
                if (data.message) {
                    messageBlock.text(data.message);
                    messageModal.modal('show');
                }
                else if (data.length > 0) {
                    var table = $('#search-results tbody');
                    $.each(data, function(idx, elem){
                        table.append('<tr class="search-detail"><td>'+elem.vin+'</td><td>'+elem.id+'</td><td>'+elem.name+'</td><td>'+elem.phone+'</td></tr>');
                    });

                }
            },
            error: function() {
                    messageBlock.text('Some error occurred. Please contact customer support: +91-9741775128');
                    messageModal.modal('show');
                }
        });
        return false;
    });
    
    $('.ucn-recovery-form').on('submit', function() {
        var formData = new FormData($(this).get(0));
        var messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            waitingModal = $('.modal.waiting-dialog'),
        jqXHR = $.ajax({
            type: 'POST',
            url: '/aftersell/exceptions/recover',
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
        });
        return false;
    });
    
    $('.help-desk-form').on('submit', function() {
        var formData = new FormData($(this).get(0)),
            messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            messageHeader = $('.modal-title', messageModal),
            waitingModal = $('.modal.waiting-dialog'),
      jqXHR = $.ajax({
            type: 'POST',
            url: '/v1/feedbacks/add-ticket/',
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
            url: '/v1/feedbacks/add-ticket/',
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

    $('#jobCard').on('change', function() {
        var fileInput = $(this),
            ext = fileInput.val().split('.').pop().toLowerCase();
        if($.inArray(ext, ['pdf','tiff','jpg']) === -1) {
            alert('Invalid file type!');
            fileInput.replaceWith(fileInput=fileInput.clone(true));
        }
    });
    
    $('.report-type-dropdown').on('change', function() {
        var reportType = $(this),
            couponStatus = $('.coupon-status');
        if (reportType.val() === 'credit') {
            couponStatus.addClass('hide');
        }
        else {
            couponStatus.removeClass('hide');
        }
    });
    $('.sa-reg-form').on('submit', function() {
        var saMobile = $('#srch-sa').val(),
            messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal);
        
        var jqXHR = $.ajax({
            type: 'POST',
            url: '/aftersell/exceptions/serviceadvisor',
            data: {'phone_number': saMobile},
            success: function(data){
                if (data.phone) {
                    $('.sa-phone').val(data.phone).attr('readOnly', true);
                    $('.sa-name').val(data.name).attr('readOnly', true);
                    $('.sa-id').val(data.id).attr('readOnly', true);
                    $('.sa-status').val(data.status).attr('readOnly', false);
                    $('.sa-submit').attr('disabled', false);
                    if (data.active>0){
                        $('.sa-status').attr('readOnly', true);
                        $('.sa-submit').attr('disabled', true);
                        messageBlock.text(data.message);
                        messageModal.modal('show');
                    }
                }
                else if (data.message) {
                    $('.sa-phone').val('').attr('readOnly', false);
                    $('.sa-status').val('').attr('readOnly', false);
                    $('.sa-name').val('').attr('readOnly', false);
                    $('.sa-id').val('').attr('readOnly', false);
                    $('.sa-submit').attr('disabled', true);
                    messageBlock.text(data.message);
                    messageModal.modal('show');
                    if (!data.status) {
                        $('.sa-id').val('').attr('readOnly', true);
                        $('.sa-submit').attr('disabled', false);
                    }
                }
            },
            error: function() {
                    messageBlock.text('Some error occurred. Please contact customer support: +91-9741775128');
                    messageModal.modal('show');
                }
        });
        return false;
    });
    $('.asc td:nth-child(1)').click(function(){
        var url = '/aftersell/sa/'+$(this)[0].id+'/',
            messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body'),
            messageHeader = $('.modal-title'),
            waitingModal = $('.modal.waiting-dialog'),
    jqXHR = $.ajax({
            type: 'POST',
            url: url,
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function(){
                waitingModal.modal('show');
            },
            success: function(data){
                messageBlock.html(data);
                messageHeader.text('Service Advisor');
                waitingModal.modal('hide');
                messageModal.modal('show');
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