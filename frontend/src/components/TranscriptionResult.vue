<template>
    <div class="transcription-section">
      <h2>Transcription</h2>
      <p>{{ transcription }}</p>
    </div>
  </template>
  
  <script>
  export default {
    props: ['transcription']
  };
  </script>
  
  <style>
  .transcription-section {
    background: linear-gradient(to right, #ffecd2, #fcb69f);
    padding: 20px;
  }
  </style>
  