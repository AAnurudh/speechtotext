const express = require("express");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

io.on("connection", (socket) => {
  socket.on("offer", (offer) => socket.broadcast.emit("offer", offer));
  socket.on("answer", (answer) => socket.broadcast.emit("answer", answer));
  socket.on("iceCandidate", (candidate) => socket.broadcast.emit("iceCandidate", candidate));

  socket.on("audioData", async (data) => {
    // Transcription and translation logic here (using Whisper API)
    const { audioData, language } = data;

    // Example transcription response
    const transcription = "Sample Transcription";  // Replace with actual transcription
    const translation = "Sample Translation";      // Replace with translated text

    // Send transcription and translation back
    socket.emit("transcription", {
      user: "local",
      transcription,
      translation,
    });
    socket.broadcast.emit("transcription", {
      user: "remote",
      transcription,
      translation,
    });
  });
});

server.listen(5000, () => {
  console.log("Server is running on http://localhost:5000");
});
