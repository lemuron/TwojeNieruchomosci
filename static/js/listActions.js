$(function() {
    $('#delusr').click(function(){
        var data_to_send = $('[name="proplist"]').filter($(':checked')).serialize().toString();
        data_to_send = data_to_send.concat("&operation=delete");
        console.log(data_to_send);
        $.ajax({
            url: '/propertyAction',
            data: data_to_send,
            processData: false,
            type: 'POST',
            success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
        });
    });
    $('#addusr').click(function(){
        var data_to_send = $('[name="proplist"]').filter($(':checked')).serialize().toString();
        data_to_send = data_to_send.concat("&operation=add");
        console.log(data_to_send);
        $.ajax({
            url: '/propertyAction',
            data: data_to_send,
            processData: false,
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
