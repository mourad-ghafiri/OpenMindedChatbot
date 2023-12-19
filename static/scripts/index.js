var stream_completion_ws = new WebSocket(window.location.origin.replace(/^http/, 'ws') + "/stream_completion");
var isStreamFinished = false;
var evilMode = false;
var useInternetFunction = false;
var userTimeFunction = false;
var userWeatherFunction = false;
var userMathFunction = false;
var useTerminalFunction = false;

stream_completion_ws.onmessage = function (event) {
    var response = document.getElementById('response');
    var message = JSON.parse(event.data);

    if (message.type === 'message') {
        loader.classList.add('hidden');
        sendButton.classList.remove('hidden');
        var lastMessage = response.lastElementChild;
        if (lastMessage && lastMessage.classList.contains('bot-message')) {
            // Convert newlines to <br> and append the new text
            lastMessage.innerHTML += message.data.replace(/\n/g, '<br>');
        } else {
            var el = document.createElement('div');
            el.style = "color: white; background: #560f0f;";
            el.className = "message bot-message p-2 rounded-md";
            // Convert newlines to <br> for the new message
            el.innerHTML = message.data.replace(/\n/g, '<br>');
            response.appendChild(el);
        }
    }

    response.scrollTop = response.scrollHeight; // Auto-scroll to bottom
};

function sendMessage(event) {
    var input = document.getElementById("messageText");
    var response = document.getElementById('response');
    var sendButton = document.getElementById('sendButton');
    var loader = document.getElementById('loader');
    

    if (input.value.trim() !== '') {
        // Hide send button and show loader
        sendButton.classList.add('hidden');
        loader.classList.remove('hidden');
        var userEl = document.createElement('div');
        userEl.className = "message user-message bg-gray-200 p-2 my-2 rounded-md";
        userEl.textContent = input.value;
        response.appendChild(userEl);

        stream_completion_ws.send(JSON.stringify({
            message: input.value, evilMode,
            useInternetFunction, userTimeFunction, userWeatherFunction, userMathFunction, useTerminalFunction
        }));
        input.value = '';
    }
    response.scrollTop = response.scrollHeight; // Auto-scroll to bottom
    event.preventDefault();
}

document.getElementById('evilModeToggle').addEventListener('change', function() {
    if(this.checked) {
        // Code to enable Evil Mode
        document.body.classList.add('evil-mode');
        evilMode = true;
    } else {
        // Code to disable Evil Mode
        document.body.classList.remove('evil-mode');
        evilMode = false;
    }
});

document.getElementById('useInternetFunction').addEventListener('change', function() {
    useInternetFunction = this.checked;
});

document.getElementById('userTimeFunction').addEventListener('change', function() {
    userTimeFunction = this.checked;
});

document.getElementById('userWeatherFunction').addEventListener('change', function() {
    userWeatherFunction = this.checked;
});

document.getElementById('userMathFunction').addEventListener('change', function() {
    userMathFunction = this.checked;
});

document.getElementById('useTerminalFunction').addEventListener('change', function() {
    useTerminalFunction = this.checked;
});
