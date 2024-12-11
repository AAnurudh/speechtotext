<template>
    <div class="download-section">
      <a v-if="videoUrl" :href="videoUrl" download>Download Video with Subtitles</a>
    </div>
  </template>
  
  <script>
  export default {
    props: ['videoUrl']
  };
  </script>
  
  <style>
  .download-section {
    margin-top: 20px;
  }
  </style>
  