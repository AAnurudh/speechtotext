<template>
  <div class="video-chat">
    <h2>Video Chat with Real-Time Translation and Transcription</h2>

    <div class="video-container">
      <video ref="localVideo" autoplay playsinline class="video-stream" muted></video>
    </div>

    <div class="transcription-container">
      <div v-if="localTranslation" class="transcription">
        <h3>You ({{ localLanguage }} → {{ targetLanguage }})</h3>
        <p>{{ localTranslation }}</p>
      </div>
      <div v-if="translatedText" class="translated-transcription">
        <h3>Translated Text:</h3>
        <p>{{ translatedText }}</p>
      </div>
    </div>

    <div class="language-selection">
      <label for="language-select">Select Preferred Language:</label>
      <select id="language-select" v-model="targetLanguage">
        <option value="en">English</option>
        <option value="es">Spanish</option>
        <option value="fr">French</option>
        <option value="de">German</option>
        <!-- Add more languages as needed -->
      </select>
    </div>

    <div class="call-controls">
      <button @click="startCall" v-if="!isCallStarted" class="start-call">Start Call</button>
      <button @click="endCall" v-if="isCallStarted" class="end-call">End Call</button>
    </div>
  </div>
</template>

<script>
import { io } from "socket.io-client";
const SOCKET_URL = "http://localhost:5000"; // Update with your backend URL
const PC_CONFIG = { iceServers: [{ urls: "stun:stun.l.google.com:19302" }] };

export default {
  data() {
    return {
      localStream: null,
      socket: null,
      isCallStarted: false,
      localTranslation: '',
      translatedText: '',
      localLanguage: 'en', // Set dynamically or by user selection
      targetLanguage: 'en' // Default to English, can be changed by user
    };
  },
  methods: {
    async startCall() {
      this.socket = io(SOCKET_URL);

      // Capture local media stream
      this.localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      this.$refs.localVideo.srcObject = this.localStream;

      // Start sending audio for transcription and translation
      this.sendAudioForTranscription();
      this.isCallStarted = true;

      // Listen for translated transcription from the server
      this.socket.on("translatedTranscription", (data) => {
        this.localTranslation = data.transcription;
        this.translatedText = data.translatedText; // Get the translated text
      });
    },

    async sendAudioForTranscription() {
      const audioContext = new AudioContext();
      const source = audioContext.createMediaStreamSource(this.localStream);
      const processor = audioContext.createScriptProcessor(4096, 1, 1);

      source.connect(processor);
      processor.connect(audioContext.destination);

      processor.onaudioprocess = (event) => {
        const audioData = event.inputBuffer.getChannelData(0);
        this.socket.emit("audioData", {
          audioData,
          sourceLanguage: this.localLanguage,
          targetLanguage: this.targetLanguage
        });
      };
    },

    endCall() {
      if (this.localStream) {
        const tracks = this.localStream.getTracks();
        tracks.forEach(track => track.stop()); // Stop the video/audio stream
      }

      if (this.socket) {
        this.socket.disconnect(); // Disconnect from the WebSocket
      }

      // Reset data fields
      this.isCallStarted = false;
      this.localTranslation = '';
      this.translatedText = '';
      this.localStream = null;
    }
  },
  beforeDestroy() {
    this.endCall(); // Ensure resources are cleaned up when component is destroyed
  }
};
</script>

<style scoped>
.video-chat {
  text-align: center;
  padding: 20px;
}
.video-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.video-stream {
  width: 300px;
  height: 200px;
  border-radius: 10px;
  background-color: #333;
}
.transcription-container {
  margin-top: 20px;
  background: linear-gradient(to right, #ff7e5f, #feb47b);
  color: white;
  padding: 10px;
  border-radius: 8px;
}
.transcription {
  text-align: left;
}
.translated-transcription {
  text-align: left;
  margin-top: 10px;
}
.language-selection {
  margin-top: 10px;
}
.call-controls {
  margin-top: 15px;
}
.start-call {
  background-color: #4CAF50; /* Green */
  color: white;
  border: none;
  padding: 10px 20px;
  margin-right: 10px; /* Space between buttons */
  border-radius: 5px;
  cursor: pointer;
}

.end-call {
  background-color: #f44336; /* Red */
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

</style>
