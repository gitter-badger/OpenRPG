/**
 *  This class handles all resource pre-loading
 **/
class ResourceManager {

    constructor() {
        const resources = {};
    }

    preloadLevelResources(level) {

    }

    hasResource(key) {
        return key in this.resources;
    }

    getResource(key) {
        return resources[key];
    }
}