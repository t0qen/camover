let keys = {}
let last_command = "";

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);
setInterval(main, 100);

// command
// function send_command(direction) { // send command to motors without reloadingthe page
    // fetch(`/control/${direction}`)
// }

// battery refresh
setInterval(function() { // refresh battery level every 2s
    fetch('/battery')
        .then(response => response.text())
        .then(level => {
            document.getElementById('battery-level').textContent = level;
        });
}, 2000);

function main() {
    console.log(keys);
    let command = "";

    if (keys["w"]) command = "forward";
    else if (keys["s"]) command = "backward";
    else if (keys["q"]) command = "fast_turn_left";
    else if (keys["e"]) command = "fast_turn_right";
    else if (keys["a"]) command = "turn_left";
    else if (keys["d"]) command = "turn_right";
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

