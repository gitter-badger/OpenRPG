const _toggleButtons = document.querySelectorAll('.ToggleListButton');

_toggleButtons.forEach((button) => {
    button.onclick = function(e) {
        const parent = e.target.parentElement.parentElement;
        const toggleList = parent.getElementsByClassName('ToggleList')[0];
        if (toggleList.style.display != 'none') {
            toggleList.style.display = 'none';
        }
        else {
            toggleList.style.display = 'block';
        }
        console.log(toggleList.style.display);
    }
});