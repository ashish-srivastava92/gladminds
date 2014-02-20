var ipaddress = "http://rkarthik.in/mobile/gm/";
//var ipaddress = "http://localhost/gm/";
var loader = new Image(); 
loader.src="images/ajax-loader.gif";

function showLoading(){
    $("#loading").show();
}

function hideLoading(){
    $("#loading").hide();
}


function enableFormsInIscroll(){
  [].slice.call(document.querySelectorAll('input, select, button, textarea')).forEach(function(el){
    el.addEventListener(('ontouchstart' in window)?'touchstart':'mousedown', function(e){
      e.stopPropagation();
    })
  })
}

mycallback = function(jsonObj){

	data = $.parseJSON(jsonObj);
	hideLoading();
	if(data.status=="0"){
		$(".login-screen .alert").removeClass("alert-success").addClass("alert-error").html("Incorrect Username or Password!").show();
		$("#username").focus();
		//alert("no")
	}
	else{

        localStorage.setItem("userid", data.id);
        localStorage.setItem("username", data.username);
        localStorage.setItem("unique_id", data.unique_id);
		$(".login-screen .alert").removeClass("alert-error").addClass("alert-success").html("Login success. Please wait while you are redirected").show();
		$.mobile.changePage( '#dashboard', {transition: 'flip'});
		//document.location.href="index.php";
	}
};

regCallBack = function(jsonObj){

	data = $.parseJSON(jsonObj);
	hideLoading();
	if(data.status=="0" || data.status=="2"){

		$(".alert").removeClass("alert-error").addClass("alert-error").html(data.message).show();

		if(data.status =="2"){
			$("#frmRegister #txtEmail").focus();
		}
		
		return false;
	}
	else{

        localStorage.setItem("userid", data.id);
        localStorage.setItem("username", data.username);
        localStorage.setItem("unique_id", data.unique_id);
		$(".alert").removeClass("alert-error").addClass("alert-success").html(data.message).show();
		$("#after-buy .success-key").html(data.unique_id);
		$.mobile.changePage( '#after-buy', {transition: 'slide'});
		//document.location.href="index.php";
	}

};

function testPost(form,cbfunction)
{
	// console.log($(form).serialize())
    postCORS(ipaddress+'loginCheck.php', $(form).serialize(), cbfunction);
} 

function testGet(str,cbfunction){
	getCORS(ipaddress+'getData.php', str, cbfunction);
}

function populateStates(data){
	hideLoading();
	$('#txtState').find('option').remove();
	$('#txtState').append("<option value=''>Select State</option>");
	if(!data==""){
		stateArray = data.split(",");
		 jQuery.each(stateArray, function() {
			 $('#txtState').append("<option value='"+this+"'>"+this+"</option>");
		 });
	}
}

function populateProfile(data){
	hideLoading();
	if(!data==""){
		data = $.parseJSON(data);
		localStorage.setItem("username",data.name);
		$("#pr_name").html(data.name); 
		$("#pr_email").html("<a href='mailto:"+data.email+"'>"+data.email+"</a>");
		$("#pr_mobile").html(data.mobile);
		$("#pr_address").html(data.address);
		$("#pr_country").html((data.country).toUpperCase());
		$("#pr_state").html(data.state);
		$("#pr_dob").html(data.dob);

		if(data.gender=="1")
			$("#pr_gender").html("Male");

		if(data.gender=="2")
			$("#pr_gender").html("female");

		$("#pr_interests").html(data.Interests);

		$("#span_username_profile").html(localStorage.getItem("username"));
		$("#span_unique_id_profile").html(localStorage.getItem("unique_id"));

	}
}

function populate_edit(data){
	
	populateStates_edit(data);
	showLoading();

	getCORS(ipaddress+'getData.php?action=getProfile&unique_id='+localStorage.getItem("unique_id"), null, showEditSettings);
}

function populateStates_edit(data){
	$('#txt_state').find('option').remove();
	$('#txt_state').append("<option value=''>Select State</option>");
	if(!data==""){
		stateArray = data.split(",");
		 jQuery.each(stateArray, function() {
			 $('#txt_state').append("<option value='"+this+"'>"+this+"</option>");
		 });
	}
	hideLoading();
}


