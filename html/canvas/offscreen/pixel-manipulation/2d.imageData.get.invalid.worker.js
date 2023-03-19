// DO NOT EDIT! This test has been generated by /html/canvas/tools/gentest.py.
// OffscreenCanvas test in a worker:2d.imageData.get.invalid
// Description:Verify getImageData() behavior in invalid cases.
// Note:

importScripts("/resources/testharness.js");
importScripts("/html/canvas/resources/canvas-tests.js");

var t = async_test("Verify getImageData() behavior in invalid cases.");
var t_pass = t.done.bind(t);
var t_fail = t.step_func(function(reason) {
    throw reason;
});
t.step(function() {

var canvas = new OffscreenCanvas(100, 50);
var ctx = canvas.getContext('2d');

imageData = ctx.getImageData(0,0,2,2);
var testValues = [NaN, true, false, "\"garbage\"", "-1",
                  "0", "1", "2", Infinity, -Infinity,
                  -5, -0.5, 0, 0.5, 5,
                  5.4, 255, 256, null, undefined];
var testResults = [0, 1, 0, 0, 0,
                   0, 1, 2, 255, 0,
                   0, 0, 0, 0, 5,
                   5, 255, 255, 0, 0];
for (var i = 0; i < testValues.length; i++) {
    imageData.data[0] = testValues[i];
    _assert(imageData.data[0] == testResults[i], "imageData.data[\""+(0)+"\"] == testResults[\""+(i)+"\"]");
}
imageData.data['foo']='garbage';
_assert(imageData.data['foo'] == 'garbage', "imageData.data['foo'] == 'garbage'");
imageData.data[-1]='garbage';
_assert(imageData.data[-1] == undefined, "imageData.data[-1] == undefined");
imageData.data[17]='garbage';
_assert(imageData.data[17] == undefined, "imageData.data[\""+(17)+"\"] == undefined");
t.done();

});
done();
