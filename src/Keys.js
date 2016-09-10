const W_KEY = 87;
const A_KEY = 65;
const S_KEY = 83;
const D_KEY = 68;
const SPACE = 32;
const SHIFT = 16;
const CTRL = 17;
const LEFT_MOUSE_BUTTON = 1;
const RIGHT_MOUSE_BUTTON = 2;
const keysDown = {};
let leftMouseButton = false;
let rightMouseButton = false;
let mouseX = null;
let mouseY = null;
let pMouseX = null;
let pMouseY = null;
let dMouseX = null;
let dMouseY = null;

document.onkeydown = function(e) {
    keysDown[e.keyCode] = true;
};

document.onkeyup = function(e) {
    keysDown[e.keyCode] = false;
};

document.onmousemove = function(e) {
    dMouseX = e.movementX;
    dMouseY = e.movementY;
};

document.onmousedown = function(e) {
    if (e.button === LEFT_MOUSE_BUTTON) {
        leftMouseButton = true;
    }
    else if (e.button === RIGHT_MOUSE_BUTTON) {
        rightMouseButton = true;
    }
};

document.onmouseup = function(e) {
    if (e.button === LEFT_MOUSE_BUTTON) {
        leftMouseButton = false;
    }
    else if (e.button === RIGHT_MOUSE_BUTTON) {
        rightMouseButton = false;
    }
    return true;
};