/*
editReturn = function(jsonObj){

	data = $.parseJSON(jsonObj);
	hideLoading();
	if(data.status=="0" || data.status=="2"){

		alert(data.message);
		return false;
	}
	else{
		showLoading();
		//getCORS(ipaddress+'getData.php?action=getProfile&unique_id='+localStorage.getItem("unique_id"), null, populateProfile);

		$.mobile.changePage( '#myprofile', {transition: 'slide'});
		//document.location.href="index.php";
	}

};
*/

function showEditSettings(data){
	

	if(!data==""){
		data = $.parseJSON(data);
		$("#editForm #userID").val(localStorage.getItem("userid"));
		$("#txt_name").val(data.name);
		$("#txt_dob").val(data.dob);
		$("#txt_email").val(data.email);
		$("#txt_mob").val(data.mobile);
		$("#txt_gender").val(data.gender);
		$("#txt_address").val(data.address);
		$("#txt_country").val(data.country);
		$("#txt_state").val(data.state);
		$("#txt_interest").val(data.Interests);

		

	}
	hideLoading();
}

function showConfirmation(data){
	hideLoading();
	data = $.parseJSON(data);

		status = data.status;
		if(status==1){
			alert("Thank you very much for your interest. Authorised person will contact you soon.");
			selRow.hide("slow");
			ncount = parseInt($(".notification-icon").html());
	 		if(ncount>0)
	 			$(".notification-icon").html(ncount-1);
		}
		else
			alert("Your request was not processed. Please try again later.");

	if(movePage){
		$.mobile.changePage( '#profile-page', {transition: 'slide'});
		movePage = 0;
	}

}
var selRow;
var movePage;

