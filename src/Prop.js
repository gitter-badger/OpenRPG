function Prop(x, z, texture) {
	/**
		A vertical prop
	**/

	var geometry = new THREE.PlaneBufferGeometry(1, 1);
	var material;
	if (texture){
		material = new THREE.MeshBasicMaterial(
			{map: texture}
		);
	}
	else {
		material = new THREE.MeshBasicMaterial(
			{color: 0xff0000}
		);
	} 

	var mesh = new THREE.Mesh(geometry, material);
	mesh.position.y = 1;
	mesh.position.x = x || 0;
	mesh.position.z = z || 0;

	this.getMesh = function() {
		return mesh;
	};
}

Prop.loadAll = function() {
	/**
		Pre-load all prop images
		Return a dict of image names mapped to textures
		Can take a long time, should be used with caution
	**/
};