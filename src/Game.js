"use strict";

function Game(config) {
    this.name = config.name || "New Game"
};

Game.fromJSON = function(jsonString) {
    return new Game(JSON.parse(jsonString));
};