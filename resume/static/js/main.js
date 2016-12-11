/**
 * Created by me on 1/28/16.
 */

String.prototype.toFaDigit = function () {
    return this.replace(/\d+/g, function (digit) {
        var ret = '';
        for (var i = 0, len = digit.length; i < len; i++) {
            ret += String.fromCharCode(digit.charCodeAt(i) + 1728);
        }

        return ret;
    });
};

String.prototype.toEnDigit = function () {
    return this.replace(/[\u06F0-\u06F9]+/g, function (digit) {
        var ret = '';
        for (var i = 0, len = digit.length; i < len; i++) {
            ret += String.fromCharCode(digit.charCodeAt(i) - 1728);
        }

        return ret;
    });
};

function readablizeBytes(bytes) {
    if (bytes) {
        var s = ['bytes', 'kB', 'MB', 'GB', 'TB', 'PB'];
        var e = Math.floor(Math.log(bytes) / Math.log(1024));
        return (bytes / Math.pow(1024, e)).toFixed(2) + " " + s[e];
    }
    else {
        return bytes
    }
}

var main_app = angular.module('main_app', []);

//main_app.controller('main_controller', function ($scope) {
//
//});


$(document).ready(function(){
    $('[data-toggle="popover"]').popover();
});