$(document).ready(function() {

	$("#feedbackForm .userID").val(localStorage.getItem("userid"));

	$("#btn_feedback").click(function(){
		$.mobile.changePage( '#profile-page', {transition: 'slide'});
	})

	$(".newPurchase").click(function(){

		interest_item = $(this).parent().parent().parent().find(".item-name").html() + "-" + $(this).parent().parent().find(".purchaseItem").html();
		selRow = $(this).closest(".item");

		showLoading();
		getCORS(ipaddress+'getData.php?action=itemPurchaseInterest&item="'+interest_item+'"&unique_id='+localStorage.getItem("unique_id"), null, showConfirmation);

	});

	$(".waranteeExtend").click(function(){
		warr_item = $(this).parent().parent().parent().find(".item-name").html();
		selRow = $(this).closest(".item");

		movePage = 0;
		if(warr_item==undefined){
			warr_item = $("a[rel='"+localStorage.getItem("itemID")+"']").closest(".item").find(".item-name").html();
			movePage=1;
		}

		showLoading();
		getCORS(ipaddress+'getData.php?action=waranteeExtend&item="'+warr_item+'"&unique_id='+localStorage.getItem("unique_id"), null, showConfirmation);

	});

	$(".insuranceExtend").click(function(){
		ins_item = $(this).parent().parent().parent().find(".item-name").html();
		selRow = $(this).closest(".item");

		movePage = 0;
		if(ins_item==undefined){
			ins_item = $("a[rel='"+localStorage.getItem("itemID")+"']").closest(".item").find(".item-name").html();
			movePage=1;
		}


		showLoading();
		getCORS(ipaddress+'getData.php?action=insuranceExtend&item="'+ins_item+'"&unique_id='+localStorage.getItem("unique_id"), null, showConfirmation);

	});

	 $(".btn_no").click(function(){
	 	selRow = $(this).closest(".item");
	 	if(confirm("Do you want to delete this Notification?")){
	 		selRow.hide("slow");
	 		ncount = parseInt($(".notification-icon").html());
	 		if(ncount>0)
	 			$(".notification-icon").html(ncount-1);
	 	}

	 });

	"use strict";
/*
	$("#edit_addNewItem").click(function(){
		showLoading();
		$("#addnewitem_userID").val(localStorage.getItem("userid"));
		// testPost($("#edit-adding-item-form"),addNewItemReturn);
		testPost($("#edit-adding-item-form"),function(){
			$.mobile.changePage( '#profile-page', {transition: 'slide'});
		});
		return false;
	});
*/

	$('#edit-adding-item-form').ajaxForm({
	    beforeSend: function() {
	    	//alert("dd")
	        $("#edit_addNewItem #addnewitem_userID").val(localStorage.getItem("userid"));
	        showLoading();
	        //alert($("#addnewitem_userID").val())
	        //percent.html(percentVal);
	    },
	    uploadProgress: function(event, position, total, percentComplete) {
	        // var percentVal = percentComplete + '%';
	        // barA.width(percentVal);
	        //percent.html(percentVal);
	    },
	    success: function(data, statusText, xhr) {


			data = $.parseJSON(data);

			if(data.status=="1"){
				hideLoading();
				$.mobile.changePage( '#profile-page', {transition: 'slide'});
			}
			else
				alert(data.message);


	    },
	    error: function(xhr, statusText, err) {
	    	alert(err || statusText);
	        //status.html(err || statusText);
	    }
	}); 


	"use strict";

	$('#adding-item-form').ajaxForm({
	    beforeSend: function() {
	    	//alert("dd")
	        $("#addnewitem_userID").val(localStorage.getItem("userid"));
	        showLoading();
	        //alert($("#addnewitem_userID").val())
	        //percent.html(percentVal);
	    },
	    uploadProgress: function(event, position, total, percentComplete) {
	        // var percentVal = percentComplete + '%';
	        // barA.width(percentVal);
	        //percent.html(percentVal);
	    },
	    success: function(data, statusText, xhr) {


			data = $.parseJSON(data);

			if(data.status=="1"){
				hideLoading();
				$.mobile.changePage( '#profile-page', {transition: 'slide'});
			}
			else
				alert(data.message);


	    },
	    error: function(xhr, statusText, err) {
	    	alert(err || statusText);
	        //status.html(err || statusText);
	    }
	}); 



	$(".csoon").click(function(){
		$(this).find("div").animate({opacity:1},100).animate({opacity:0},1000)
	})


	$(function () {
	    $('#profilePIC').fileupload({
	        // your options
	    });
	});

	//Redirect the user to login page if the session is out.
	if(localStorage.getItem("username")=="null" || localStorage.getItem("username")==null)
		$.mobile.changePage( '#signin-page', {transition: 'flip'});

	$("footer").html("<div class='release'><span>&alpha;</span>r</div><p>Copyright Â© 2013,  All Rights Reserved</p>");
	//Edit Profile 
	/*$("#editSave").click(function(){
		showLoading();
		$("#userID").val(localStorage.getItem("userid"));
		testPost($("#editForm"),editReturn);
		return false;
	});

*/


	"use strict";

	var barA = $('#editForm .bar');
	var percentA = $('#editForm .percent');
	var statusA = $('#editForm #status');
	   
	$('#editForm').ajaxForm({
	    beforeSend: function() {
	        status.empty();
	        var percentVal = '0%';
	        barA.width(percentVal);
	        showLoading();
	        //percent.html(percentVal);
	    },
	    uploadProgress: function(event, position, total, percentComplete) {
	        var percentVal = percentComplete + '%';
	        barA.width(percentVal);
	        //percent.html(percentVal);
	    },
	    success: function(data, statusText, xhr) {
	        var percentVal = '100%';
	        barA.width(percentVal);
	        //percent.html(percentVal);
	       
	        //status.html(xhr.responseText);

			data = $.parseJSON(data);
			hideLoading();
			if(data.status=="0" || data.status=="2"){

				alert(data.message);
				return false;
			}
			else{
				showLoading();
		        localStorage.setItem("thumbURL", data.thumbURL);
		        localStorage.setItem("sourceURL", data.sourceURL);

				$.mobile.changePage( '#myprofile', {transition: 'slide'});
				//document.location.href="index.php";
			}

	    },
	    error: function(xhr, statusText, err) {
	        status.html(err || statusText);
	    }
	}); 


	$('#feedbackForm').ajaxForm({
	    beforeSend: function() {
	    	$("#feedbackForm .userID").val(localStorage.getItem("userid"));
	        showLoading();
	        
	        //percent.html(percentVal);
	    },
	    uploadProgress: function(event, position, total, percentComplete) {
	        //var percentVal = percentComplete + '%';
	       // barA.width(percentVal);
	        //percent.html(percentVal);
	       
	    },
	    success: function(data, statusText, xhr) {
	      	//alert(data)
			data = $.parseJSON(data);
			hideLoading();
			if(data.status=="0" || data.status=="2"){

				alert(data.message);
				return false;
			}
			else{
				$.mobile.changePage( '#feedbackThanks', {transition: 'slide'});
			}

	    },
	    error: function(xhr, statusText, err) {
	        status.html(err || statusText);
	    }
	}); 



	$("#adding-item #ai_txtManufacturer").change(function(){
		// alert($(this).val())
		if($(this).val()==0){
			$("#addItem_other").css("display","block");
			$("#ai_txtmanufacturer").focus();
		}
		else
			$("#addItem_other").css("display","none");
	})

	

/*
	$("#edit_addNewItem").click(function(){
		showLoading();
		$("#addnewitem_userID").val(localStorage.getItem("userid"));
		// testPost($("#edit-adding-item-form"),addNewItemReturn);
		testPost($("#edit-adding-item-form"),function(){
			$.mobile.changePage( '#profile-page', {transition: 'slide'});
		});
		return false;
	});
*/

	//Load states on change of country dropdown in registerpage.
	$("#txtCountry").change(function(){
			showLoading();
			getCORS(ipaddress+'getData.php?action=getStates&cID='+$(this).val(), null, populateStates);
	});

	//Load states on change of country dropdown in Edit Profile.
	$("#txt_country").change(function(){
			showLoading();
			getCORS(ipaddress+'getData.php?action=getStates&cID='+$(this).val(), null, populateStates_edit);
	});

	$(document).on("click", "#Login", function() {
		showLoading();
		if($("#txtUsername").val()==""){
			alert("Please enter username");
			$("#txtUsername").focus();
			hideLoading();
			return false;
		}

		if($("#txtPassword").val()==""){
			alert("Please enter password");
			$("#txtPassword").focus();
			hideLoading();
			return false;
		}


		testPost($("#loginForm"),mycallback);
		return false;
	});


/*
	$(document).on("click", "#btn_reg_submit", function() {
		errored = false;

		$("#frmRegister #txtName,#frmRegister #txtEmail,#frmRegister #txtMobile,#frmRegister #txtPassword,#frmRegister #txtAddress,#frmRegister #txtCountry,#frmRegister #txtState").removeClass("error");

		if($("#frmRegister #txtPassword").val()==$("#frmRegister #txtConfirmPassword").val()){
			
			$("#frmRegister #txtName,#frmRegister #txtEmail,#frmRegister #txtMobile,#frmRegister #txtPassword,#frmRegister #txtAddress,#frmRegister #txtCountry,#frmRegister #txtState").each(function() {
				if($(this).val() === ""){
			   			$(this).addClass("error");
			   			errored = true;
			   		}
				});
			
			if(!errored){
				showLoading();
				//testPost($("#frmRegister"),regCallBack);
			}
			
			return false;
		}
		else
		{
			alert("Passwords donot match");
			$("#txtPassword, #txtConfirmPassword").addClass("error");
			$("#txtPassword").focus();
		}
		return false;
	});
*/



	"use strict";

	var bar = $('.bar');
	var percent = $('.percent');
	var status = $('#status');
	   
	$('#frmRegister').ajaxForm({
	    beforeSend: function() {
	        status.empty();
	        var percentVal = '0%';
	        bar.width(percentVal);
	        showLoading();
	        //percent.html(percentVal);
	    },
	    uploadProgress: function(event, position, total, percentComplete) {
	        var percentVal = percentComplete + '%';
	        bar.width(percentVal);
	        //percent.html(percentVal);
	    },
	    success: function(data, statusText, xhr) {
	        var percentVal = '100%';
	        bar.width(percentVal);
	        //percent.html(percentVal);
	       
	        //status.html(xhr.responseText);

	        data = $.parseJSON(xhr.responseText);

			hideLoading();
			if(data.status=="0" || data.status=="2"){

				$(".alert").removeClass("alert-error").addClass("alert-error").html(data.message).show();

				if(data.status =="2"){
					$("#frmRegister #txtEmail").focus();
				}
				
				return false;
			}
			else{

		        localStorage.setItem("userid", data.id);
		        localStorage.setItem("username", data.username);
		        localStorage.setItem("unique_id", data.unique_id);
		       
		        localStorage.setItem("thumbURL", data.thumbURL);
		        localStorage.setItem("sourceURL", data.sourceURL);
		        
		        //$(".profile").attr("src",ipaddress+data.thumbURL);


				$(".alert").removeClass("alert-error").addClass("alert-success").html(data.message).show();
				$("#after-buy .success-key").html(data.unique_id);
				$.mobile.changePage( '#after-buy', {transition: 'slide'});
				//document.location.href="index.php";
			}



	    },
	    error: function(xhr, statusText, err) {
	        status.html(err || statusText);
	    }
	}); 
	
})



