(function (){

  $("input.advisor-action").click(function() {
    var actionSet = $(this).parents(".advisor-action-item"),
        postAction = $(this).val(),
        sibblingActionSet = actionSet.siblings(".advisor-action-item")
        disabledInputs = actionSet.find("input[type='text']")
        activeInputs = sibblingActionSet.find("input[type='text']");

        activeInputs.attr("disabled", "disabled").removeAttr("required");
        disabledInputs.removeAttr("disabled").attr("required", "required");
  });

  $(document).ready(function() {
    
  });
})();