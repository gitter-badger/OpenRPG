function Player(x, z, img) {
	/**
		
	**/

	var geometry = new THREE.PlaneBufferGeometry(1, 1);
	var material = new THREE.MeshBasicMaterial(
		{color: 0x000088}
	);
	var mesh = new THREE.Mesh(geometry, material);
	mesh.position.y = 1;
	mesh.position.x = x || 0;
	mesh.position.z = z || 0;

	this.getMesh = function() {
		return mesh;
	};

	this.move = function(dx, dz) {
		mesh.position.x += dx;
		mesh.position.z += dz;
	};
}