document.addEventListener('DOMContentLoaded', () => {
    let msg = document.getElementById("user_message");
    msg.addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            document.getElementById("send_message").click();
        }
    });
});