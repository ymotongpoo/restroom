//    Copyright 2016 Yoshi Yamaguchi
// 
//    Licensed under the Apache License, Version 2.0 (the "License");
//    you may not use this file except in compliance with the License.
//    You may obtain a copy of the License at
// 
//        http://www.apache.org/licenses/LICENSE-2.0
// 
//    Unless required by applicable law or agreed to in writing, software
//    distributed under the License is distributed on an "AS IS" BASIS,
//    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//    See the License for the specific language governing permissions and
//    limitations under the License.

'use strict';

var gulp = require('gulp');
var del = require('del');
var path = require('path');
var ts = require('gulp-typescript');

var paths = {
    ts: {
        dir: 'ts',
        src: {
            dir: 'ts/src',
            files: 'ts/src/**/*.ts'
        }
    },
    release: {
        dir: 'release',
        js: {
            dir: 'release/js'
        }
    }
};

gulp.task('build', function() {
    return gulp.src(paths.ts.src.files)
      .pipe(ts({
          noImplicitAny: true,
          out: 'main.js'
      }))
      .pipe(gulp.dest(paths.release.js.dir));
});

gulp.task('clean', function() {
    return del(paths.release.dir);
});