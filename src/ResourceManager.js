function ResourceManager() {
	var propTextures = {};

	this.loadAll = function() {
		/**
			Load all the resources
		**/
	
		// Load things
		var loader = new THREE.TextureLoader();


		// Start the game
		render();
	};

	this.getPropTextures = function() {
		return propTextures;
	};
}