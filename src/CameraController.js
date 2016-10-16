require('three.js');
require('Keys.js');

class CameraController {
    constructor(camera) {
        camera.rotation.set(0, 0, 0);

        this._pitchObject = new THREE.Object3D();
        this._pitchObject.add(camera);

        this._yawObject = new THREE.Object3D();
        this._yawObject.position.y = 10;
        this._yawObject.add(this._pitchObject);

        this._halfPi = Math.PI/2;
    }

    update() {
        if (keysDown[W_KEY]) {
            this._yawObject.translateZ(-1);
        }
        if (keysDown[S_KEY]) {
            this._yawObject.translateZ(1);
        }
        if (keysDown[A_KEY]) {
            this._yawObject.translateX(-1);
        }
        if (keysDown[D_KEY]) {
            this._yawObject.translateX(1)
        }
        if (keysDown[SHIFT]) {
            this._yawObject.position.y++;
        }
        if (keysDown[CTRL]) {
            this._yawObject.position.y--;
        }
        if (rightMouseButton) {
            this._yawObject.rotation.y -= dMouseX / 100;
            this._pitchObject.rotation.x -= dMouseY / 100;
            this._pitchObject.rotation.x = Math.max(-this._halfPi, Math.min(this._halfPi, this._pitchObject.rotation.x));
        }
    }

    setPosition(x, y, z) {
        this._yawObject.position.set(x, y, z);
    }

    getObject() {
        return this._yawObject;
    }
}