function confirmLogout(){
	z = confirm("Do you really want to logout?");
	if(z){
		showLoading();
		getCORS(ipaddress+'logout.php?action=getProfile&unique_id='+localStorage.getItem("unique_id"), null, redirectToLogin);

	}
}

function showSideBar(){
	$('#container').animate({
		'right': '200px'
	}, 250);

	$('[data-role*="header"]').animate({
		'right': '200px'
	}, 250);

	$('[data-role*="footer"]').animate({
		'margin-left': '-200px'
	}, 250);
}

function hideSideBar(){
	$('#container').animate({
		'right': '0px'
	}, 200);

	$('[data-role*="header"]').animate({
		'right': '0px'
	}, 200);

	$('[data-role*="footer"]').animate({
		'margin-left': '0px'
	}, 200);	
}

function redirectToLogin(){

	// $('#container').removeClass('active').addClass("activeOff");

	hideSideBar();

	localStorage.setItem("userid", null);
	localStorage.setItem("username", null);
	localStorage.setItem("unique_id", null);
	$(".alert-success").hide();
	hideLoading();
	$.mobile.changePage( '#signin-page', {transition: 'flip'});
}




$('#signin-page').on('pagebeforeshow',function(event, ui)
{
 	
	if(localStorage.getItem("username")=="null" || localStorage.getItem("username")==null)
		$("#txtUsername").focus();
	else
		$.mobile.changePage( '#dashboard', {transition: 'flip'});
		
});


