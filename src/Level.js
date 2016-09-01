"use strict";

class Level {
    constructor(config) {
        var name;
        if (config.name) {
            name = config.name;
        }
        else {
            name = "level_" + Level.currentLevelIndex;
            Level.currentLevelIndex++;
        }

        this.scene = new THREE.Scene();
        this.renderer = config.renderer;

        // Load all required resources, then call init()
        const requiredResources = ['/img/floors/download.png'];
        let resourcesLoaded = 0;
        const resources = {};
        const self = this;

        const loader = new THREE.TextureLoader();
        for (let i in requiredResources) {
            loader.load(requiredResources[i],
                function(texture) {
                    resources[requiredResources[i]] = texture;
                    resourcesLoaded++;
                    if (resourcesLoaded === requiredResources.length) {
                        self.init();
                    }
                }
            );
        }
        this.resources = resources;
    }

    init() {
        // Ground
        const groundGeometry = new THREE.PlaneBufferGeometry(640, 480, 32);
        const groundTexture = this.resources['/img/floors/download.png'];
        const groundMaterial = new THREE.MeshBasicMaterial(
            {map: groundTexture}
        );
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.position.y = 0;
        ground.rotation.x = -Math.PI * 0.5;
        this.scene.add(ground);

        //this.npcs = config.npcs || null;
        //this.exits = config.exits || null;

        render();
    }

    render() {
        this.renderer.render(this.scene, camera);
    }

    addProp(prop) {
        /**
            Add a Prop to the level
        **/
        this.scene.add(prop.getMesh());
    }
};