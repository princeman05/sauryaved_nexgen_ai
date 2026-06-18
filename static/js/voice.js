
function startVoice(){

    const recognition =
        new webkitSpeechRecognition();

    recognition.lang = 'en-US';

    recognition.start();

    recognition.onresult = function(event){

        document.querySelector('textarea').value =
            event.results[0][0].transcript;
    }
}
