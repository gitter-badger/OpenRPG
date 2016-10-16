'use strict';

provide('GameObject.js');

class GameObject {
    constructor(updateURL) {
        this.title = 'New GameObject';
        this.fields = {};
        this._form = document.createElement('form');
        this._form.setAttribute('method', 'POST');
        this._form.setAttribute('action', updateURL);
    }

    addField(title, options) {
        if (title in this.fields) {
            return;
        }

        this.fields[title] = {
            value: null,
            options:options || []
        };

        const field = document.createElement('input');
        field.setAttribute('type', 'text');
        field.setAttribute('name', title);
    }

    setField(title, value) {
        this.fields[title].value = value;
        // TODO: Update form
        this.update();
    }

    update() {
        this._form.submit();
    }
}