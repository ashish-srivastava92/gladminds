(function() {

    $("input.advisor-action").click(function() {
        var actionSet = $(this).parents(".advisor-action-item"), postAction = $(this).val(), sibblingActionSet = actionSet.siblings(".advisor-action-item"), disabledInputs = actionSet.find("input[type='text']"), activeInputs = sibblingActionSet.find("input[type='text']");

        activeInputs.attr("disabled", "disabled").removeAttr("required");
        disabledInputs.removeAttr("disabled").attr("required", "required");
    });

    $(".query-form").on("submit", function(e) {
        var messageBlock = $(".user-message .message");
        $(this).find("input[type='text']").val('');
        var jqXHR = $.ajax({
            url : "/v1/messages",
            data : $("form.query-form").serializeArray(),
            type : "POST",
            beforeSend : function() {
                messageBlock.stop().fadeOut(0);
                $(".query-submit").prop("disabled", true);
            },
            success : function() {
                messageBlock.text("Query has been submitted");
                messageBlock.fadeIn(1000).fadeOut(5000);
                $(".query-submit").prop("disabled", false);
            },
            error : function() {
                messageBlock.text("Invalid Data. Please Check");
                messageBlock.fadeIn(1000).fadeOut(5000);
                $(".query-submit").prop("disabled", false);
            }
        });
        return false;
    });

    $(".asc-form").on("submit", function(e) {
        var data = $(".asc-form").serializeArray();
        $(".asc-form").serializeArray().map(function(x) {
            data[x.name] = x.value;
        });
        
        if (data["pwd"] != data["re-pwd"]){
            alert("Password should be same");
            return false;             
        }
        var jqXHR = $.ajax({
            type : 'POST',
            data : data,
            url : '/save/asc',
            success : function(data, status, jqxhr) {
                alert("Successfully registered");
            },
            error : function(data, status, jqxhr) {
                alert("error on saving Please retry");
            }
        });
        return false;
    });

    $(document).ready(function() {

    });
})();
