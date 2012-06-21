$(document).ready(function(){
	
	$(".trigger").click(function() {
	    $(this).siblings("div").slideToggle("fast");
	});
});
