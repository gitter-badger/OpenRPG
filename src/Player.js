function Player(x, z, camera, img) {
	/**
		
	**/

	var camera = camera;
	var geometry = new THREE.PlaneBufferGeometry(1, 1);
	var material = new THREE.MeshBasicMaterial(
		{color: 0x000088}
	);
	var mesh = new THREE.Mesh(geometry, material);
	mesh.position.y = 1;
	mesh.position.x = x || 0;
	mesh.position.z = z || 0;

	var gravity = -0.01;
	var vy = 0;

	this.getMesh = function() {
		return mesh;
	};

	this.move = function(dx, dz) {
		mesh.position.x += dx;
		mesh.position.z += dz;
		this.aimCamera();
	};

	this.update = function() {
		vy += gravity;
		mesh.position.y += vy;
		if (mesh.position.y < 0) {
			mesh.position.y = 0;
			vy = 0;
		}
	};

	this.jump = function() {
		vy = 0.2;
	};

	this.aimCamera = function() {
		/**
			Aim the camera at the player
		**/
		camera.position.z = mesh.position.z + 5;
		camera.position.x = mesh.position.x;
		camera.position.y = 2;
	};
	this.aimCamera();
}