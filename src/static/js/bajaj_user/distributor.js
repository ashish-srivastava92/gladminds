$(document).ready(function(){

// alert("hi");
url = "tritory.json"

            $.ajax({
                type: 'GET',
                url: url,
                data: { get_param: 'value' }, 
                dataType: 'json',
                success: function(result){
                	
                    
                    $(".territory").append("<option value='00'>Select</option>");

                    for(i=0;i<result.teritory.length;i++){
                        $(".territory").append('<option value="01">'+result.teritory[i].teritoryname+'</option>');
                    }
                    
                }

               });

url="userrole.json" 

// for getting userroles
$.ajax({
                type: 'GET',
                url: url,
                dataType: 'json',
                success: function(result){
                    console.log(result);
                    var userole = result[0].role;
                    console.log(userole);
                    filter(userole);    
                }

               });



function filter(userole)
{       
        if(userole=="asm")
        {
            document.getElementById("myStacked").children[0].style.display = "none"
        }
        if(userole=="distributor")
        {            
            document.getElementById("myStacked").children[0].style.display = "none"
            document.getElementById("myStacked").children[1].style.display = "none"
        }
        if(userole=="distributorsalesrep")
        {
            document.getElementById("myStacked").children[0].style.display = "none"
            document.getElementById("myStacked").children[1].style.display = "none"
            document.getElementById("myStacked").children[2].style.display = "none"      
        }
        if(userole="admin")
        {

        }
        if(userole=="")
        {

        }
        
}


// -------------------------upon clicking submit of retailer i am dealing with multiselect here---------------------------

$('#submit').click(function () {
        var selected1 = $("#mterritory_id option:selected");
        var message1 = "";
        selected1.each(function () {
            message1 +=  $(this).val() + ",";
            
        });
        str1 = message1.substring(0, message1.length - 1);
        
        console.log(str1);
     });   

$('#submit').click(function () {
        var selected2 = $("#mstate_id option:selected");
        var message2 = "";
        message2 += "["
        selected2.each(function () {

            message2 +=  $(this).val() + ",";
            
        });
        str2 = message2.substring(0, message2.length - 1);
        message2 += "]"
        console.log(str2);
     });  
 

$('#submit').click(function () {
        var selected3 = $("#mdsr_id option:selected");
        var message3 = "";
            message3 +=  "[";
        selected3.each(function () {
            message3+="\""
            message3 +=  $(this).val();
            message3+="\""
            message3+=","

        });
        

        str3 = message3.substring(0, message3.length - 1);

        str3+="]";
        console.log(str3);
     });   




  


$('#submit').click(function () {
        var selected4 = $("#mlocality_dropdown option:selected");
        var message4 = "";
            message4 +=  "[";
        selected4.each(function () {
            message4+="\""
            message4 +=  $(this).val();
            message4+="\""
            message4+=","

        });
        

        str4 = message4.substring(0, message4.length - 1);

        str4+="]";
        console.log(str4);
     });   

  
$('#submit').click(function () {
        var selected5 = $("#mdistrict_id option:selected");
        var message5 = "";
        selected5.each(function () {
            message5 +=  $(this).val() + ",";
            
        });
        str5 = message5.substring(0, message5.length - 1);
        
        console.log(str5);
     });   




$('#submit').click(function () {
        var selected6 = $("#mdistributor_ret_id option:selected");
        var message6 = "";
            message6 +=  "[";
        selected6.each(function () {
            message6+="\""
            message6 +=  $(this).val();
            message6+="\""
            message6+=","

        });
        

        str6 = message6.substring(0, message6.length - 1);

        str6+="]";
        console.log(str6);
     });   




// -------------------------upon clicking submit of dsp i am dealing with multiselect here---------------------------


$('#submit2').click(function () {
        var selected1 = $("#mterritory_id option:selected");
        var message1 = "";
        selected1.each(function () {
            message1 +=  $(this).val() + ",";
            
        });
        str1 = message1.substring(0, message1.length - 1);
        
        console.log(str1);
     });   


$('#submit2').click(function () {
        var selected7 = $("#distributor_dsr_id option:selected");
        var message7 = "";
            message7 +=  "[";
        selected7.each(function () {
            message7+="\""
            message7 +=  $(this).val();
            message7+="\""
            message7+=","

        });
        

        str7 = message7.substring(0, message7.length - 1);

        str7+="]";
        console.log(str7);
     });   




$('#submit2').click(function () {
        var selected2 = $("#mstate_id option:selected");
        var message2 = "";
        selected2.each(function () {
            message2 +=  $(this).val() + ",";
            
        });
        str2 = message2.substring(0, message2.length - 1);
        
        console.log(str2);
     });  








$('#submit2').click(function () {
        var selected3 = $("#mdsr_id option:selected");
        var message3 = "";
        selected3.each(function () {
            message3 +=  $(this).val() + ",";
            
        });
        str3 = message3.substring(0, message3.length - 1);
        
        console.log(str3);
     });   

$('#submit2').click(function () {
        var selected4 = $("#mlocality_dropdown option:selected");
        var message4 = "";
        selected4.each(function () {
            message4 +=  $(this).val() + ",";
            
        });
        str4 = message4.substring(0, message4.length - 1);
        
        console.log(str4);
     });   
  
$('#submit2').click(function () {
        var selected5 = $("#mdistrict_id option:selected");
        var message5 = "";
        selected5.each(function () {
            message5 +=  $(this).val() + ",";
            
        });
        str5 = message5.substring(0, message5.length - 1);
        
        console.log(str5);
     });   

$('#submit2').click(function () {
        var selected6 = $("#mdistributor_ret_id option:selected");
        var message6 = "";
        selected6.each(function () {
            message6+=  $(this).val() + ",";
            
        });
        str6 = message6.substring(0, message6.length - 1);
        
        console.log(str6);
     });   
    
        

// -------------------------upon clicking submit of ASM i am dealing with multiselect here---------------------------   

$('#submit3').click(function () {
        var selected1 = $("#mterritory_id option:selected");
        var message1 = "";
        selected1.each(function () {
            message1 +=  $(this).val() + ",";
            
        });
        str1 = message1.substring(0, message1.length - 1);
        
        console.log(str1);
     });   



$('#submit3').click(function () {
        var selected2 = $("#mstate_id option:selected");
        var message2 = "";
            message2 +=  "[";
        selected2.each(function () {
            message2+="\""
            message2 +=  $(this).val();
            message2+="\""
            message2+=","

        });
        

        str2 = message2.substring(0, message2.length - 1);

        str2+="]";
        console.log(str2);
     });




$('#submit3').click(function () {
        var selected8 = $("#nsm_id option:selected");
        console.log(selected8);
        var message8 = "";
            message8 +=  "[";
            console.log(message8);
        selected8.each(function () {
            message8+="\""
            message8 +=  $(this).val();
            message8+="\""
            message8+=","

        });
        
        console.log(message8);
        str8 = message8.substring(0, message8.length - 1);

        str8+="]";
        console.log(str8);
     });        



$('#submit3').click(function () {
        var selected3 = $("#mdsr_id option:selected");
        var message3 = "";
        selected3.each(function () {
            message3 +=  $(this).val() + ",";
            
        });
        str3 = message3.substring(0, message3.length - 1);
        
        console.log(str3);
     });   

$('#submit3').click(function () {
        var selected4 = $("#mlocality_dropdown option:selected");
        var message4 = "";
        selected4.each(function () {
            message4 +=  $(this).val() + ",";
            
        });
        str4 = message4.substring(0, message4.length - 1);
        
        console.log(str4);
     });   
  
$('#submit3').click(function () {
        var selected5 = $("#mdistrict_id option:selected");
        var message5 = "";
        selected5.each(function () {
            message5 +=  $(this).val() + ",";
            
        });
        str5 = message5.substring(0, message5.length - 1);
        
        console.log(str5);
     });   

$('#submit3').click(function () {
        var selected6 = $("#mdistributor_ret_id option:selected");
        var message6 = "";
        selected6.each(function () {
            message6+=  $(this).val() + ",";
            
        });
        str6 = message6.substring(0, message6.length - 1);
        
        console.log(str6);
     });   

// -------------------------upon clicking submit of ASM i am dealing with multiselect here---------------------------

$('#submit4').click(function () {
        var selected1 = $("#mterritory_id option:selected");
        var message1 = "";
            message1 +=  "[";
        selected1.each(function () {
            message1+="\""
            message1 +=  $(this).val();
            message1+="\""
            message1+=","

        });
        

        str1 = message1.substring(0, message1.length - 1);

        str1+="]";
        console.log(str1);
     });


$('#submit4').click(function () {
        var selected1 = $("#mterritory_id option:selected");
        var message1 = "";
            message1 +=  "[";
        selected1.each(function () {
            message1+="\""
            message1 +=  $(this).val();
            message1+="\""
            message1+=","

        });
        

        str1 = message1.substring(0, message1.length - 1);

        str1+="]";
        console.log(str1);
     });   

$('#submit4').click(function () {
        var selected2 = $("#mstate_id option:selected");
        var message2 = "";
        selected2.each(function () {
            message2 +=  $(this).val() + ",";
            
        });
        str2 = message2.substring(0, message2.length - 1);
        
        console.log(str2);
     });  
$('#submit4').click(function () {
        var selected3 = $("#mdsr_id option:selected");
        var message3 = "";
        selected3.each(function () {
            message3 +=  $(this).val() + ",";
            
        });
        str3 = message3.substring(0, message3.length - 1);
        
        console.log(str3);
     });   

$('#submit4').click(function () {
        var selected4 = $("#mlocality_dropdown option:selected");
        var message4 = "";
        selected4.each(function () {
            message4 +=  $(this).val() + ",";
            
        });
        str4 = message4.substring(0, message4.length - 1);
        
        console.log(str4);
     });   
  
$('#submit4').click(function () {
        var selected5 = $("#mdistrict_id option:selected");
        var message5 = "";
        selected5.each(function () {
            message5 +=  $(this).val() + ",";
            
        });
        str5 = message5.substring(0, message5.length - 1);
        
        console.log(str5);
     });   

$('#submit4').click(function () {
        var selected6 = $("#mdistributor_ret_id option:selected");
        var message6 = "";
        selected6.each(function () {
            message6+=  $(this).val() + ",";
            
        });
        str6 = message6.substring(0, message6.length - 1);
        
        console.log(str6);
     });   


// -------------------------upon clicking submit of distributor i am dealing with multiselect here---------------------------

$('#submit5').click(function () {
        var selected1 = $("#mterritory_id option:selected");
        var message1 = "";
        selected1.each(function () {
            message1 +=  $(this).val() + ",";
            
        });
        str1 = message1.substring(0, message1.length - 1);
        
        console.log(str1);
     });   




$('#submit5').click(function () {
        var selected2 = $("#mdstate_id option:selected");
        var message2 = "";
            message2 +=  "[";
        selected2.each(function () {
            message2+="\""
            message2 +=  $(this).val();
            message2+="\""
            message2+=","

        });
        str2 = message2.substring(0, message2.length - 1);
        str2+="]";
        console.log(str2);
     }); 

$('#submit5').click(function () {
        var selected7 = $("#asm_id option:selected");
        var message7 = "";
            message7 +=  "[";
        selected7.each(function () {
            message7+="\""
            message7 +=  $(this).val();
            message7+="\""
            message7+=","

        });
        str7 = message7.substring(0, message7.length - 1);
        str7+="]";
        console.log(str7);
     }); 


$('#submit5').click(function () {
        var selected3 = $("#mdsr_id option:selected");
        var message3 = "";
        selected3.each(function () {
            message3 +=  $(this).val() + ",";
            
        });
        str3 = message3.substring(0, message3.length - 1);
        
        console.log(str3);
     });   

$('#submit5').click(function () {
        var selected4 = $("#mlocality_dropdown option:selected");
        var message4 = "";
        selected4.each(function () {
            message4 +=  $(this).val() + ",";
            
        });
        str4 = message4.substring(0, message4.length - 1);
        
        console.log(str4);
     });   
  


$('#submit5').click(function () {
        var selected5 = $("#mddistrict_id option:selected");
        var message5 = "";
            message5 +=  "[";
        selected5.each(function () {
            message5+="\""
            message5 +=  $(this).val();
            message5+="\""
            message5+=","

        });
        str5 = message5.substring(0, message5.length - 1);
        str5+="]";
        console.log(str5);
     }); 





$('#submit5').click(function () {
        var selected6 = $("#mdistributor_ret_id option:selected");
        var message6 = "";
        selected6.each(function () {
            message6+=  $(this).val() + ",";
            
        });
        str6 = message6.substring(0, message6.length - 1);
        
        console.log(str6);
     });   







        
// ----------------------the below functionis for retailer(json)---------------------

$(document).on('submit','#UserDetails',function (e) {
        //e.preventDefault();
        var role = $('#role').val();
        alert(role);
        alert(map[role]);
        var data1="{";
        var other_data = $('#UserDetails').serializeArray();
        $.each(other_data,function(key,input){
            data1+="\""+input.name+"\":\""+input.value+"\"";
            data1+=",";
        });
        var file=$("#user_agreement").val();
         var file2=$("#user_agreement1").val();
         var file3=$("#user_agreement2").val();
         var file4 = str1;
         var file5 = str2;
         var file6 = str3;
         var file7 = str4;
         var file8 = str5;
         var file9 = str6;

        data1+="\"user_agreement\":\""+file+"\"";
         data1+=",";
         data1+="\"user_agreement1\":\""+file2+"\"";
         data1+=",";
         data1+="\"user_agreement2\":\""+file3+"\"";
         data1+=",";
         // data1+="\"mterritory_id\":\""+file4+"\"";
         // data1+=",";
         // data1+="\"mstate_id\":\""+file5+"\"";
         // data1+=",";
         data1+="\"mdsr_id\":"+file6+"";
         data1+=",";
         data1+="\"mlocality_dropdown\":"+file7+"";
         data1+=",";
         // data1+="\"mdistrict_id\":\""+file8+"\"";
         // data1+=",";
         data1+="\"mdistributor_ret_id\":"+file9+"";
        data1+="}";
        data1 = JSON.stringify(data1);
        var data2 = JSON.parse(data1);
        console.info(data2);
        return false;
       
        
        

        $.ajax({
            url: map[role],
            type: 'POST',
            
            data:data2,
            
            success: function(data) {
                alert(data.message)
                location.href = "/add_users"
            },
            
            
        
        }); 
    });

// ----------------------------the below function is for dsp(json)-------------------------
// $('#submit2').click(function (e) {
 function submi2()
    {
        //e.preventDefault();
        var role = $('#role').val();
        alert(role);
        alert(map[role]);
        var data1="{";
        var other_data = $('#UserDetails2').serializeArray();
        $.each(other_data,function(key,input){
            data1+="\""+input.name+"\":\""+input.value+"\"";
            data1+=",";
        });
        var file=$("#user_agreement").val();
         var file2=$("#user_agreement1").val();
         var file3=$("#user_agreement2").val();
         var file4 = str1;
         var file5 = str2;
         var file6 = str3;
         var file7 = str4;
         var file8 = str5;
         var file9 = str6;
         var file10 = str7;

        data1+="\"user_agreement\":\""+file+"\"";
         data1+=",";
         data1+="\"user_agreement1\":\""+file2+"\"";
         data1+=",";
         data1+="\"user_agreement2\":\""+file3+"\"";
         data1+=",";
         // data1+="\"mterritory_id\":\""+file4+"\"";
         // data1+=",";
         // data1+="\"mstate_id\":\""+file5+"\"";
         // data1+=",";
         // data1+="\"mdsr_id\":\""+file6+"\"";
         // data1+=",";
         // data1+="\"mlocality_dropdown\":\""+file7+"\"";
         // data1+=",";
         // data1+="\"mdistrict_id\":\""+file8+"\"";
         // data1+=",";
         // data1+="\"mdistributor_ret_id\":\""+file9+"\"";
         // data1+=",";
         data1+="\"mdistributor_id\":"+file10+"";
        data1+="}";
        data1 = JSON.stringify(data1);
        var data2 = JSON.parse(data1);
        console.info(data2);
        return false;
       
        
        

                                $.ajax({
                                    url: map[role],
                                    type: 'POST',
                                    
                                    data:data2,
                                    
                                    success: function(data) {
                                        alert(data.message)
                                        location.href = "/add_users"
                                    },
                                    
                                    
                                
                                }); 
    }


// -----------------------------------the below function is for ASM(json)----------------
function submi3(){
    
        //e.preventDefault();
        var role = $('#role').val();
        alert(role);
        alert(map[role]);
        var data1="{";
        var other_data = $('#UserDetails3').serializeArray();
        $.each(other_data,function(key,input){
            data1+="\""+input.name+"\":\""+input.value+"\"";
            data1+=",";
        });
        var file=$("#user_agreement").val();
         var file2=$("#user_agreement1").val();
         var file3=$("#user_agreement2").val();
         var file4 = str1;
         var file5 = str2;
         var file6 = str3;
         var file7 = str4;
         var file8 = str5;
         var file9 = str6;
         var file10 = str8;

        data1+="\"user_agreement\":\""+file+"\"";
         data1+=",";
         data1+="\"user_agreement1\":\""+file2+"\"";
         data1+=",";
         data1+="\"user_agreement2\":\""+file3+"\"";
         data1+=",";
         // data1+="\"mterritory_id\":\""+file4+"\"";
         // data1+=",";
         data1+="\"mstate_id\":"+file5+"";
         data1+=",";
         // data1+="\"mdsr_id\":\""+file6+"\"";
         // data1+=",";
         // data1+="\"mlocality_dropdown\":\""+file7+"\"";
         // data1+=",";
         // data1+="\"mdistrict_id\":\""+file8+"\"";
         // data1+=",";
         // data1+="\"mdistributor_ret_id\":\""+file9+"\"";
         // data1+=",";
         data1+="\"mnsm_id\":"+file10+"";
        data1+="}";
        data1 = JSON.stringify(data1);
        var data2 = JSON.parse(data1);
        console.info(data2);
        return false;
       
        
        

                                $.ajax({
                                    url: map[role],
                                    type: 'POST',
                                    
                                    data:data2,
                                    
                                    success: function(data) {
                                        alert(data.message)
                                        location.href = "/add_users"
                                    },
                                    
                                    
                                
                                }); 
    }
// -----------------------------------the below function us for NSM(json)-------------------------
function submi4()
    {
        //e.preventDefault();
        var role = $('#role').val();
        alert(role);
        alert(map[role]);
        var data1="{";
        var other_data = $('#UserDetails4').serializeArray();
        $.each(other_data,function(key,input){
            data1+="\""+input.name+"\":\""+input.value+"\"";
            data1+=",";
        });
        var file=$("#user_agreement").val();
         var file2=$("#user_agreement1").val();
         var file3=$("#user_agreement2").val();
         var file4 = str1;
         var file5 = str2;
         var file6 = str3;
         var file7 = str4;
         var file8 = str5;
         var file9 = str6;

        data1+="\"user_agreement\":\""+file+"\"";
         data1+=",";
         data1+="\"user_agreement1\":\""+file2+"\"";
         data1+=",";
         data1+="\"user_agreement2\":\""+file3+"\"";
         data1+=",";
         data1+="\"mterritory_id\":"+file4+"";
         // data1+=",";
         // data1+="\"mstate_id\":\""+file5+"\"";
         // data1+=",";
         // data1+="\"mdsr_id\":\""+file6+"\"";
         // data1+=",";
         // data1+="\"mlocality_dropdown\":\""+file7+"\"";
         // data1+=",";
         // data1+="\"mdistrict_id\":\""+file8+"\"";
         // data1+=",";
         // data1+="\"mdistributor_ret_id\":\""+file9+"\"";
        data1+="}";
        data1 = JSON.stringify(data1);
        var data2 = JSON.parse(data1);
        console.info(data2);
        return false;
       
        
        

                                $.ajax({
                                    url: map[role],
                                    type: 'POST',
                                    
                                    data:data2,
                                    
                                    success: function(data) {
                                        alert(data.message)
                                        location.href = "/add_users"
                                    },
                                    
                                    
                                
                                }); 
    }
// --------------------the below function is for distibutor---------------------------------
function submi5()
    {
        //e.preventDefault();
        var role = $('#role').val();
        alert(role);
        alert(map[role]);
        var data1="{";
        var other_data = $('#UserDetails5').serializeArray();
        $.each(other_data,function(key,input){
            data1+="\""+input.name+"\":\""+input.value+"\"";
            data1+=",";
        });
        var file=$("#user_agreement").val();
         var file2=$("#user_agreement1").val();
         var file3=$("#user_agreement2").val();
         var file4 = str1;
         var file5 = str2;
         var file6 = str3;
         var file7 = str4;
         var file8 = str5;
         var file9 = str6;
         var file10 = str7;
        data1+="\"user_agreement\":\""+file+"\"";
         data1+=",";
         data1+="\"user_agreement1\":\""+file2+"\"";
         data1+=",";
         data1+="\"user_agreement2\":\""+file3+"\"";
         data1+=",";
         // data1+="\"mterritory_id\":\""+file4+"\"";
         // data1+=",";
         data1+="\"mstate_id\":"+file5+"";
         data1+=",";
         // data1+="\"mdsr_id\":\""+file6+"\"";
         // data1+=",";
         // data1+="\"mlocality_dropdown\":\""+file7+"\"";
         // data1+=",";
         data1+="\"mdistrict_id\":"+file8+"";
         data1+=",";
         // data1+="\"mdistributor_ret_id\":\""+file9+"\"";
         // data1+=",";
         data1+="\"asm_id\":"+file10+"";
        data1+="}";
        data1 = JSON.stringify(data1);
        var data2 = JSON.parse(data1);
        console.info(data2);
        return false;
       
        
        

                                $.ajax({
                                    url: map[role],
                                    type: 'POST',
                                    
                                    data:data2,
                                    
                                    success: function(data) {
                                        alert(data.message)
                                        location.href = "/add_users"
                                    },
                                    
                                    
                                
                                }); 
    }

// -----------------------------------------start of new code--------------------




// ------------------------------------------------ending---------
 });