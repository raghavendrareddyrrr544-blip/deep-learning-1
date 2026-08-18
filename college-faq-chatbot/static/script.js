async function sendMessage() {

    const input =
        document.getElementById("user-input");

    const message =
        input.value.trim();


    if (message === "") {

        return;

    }


    const chatBox =
        document.getElementById("chat-box");


    chatBox.innerHTML +=
        `<div class="user">${message}</div>`;


    input.value = "";


    const response = await fetch(
        "/chat",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        }
    );


    const data =
        await response.json();


    chatBox.innerHTML +=
        `<div class="bot">
            ${data.response}
        </div>`;


    chatBox.scrollTop =
        chatBox.scrollHeight;

}


document
    .getElementById("user-input")
    .addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                sendMessage();

            }

        }
    );