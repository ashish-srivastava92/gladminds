$(function() {
  
  $(".pass-reset-form").on("submit", function() {
    if($("#password").val() != $("#duplicate").val()) {
      alert("Passwords do not match");
      return false;
    }
  });
  
  $("a.otp-redirect").click(function(event) {
    if(!$("#mobile").val()) {
      event.preventDefault();
      alert("Enter Mobile Number");
    }
  });
  
  var userMessage = function() {
    var splittedUrl = window.location.href.split('?'),
        messageBlock = $(".user-message .message");
    
    if(splittedUrl.length > 1) {
      if(splittedUrl[1].indexOf("details=invalid")>=0){
        messageBlock.text("Invalid Details");
      } else if(splittedUrl[1].indexOf("token=invalid")>=0){
        messageBlock.text("Invalid Token");
      } else if(splittedUrl[1].indexOf("update=true")>=0){
        messageBlock.text("Your password has been updated. Please Login.");
      }
      messageBlock.fadeIn(1000).fadeOut(7000);
    }
  }
  
  var populateFields = function() {
    var splittedUrl = window.location.href.split('?');
    if(splittedUrl.length > 1) {
      if(splittedUrl[1].indexOf("phone")>=0){
        var pattern = /[0-9]{10}/g,
            phone = splittedUrl[1].match(pattern)[0];
        $(".otp-validation-form #phone").val(phone);
      }
    }
  }

  $(document).ready(function() {
    userMessage();
    populateFields();
  });
  
});