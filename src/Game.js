"use strict";

function Game(config) {
    this.name = config.name || "New Game"
    this.props = [];
};

Game.fromJSON = function(jsonString) {
    return new Game(JSON.parse(jsonString));
};