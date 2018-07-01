$(function() {
    $('#delusr').click(function(){
        $.ajax({
            url: '/propertyAction',
            data: $('[name="proplist"]').filter($(':checked')).serialize(),
            type: 'POST',
            success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
        });
    });
});
