
let time = 120;

const timer = setInterval(() => {

    let minutes = Math.floor(time / 60);

    let seconds = time % 60;

    console.log(minutes + ":" + seconds);

    time--;

    if(time < 0){

        clearInterval(timer);

        alert("Interview Time Over");
    }

}, 1000);
