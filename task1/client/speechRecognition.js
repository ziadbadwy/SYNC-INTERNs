const textInput = document.querySelector('#textInput');
const message = document.querySelector('#message');
const closeModal = document.querySelector('#close-modal');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const SpeechGrammarList = window.SpeechGrammarList || window.webkitSpeechGrammarList;

const grammar = '#JSGF V1.0;'

const recognition = new SpeechRecognition();
const speechRecognitionList = new SpeechGrammarList();
speechRecognitionList.addFromString(grammar, 1);
recognition.grammars = speechRecognitionList;
recognition.lang = 'en-eg';
recognition.interimResults = false;
const p = document.createElement("p");

const CloseM = () => {
sendButton();
}

message.value = "";
recognition.onresult = (event) => {
const last = event.results.length - 1;
const command = event.results[last][0].transcript;
textInput.value = command;
message.textContent = `${'Voice Input: '} ${command} ${'.'}`;
};

recognition.onspeechend = () => {
recognition.stop();
};

recognition.onerror = (event) => {
message.textContent = `Error occurred in recognition: ${event.error}`;
};

const VoiceReco = () => {
recognition.start();
}

//firstBot msg
const firstMessage = "hi have a nice day!";
firstBotMessage(firstMessage);