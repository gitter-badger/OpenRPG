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

    var scene = new THREE.Scene();
    var renderer = config.renderer;
    var requiredResources = [];

    // Ground
    var groundImg = config.groundImg || null;
    var groundGeometry = new THREE.PlaneBufferGeometry(5, 5, 32);
	var groundMaterial = new THREE.MeshBasicMaterial(
		{color: 0xaaaaaa}
	);
	var ground = new THREE.Mesh(groundGeometry, groundMaterial);
	ground.position.y = 0;
	ground.rotation.x = -Math.PI * 0.5;
	scene.add(ground);

    var npcs = config.npcs || null;
    var exits = config.exits || null;

    this.render = function() {
    	renderer.render(scene, camera);
    };

    this.addProp = function(prop) {
    	/**
			Add a Prop to the level
    	**/
    	scene.add(prop.getMesh());
    }
};

Level.currentLevelIndex = 0;

Level.fromJSON = function(jsonString) {
    return new Level(JSON.parse(jsonString));
};