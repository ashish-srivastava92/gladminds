(function() {
	'use strict';
    $('#platImage').on('change', function() {
        var fileInput = $(this),
            ext = fileInput.val().split('.').pop().toLowerCase();
        if($.inArray(ext, ['pdf','tiff','jpg','png']) === -1) {
            alert('Invalid file type!');
            fileInput.replaceWith(fileInput=fileInput.clone(true));
        }
    });
    $('#plateMap').on('change', function() {
        var fileInput = $(this),
            ext = fileInput.val().split('.').pop().toLowerCase();
        if($.inArray(ext, ['xlsx','csv']) === -1) {
            alert('Invalid file type!');
            fileInput.replaceWith(fileInput=fileInput.clone(true));
        }
    });
    
    $('.plate-map-form').on('submit', function() {
        var formData = new FormData($(this).get(0));
        var messageModal = $('.modal.message-modal'),
            messageBlock = $('.modal-body', messageModal),
            waitingModal = $('.modal.waiting-dialog'),
        jqXHR = $.ajax({
            type: 'POST',
            url: '/v1/bom-plate-parts/save-part/',
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
})();



