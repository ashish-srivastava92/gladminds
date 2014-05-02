(function() {
  
  $(document).ready(function() {
    
  });
  
  $(".reset-pass").on("submit", function() {
    if($("#password").val() != $("#duplicate").val()) {
      alert("Passwords do not match");
      return false;
    }
  });
  
});