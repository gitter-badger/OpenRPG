const W_KEY = 87;
const A_KEY = 65;
const S_KEY = 83;
const D_KEY = 68;
const SPACE = 32;
const SHIFT = 16;
const CTRL = 17;
const keysDown = {};

document.onkeydown = function(e) {
    keysDown[e.keyCode] = true;
};

document.onkeyup = function(e) {
    keysDown[e.keyCode] = false;
};