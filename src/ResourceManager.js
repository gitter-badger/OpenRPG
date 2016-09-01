/**
 *  This class handles all resource pre-loading
 **/
class ResourceManager {

    constructor(resourceList, onCompletion) {
        this.toLoad = resourceList;
        this.resources = {};
        this.numResourcesLoaded = 0;
        this._onCompletion = onCompletion;
    }

    _onResourceLoaded(event) {
        const manager = event.data;

        manager.numResourcesLoaded++;
        if (manager.numResourcesLoaded === manager.toLoad.length) {
            manager._onCompletion();
        }
    }

    preloadLevelResources() {
        for (let i in this.toLoad) {
            this.resources[this.toLoad[i]] = $('<img />').attr(
                'src', this.toLoad[i]).on(
                'load', null, this, this._onResourceLoaded);
        }
    }

    hasResource(key) {
        return key in this.resources;
    }

    getResource(key) {
        return this.resources[key][0];
    }
}