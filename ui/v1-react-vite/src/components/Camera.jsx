import { useEffect } from "react";

const Camera = () => {
    useEffect(() => {
        let video = document.getElementById('video');
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then((stream) => {
                video.srcObject = stream;
                video.play();
            })
            .catch((err) => console.log('getUserMedia failed' + err));
    }, []);

    /*
    const startCamera = () => {
        let video = document.getElementById('video');
        if (video) {
            navigator.mediaDevices
                .getUserMedia({ video: true })
                .then((stream) => {
                    video.srcObject = stream;
                    video.play();
                });
        } else {
            console.log("'video' not found");
        }
    };
    */
    
    const handleClick = () => {
        console.log('Snap!');
    };

    return (
        <>
        <div id="cameraMsg" className="output thick green">
            Kyk asseblief vir die kamera...
        </div>

        <video id="video" autoPlay width="640" height="480" />
        <canvas id="canvas" hidden width="640" height="480" />

        <p>
            <button id="cameraBtn" className="btn btn-primary" onClick={handleClick}>
                Neem foto
            </button>
        </p>
        </>
    );
}

export default Camera