$('#dashboard').on('pagebeforeshow',function(event, ui)
{
	$("#span_username").html(localStorage.getItem("username"));
	$("#span_unique_id").html(localStorage.getItem("unique_id"));
	$("#txtPassword").val("");
	$("#txtUsername").val("");
	$("#dashboard .profile").attr("src",ipaddress+localStorage.getItem("thumbURL"));
});

$('#notification-page').on('pagebeforeshow',function(event, ui)
{
	$("#notification-page #span_username").html(localStorage.getItem("username"));
	$("#notification-page #span_unique_id").html(localStorage.getItem("unique_id"));
	if(myScroll)
		myScroll.refresh();
});


$('#item-insurance-check').on('pagebeforeshow',function(event, ui)
{
   	$("#profile-page .sp_username").html(localStorage.getItem("username"));
	$("#profile-page .sp_unique_id").html(localStorage.getItem("unique_id"));
});


//My Items Listing Page
$('#profile-page').on('pagebeforeshow',function(event, ui)
{
	showLoading();

   	$("#profile-page .sp_username").html(localStorage.getItem("username"));
	$("#profile-page .sp_unique_id").html(localStorage.getItem("unique_id"));
	getCORS(ipaddress+'getData.php?action=getmyItems&unique_id='+localStorage.getItem("unique_id"), null, listMyItems);



});


function myItemPageChange(obj){
	localStorage.setItem("itemID",$(obj).attr("rel"));
	localStorage.setItem("itemName",$(obj).attr("itemname"));
	$.mobile.changePage( $(obj).attr("pgname"), {transition: 'slide'});

}

function listMyItems(data){
	
	if(!data==""){
		data = $.parseJSON(data);
		//alert(data.myitems);
		myitems = data.myitems;

		if(myitems.length==0){
			//$("#profile-page .profile_items").html('<h4 class="center"><span>&#9786;</span> No Items in your List. Click <a href="#adding-item" data-transition="slide"><img src="images/more.png" alt="My Profile" style="display:inline;"></a> Button to add your items.</h4>');
		}
		else{
			str="";
			for(i=0;i<myitems.length;i++){
				if($('.item').hasClass('item-'+myitems[i].id)){
					$('.item-'+myitems[i].id).remove();
				}
				
					str +='<div class="item item-' + myitems[i].id + '">\
		               <h3 class="item-name">'+myitems[i].Product+'</h3>\
		               <ul class="unstyled clearfix">\
		                  <li class="item-icon"><a href="#" onclick="javascript:myItemPageChange(this)" pgname="#item-details" rel="'+myitems[i].id+'" data-transition="slide"><img src="images/item-icon1.png" alt=""></a></li>\
		                  <li><a href="#" onclick="javascript:myItemPageChange(this)" pgname="#item-insurance-check" rel="'+myitems[i].id+'" itemname="'+myitems[i].Product+'" data-transition="slide" data-role="none"><img src="images/insurance.png" alt=""><span>Insurance</span></a></li>\
		                  <li><a href="#" onclick="javascript:myItemPageChange(this)" pgname="#item-warranty-check" rel="'+myitems[i].id+'" itemname="'+myitems[i].Product+'" data-transition="slide" data-role="none"><img src="images/warranty.png" alt=""><span>Warranty</span></a></li>\
		                  <li><div class="comingsoon">Coming Soon</div><a href="#" data-role="none" class="csa"><img src="images/spares.png" alt=""><span>Spares</span></a></li>\
		                  <li><a href="#" data-role="none" rel="'+myitems[i].id+'" itemname="'+myitems[i].Product+'" onclick="javascript:editItem(this)"><img src="images/edit.png" alt=""><span>Edit</span></a></li>\
		                  <li><a href="#" data-role="none" rel="'+myitems[i].id+'" itemname="'+myitems[i].Product+'" onclick="javascript:deleteItem(this)"><img src="images/delete.png" alt=""><span>Delete</span></a></li>\
		               </ul>\
		            </div>';
			}
			$("#profile-page #scroller1").prepend(str);

			$(".csa").click(function(){

				$(this).parent().find(".comingsoon").animate({opacity:1},100).animate({opacity:0},1000)

			});
			if(myScroll1)
				myScroll1.refresh();

		}
	}


	hideLoading();

}

