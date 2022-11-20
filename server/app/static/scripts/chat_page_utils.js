document.addEventListener('DOMContentLoaded', () => {
    let msg = document.getElementById("user_message");
    msg.addEventListener("keyup", function (event) {
        if (event.key === "Enter") {
            document.getElementById("send_message").click();
        }
    });
});

function create_chat_container(id, name, timestamp = null, last_msg_text = null) {
    let container = document.createElement('div');

    container.id = id;
    container.className = 'select-room list-group-item list-group-item-action py-3 lh-sm';
    container.role = 'button';
    let inner_div = document.createElement('div');
    inner_div.className = 'd-flex w-100 align-items-center justify-content-between';
    let chat_name_div = document.createElement('strong');
    chat_name_div.className = 'recipient_name mb-1';
    chat_name_div.innerText = name;
    let chat_timestamp_div = document.createElement('small');
    if (timestamp) {
        chat_timestamp_div.innerText = convert_time(timestamp);
    }
    let msg_text = document.createElement('div');
    msg_text.className = "col-10 mb-1 small"
    if (last_msg_text) {
        msg_text.innerText = last_msg_text;
    }
    inner_div.append(chat_name_div);
    inner_div.append(chat_timestamp_div);
    container.append(inner_div);
    container.append(msg_text);

    return container;
}

/**
 * @param {String} str
 * @param {Array.<{id: Number, name: String}>} allowed_users**/
function search_user_chat(str, allowed_users) {
    let results = [];
    const val = str.toLowerCase();

    for (let i = 0; i < allowed_users.length; i++) {
        if (allowed_users[i].name.toLowerCase().indexOf(val) > -1) {
            results.push(allowed_users[i]);
        }
    }
    return results;
}

function createSysMsg(msg) {
    const p = document.createElement('p');
    p.setAttribute("class", "system-msg");
    p.innerHTML = msg;
    return p;
}

/**
 * @param {Object} message
 * @param {string} message.msg
 * @param {string} message.username
 * @param {string} message.timestamp
 * @param {string} current_user
 * **/
function createMsg(message, current_user) {
    const div = document.createElement('div');
    div.className = "d-flex flex-row";
    const p = document.createElement('p');
    p.className = "msg text-break";
    // const span_username = document.createElement('span');
    const span_timestamp = document.createElement('span');
    const br = document.createElement('br')

    // Display system message
    if (typeof message.username == 'undefined') {
        return createSysMsg(message.msg);
    }
    // Display user's own message
    if (message.username === current_user) {
        div.classList.add('justify-content-end');
        p.classList.add("my-msg");
        // span_username.setAttribute("class", "my-username");
    }
    // Display other users' messages
    else {
        div.classList.add('justify-content-start');
        p.classList.add("others-msg");
        // span_username.setAttribute("class", "other-username");
    }

    span_timestamp.className = "timestamp d-flex justify-content-end";

    span_timestamp.innerText = convert_time(message.timestamp);

    p.innerHTML = message.msg + span_timestamp.outerHTML
    div.append(p);
    return div;
}

function convert_time(timestamp) {
    if (!timestamp) {
        return ''
    }
    let date = new Date(timestamp);
    let cur_date = new Date();
    let options_today = {
        hour: 'numeric',
        minute: 'numeric',
    };
    let options_other = {
        month: 'short',
        day: 'numeric',
    };

    if (isToday(date)) {
        return date.toLocaleString('ru', options_today);
    }
    return date.toLocaleString('ru', options_other);

}

function isToday(someDate) {
    const today = new Date()
    return someDate.getDate() === today.getDate() &&
        someDate.getMonth() === today.getMonth() &&
        someDate.getFullYear() === today.getFullYear()
}