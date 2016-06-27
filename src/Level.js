"use strict";

function Level(config) {
    var name;
    if (config.name) {
        name = config.name;
    }
    else {
        name = "level_" + Level.currentLevelIndex;
        Level.currentLevelIndex++;
    }
    var tileImages = config.tileImages || null;
    var npcs = config.npcs || null;
    var exits = config.exits || null;

    var isVisible = function(image) {

    };

    this.draw = function(xoff, yoff) {
        pushMatrix();
        traslate(xoff, yoff);

        // Draw all tiles

        popMatrix();
    };
};

Level.currentLevelIndex = 0;

Level.fromJSON = function(jsonString) {
    return new Level(JSON.parse(jsonString));
};