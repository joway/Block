var gulp = require('gulp'),
    notify = require('gulp-notify'),
    minifycss = require('gulp-minify-css'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    concat = require('gulp-concat');

// 样式处理任务
gulp.task('styles', function () {
    // return gulp.src(['libs/css/normalize.min.css',
    //    'libs/css/font-awesome.min.css',
    //    'libs/css/animate.min.css',
    //    'libs/css/typo.min.css'])    //引入所有CSS
    return gulp.src('libs/css/*.min.css')    //引入所有CSS
        .pipe(concat('lib.css'))           //合并CSS文件
        .pipe(minifycss())                  //CSS压缩
        .pipe(gulp.dest('static/libs/css/'))      //压缩版输出
        .pipe(notify({message: '样式文件处理完成'}));
});


// JS处理任务
gulp.task('scripts', function () {
    return gulp.src('static/js/*.js')      //引入所有需处理的JS
        .pipe(concat('index.js'))                  //合并JS文件
        .pipe(uglify())                           //压缩JS
        .pipe(gulp.dest('static/js/'))        //压缩版输出
        .pipe(notify({message: 'JS文件处理完成'}));
});
gulp.task('scripts-lib', function () {
    return gulp.src([
        'static/libs/js/jquery.min.js',
        'static/libs/js/materialize.min.js',
        'static/libs/js/fetch.min.js',
        'static/libs/js/paste.min.js',
    ])
        .pipe(concat('lib.js'))                  //合并JS文件
        .pipe(gulp.dest('static/libs/js/'))        //压缩版输出
        .pipe(notify({message: 'Lib JS文件处理完成'}));
});

// 图片处理任务
gulp.task('images', function () {
    return gulp.src('static/img/*')        //引入所有需处理的JS
        .pipe(imagemin({optimizationLevel: 3, progressive: true, interlaced: true}))      //压缩图片
        .pipe(gulp.dest('static/img/'))
        .pipe(notify({message: '图片处理完成'}));
});


// 文档临听
gulp.task('watch', function () {

    // 监听所有css文档
    // gulp.watch('static/css/*.css', ['styles']);

    // 监听所有.js档
    gulp.watch('static/js/*.js', ['scripts']);

    // 监听所有图片档
    gulp.watch('static/img/*', ['images']);

});

gulp.task('default', function () {
    // 将你的默认的任务代码放在这
    gulp.start('styles', 'scripts', 'scripts-lib', 'images');
});