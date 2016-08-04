'use strict';

const gulp = require('gulp');
const del = require('del');
const browserify = require('browserify');
const source = require('vinyl-source-stream');
const tsify = require('tsify');
const watch = require('gulp-watch');

const paths = {
    ts: {
        dir: 'ts',
        src: {
            dir: 'ts/src',
            files: [
                './ts/src/**/*.ts',
                '!./node_modules/**'
            ]
        }
    },
    dist: {
        dir: 'dist',
        js: {
            files: [
                './dist/**/*.js'
            ]
        }
    }
};

gulp.task('build', [], () => {
    return browserify([], {
            basedir: '.',
            debug: true,
            entries: ['ts/src/main.ts'],
            cache: {},
            packageCache: {}
        })
        .plugin(tsify)
        .bundle()
        .pipe(source('main.js'))
        .pipe(gulp.dest(paths.dist.dir));
});

gulp.task('watch', [], () => {
    watch(paths.ts.src.files, () => {
        gulp.start('build');
    });
});

gulp.task('clean', [], () => {
    return del(paths.dist.dir);
});

gulp.task('default', ['watch']);