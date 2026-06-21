let keys = {};
let button = {};
let current_button = "";
let last_command = "";
let last_buzzer_state = false;

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);
setInterval(main, 100);

// battery refresh
setInterval(function() {
    fetch('/battery')
        .then(response => response.text())
        .then(level => {
            document.getElementById('battery-level').textContent = level;
        });
}, 5000);

function main() {
    console.log(keys);
    let command = "";

    if (keys["w"] || button["forward"]) command = "forward";
    else if (keys["q"] || button["fast_turn_left"]) command = "fast_turn_left";
    else if (keys["e"] || button["fast_turn_right"]) command = "fast_turn_right";
    else if (keys["a"] || button["turn_left"]) command = "turn_left";
    else if (keys["d"] || button["turn_right"]) command = "turn_right";
    else if (keys["s"] || button["backward"]) command = "backward";
    else if (keys[" "] || button["buzzer"]) {
        if (!last_buzzer_state) {
            fetch(`/buzzer`);
            last_buzzer_state = true;
        } else {
            last_buzzer_state = false;
        }
    
            
    }
    else command = "stop";

    send_command(command);
}

function send_command(command) {
    console.log("send", command);

    if (command != last_command) {
        last_command = command;
        fetch(`/control/${command}`);
    } else {
        return;
    }
}

function keyDownHandler(e) {
    keys[e.key] = true;
}

function keyUpHandler(e) {
    keys[e.key] = false;
}