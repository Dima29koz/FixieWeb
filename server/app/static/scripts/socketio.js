document.addEventListener('DOMContentLoaded', () => {
    const username = document.getElementById('get-user-name').innerHTML;
    const input = document.querySelector('#user-search');
    const suggestions = document.querySelector('.suggestions ul');

    input.addEventListener('keyup', searchHandler);
    suggestions.addEventListener('click', useSuggestion);

    let socket = io('/chat');

    // Set default room
    let room = null;


    let users = [];
    fetch(`./api/users_to_chat`)
        .then(response => response.json())
        .then(users_json => {
            users = users_json.users;
        });

    function search(str) {
        let results = [];
        const val = str.toLowerCase();

        for (let i = 0; i < users.length; i++) {
            if (users[i].name.toLowerCase().indexOf(val) > -1) {
                results.push(users[i]);
            }
        }
        return results;
    }

    function searchHandler(e) {
        const inputVal = e.currentTarget.value;
        let results = [];
        if (inputVal.length > 0) {
            results = search(inputVal);
        }
        showSuggestions(results, inputVal);
    }

    function showSuggestions(results, inputVal) {
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
        let new_room = e.target.innerHTML;
        suggestions.innerHTML = '';
        input.value = '';
        create_room(new_room);
        check_room(new_room);
    }

    function create_room(new_room) {
        const rooms = document.getElementById('rooms');
        let container = document.createElement('div');

        container.className = 'select-room list-group-item list-group-item-action py-3 lh-sm';
        container.role = 'button';
        container.id = new_room;
        let inner_div = document.createElement('div');
        inner_div.className = 'd-flex w-100 align-items-center justify-content-between';
        inner_div.innerHTML =`<strong className="mb-1">${new_room}</strong><small>timestamp</small>`;
        container.append(inner_div);
        container.onclick = () => {
            check_room(new_room);
        };
        rooms.prepend(container);
    }

    // Send messages
    document.getElementById('send_message').onclick = () => {
        socket.emit('message', {
            'msg': document.querySelector('#user_message').value,
            'username': username,
            'room': room
        });
        document.querySelector('#user_message').value = '';
    };

    // Display all incoming messages
    socket.on('message', data => {

        // Display current message
        if (data.msg) {
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br')
            // Display user's own message
            if (data.username === username) {
                    p.setAttribute("class", "my-msg");

                    // Username
                    span_username.setAttribute("class", "my-username");
                    span_username.innerText = data.username;

                    // Timestamp
                    span_timestamp.setAttribute("class", "timestamp");
                    span_timestamp.innerText = data.time_stamp;

                    // HTML to append
                    p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML

                    //Append
                    document.querySelector('#display-message-section').append(p);
            }
            // Display other users' messages
            else if (typeof data.username !== 'undefined') {
                p.setAttribute("class", "others-msg");

                // Username
                span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;

                // Timestamp
                span_timestamp.setAttribute("class", "timestamp");
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                //Append
                document.querySelector('#display-message-section').append(p);
            }
            // Display system message
            else {
                printSysMsg(data.msg);
            }


        }
        scrollDownChatWindow();
    });

    // Select a room
    document.querySelectorAll('.select-room').forEach(elem => {
        elem.onclick = () => {
            let newRoom = elem.id;
            // Check if user already in the room
            check_room(newRoom);
        };
    });

    function check_room(new_room) {
        if (new_room === room) {
            let msg = `You are already in ${room} room.`;
            printSysMsg(msg);
        } else {
            if (room) {
                leaveRoom(room);
            }
            joinRoom(new_room);
            room = new_room;
        }
    }

    // Trigger 'leave' event if user was previously on a room
    function leaveRoom(room) {
        socket.emit('leave', {'username': username, 'room': room});

        document.querySelectorAll('.select-room').forEach(elem => {
            elem.classList.remove('active');
        });
    }

    // Trigger 'join' event
    function joinRoom(room) {

        // Join room
        socket.emit('join', {'username': username, 'room': room});
        document.querySelector('#' + CSS.escape(room)).classList.add('active');
        // Clear message area
        document.querySelector('#display-message-section').innerHTML = '';

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }

    // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Print system messages
    function printSysMsg(msg) {
        const p = document.createElement('p');
        p.setAttribute("class", "system-msg");
        p.innerHTML = msg;
        document.querySelector('#display-message-section').append(p);
        scrollDownChatWindow()

        // Autofocus on text box
        document.querySelector("#user_message").focus();
    }
});