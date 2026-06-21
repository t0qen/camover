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



// mobile part
document.addEventListener("contextmenu", function(e) {
    e.preventDefault();
});
window.addEventListener("blur", () => {
    for (const key in button) {
        button[key] = false;
    }
});
document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
        for (const key in button) {
            button[key] = false;
        }
    }
});

// mobile inputs (longgggg)
document.getElementById("forward").addEventListener("pointerdown", () => {
    button["forward"] = true;
});

document.getElementById("forward").addEventListener("pointerup", () => {
    button["forward"] = false;
});

document.getElementById("forward").addEventListener("pointercancel", () => {
    button["forward"] = false;
});


document.getElementById("turn_left").addEventListener("pointerdown", () => {
    button["turn_left"] = true;
});

document.getElementById("turn_left").addEventListener("pointerup", () => {
    button["turn_left"] = false;
});

document.getElementById("turn_left").addEventListener("pointercancel", () => {
    button["turn_left"] = false;
});


document.getElementById("turn_right").addEventListener("pointerdown", () => {
    button["turn_right"] = true;
});

document.getElementById("turn_right").addEventListener("pointerup", () => {
    button["turn_right"] = false;
});

document.getElementById("turn_right").addEventListener("pointercancel", () => {
    button["turn_right"] = false;
});


document.getElementById("fast_turn_left").addEventListener("pointerdown", () => {
    button["fast_turn_left"] = true;
});

document.getElementById("fast_turn_left").addEventListener("pointerup", () => {
    button["fast_turn_left"] = false;
});

document.getElementById("fast_turn_left").addEventListener("pointercancel", () => {
    button["fast_turn_left"] = false;
});


document.getElementById("fast_turn_right").addEventListener("pointerdown", () => {
    button["fast_turn_right"] = true;
});

document.getElementById("fast_turn_right").addEventListener("pointerup", () => {
    button["fast_turn_right"] = false;
});

document.getElementById("fast_turn_right").addEventListener("pointercancel", () => {
    button["fast_turn_right"] = false;
});


document.getElementById("backward").addEventListener("pointerdown", () => {
    button["backward"] = true;
});

document.getElementById("backward").addEventListener("pointerup", () => {
    button["backward"] = false;
});

document.getElementById("backward").addEventListener("pointercancel", () => {
    button["backward"] = false;
});


document.getElementById("buzzer").addEventListener("pointerdown", () => {
    button["buzzer"] = true;
});

document.getElementById("buzzer").addEventListener("pointerup", () => {
    button["buzzer"] = false;
});

document.getElementById("buzzer").addEventListener("pointercancel", () => {
    button["buzzer"] = false;
});