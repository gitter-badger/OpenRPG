class CameraController {
    constructor(camera) {
        this.camera = camera;
    }

    update() {
        if (keysDown[W_KEY]) {
            this.camera.position.z--;
        }
        if (keysDown[S_KEY]) {
            this.camera.position.z++;
        }
        if (keysDown[A_KEY]) {
            this.camera.position.x--;
        }
        if (keysDown[D_KEY]) {
            this.camera.position.x++;
        }
        if (keysDown[SHIFT]) {
            this.camera.position.y++;
        }
        if (keysDown[CTRL]) {
            this.camera.position.y--;
        }
    }
}