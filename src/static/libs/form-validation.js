(function() {

	$('form').on('submit', function(e){ 
		var flag = 0,
			elements = $("form :input[required]");
		$.each(elements, function(i){
			if (elements[i].value == "") {
				flag = 1;
			 };
		});
		if (flag==1){
			alert("Fill all required fields");
			e.stopImmediatePropagation();
			return false
		};
		return true
	});
})();