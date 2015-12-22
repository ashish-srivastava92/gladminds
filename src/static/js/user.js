
      $(document).ready(function() {
      	
		$("#id_first_name, #id_last_name, #id_email,#id_date_birth, #id_pincode").attr("disabled","disabled")

        $('#id_user').change(function() {
          $.ajax({
            type: 'GET',
            url: "/get_user_info/",
            data: {'user_id': $('#id_user').val()},
            success: function(data, _status) {
              $('#id_first_name').val(data.first_name);
              $('#id_last_name').val(data.last_name);             
               $('#id_email').val(data.email);
               $('#id_pincode').val(data.pincode);
           
            },
            dataType: "json"
          });               
        });
        
            $('#id_state').change(function() {
          $.ajax({
            type: 'GET',
            url: "/get_districts/",
            data: {'selected_state': $('#id_state').val()},
            success: function(data, _status) {
            
            	$('#id_district').find("option").remove().end();
            	$.each(data, function (index, item) {
                 $('#id_district').append($('<option></option>').val(item.id).html(item.name));
             });
              // $('#id_districts').val(data.first_name);
              // $('#id_last_name').val(data.last_name);             
               // $('#id_email').val(data.email);
               // ('#id_date_of_birth').val(data.dob);
               // $('#id_pincode').val(data.pincode);
//            
            },
            dataType: "json"
          });               
        });
        

        
      });




  $(function() {
  
  if($( "#datepicker" ).length)
    $( "#datepicker" ).datepicker();
  });


