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
                if (data.phone) {
                    $('.customer-phone').val(data.phone);
                    $('.customer-name').val(data.name).attr('readOnly', true);
                    $('.purchase-date').val(data.purchase_date).attr('readOnly', true);
                    $('.customer-id').val(data.id).attr('readOnly', true);
                    $('.customer-submit').attr('disabled', false);
                }
              else if (data.message) {
                    $('.customer-phone').val('');
                    $('.customer-name').val('').attr('readOnly', false);
                    $('.purchase-date').val('').attr('readOnly', false);
                    $('.customer-id').val('').attr('readOnly', false);
                    $('.customer-submit').attr('disabled', true);
                    messageBlock.text(data.message);
                    messageModal.modal('show');
                    if (!data.status) {
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
                $('#message').val('');
                $('#priority').val(''); 
                $('#type').val('');
                $('#subject').val('');
                $('#advisorMobile').val('');
                
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
            waitingModal = $('.modal.waiting-dialog'),
        jqXHR = $.ajax({
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
    
    $(document).ready(function() {

    });

})();

function rootCause(status){
	if (status === 'Resolved'){
		$('#rootcause').removeClass('hide');
		$('#resolution').removeClass('hide');
	}else {
		$('#rootcause').addClass('hide');
		$('#resolution').addClass('hide');
	}
}


