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
        const field = document.createElement('input');

        this.fields[title] = {
            value: null,
            options: options || [],
            element: field
        };

        field.setAttribute('type', 'text');
        field.setAttribute('name', title);
    }

    setField(title, value) {
        this.fields[title].value = value;
        this.fields[title].element.setAttribute('value', value);
        this.update();
    }

    update() {
        this._form.submit();
    }
}