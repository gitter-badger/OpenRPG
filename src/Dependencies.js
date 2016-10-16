/*
    A simple library for tracking JS dependencies
*/

const _dependencies = new Set();

function require(fileName) {
    if (!_dependencies.has(fileName)) {
        throw 'Missing dependency: ' + fileName;
    }
}

function provide(fileName) {
    _dependencies.add(fileName);
}