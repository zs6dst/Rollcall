const API = 'http://localhost:5000/api';
const TIMEOUT = 5000;
const HttpStatus = {
    OK: 200,
    CREATED: 201,
    NOCONTENT: 204,
    BADREQUEST: 400,
    NOTFOUND: 404
}
const State = {
    START: 1,
    RETRY: 2,
    CONFIRM: 3,
    UNKNOWN: 4,
    WELCOME: 5,
}


var photoId = '';
var member = null;

function setupPage(state) {
    if (member == null) member = { language: 'A' };

    const camera = document.getElementById('camera');
    const confirmation = document.getElementById('confirmation');
    const registration = document.getElementById('registration');
    const welcome = document.getElementById('welcome');

    switch (state) {
        case State.START:
        case State.RETRY:
            startCamera();
            camera.hidden = false;
            confirmation.hidden = true;
            registration.hidden = true;
            welcome.hidden = true;
            const cameraBtn = document.getElementById('cameraBtn');
            const cameraMsg = document.getElementById('cameraMsg');
            if (member.language == 'A') {
                cameraBtn.innerText = 'Neem foto';
                cameraMsg.innerText = (state == State.START)
                    ? 'Kyk asseblief vir die kamera'
                    : "Neem asb nog 'n foto";
            } else {
                cameraBtn.innerText = 'Click me!';
                cameraMsg.innerText = (state == State.START)
                    ? 'Please look at the camera'
                    : "Please take another photo";
            }
            break;
        case State.CONFIRM:
            stopCamera();
            camera.hidden = true;
            confirmation.hidden = false;
            registration.hidden = false;
            welcome.hidden = true;
            let memberDesc = `${member.name} ${member.surname} (${member.id})`
            if (member.language == 'A') {
                document.getElementById('confirmMsg').innerText = `Is jy ${memberDesc} ?`;
                document.getElementById('confirmBtn').innerText = 'Ja, dis ek!';
                document.getElementById('registerMsg').innerText = 'Nee, dis nie ek nie';
                document.getElementById('registerBtn').innerText = 'Registreer my!';
            } else {
                document.getElementById('confirmMsg').innerText = `Are you ${memberDesc} ?`;
                document.getElementById('confirmBtn').innerText = "Yes, it's me!";
                document.getElementById('registerMsg').innerText = "No, that's not me";
                document.getElementById('registerBtn').innerText = 'Register me!';
            }
            break;
        case State.UNKNOWN:
            stopCamera();
            camera.hidden = true;
            confirmation.hidden = true;
            registration.hidden = false;
            welcome.hidden = true;
            if (member.language == 'A') {
                document.getElementById('registerMsg').innerText = 'Ek is jammer, maar ek herken jou nie';
                document.getElementById('registerBtn').innerText = 'Registreer my!';
            } else {
                document.getElementById('registerMsg').innerText = "I'm sorry, but I don't recognise you";
                document.getElementById('registerBtn').innerText = 'Register me!';
            }
            break;
        case State.WELCOME:
            stopCamera();
            camera.hidden = true;
            confirmation.hidden = true;
            registration.hidden = true;
            welcome.hidden = false;
            if (member.language == 'A') {
                document.getElementById('welcomeMsg').innerText = `Welkom ${member.name}! Jou teenwoordigheid is geregistreer.`;
                document.getElementById('welcomeBtn').innerText = 'Dankie!';
            } else {
                document.getElementById('welcomeMsg').innerText = `Welcome ${member.name}! Your attendance has been recorded.`;
                document.getElementById('welcomeBtn').innerText = 'Thank you!';
            }
    }
}

function start() {
    member = null;
    setupPage(State.START);
}

async function startCamera() {
    let video = document.getElementById('video');
    let stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    video.play();
}

function stopCamera() {
    const tracks = document.getElementById('video').srcObject.getTracks();
    tracks.forEach(track => track.stop());
}

function snapPhoto() {
    let canvas = document.getElementById('canvas');
    canvas.getContext('2d').drawImage(video, 0, 0, 640, 480);
    const photo = canvas.toDataURL().split(',')[1].replace(' ', '+')

    identifyMember(photo);
}

async function identifyMember(photo) {
    try {
        const request = { method: 'POST', body: JSON.stringify({ photo: photo }) };
        const response = await fetch(`${API}/identify`, request, TIMEOUT);
        let json = null;
        let state = State.RETRY;
        switch (response.status) {
            case HttpStatus.OK: //Member recognized
                console.log('api.identify: OK');
                console.log(response);
                json = await response.json();
                photoId = json.photoId;
                member = json.member;
                state = State.CONFIRM;
                break;
            case HttpStatus.NOCONTENT: //Face detected, but not recognized (ie. member not found)
                console.log('api.identify: NOCONTENT')
                console.log(response);
                json = await response.json();
                photoId = json.photoId;
                state = State.UNKNOWN;
                break;
            case HttpStatus.BADREQUEST: //Bad photo
                console.log('api.identify: BADREQUEST')
                photoId = null;
                break;
            default:
                console.log('api.identify: default')
                photoId = null;
        }
        setupPage(state);
    }
    catch (error) {
        console.log(error)
        setupPage(State.START);
    }
}

function registerManual() {
    try {
        id = parseInt(document.getElementById('registerId').innerText);
    }
    catch (error) {
        console.log(error);
    }
    member = (id <= 999999) ? { 'id': id } : { 'altdId': id };
    register();
}

async function register() {
    try {
        const request = { method: 'POST', body: JSON.stringify({ member: member, photoId: photoId }) };
        const response = await fetch(`${API}/register`, request, TIMEOUT);
        switch (response.status) {
            case HttpStatus.CREATED: //Attendance recorded
                setupPage(State.WELCOME);
                break;
            case HttpStatus.NOCONTENT: //Member number unknown
                break;
        }
    }
    catch (error) {
        console.log(error);
    }
}