function deleteItem(obj){
	z = confirm("Are you sure you want to delete "+$(obj).attr("itemname")+"?");
	if(z){
		showLoading();
		getCORS(ipaddress+'getData.php?action=deleteRec&itemID='+$(obj).attr("rel"), null, function(data){
			//debugger;
			data = $.parseJSON(data);
			//alert(data.status)
			if(data.status==1){
				getCORS(ipaddress+'getData.php?action=getmyItems&unique_id='+localStorage.getItem("unique_id"), null, listMyItems);
				$(obj).parents('.item').remove();
			}
			else{
				alert("Error removing your item. Please try again later.")
				hideLoading();
			}
		});
	}
	else
		return false;
}


isAdded_editmyItem = false;

function editItem(obj){
	showLoading();
	$("#edit-adding-item-form")[0].reset();
	if(navigator.onLine){
		
		getCORS(ipaddress+'getData.php?action=getProducts', null, function(data){
			//alert(isAdded_editmyItem)
			if(!(isAdded_editmyItem)){
				isAdded_editmyItem = true;
				data = $.parseJSON(data);
				prdData = data.Products;


				manufacturers = data.manufacturers;
				for(i=0;i<manufacturers.length;i++){
					$("#edit-adding-item #ai_txtManufacturer").append('<option value="'+manufacturers[i].id+'">'+manufacturers[i].manufacturer+'</option>');
				}

				$("#edit-adding-item #ai_txtManufacturer").append('<option value="0">Others</option>')

				prdData = prdData.split(",");
				var availableTags = prdData ;
				$( "#edit-adding-item #ai_txtProduct" ).autocomplete({
					source: availableTags
				});
			}

			getCORS(ipaddress+'getData.php?action=fetchRec&itemID='+$(obj).attr("rel"), null, function(data){
				//debugger;
				data = $.parseJSON(data);
				//alert(data.status)
				if(data.status==1){

					userid  	= data.userid;
					pr_name		= data.pr_name;
					m_id  		= data.m_id;
					item_num  	= data.item_num;
					pur_date  	= data.pur_date;
					purchased_from 	= data.purchased_from;
					seller_email	= data.seller_email;
					seller_phone	= data.seller_phone;
					warranty_yrs  = data.warranty_yrs;
					insurance_yrs  = data.insurance_yrs;

					invoice_URL  = data.invoice_URL;
					warranty_URL  = data.warranty_URL;
					insurance_URL  = data.insurance_URL;



					if(!invoice_URL=="")
						$("#edit-adding-item .add-invoice .epthumbnail img").attr("src",ipaddress+invoice_URL);

					if(!warranty_URL=="")
						$("#edit-adding-item .add-warranty .epthumbnail img").attr("src",ipaddress+warranty_URL);

					if(!insurance_URL=="")
						$("#edit-adding-item .add-insurance .epthumbnail img").attr("src",ipaddress+insurance_URL);


					
					
					$("#edit-adding-item #edit-addnewitem_ID").val($(obj).attr("rel"))
					$("#edit-adding-item #ai_txtProduct").val(pr_name);
					$("#edit-adding-item #ai_txtManufacturer").val(m_id);

					$("#edit-adding-item #ai_txtitem-no").val(item_num);
					$("#edit-adding-item #ai_txtpur-date").val(pur_date);
					$("#edit-adding-item #ai_txtpurchased-from").val(purchased_from);
					$("#edit-adding-item #ai_txtseller-email").val(seller_email);
					$("#edit-adding-item #ai_txtseller-phone").val(seller_phone);
					$("#edit-adding-item #ai_txtwarranty").val(warranty_yrs);
					$("#edit-adding-item #ai_txtinsurance").val(insurance_yrs);

					$('#edit-adding-item .sp_username').html(localStorage.getItem("username"));
					$('#edit-adding-item .unique_id').html(localStorage.getItem("unique_id"));





					$.mobile.changePage( "#edit-adding-item", {transition: 'slide'});
					hideLoading();
				}
				else{
					alert("Error fetching data. Please try again later.")
					hideLoading();
				}
			});




	});
	


		
}
}





