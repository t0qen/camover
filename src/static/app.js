let keys = {};
let button = {};
let current_button = "";
let last_command = "";
let last_buzzer_state = false;
let is_fullscreen = false
let global_speed = 1;

document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);
setInterval(main, 100);
document.documentElement.requestFullscreen();


// battery refresh
setInterval(function () {
    fetch('/battery')
        .then(response => response.text())
        .then(level => {
            document.getElementById('battery-level').textContent = `${level}V`;
        });
}, 5000);
setInterval(() => {
    fetch('/cpu_temp')
        .then(response => response.text())
        .then(temp => {
            document.getElementById('cpu-temp').textContent = `${temp}°C`;
        });
}, 2000);


function main() {
    console.log(button);
    let command = "";

    if (keys["w"] || button["forward"]) command = "forward";
    else if (keys["q"] || button["fast_turn_left"]) command = "fast_turn_left";
    else if (keys["e"] || button["fast_turn_right"]) command = "fast_turn_right";
    else if (keys["a"] || button["turn_left"]) command = "turn_left";
    else if (keys["d"] || button["turn_right"]) command = "turn_right";
    else if (keys["s"] || button["backward"]) command = "backward";
    else if (keys["-"] || button["speed-down"]) command = "speed-down";
    else if (keys["+"] || button["speed-up"]) command = "speed-up";
    else if (keys[" "] || button["buzzer"]) command = "buzzer";
    //     if (!last_buzzer_state) {
    //         fetch(`/buzzer`);
    //         last_buzzer_state = true;
    //     } else {
    //         last_buzzer_state = false;
    //     }

    //     command = "stop"
    // }
    else command = "stop";

    send_command(command);
}


function send_command(command) {
    //console.log("send", command);

    if (command != last_command) {
        last_command = command;
        if (command == "speed-up") {
            console.log("speed up");
            global_speed = Number((global_speed + 0.05).toFixed(2));
            if (global_speed > 1) {
                global_speed = 1;
            }
            document.getElementById('speed-display').textContent = global_speed.toFixed(2);
            fetch(`/speed/${global_speed}`)
        } else if (command == "speed-down") {
            console.log("speed down");
            global_speed = Number((global_speed - 0.05).toFixed(2));
            if (global_speed < 0.4) {
                global_speed = 0.4;
            }
            document.getElementById('speed-display').textContent = global_speed.toFixed(2);
            fetch(`/speed/${global_speed}`)
        } else if (command == "buzzer") {
            fetch(`/buzzer`);
        } else {
            fetch(`/control/${command}`);
        }
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
document.addEventListener("contextmenu", function (e) {
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

document.getElementById("fullscreen").addEventListener("click", () => {
    if (is_fullscreen) {
        document.exitFullscreen();
    } else {
        document.documentElement.requestFullscreen();
        try {
            screen.orientation.lock("landscape");
        } catch (err) {
            console.log("Orientation lock non supporté");
        }
    }
    is_fullscreen = !is_fullscreen
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


document.getElementById("speed-down").addEventListener("pointerdown", () => {
    button["speed-down"] = true;
});

document.getElementById("speed-down").addEventListener("pointerup", () => {
    button["speed-down"] = false;
});

document.getElementById("speed-down").addEventListener("pointercancel", () => {
    button["speed-down"] = false;
});

document.getElementById("speed-up").addEventListener("pointerdown", () => {
    button["speed-up"] = true;
});

document.getElementById("speed-up").addEventListener("pointerup", () => {
    button["speed-up"] = false;
});

document.getElementById("speed-up").addEventListener("pointercancel", () => {
    button["speed-up"] = false;
});