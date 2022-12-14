document.addEventListener('DOMContentLoaded', () => {
    const username = document.getElementById('get-user-name').innerHTML;
    const input = document.querySelector('#user-search');
    const suggestions = document.querySelector('.suggestions ul');
    const rooms = document.querySelector('#rooms')

    let room_id = null;
    let room_name = '';
    let allowed_users = [];

    fetch(`./api/users_to_chat`)
        .then(response => response.json())
        .then(/**
         * @property users_json
         * @property users_json.users
         **/users_json => {
            allowed_users = users_json.users;
        });

    fetch(`./api/user_chats`)
        .then(response => response.json())
        .then(/**
         * @property user_chats_json
         * @property users_json.chats
         **/user_chats_json => {
            show_chats(user_chats_json.chats);
        });

    input.addEventListener('keyup', searchHandler);
    suggestions.addEventListener('click', useSuggestion);

    let socket = io('/chat');

    socket.on('message', data => {
        // Display current message
        displayMsg(data);
        scrollDownChatWindow();
        updateChats(data);
    });

    socket.on('load_messages', data => {
        /**
         * @property data
         * @property data.messages
         * **/
        for (let msg of data.messages) {
            displayMsg(msg);
        }
        scrollDownChatWindow();
    });

    /**
     * @param {Array.<{id: Number, name: String, last_msg: {timestamp: String, text: String}}>} chats
     **/
    function show_chats(chats) {
        for (let chat of chats) {
            let elem = create_chat_container(chat.id, chat.name, chat.last_msg.timestamp, chat.last_msg.text);
            elem.onclick = () => {
                check_room(chat.id);
            };
            rooms.append(elem);
        }
    }

    function updateChats(data) {
        const chat = document.getElementById(`${data.chat_id}`);
        let msg_text = chat.querySelector('.small');
        msg_text.innerHTML = data.msg;
        let timestamp = chat.querySelector('div > small');
        timestamp.innerHTML = convert_time(data.timestamp);
        chat.remove();
        rooms.prepend(chat);
    }

    function searchHandler(e) {
        const inputVal = e.currentTarget.value;
        let results = [];
        if (inputVal.length > 0) {
            results = search_user_chat(inputVal, allowed_users);
        }
        showSuggestions(results);
    }

    function showSuggestions(results) {
        suggestions.innerHTML = '';

        if (results.length > 0) {
            for (let i = 0; i < results.length; i++) {
                let user_name = results[i].name;
                let li_new = document.createElement('div');
                li_new.className = 'list-group-item list-group-item-action';
                li_new.innerHTML = `${user_name}`;
                suggestions.append(li_new);
            }

        } else {
            suggestions.innerHTML = '';
        }
    }

    function useSuggestion(e) {
        let recipient_name = e.target.innerHTML;
        suggestions.innerHTML = '';
        input.value = '';
        create_room(recipient_name);
    }

    function create_room(recipient_name) {
        const rooms = document.getElementById('rooms');

        fetch(`./api/create_chat/${recipient_name}`)
            .then(response => response.json())
            .then(/**
             * @property chat
             * @property chat.users
             * @property chat.id
             * @property chat.name**/chat => {

                let users = chat.users;
                let new_room_id = chat.id;
                let new_room = chat.name;

                room_name = new_room;
                if (document.getElementById(new_room_id)) {
                    check_room(new_room_id);
                    return;
                }
                let container = create_chat_container(new_room_id, new_room)
                container.onclick = () => {
                    check_room(new_room_id);
                };
                rooms.prepend(container);
                check_room(new_room_id);
            });
    }

    // Send messages
    document.getElementById('send_message').onclick = () => {
        socket.emit('message', {
            'msg': document.querySelector('#user_message').value,
            'sender': username,
            'room_id': room_id
        });
        document.querySelector('#user_message').value = '';
    };

    function displayMsg(message) {
        if (message.msg) {
            let p = createMsg(message, username)
            document.querySelector('#display-message-section').append(p);
            scrollDownChatWindow();
        }
        document.querySelector("#user_message").focus();
    }

    // Select a room
    document.querySelectorAll('.select-room').forEach(elem => {
        elem.onclick = () => {
            let new_room_id = elem.id;
            room_name = elem.querySelector('.recipient_name').innerHTML;
            check_room(new_room_id);
        };
    });

    function check_room(new_room_id) {
        if (new_room_id === room_id) {
            let message = {
                msg: `You are already in ${room_id} room.`
            };
            displayMsg(message);
        } else {
            if (room_id) {
                leaveRoom(room_id);
            }
            joinRoom(new_room_id);
        }
    }

    // Trigger 'leave' event if user was previously on a room
    function leaveRoom(room_id) {
        socket.emit('leave', {'username': username, 'room_id': room_id});
        const chat_title = document.querySelector('#chat-title');
        chat_title.innerHTML = '';
        document.querySelectorAll('.select-room').forEach(elem => {
            elem.classList.remove('active');
        });
    }

    // Trigger 'join' event
    function joinRoom(new_room_id) {
        // Join room
        socket.emit('join', {'username': username, 'room_id': new_room_id});
        document.querySelector('#' + CSS.escape(new_room_id)).classList.add('active');
        let chat_title = document.querySelector('#chat-title');
        chat_title.innerHTML = room_name;
        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';

        // Autofocus on text box
        document.querySelector("#user_message").focus();
        room_id = new_room_id;
    }

    // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});