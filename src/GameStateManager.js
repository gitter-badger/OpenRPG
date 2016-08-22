"use strict";

function GameStateManager() {
    var MODES = {
        GAME_SELECT:0,
        TITLE_SCREEN:1,
        CHARACTER_SELECT:2,
        PLAY_GAME:3
    };
    var mode = MODES.PLAY_GAME;
    var games = null;
    var currentGame = null;
    var currentLevel = null;
    var player = null;
    var serverURL = "http://127.0.0.1:5000"

    function onGamesFileLoaded(data) {
        var gameData = data["games"];
        games = [];

        for (var i = 0; i < gameData.length; i++) {
            games.push(gameData[i]);
        }
    };

    function loadGames() {
        $.get(serverURL + "/games/games.json", null, onGamesFileLoaded);
    };
    loadGames();

    function setMode(mode) {

    };

    function drawGameSelect() {
        background(0);
        fill(255);
        textAlign(CENTER, CENTER);
        textSize(24);
        text("Select a Game", width/2, 50)

        if (games === null) {
            textSize(18);
            push();
            translate(width/2, height/2);
            text("Loading...", 0, -50);
            rotate(millis()/500);
            stroke(255);
            noFill();
            arc(0, 0, 50, 50, 0, PI * 1.75);
            pop();
        }
        else {
            textSize(18);
            noFill();
            stroke(255);
            rect(width/2 - 75, height/2 - 15, 150, 30);

            fill(255);
            for (var i = 0; i < games.length; i++) {
                text(games[i].title, width/2, height/2 + 20 * i);
            }
        }
    };

    function drawTitleScreen() {

    };

    function drawCharacterSelect() {

    };

    function drawGame() {
        // Update the world
        // Update character
    };

    this.step = function() {
        if (mode === MODES.GAME_SELECT) {
            drawGameSelect();    
        }
    };
};