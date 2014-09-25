(function() {
	
    $('input.advisor-action').click(function() {
        var actionSet = $(this).parents('.advisor-action-item'), postAction = $(this).val(), sibblingActionSet = actionSet.siblings('.advisor-action-item'), disabledInputs = actionSet.find('input[type="text"]'), activeInputs = sibblingActionSet.find('input[type="text"]');

        activeInputs.attr('disabled', 'disabled').removeAttr('required');
        disabledInputs.removeAttr('disabled').attr('required', 'required');
    });

    $('form.coupon-check-form, form.coupon-close-form').on('submit', function(e) {
    	var data = $(this).serializeArray();
    	Utils.submitForm(e, data, '/v1/messages');
        return false;
    });

    $('.asc-form').on('submit', function(e) {
        var data = Utils.getFormData('.asc-form')
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
        return false;
    });
    

    $('.customer-form').on('submit', function(e) {
    	var data = Utils.getFormData('.customer-form'),
            vin = $('#srch-vin').val();
    	data['vin'] = vin;
    	Utils.submitForm(e, data, '/aftersell/register/customer');
    	$('.customer-phone').val('').attr('readOnly', false);
  	    $('.customer-name').val('').attr('readOnly', false);
        $('.purchase-date').val('').attr('readOnly', false);
        $('.customer-id').val('').attr('readOnly', false);
        $('.customer-submit').attr('disabled', true);
        return false;
      });
    
    $('.cutomer-reg-form').on('submit', function() {
      var vin = $('#srch-vin').val(),
          messageModal = $('.modal.message-modal'),
          messageBlock = $('.modal-body', messageModal);
      $('.customer-vin').val(vin);
      
      var jqXHR = $.ajax({
            type: 'POST',
            url: '/aftersell/exceptions/customer',
            data: {'vin': vin},
            success: function(data){
              if (data['phone']) {
                  $('.customer-phone').val(data['phone']);
                  $('.customer-name').val(data['name']).attr('readOnly', true);
                  $('.purchase-date').val(data['purchase_date']).attr('readOnly', true);
                  $('.customer-id').val(data['id']).attr('readOnly', true);
                  $('.customer-submit').attr('disabled', false);
              }	
              else if (data['message']) {
                  $('.customer-phone').val('');
            	  $('.customer-name').val('').attr('readOnly', false);
                  $('.purchase-date').val('').attr('readOnly', false);
                  $('.customer-id').val('').attr('readOnly', false);
                  $('.customer-submit').attr('disabled', true);
                  messageBlock.text(data.message);
                  messageModal.modal('show');
                  if (!data['status']) {
                	  $('.customer-id').val('').attr('readOnly', true);
                	  $('.customer-submit').attr('disabled', false);
                  }
              }
            },
            error: function() {
            	messageBlock.text('Oops! Some error occurred!');
                messageModal.modal('show');
            }
          });
      return false;
    });

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
            	}
            	if (service_detail.length > 0) {
            		var details_html = "<div class='other-details'><label class='control-label'>VIN:&nbsp</label>"+ other_details.vin +"<br><label class='control-label'>Customer Id:&nbsp</label>"+ other_details.customer_id +"<br><label class='control-label'>Customer Name:&nbsp</label>"+ other_details.customer_name +"</div>",
            			table = $(".status-search-results tbody");
            			$('.status-result-detail').append(details_html);
            			$.each(service_detail, function(idx, elem){
            				table.append("<tr class='search-detail'><td>"+elem.service_type+"</td><td>"+elem.status+"</td></tr>");
            			});
            	}	
            },
            error: function() {
            	messageBlock.text('Oops! Some error occurred!');
                messageModal.modal('show');
            }
          });
      return false;

    });

    $(".change-password-form").on("submit", function() {
	    if($(".new-password").val() != $(".retype-new-pass").val()) {
	    	Utils.showErrorMessage('Password does not matches.', 1000, 7000);
		    return false;
	    }else{
	    	var data = Utils.getFormData('.change-password-form');
	    	$.ajax({
	              type: 'POST',
	              url: '/aftersell/provider/change-password',
	              data: data,
	              success: function(data){
	            	  if (data['message']) {
	            		  Utils.showErrorMessage(data['message'], 10, 7000)
	            	  }
            		  setTimeout(function(){
            			  if(data['status']){
            				  history.back();
            			  }
            		  }, 2000); 
	              },
	              error: function(data) {
	            	  messageBlock.text('Oops! Some error occurred!');
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
    	var table = $("#search-results tbody .search-detail");
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
                if (data['message']) {
                      messageBlock.text(data.message);
                      messageModal.modal('show');
                }
                else if (data.length > 0) {
                	var table = $("#search-results tbody");
                    $.each(data, function(idx, elem){
                        table.append("<tr class='search-detail'><td>"+elem.vin+"</td><td>"+elem.id+"</td><td>"+elem.name+"</td><td>"+elem.phone+"</td></tr>");
                    });
                }	

              },
              error: function() {
              	messageBlock.text('Oops! Some error occurred!');
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
    
    $('#jobCard').on('change', function() {
      var fileInput = $(this),
          ext = fileInput.val().split('.').pop().toLowerCase();
      if($.inArray(ext, ['pdf','tiff','jpg']) == -1) {
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
})();
