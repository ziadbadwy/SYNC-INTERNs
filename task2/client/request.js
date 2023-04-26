let socket = io.connect('http://127.0.0.1:5000');

socket.on('connect', function(){
    console.log("Connected......!", socket.connected)
});

let canvas = document.getElementById('canvas');
let context = canvas.getContext('2d');
const video = document.querySelector("#videoElement");

video.width = 400;
video.height = 300;
// open camera with get user media
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function (err0r) {
        //
    });
}
//now lets send capture video to the server
const FPS = 6;
setInterval(() => {
    width = video.width;
    height = video.height;
    //draws the current video frame onto a canvas element , drawImage(video, x , y , width, height)
    context.drawImage(video, 0, 0, width, height);
    //encoding
    let data = canvas.toDataURL('image/jpeg', 0.5);
    //clear
    context.clearRect(0, 0, width, height);
    //send encoded frame
    socket.emit('image', data);
}, 1000/FPS);
//when geting response
socket.on('response_back', function(image){
    let photo = document.getElementById("photo");
    //display response
    photo.setAttribute('src', image);
});

