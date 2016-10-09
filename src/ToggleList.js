const _toggleButtons = document.querySelectorAll('.ToggleButton');
let _initialDispay = null;

_toggleButtons.forEach((button) => {
    button.onclick = function(e) {
        const parent = e.target.parentElement.parentElement;
        const toggleList = parent.getElementsByClassName('ToggleList')[0];
        if (toggleList.style.display != 'none') {
            if (!_initialDispay) {
                _initialDispay = toggleList.style.display;
            }
            toggleList.style.display = 'none';
            e.target.innerHTML = '+';
        }
        else {
            toggleList.style.display = _initialDispay;
            e.target.innerHTML = '-';
        }
    }
});