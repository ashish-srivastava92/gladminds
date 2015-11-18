
      $(document).ready(function() {
      	
		$("#id_first_name, #id_last_name, #id_email, #id_pincode").attr("disabled","disabled")

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
        
            $('#id_states').change(function() {
          $.ajax({
            type: 'GET',
            url: "/get_districts/",
            data: {'selected_state': $('#id_states').val()},
            success: function(data, _status) {
            	$('#id_districts').find("option").remove().end();
            	$.each(data, function (index, item) {
                 $('#id_districts').append($('<option></option>').val(item.city).html(item.city));
             });
              $('#id_districts').val(data.first_name);
              $('#id_last_name').val(data.last_name);             
               $('#id_email').val(data.email);
               $('#id_pincode').val(data.pincode);
           
            },
            dataType: "json"
          });               
        });
        

        
      });

