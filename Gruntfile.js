module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        mangle: true,
        compress: true,
        report: true,
        screw_ie8: true,
        stats: true,
        preserveComments: false
      },
      build: {
        files: {
          'static/js/bakery.min.js': ['static/js/bakery.js']
        }
      }
    },
    jshint: {
      options: {
        ignores: ['static/js/*.min.js']
      },
      files: ['static/js/*.js'],
    },
    recess: {
      dist: {
        options: {
          compile: true,
        },
        files: {
          'static/css/vendor/bootstrap.css': [
            'static/less/vendor/bootstrap.less'
          ],
          'static/css/<%= pkg.name %>.css': [
            'static/less/<%= pkg.name %>.less'
          ],
        }
      },
      min: {
        options: {
          compile: true,
          compress: true,
        },
        files: {
          'static/css/vendor/bootstrap.min.css': [
            'static/less/vendor/bootstrap.less'
          ],
          'static/css/<%= pkg.name %>.min.css': [
            'static/less/<%= pkg.name %>.less'
          ],
        }
      }
    },
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-recess');

  // Default task(s).
  grunt.registerTask('default', ['uglify', 'recess']);

  // Alias jshint to lint
  grunt.registerTask('lint', ['jshint']);

};