$('#item-warranty-check').on('pagebeforeshow',function(event, ui)
{
	showLoading();
	$('#item-warranty-check .sp_username').html(localStorage.getItem("username"));
	$('#item-warranty-check .unique_id').html(localStorage.getItem("unique_id"));
	$('#item-warranty-check .item-name-heading').html(localStorage.getItem("itemName"));
	
	itemID = localStorage.getItem("itemID");

	if(itemID == "a1" || itemID == "a2" || itemID == "a3" || itemID == "a4"){
		data = '{"status" : "1","purchaseDate" : "2013-03-02","waranteeYear" : "1"}';
		warrantyCheck(data);
	}
	else
		getCORS(ipaddress+'getData.php?action=getWarantee&itemID='+localStorage.getItem("itemID"), null, warrantyCheck);



});


function warrantyCheck(data){
	data = $.parseJSON(data);

	if(data.status=="1"){
		var pdate 	= new Date(data.purchaseDate);
		var yr 		= data.waranteeYear;

		var myDate = new Date(pdate);
		myDate.setFullYear(myDate.getFullYear() + 1);
		myDate.setDate(myDate.getDate() - 1);


		var start = new Date();
		var diff = (new Date(myDate - start))/1000/60/60/24;
		var days = Math.round(diff);
		var hours = Math.floor(24 + ((diff - days)*24) + (new Date().getTimezoneOffset()/60));

		var strDays = 'days';
		if(days == 1)
		  strDays = 'day';

		console.log(days + ' ' + strDays + ' ' + hours + ' hours');
		$("#warrantee_days").html(days);
		$("#warrantee_hours").html(hours);
	}
	else{
		alert("No Data");
	}
	hideLoading();
}


$('#item-insurance-check').on('pagebeforeshow',function(event, ui)
{
	showLoading();
	$('#item-insurance-check .sp_username').html(localStorage.getItem("username"));
	$('#item-insurance-check .unique_id').html(localStorage.getItem("unique_id"));
	$('#item-insurance-check .item-name-heading').html(localStorage.getItem("itemName"));
	
	itemID = localStorage.getItem("itemID");

	if(itemID == "a1" || itemID == "a2" || itemID == "a3" || itemID == "a4"){
		data = '{"status" : "1","purchaseDate" : "2013-03-02","insuranceYear" : "1"}';
		insuranceCheck(data);
	}
	else
		getCORS(ipaddress+'getData.php?action=getInsurance&itemID='+localStorage.getItem("itemID"), null, insuranceCheck);



});

function insuranceCheck(data){
	data = $.parseJSON(data);

	if(data.status=="1"){
		var pdate 	= new Date(data.purchaseDate);
		var yr 		= data.insuranceYear;

		var myDate = new Date(pdate);
		myDate.setFullYear(myDate.getFullYear() + 1);
		myDate.setDate(myDate.getDate() - 1);


		var start = new Date();
		var diff = (new Date(myDate - start))/1000/60/60/24;
		var days = Math.round(diff);
		var hours = Math.floor(24 + ((diff - days)*24) + (new Date().getTimezoneOffset()/60));

		var strDays = 'days';
		if(days == 1)
		  strDays = 'day';

		console.log(days + ' ' + strDays + ' ' + hours + ' hours');
		$("#insurance_days").html(days);
		$("#insurance_hours").html(hours);
	}
	else{
		alert("No Data");
	}
	hideLoading();
}

$('#item-details').on('pagebeforeshow',function(event, ui)
{
	showLoading();

	//alert(itemID);

	hideLoading();


});

