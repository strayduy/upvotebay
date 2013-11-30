module.exports = function(grunt) {

    var path = require('path');

    // Configuration
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        bower: {
            install: {
                options: {
                    targetDir: './upvotebay/static',
                    layout: 'byType',
                    install: true,
                    verbose: false,
                    cleanTargetDir: false,
                    cleanBowerDir: false,
                    bowerOptions: {}
                }
            }
        }
    });

    // Plugins
    grunt.loadNpmTasks('grunt-bower-task');

    // Tasks
    grunt.registerTask('default', ['bower']);

};
