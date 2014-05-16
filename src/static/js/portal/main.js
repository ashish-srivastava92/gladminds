(function() {

    $("input.advisor-action").click(function() {
        var actionSet = $(this).parents(".advisor-action-item"), postAction = $(this).val(), sibblingActionSet = actionSet.siblings(".advisor-action-item"), disabledInputs = actionSet.find("input[type='text']"), activeInputs = sibblingActionSet.find("input[type='text']");

        activeInputs.attr("disabled", "disabled").removeAttr("required");
        disabledInputs.removeAttr("disabled").attr("required", "required");
    });

    $("form.coupon-check-form, form.coupon-close-form").on("submit", function(e) {
        var messageModal = $(".modal.message-modal"),
            messageBlock = $(".modal-body", messageModal),
            jqXHR = $.ajax({
            url : "/v1/messages",
            data : $(this).serializeArray(),
            type : "POST",
            beforeSend : function() {
              $(this).find("input[type='text']").val('');
            },
            success : function(data) {
              messageBlock.text(data.message);
              messageModal.modal("show");
            },
            error : function() {
              messageBlock.text("Invalid Data");
              messageModal.modal("show");
            }
        });
        return false;
    });

    $(".asc-form").on("submit", function(e) {
        var data = $(".asc-form").serializeArray();
        $(".asc-form").serializeArray().map(function(x) {
            data[x.name] = x.value;
        });
        
        if (data["password"] != data["re-password"]){
            return;          
        }
        var messageModal = $(".modal.message-modal"),
            messageBlock = $(".modal-body", messageModal),
            jqXHR = $.ajax({
                type : 'POST',
                data : data,
                url : '/register/asc',
                success : function(data) {
                    messageBlock.text(data.message);
                    messageModal.modal("show");
                    e.preventDefault();
                },
                error : function() {
                    messageBlock.text("Invalid Data");
                    messageModal.modal("show");
              }
            });
        return false;
    });
    
    $(".asc-self-form").on("submit", function(e) {
        var data = $(".asc-self-form").serializeArray();
        $(".asc-self-form").serializeArray().map(function(x) {
            data[x.name] = x.value;
        });
        
        if (data["password"] != data["re-password"]){
            return;          
        }
        var messageModal = $(".modal.message-modal"),
            messageBlock = $(".modal-body", messageModal);
        var jqXHR = $.ajax({
            type : 'POST',
            data : data,
            url : '/asc/self-register/',
            success : function(data) {
                messageBlock.text(data.message);
                messageModal.modal("show");
            },
            error : function() {
                messageBlock.text("Invalid Data");
                messageModal.modal("show");
          }
        });
        return false;
    });
    
    $(".sa-form").on("submit", function(event) {
      var data = $(".sa-form").serializeArray();
      $(".sa-form").serializeArray().map(function(x) {
          data[x.name] = x.value;
      });
      
      var jqXHR = $.ajax({
          type : 'POST',
          data : data,
          url : '/register/sa',
          success : function(data) {
              alert(data);
          }
      });
      return false;
    });
    
    $(".vin-form").on("submit", function() {
      var vin = $("#srch-vin").val();
      $(".customer-vin").val(vin);
      var jqXHR = $.ajax({
            type: "POST",
            url: "/exceptions/customer",
            data: {"vin": vin},
            success: function(data){
              $(".customer-phone").val(data['customer_phone']);
              $(".customer-name").val(data["customer_name"])
              $(".name-readonly").attr('disabled', true);
              $(".purchase-date").val(data["purchase_date"]).attr('disabled', true);
            },
            error: function() {
              var errorMessage = "Not Found"
              $(".customer-phone").val(errorMessage).attr('disabled', false);
              $(".customer-name").val(errorMessage).attr('disabled', false);
              $(".purchase-date").val(errorMessage).attr('disabled', false);
            }
          });
      return false;
    });

    $(".customer-form").on("submit", function(e) {
        var data = $(".customer-form").serializeArray(),
            vin = $("#srch-vin").val();
            messageModal = $(".modal.message-modal"),
            messageBlock = $(".modal-body", messageModal);
        $(".customer-form").serializeArray().map(function(x) {
            data[x.name] = x.value;
        });
        data['vin'] = vin;
    	console.log('data', data);
        var jqXHR = $.ajax({
              type: "POST",
              url: '/register/customer',
              data: data,
              success: function(data){
                  messageBlock.text(data.message);
                  messageModal.modal("show");
            	  e.preventDefault();
              },
              error: function(data) {
                  messageBlock.text('Invalid data');
                  messageModal.modal("show");
              }
            });
        return false;
      });    
    
    $(".ucn-recovery-form").on("submit", function() {
      var formData = new FormData($(this).get(0));
      var messageModal = $(".modal.message-modal"),
          messageBlock = $(".modal-body", messageModal),
          waitingModal = $(".modal.waiting-dialog"),
          jqXHR = $.ajax({
          type: "POST",
          url: "/exceptions/recover",
          data: formData,
          cache: false,
          processData: false,
          contentType: false,
          beforeSend: function(){
            $(this).find("input[type='text']").val('');
            waitingModal.modal("show");
          },
          success: function(data){
            messageBlock.text(data.message);
            waitingModal.modal("hide");
            messageModal.modal("show");
          },
          error: function() {
            messageBlock.text("Invalid Data");
            waitingModal.modal("hide");
            messageModal.modal("show");
          }
        });
      return false;
    });
    
    $("#jobCard").on("change", function() {
      var fileInput = $(this),
          ext = fileInput.val().split('.').pop().toLowerCase();
      if($.inArray(ext, ['pdf','tiff','jpg']) == -1) {
          alert('Invalid file type!');
          fileInput.replaceWith(fileInput=fileInput.clone(true));
      }
    });
    
    $(document).ready(function() {

    });
})();