$('#myprofile').on('pagebeforeshow',function(event, ui)
{
	showLoading();

	$("#myprofile .profile").attr("src",ipaddress+localStorage.getItem("thumbURL"));
	$("#myprofile #span_username_profile").html(localStorage.getItem("username"));
	$("#myprofile #span_unique_id_profile").html(localStorage.getItem("unique_id"));

	getCORS(ipaddress+'getData.php?action=getProfile&unique_id='+localStorage.getItem("unique_id"), null, populateProfile);


});
isAdded_myItem = false;

$('#warranty-check-conf').on('pagebeforeshow',function(event, ui){
   	$("#warranty-check-conf .sp_username").html(localStorage.getItem("username"));
	$("#warranty-check-conf .sp_unique_id").html(localStorage.getItem("unique_id"));

});
$('#feedback').on('pagebeforeshow',function(event, ui){
   	$("#feedback .sp_username").html(localStorage.getItem("username"));
	$("#feedback .sp_unique_id").html(localStorage.getItem("unique_id"));

});
$('#item-details-des').on('pagebeforeshow',function(event, ui){
   	$("#item-details-des .sp_username").html(localStorage.getItem("username"));
	$("#item-details-des .sp_unique_id").html(localStorage.getItem("unique_id"));

});
$('#installation-complete').on('pagebeforeshow',function(event, ui){
   	$("#installation-complete .sp_username").html(localStorage.getItem("username"));
	$("#installation-complete .sp_unique_id").html(localStorage.getItem("unique_id"));

});
$('#add-new-item').on('pagebeforeshow',function(event, ui){
   	$("#add-new-item .sp_username").html(localStorage.getItem("username"));
	$("#add-new-item .sp_unique_id").html(localStorage.getItem("unique_id"));

});

$('#edit-adding-item').on('pageaftershow',function(event, ui){

			if(myScroll3)
				myScroll3.refresh();
});

$('#insurance-check-conf').on('pagebeforeshow',function(event, ui){
   	$("#insurance-check-conf .sp_username").html(localStorage.getItem("username"));
	$("#insurance-check-conf .sp_unique_id").html(localStorage.getItem("unique_id"));

});

$('#feedbackThanks').on('pagebeforeshow',function(event, ui){
	$("#feedbackForm")[0].reset();
   	$("#feedbackThanks .sp_username").html(localStorage.getItem("username"));
	$("#feedbackThanks .sp_unique_id").html(localStorage.getItem("unique_id"));

});


$('#adding-item').on('pagebeforeshow',function(event, ui){

	$("#adding-item-form")[0].reset();
   	$("#addnewitem_userID").val(localStorage.getItem("userid"));
   	$("#adding-item .sp_username").html(localStorage.getItem("username"));
	$("#adding-item .sp_unique_id").html(localStorage.getItem("unique_id"));

	if(navigator.onLine && !(isAdded_myItem)){
		getCORS(ipaddress+'getData.php?action=getProducts', null, function(data){

			data = $.parseJSON(data);
			prdData = data.Products;


			manufacturers = data.manufacturers;
			for(i=0;i<manufacturers.length;i++){
				$("#adding-item #ai_txtManufacturer").append('<option value="'+manufacturers[i].id+'">'+manufacturers[i].manufacturer+'</option>');
			}

			$("#adding-item #ai_txtManufacturer").append('<option value="0">Others</option>')

			prdData = prdData.split(",");
			var availableTags = prdData ;
			$( "#adding-item #ai_txtProduct" ).autocomplete({
				source: availableTags
			});

		});
		isAdded_myItem = true;


			if(myScroll2)
				myScroll2.refresh();


	}
});

$('#user-settings').on('pagebeforeshow',function(event, ui){

	showLoading();
	$("#editForm")[0].reset();
	$(".epthumbnail img").attr("src",ipaddress+localStorage.getItem("sourceURL"));
	$("#txt_country").val("india");

	getCORS(ipaddress+'getData.php?action=getStates&cID=india', null, populate_edit);
});

//SideBar Pages
$('#feedback').on('pagebeforeshow',function(event, ui){
   	hideSideBar();   	
});

$('#user-settings').on('pagebeforeshow',function(event, ui){
   	hideSideBar();   	
});

$('#privacy-policy').on('pagebeforeshow',function(event, ui){
   	hideSideBar();
});


$('#register-account').on('pagebeforeshow',function(event, ui){
	$("#frmRegister")[0].reset();

});