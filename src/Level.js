"use strict";

class Level {
    constructor(config) {
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
                    texture.minFilter = THREE.LinearFilter;
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