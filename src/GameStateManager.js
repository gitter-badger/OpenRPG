"use strict";

function GameStateManager() {
    var MODES = {
        GAME_SELECT: 0,
        TITLE_SCREEN: 1,
        CHARACTER_SELECT: 2,
        PLAY_GAME: 3
    };
    var mode = MODES.PLAY_GAME;
    var games = null;
    var currentGame = null;
    var currentLevel = null;
    var player = null;

    function onGamesFileLoaded(data) {
        var gameData = data["games"];
        games = [];

        for (var i = 0; i < gameData.length; i++) {
            games.push(gameData[i]);
        }
    };

    function loadGames() {
        $.get(SERVER_URL + "/games/games.json", null, onGamesFileLoaded);
    };
    loadGames();

    function setMode(mode) {

    };
};