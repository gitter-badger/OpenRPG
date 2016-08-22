function Prop(scene, x, z, img) {
	/**
		A vertical prop
	**/

	var geometry = new THREE.PlaneBufferGeometry(1, 1);
	var material = new THREE.MeshBasicMaterial(
		{color: 0x880000}
	);
	var mesh = new THREE.Mesh(geometry, material);
	mesh.position.y = 1;
	mesh.position.x = x || 0;
	mesh.position.z = z || 0;

	this.getMesh = function() {
		return mesh;
	};

	this.draw = function() {

	};
}