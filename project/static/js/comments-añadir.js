var main = function(){
    "use strict";
    var formData = {};
    formData.comentario=$('input[name="comentario"]').val()

    $.ajax({
        type:"POST",
        data:JSON.stringify(formData),
        contentType : 'application/json;charset=UTF-8',
        dataType: "json",
        url:"/comments",
        beforeSend: function(){
            console.log("Se está iniciando")
        },
        complete: function(){
            console.log("Se completó")
        },
        statusCode:{
            0: function(event){
                console.log("El error de la llamada AJAX es: ERR_NAME_NOT_RESOLVED")
            },
            404: function(event){
                console.log("Servidor no encontrado")
            },
            500: function(){
                console.log("Error interno del servidor")
            }
        },
        success: function(responseJson){
            alert('Success ' + responseJson.message);
        },
        error: function(response){
            let json = response.responseJSON;
            console.log(response);
            alert("Error en la llamada AJAX")
            //alert('Error: ' + json.message);
        }
    });
};

$(document).ready(main);