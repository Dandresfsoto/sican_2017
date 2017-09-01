    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/realtime/");

    socket.onmessage = function(message) {
        var contact_selected = document.getElementById("contact_selected");
        var user_id = document.getElementById("user_id");


        var data = JSON.parse(message.data);
        if(data.hasOwnProperty('conected') && window.location.pathname == '/realtime/'){
            for(i=0;i<data.conected.length;i++){
                var contacto_list = document.getElementById("conected_list_"+data.conected[i].id);
                var contacto_container = document.getElementById("conected_container_"+data.conected[i].id);
                if(data.conected[i].online){
                    contacto_list.classList.add('online');
                    if(contacto_container != null) {
                        contacto_container.classList.add('online');
                    }
                }
                else{
                    contacto_list.classList.remove('online');
                    if(contacto_container != null) {
                        contacto_container.classList.remove('online');
                    }
                }
            }
        }


        if(data.hasOwnProperty('mensaje') && window.location.pathname == '/realtime/'){
            if(data.mensaje.de == user_id.value.toString()){
                if(data.mensaje.para == contact_selected.value.toString()){
                    $('#chat-list').prepend("<div class='me style-scope chat-container-sican'><div class='bubble style-scope chat-container-sican'><p class='me_p style-scope chat-container-sican'>"+ data.mensaje.mensaje +"</p></div></div>");
                }
            }

            if(data.mensaje.para == user_id.value.toString()){
                if(data.mensaje.de == contact_selected.value.toString()){
                    $('#chat-list').prepend("<div class='you style-scope chat-container-sican'><div class='bubble style-scope chat-container-sican'><p class='you_p style-scope chat-container-sican'>"+ data.mensaje.mensaje +"</p></div></div>");
                }
            }

        }

    }

    socket.onopen = function() {
    }


    function send_message(to,text){
        socket.send(JSON.stringify({mensaje: {para:to, mensaje:text}}));
    }
